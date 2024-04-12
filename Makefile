IMAGE_NAME=chatrapper

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -it --rm -p 9000:9000 $(IMAGE_NAME)

test:
	poetry run pytest -vv
