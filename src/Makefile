lint:
	black . && isort . && flake8

upload-arm:
	docker build . -f Dockerfile.arm -t m2n2/wiki-telegram-bot-arm:latest -t m2n2/wiki-telegram-bot-arm:1.0.2 \
	&& docker push m2n2/wiki-telegram-bot-arm --all-tags

upload-amd:
	docker build . -f Dockerfile.amd64 -t m2n2/wiki-telegram-bot-amd64:latest -t m2n2/wiki-telegram-bot-amd64:1.0.2 \
	&& docker push m2n2/wiki-telegram-bot-amd64 --all-tags

upload:
	make upload-arm && make upload-amd
