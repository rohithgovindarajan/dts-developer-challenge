# src/main/python/uk/gov/hmcts/reform/dev/errors.py

from flask import jsonify
from werkzeug.exceptions import HTTPException

# Function to register error handlers for the Flask application
def register_error_handlers(app):
    # Handler for HTTP exceptions (e.g., 404, 403, etc.)
    @app.errorhandler(HTTPException)
    def handle_http(e):
        # Return a JSON response with the error name, description, and HTTP status code
        return jsonify(error=e.name, description=e.description), e.code

    # Generic handler for all other exceptions
    @app.errorhandler(Exception)
    def handle_all(e):
        # Return a JSON response with a generic error message and a 500 status code
        return jsonify(error='InternalServerError', description=str(e)), 500
