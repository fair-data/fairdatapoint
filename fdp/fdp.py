import connexion
from fdp import config

def create_app(host, port, sparql_endpoint=None, grlc_endpoint=None):
    config.init_fairgraph(host, port, sparql_endpoint)
    config.init_grlc(grlc_endpoint, sparql_endpoint)

    app = connexion.FlaskApp(__name__, specification_dir='openapi/', debug=True)
    options = {"swagger_ui": True}
    app.add_api('openapi.yaml',
            options=options,
            arguments={'title': 'FDP server'},
            strict_validation=True,
            validate_responses=True
            )

    return app.app

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 80
    app = create_app(host, port)
    app.run(host=host, port=port, debug=True)