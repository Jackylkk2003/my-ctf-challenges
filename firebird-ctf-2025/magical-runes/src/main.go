package main

import (
	"bufio"
	"fmt"
	"os"
)

func abracadabra(s string, p, m int) rune {
	var value int = 0
	for _, c := range s {
		value = (value*p + int(c)) % m
	}
	return rune(value)
}

func main() {
	var flag string
	file, err := os.Open("flag.txt")
	if err != nil {
		fmt.Println("Error opening file")
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		flag = scanner.Text()
	}
	magic := make([]rune, 0)
	var p int = 127
	var m int = 4099
	for i := 0; i < len(flag); i++ {
		for j := i + 1; j <= len(flag); j++ {
			magic = append(magic, abracadabra(flag[i:j], p, m))
		}
	}
	for i := range magic {
		for j := 0; j < len(magic)-i-1; j++ {
			if magic[j] > magic[j+1] {
				magic[j], magic[j+1] = magic[j+1], magic[j]
			}
		}
	}

	grimoire, err := os.Create("grimoire.txt")
	if err != nil {
		fmt.Println("Error creating file")
		panic(err)
	}
	defer grimoire.Close()
	grimoire.WriteString(string(magic))
}
