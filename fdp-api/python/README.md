# Install Python modules & Swagger UI

`make install`

# Deploy FDP in development

`make serve-dev` # with default HOST=127.0.0.1:8080

# Deploy FDP in production

`make -e serve-prod HOST=example.com`

# Clean up: .pyc and Swagger UI files in doc directory (except swagger.json)

`make clean`

# Run tests on running app (in development)

`make test`
