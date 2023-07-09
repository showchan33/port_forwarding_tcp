FROM alpine:3.18.2

RUN apk update && \
    apk add iptables && \
    apk add curl
