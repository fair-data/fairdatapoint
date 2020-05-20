.PHONY: all requirements doc install install-test reinstall clean serve-dev

all: install

install: requirements doc

requirements:
    pip install -r requirements.txt

install-test:
    pip install -e .[tests]

doc:
    git clone https://github.com/swagger-api/swagger-ui.git
    mv swagger-ui/dist/* doc
    rm -fr swagger-ui
    sed -i.org 's/http.*\(swagger.json\)/\/doc\/\1/' doc/index.html

reinstall:
    pip install --upgrade --no-deps .

clean:
    rm -f *.pyc
    cd doc && find . ! -name swagger.json -delete

test:
    pytest

serve-dev:
    fdp-run
    # python -m bottle --debug --reload --bind $(HOST) $(APP)

# serve-prod:
#   nohup python -m bottle -b $(HOST) $(APP) &