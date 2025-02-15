upload-arm:
	docker build . -f Dockerfile.arm -t m2n2/wiki-telegram-bot-arm:latest -t m2n2/wiki-telegram-bot-arm:0.1.3 \
	&& docker push m2n2/wiki-telegram-bot-arm --all-tags

upload-amd:
	docker build . -f Dockerfile.amd64 -t m2n2/wiki-telegram-bot-amd64:latest -t m2n2/wiki-telegram-bot-amd64:0.1.3 \
	&& docker push m2n2/wiki-telegram-bot-amd64 --all-tags
