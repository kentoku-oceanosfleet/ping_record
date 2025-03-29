FROM debian:stable-slim

WORKDIR /app
COPY get_timestamp.sh .
RUN chmod +x get_timestamp.sh

CMD ["./get_timestamp.sh"]