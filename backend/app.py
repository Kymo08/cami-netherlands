"""
CAMI Netherlands – Flask Backend API
Run:  python app.py
Prod: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4
"""
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from models.database import init_db
from routes.assessment import assessment_bp
from routes.admin import admin_bp
from routes.stripe_webhook import stripe_bp
from routes.calendar import calendar_bp

load_dotenv()

# Absolute path to the web/ directory (one level up from backend/)
WEB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web'))

app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'https://nl.centrocami.it',
    'https://www.centrocami.it',
])

# ── API Blueprints ─────────────────────────────────────────────────────────────
app.register_blueprint(assessment_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(stripe_bp)
app.register_blueprint(calendar_bp)


# ── API Health ─────────────────────────────────────────────────────────────────
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'service': 'cami-netherlands-api', 'version': '1.0.0'})


# ── Static Frontend (dev only) ─────────────────────────────────────────────────
# In production the web/ files are served by a CDN/static host.
# In development Flask serves them directly so you only need ONE command.

@app.route('/')
def serve_landing():
    return send_from_directory(os.path.join(WEB_DIR, 'landing'), 'index.html')

@app.route('/assessment')
@app.route('/assessment/')
def serve_assessment():
    return send_from_directory(os.path.join(WEB_DIR, 'assessment'), 'index.html')

@app.route('/admin')
@app.route('/admin/')
def serve_admin():
    return send_from_directory(os.path.join(WEB_DIR, 'admin'), 'index.html')

@app.route('/thank-you')
@app.route('/thank-you/')
def serve_thankyou():
    return send_from_directory(WEB_DIR, 'thank-you.html')

@app.route('/subscriptions')
@app.route('/subscriptions/')
def serve_subscriptions():
    return send_from_directory(os.path.join(WEB_DIR, 'subscriptions'), 'index.html')

# Serve any static asset (css, js, images) referenced by the HTML files
@app.route('/landing/<path:filename>')
def static_landing(filename):
    return send_from_directory(os.path.join(WEB_DIR, 'landing'), filename)

@app.route('/assessment/<path:filename>')
def static_assessment(filename):
    return send_from_directory(os.path.join(WEB_DIR, 'assessment'), filename)

@app.route('/admin/<path:filename>')
def static_admin_files(filename):
    return send_from_directory(os.path.join(WEB_DIR, 'admin'), filename)


# ── Error handlers ─────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    # Don't return JSON for page routes
    if str(e).startswith('404'):
        pass
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    port  = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    print(f"""
╔══════════════════════════════════════════════════════╗
║  CAMI Netherlands  –  Local Dev Server               ║
╠══════════════════════════════════════════════════════╣
║  Landing       →  http://localhost:{port}/            ║
║  Assessment    →  http://localhost:{port}/assessment  ║
║  Subscriptions →  http://localhost:{port}/subscriptions ║
║  Admin         →  http://localhost:{port}/admin       ║
║  Thank-you     →  http://localhost:{port}/thank-you   ║
║  API health    →  http://localhost:{port}/api/health  ║
╚══════════════════════════════════════════════════════╝
Admin login: admin / cami-admin-2026
""")
    app.run(host='0.0.0.0', port=port, debug=debug)
