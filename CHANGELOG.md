# Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [0.7.1] - 2020-09-15
### Added
- PUT method used to update metadata

### Changed
- Replaced `flask-restplus` with `connexion` package for OpenAPI generation
- Refactored code based on OpenAPI specification
- Removed ending '/' in endpoints, e.g. '/catalog/' was changed to '/catalog'.
- Removed Bottle and Paste dependecies
- Removed docker compose file for production run


## [0.7.0] - 2020-06-12
### Added
- POST and DELETE methods
- SHACL validator to validate different layers of metadata
- Support for SPARQL database, such as Virtuoso RDF Triple Store
- Docker compose file
- Running in production mode

### Changed
- Improved GET and POST methods
- Updated support for common RDF serializations
- Removed loading metadata for the command tool `fdp-run`
- Removed support for INI-based configuration files
- Updated docker file
- Improved unit testing
- Updated README
- Use Bottle and Paste for production run

## [0.6.0] - 2020-02-10
### Added
- Loading meta-data from RDF/Turtle file (TTL).
- Automatic Swagger API (OpenAPI) generation (via `flask-restplus`).

### Changed
- Documentation in README
- Use Flask instead of Bottle

### Fixed
- Test syntax
