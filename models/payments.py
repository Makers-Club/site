

class StripeClient():
    
    @staticmethod
    def customer_email(data):
        import json
        if not data:
            return {'error': 'no data recieved from stripe'}
        data = json.loads(data)
        data = data.get('data')
        
        error = {'payment': 'error'}

        if not data:
            error['message'] = 'no data key'
            return error
        object = data.get('object')
        if not object:
            error['message'] = 'no object in data'
            return error
        amount = object.get('amount')
        if not amount:
            error['message'] = 'no amount in object'
            return error
        billing_details = object.get('billing_details')
        if not billing_details:
            error['message'] = 'no billing details in object'
            return error
        email = billing_details.get('email')
        if not email:
            error['message'] = 'no email in billing details'
            return error
        name = billing_details.get('name')
        if not name:
            name = ''
        return {'payment': 'OK', 'email': email, 'name': name, 'customer': billing_details, 'amount': amount}
    
    @staticmethod
    def match_payment_to_user(data):
        from models.user import User
        from models.clients.maker_teams_client import MTClient
        email = data.get('email')
        name = data.get('name')
        email_match, name_match = None, None
        # need a query by email but this works for now
        users = User.get_all(MTClient)
        for user in users:
            if user.email.lower() == email.lower():
                email_match = user
                break
            elif user.name.lower() == name.lower():
                name_match = user
            print(user.name, name)
        if email_match:
            paying_user = email_match
        else:
            paying_user = name_match
        return paying_user
        
    @staticmethod
    def give_credits_to(user, amount):
        user.credits += int(amount)
        user.save()