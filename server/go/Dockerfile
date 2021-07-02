FROM golang:1.16-alpine as base

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

RUN apk --no-cache --update add build-base

COPY . .
RUN go build -o main .

# production stage
FROM alpine:latest
WORKDIR /app
COPY --from=base /app/main /app/main
RUN chmod ug+x main
CMD ["./main"]