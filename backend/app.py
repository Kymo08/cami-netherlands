"""
CAMI Netherlands – Flask Backend API
Run:  python app.py
Prod: gunicorn app:app --bind 0.0.0.0:5000
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from models.database import init_db
from routes.assessment import assessment_bp

load_dotenv()

app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'https://nl.centrocami.it',
    'https://www.centrocami.it',
])

# Register blueprints
app.register_blueprint(assessment_bp)


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'service': 'cami-netherlands-api', 'version': '1.0.0'})


@app.errorhandler(404)
def not_found(e):
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500


if __name__ == '__main__':
    init_db()
    port  = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    print(f"[CAMI API] Starting on http://0.0.0.0:{port}  debug={debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)
