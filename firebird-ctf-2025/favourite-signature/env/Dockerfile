FROM python:3.12-alpine

RUN apk --no-cache add socat build-base
RUN adduser -D firebird
RUN python3 -m pip install pycryptodome

WORKDIR /app
COPY --chown=root chall.py /app
COPY --chown=root elliptic_curve.py /app
COPY --chown=root flag.txt /app
RUN chmod -R 555 /app

USER firebird
EXPOSE 3000

CMD socat TCP-LISTEN:3000,fork,reuseaddr EXEC:"python3 -u chall.py",pty,stderr,echo=0