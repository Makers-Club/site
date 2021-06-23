from routes import payments
from flask import render_template, request, jsonify
import json

@payments.route('/', methods=['POST', 'GET'], strict_slashes=False)
def stripe_confirms_payment():
    from models.user import User
    from models.payments import StripeClient

    response = StripeClient.customer_email(request.data)
    if not response.get('email'):
        return jsonify(response)

    paying_user = StripeClient.match_payment_to_user(response)
    if not paying_user:
        return jsonify({
            'payment': 'error',
            'message': 'customer not found',
            'customer': response.get('customer')
            })
    amount = response.get('amount')
    StripeClient.give_credits_to(paying_user, amount)
    return jsonify({'payment': 'OK', 'customer': paying_user.id, 'amount': amount})

