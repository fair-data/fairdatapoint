### Install Python modules & Swagger UI

`make install`

### Deploy FDP in development

`make serve-dev` # with default HOST=127.0.0.1:8080

### Deploy FDP in production

`make -e serve-prod HOST=example.com`

### Clean up files

`make clean` # .pyc and Swagger UI files in doc dir (except .json)

### Run tests on running app (in development)

`make test`
