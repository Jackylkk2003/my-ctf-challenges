package main

import (
	"crypto/tls"
	"fmt"
	"html/template"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"
)

const (
	ServerAddr    = ":443"
	CertFile      = "cert.pem"
	KeyFile       = "key.pem"
	SSLKeyLogFile = "keys.log"
	HTTPLogFile   = "server.log"
)

// Image represents an image file for display
type Image struct {
	Name string
	Path string
}

// ImageFolder represents a folder containing images
type ImageFolder struct {
	Name   string
	Images []Image
}

// PageData holds data for the HTML template
type PageData struct {
	Title        string
	ImageFolders []ImageFolder
	HasFlag      bool
}

// loggingResponseWriter wraps http.ResponseWriter to capture status code
type loggingResponseWriter struct {
	http.ResponseWriter
	statusCode int
	size       int
}

func newLoggingResponseWriter(w http.ResponseWriter) *loggingResponseWriter {
	return &loggingResponseWriter{w, http.StatusOK, 0}
}

func (lrw *loggingResponseWriter) WriteHeader(code int) {
	lrw.statusCode = code
	lrw.ResponseWriter.WriteHeader(code)
}

func (lrw *loggingResponseWriter) Write(b []byte) (int, error) {
	size, err := lrw.ResponseWriter.Write(b)
	lrw.size += size
	return size, err
}

// httpLogger is the logger for HTTP requests
var httpLogger *log.Logger

// loggingMiddleware logs HTTP requests with verbose details
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		lrw := newLoggingResponseWriter(w)

		// Log incoming request details
		httpLogger.Printf(">>> INCOMING REQUEST >>>")
		httpLogger.Printf("  Timestamp: %s", start.Format("2006-01-02 15:04:05.000 MST"))
		httpLogger.Printf("  Remote Address: %s", r.RemoteAddr)
		httpLogger.Printf("  Method: %s", r.Method)
		httpLogger.Printf("  URL: %s", r.URL.String())
		httpLogger.Printf("  Protocol: %s", r.Proto)
		httpLogger.Printf("  Host: %s", r.Host)
		httpLogger.Printf("  Content-Length: %d", r.ContentLength)
		if r.TLS != nil {
			httpLogger.Printf("  TLS Version: %s", tlsVersionString(r.TLS.Version))
			httpLogger.Printf("  TLS Cipher Suite: %s", tls.CipherSuiteName(r.TLS.CipherSuite))
			httpLogger.Printf("  TLS Server Name: %s", r.TLS.ServerName)
		}
		httpLogger.Printf("  Request Headers:")
		for name, values := range r.Header {
			for _, value := range values {
				httpLogger.Printf("    %s: %s", name, value)
			}
		}

		next.ServeHTTP(lrw, r)

		duration := time.Since(start)

		// Log response details
		httpLogger.Printf("<<< RESPONSE <<<")
		httpLogger.Printf("  Status Code: %d %s", lrw.statusCode, http.StatusText(lrw.statusCode))
		httpLogger.Printf("  Response Size: %d bytes", lrw.size)
		httpLogger.Printf("  Duration: %v", duration)
		httpLogger.Printf("  Response Headers:")
		for name, values := range lrw.Header() {
			for _, value := range values {
				httpLogger.Printf("    %s: %s", name, value)
			}
		}
		httpLogger.Printf("-------------------------------------------")
	})
}

// tlsVersionString converts TLS version to human-readable string
func tlsVersionString(version uint16) string {
	switch version {
	case tls.VersionTLS10:
		return "TLS 1.0"
	case tls.VersionTLS11:
		return "TLS 1.1"
	case tls.VersionTLS12:
		return "TLS 1.2"
	case tls.VersionTLS13:
		return "TLS 1.3"
	default:
		return fmt.Sprintf("Unknown (0x%04x)", version)
	}
}

// getImages scans the images directory and returns structured data
func getImages() []ImageFolder {
	var folders []ImageFolder
	baseDir := "images"

	entries, err := os.ReadDir(baseDir)
	if err != nil {
		log.Printf("Error reading images directory: %v", err)
		return folders
	}

	for _, entry := range entries {
		if entry.IsDir() {
			folder := ImageFolder{Name: entry.Name()}
			folderPath := filepath.Join(baseDir, entry.Name())

			files, err := os.ReadDir(folderPath)
			if err != nil {
				continue
			}

			for _, file := range files {
				if !file.IsDir() {
					ext := strings.ToLower(filepath.Ext(file.Name()))
					if ext == ".png" || ext == ".jpg" || ext == ".jpeg" || ext == ".gif" || ext == ".webp" {
						folder.Images = append(folder.Images, Image{
							Name: file.Name(),
							Path: "/" + filepath.Join(baseDir, entry.Name(), file.Name()),
						})
					}
				}
			}

			if len(folder.Images) > 0 {
				folders = append(folders, folder)
			}
		}
	}

	return folders
}

// checkFlagExists checks if the flag.zip file exists
func checkFlagExists() bool {
	_, err := os.Stat("misc/flag.zip")
	return err == nil
}

// homeHandler serves the main page
func homeHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}

	tmpl := template.Must(template.New("index").Parse(indexHTML))

	data := PageData{
		Title:        "Firebird CTF - File Server",
		ImageFolders: getImages(),
		HasFlag:      checkFlagExists(),
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	if err := tmpl.Execute(w, data); err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		log.Printf("Template error: %v", err)
	}
}

// downloadHandler handles file downloads with proper headers
func downloadHandler(w http.ResponseWriter, r *http.Request) {
	filePath := r.URL.Query().Get("file")
	if filePath == "" {
		http.Error(w, "File parameter required", http.StatusBadRequest)
		return
	}

	// Security: prevent directory traversal
	cleanPath := filepath.Clean(filePath)
	if strings.Contains(cleanPath, "..") {
		http.Error(w, "Invalid file path", http.StatusBadRequest)
		return
	}

	// Only allow downloads from misc directory
	if !strings.HasPrefix(cleanPath, "misc/") {
		http.Error(w, "Access denied", http.StatusForbidden)
		return
	}

	file, err := os.Open(cleanPath)
	if err != nil {
		http.Error(w, "File not found", http.StatusNotFound)
		return
	}
	defer file.Close()

	stat, err := file.Stat()
	if err != nil {
		http.Error(w, "Error reading file", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Disposition", fmt.Sprintf("attachment; filename=\"%s\"", filepath.Base(cleanPath)))
	w.Header().Set("Content-Type", "application/octet-stream")
	w.Header().Set("Content-Length", fmt.Sprintf("%d", stat.Size()))

	io.Copy(w, file)
}

func main() {
	// Setup HTTP logging
	httpLogFile, err := os.OpenFile(HTTPLogFile, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		log.Fatalf("Failed to open HTTP log file: %v", err)
	}
	defer httpLogFile.Close()

	// Log to both file and stdout
	multiWriter := io.MultiWriter(os.Stdout, httpLogFile)
	httpLogger = log.New(multiWriter, "[HTTP] ", 0)

	// Setup SSL key logging
	sslKeyLogFile, err := os.OpenFile(SSLKeyLogFile, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0600)
	if err != nil {
		log.Fatalf("Failed to create SSL key log file: %v", err)
	}
	defer sslKeyLogFile.Close()

	// Load TLS certificate
	cert, err := tls.LoadX509KeyPair(CertFile, KeyFile)
	if err != nil {
		log.Fatalf("Failed to load TLS certificate: %v", err)
	}

	// Configure TLS with key logging
	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		MinVersion:   tls.VersionTLS12,
		KeyLogWriter: sslKeyLogFile,        // This writes in SSLKEYLOGFILE format
		NextProtos:   []string{"http/1.1"}, // Force HTTP/1.1, disable HTTP/2
	}

	// Setup routes
	mux := http.NewServeMux()
	mux.HandleFunc("/", homeHandler)
	mux.HandleFunc("/download", downloadHandler)

	// Serve static files (images)
	mux.Handle("/images/", http.StripPrefix("/images/", http.FileServer(http.Dir("images"))))

	// Serve misc files directly
	mux.Handle("/misc/", http.StripPrefix("/misc/", http.FileServer(http.Dir("misc"))))

	// Create server with TLS config
	// TLSNextProto set to empty map disables HTTP/2 on the server side
	server := &http.Server{
		Addr:         ServerAddr,
		Handler:      loggingMiddleware(mux),
		TLSConfig:    tlsConfig,
		TLSNextProto: make(map[string]func(*http.Server, *tls.Conn, http.Handler)), // Disable HTTP/2
	}

	// Startup logging
	log.Printf("========================================")
	log.Printf("  My Web Server with HTTPS!!!")
	log.Printf("========================================")
	log.Printf("Server starting on https://localhost%s", ServerAddr)
	log.Printf("TLS Certificate: %s", CertFile)
	log.Printf("TLS Private Key: %s", KeyFile)
	log.Printf("SSL Key Log: %s (SSLKEYLOGFILE format)", SSLKeyLogFile)
	log.Printf("HTTP Log: %s", HTTPLogFile)
	log.Printf("HTTP Version: HTTP/1.1 (HTTP/2 disabled)")
	log.Printf("----------------------------------------")
	log.Printf("Available endpoints:")
	log.Printf("  GET  /           - Main page with images")
	log.Printf("  GET  /images/... - Static image files")
	log.Printf("  GET  /download?file=misc/flag.zip - Download flag")
	log.Printf("----------------------------------------")
	log.Printf("Press Ctrl+C to stop the server")
	log.Printf("========================================")

	httpLogger.Printf("Server started on https://localhost%s", ServerAddr)

	// Start HTTPS server
	if err := server.ListenAndServeTLS("", ""); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}

// HTML template embedded in Go
const indexHTML = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{.Title}}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #eee;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        h1 {
            font-size: 2.5em;
            color: #ff6b6b;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            color: #a0a0a0;
            font-size: 1.1em;
        }
        .download-section {
            background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(233, 69, 96, 0.3);
        }
        .download-section h2 {
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        .download-btn {
            display: inline-block;
            padding: 15px 40px;
            background: #fff;
            color: #e94560;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            font-size: 1.1em;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .download-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            background: #f8f8f8;
        }
        .download-btn::before {
            content: "⬇ ";
        }
        .folder-section {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .folder-title {
            font-size: 1.4em;
            color: #4ecdc4;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #4ecdc4;
            text-transform: capitalize;
        }
        .folder-title::before {
            content: "📁 ";
        }
        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }
        .image-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .image-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        }
        .image-card img {
            width: 100%;
            height: 200px;
            object-fit: contain;
            background: rgba(0,0,0,0.2);
            padding: 10px;
        }
        .image-info {
            padding: 15px;
            text-align: center;
        }
        .image-name {
            color: #ddd;
            font-size: 0.9em;
            word-break: break-all;
        }
        footer {
            text-align: center;
            padding: 30px;
            color: #666;
            margin-top: 30px;
        }
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .stat-item {
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 10px;
        }
        .no-images {
            text-align: center;
            padding: 40px;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔥 Firebird CTF</h1>
            <p class="subtitle">My Image Gallery</p>
            <div class="stats">
                <div class="stat-item">📂 {{len .ImageFolders}} Folders</div>
                <div class="stat-item">🖼️ Image Gallery</div>
            </div>
        </header>

        {{if .HasFlag}}
        <section class="download-section">
            <h2>🚩 Capture The Flag</h2>
            <p style="margin-bottom: 15px;">Ready to begin? Why solve challenges when you can directly download the flag?</p>
            <a href="/download?file=misc/flag.zip" class="download-btn">Download flag.zip</a>
        </section>
        {{end}}

        {{if .ImageFolders}}
            {{range .ImageFolders}}
            <section class="folder-section">
                <h2 class="folder-title">{{.Name}}</h2>
                <div class="image-grid">
                    {{range .Images}}
                    <div class="image-card">
                        <img src="{{.Path}}" alt="{{.Name}}" loading="lazy">
                        <div class="image-info">
                            <span class="image-name">{{.Name}}</span>
                        </div>
                    </div>
                    {{end}}
                </div>
            </section>
            {{end}}
        {{else}}
            <div class="no-images">
                <h2>No images found</h2>
                <p>Add images to the images/ directory to display them here.</p>
            </div>
        {{end}}

        <footer>
            <p>My Image Gallery</p>
			<p>Made with AI, not with ❤️</p>
        </footer>
    </div>
</body>
</html>
`
