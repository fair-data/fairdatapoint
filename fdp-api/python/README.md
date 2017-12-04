### Install Python modules & Swagger UI

```
make install
# make clean # removes files from doc dir (except swagger.json)
```
### Edit metadata in `config.ini`

### Run tests & deploy FDP in development

```
make serve-dev # with default HOST=127.0.0.1:8080
make test
```

### Deploy FDP in production

`make -e serve-prod HOST=example.com`