"""
Stripe Webhook Handler
POST /api/webhook/stripe

Events handled:
  checkout.session.completed  → mark payment paid, enroll client
  payment_intent.payment_failed → mark payment failed

Set STRIPE_WEBHOOK_SECRET in environment (from Stripe Dashboard → Webhooks).
"""
import os
import json

import stripe
from flask import Blueprint, request, jsonify

from models.database import get_db
from services.email_service import send_assessment_confirmation

stripe.api_key        = os.getenv('STRIPE_SECRET_KEY', '')
WEBHOOK_SECRET        = os.getenv('STRIPE_WEBHOOK_SECRET', '')

stripe_bp = Blueprint('stripe_webhook', __name__)


def _enroll(session: dict):
    """Update DB record from a completed Stripe checkout session."""
    assessment_id = session.get('metadata', {}).get('assessment_id')
    if not assessment_id:
        print(f"[STRIPE] No assessment_id in session metadata: {session.get('id')}")
        return

    payment_intent = session.get('payment_intent', '')
    customer_email = session.get('customer_details', {}).get('email', '')
    amount_total   = session.get('amount_total', 0)          # in cents

    db = get_db()
    try:
        db.execute("""
            UPDATE assessments
               SET payment_status = 'paid',
                   payment_id     = ?,
                   status         = 'enrolled'
             WHERE id = ?
        """, (payment_intent, assessment_id))
        db.commit()
        row = db.execute("SELECT * FROM assessments WHERE id = ?", (assessment_id,)).fetchone()
    finally:
        db.close()

    if row:
        print(f"[STRIPE] Enrolled {dict(row)['name']} ({assessment_id}) — €{amount_total/100:.2f}")
        # Optionally re-send a payment confirmation email here
    else:
        print(f"[STRIPE] Assessment {assessment_id} not found in DB after payment")


@stripe_bp.route('/api/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload    = request.data
    sig_header = request.headers.get('Stripe-Signature', '')

    # Verify signature (skip if no secret configured — useful in dev)
    if WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
        except stripe.error.SignatureVerificationError as e:
            print(f"[STRIPE] Signature verification failed: {e}")
            return jsonify({'error': 'Invalid signature'}), 400
    else:
        try:
            event = json.loads(payload)
        except Exception:
            return jsonify({'error': 'Invalid payload'}), 400

    event_type = event.get('type', '')
    data_obj   = event.get('data', {}).get('object', {})

    print(f"[STRIPE] Event: {event_type}")

    if event_type == 'checkout.session.completed':
        _enroll(data_obj)

    elif event_type == 'payment_intent.payment_failed':
        pi_id = data_obj.get('id', '')
        db = get_db()
        try:
            db.execute(
                "UPDATE assessments SET payment_status='failed' WHERE payment_id=?",
                (pi_id,)
            )
            db.commit()
        finally:
            db.close()
        print(f"[STRIPE] Payment failed for intent {pi_id}")

    return jsonify({'received': True}), 200
