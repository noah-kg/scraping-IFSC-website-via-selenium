.PHONY: install docker convert

# install requirements
install:
	pip install -r requirements.txt

# build docker image
build:
	docker build -t ifsc . -f Dockerfile

# run docker image
run:
	docker run --rm -it ifsc bash

# convert ipynb to html
convert:
	jupyter nbconvert --execute \
	--ExecutePreprocessor.timeout=600 \
	--TemplateExporter.exclude_input=True \
	--TemplateExporter.exclude_output_prompt=True \
	--to html "IFSC Analysis.ipynb" \
	--output docs/index.html

# build docker and use to convert
all:
	make build \
	&& docker run -it -v ${PWD}/docs:/app/docs ifsc make convert