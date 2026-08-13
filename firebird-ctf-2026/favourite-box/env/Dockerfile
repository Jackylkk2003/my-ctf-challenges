FROM python:3.14-alpine

RUN apk --no-cache add socat
RUN adduser -D firebird

WORKDIR /app
COPY --chown=root fav_box.py /app
COPY --chown=root aes.py /app
COPY --chown=root flag.txt /app
RUN chmod -R 555 /app

USER firebird
EXPOSE 3000

CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:python3 -u fav_box.py,pty,stderr,echo=0"]