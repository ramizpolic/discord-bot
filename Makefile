DIR := ${CURDIR}

.PHONY: build

build: ## Build the package
	docker run -v "${DIR}:/src/" cdrx/pyinstaller-windows
	docker run -v "${DIR}:/src/" cdrx/pyinstaller-linux
