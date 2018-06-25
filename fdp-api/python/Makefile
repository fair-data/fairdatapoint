.PHONY: all requirements doc install reinstall clean serve-dev serve-prod

APP = fdp
HOST = 127.0.0.1:8080

all: install

install: requirements doc

requirements:
	pip install -r requirements.txt

doc:
	git clone https://github.com/swagger-api/swagger-ui.git
	mv swagger-ui/dist/* doc
	rm -fr swagger-ui
	sed -i.org 's/https\?:.*\(swagger.json\)/\/doc\/\1/' doc/index.html

reinstall:
	pip install --upgrade --no-deps .

clean:
	rm -f *.pyc
	cd doc && find . ! -name swagger.json -delete

test:
	nosetests -v -w tests

serve-dev:
	python -m bottle --debug --reload --bind $(HOST) $(APP)

serve-prod:
	nohup python -m bottle -b $(HOST) $(APP) &

