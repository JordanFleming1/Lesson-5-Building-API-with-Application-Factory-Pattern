from flask import Flask, send_from_directory, jsonify, render_template_string
from app.extensions import db, ma, cache, limiter
from app.config import DevelopmentConfig
from app.blueprints import register_blueprints
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    # Optional: Set a global default rate limit
    app.config['RATELIMIT_DEFAULT'] = '100 per hour'
    register_blueprints(app)

    # Serve swagger.yaml
    @app.route('/swagger.yaml')
    def swagger_yaml():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'swagger.yaml',
            mimetype='text/yaml'
        )

    # Serve Swagger UI at /docs
    @app.route('/docs')
    def swagger_ui():
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
          <title>Swagger UI</title>
          <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
        </head>
        <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
        <script>
          const ui = SwaggerUIBundle({
            url: '/swagger.yaml',
            dom_id: '#swagger-ui',
          });
        </script>
        </body>
        </html>
        ''')

    return app

