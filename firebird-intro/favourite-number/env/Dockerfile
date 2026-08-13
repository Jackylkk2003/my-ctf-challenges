FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \ 
    apt-get install -y socat && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -M firebird

WORKDIR /app
COPY src/favourite-number .
RUN chmod 755 favourite-number
ENV FLAG "flag{...}"

USER firebird
CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:./favourite-number,stderr"]
EXPOSE 3000