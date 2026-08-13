FROM python:3.14-alpine

RUN apk --no-cache add socat
RUN adduser -D firebird
RUN python3 -m pip install pycryptodome

WORKDIR /app
COPY --chown=root deed.py /app
COPY --chown=root flag.txt /app
RUN chmod -R 555 /app

USER firebird
EXPOSE 3000

CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:python3 -u deed.py,pty,stderr,echo=0"]