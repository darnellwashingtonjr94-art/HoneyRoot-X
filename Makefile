.PHONY: build run stop logs clean

build:
	docker-compose build

run:
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f honeyroot

clean:
	docker-compose down -v
	rm -rf logs/*
