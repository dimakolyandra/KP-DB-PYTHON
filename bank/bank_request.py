from flask import Flask
from flask import request
from flask import jsonify
from bank_connections import connection_dict
from client_account import ClientAccount

app = Flask(__name__)


@app.route('/get-balance', methods=['POST'])
def get_balance():
    data = request.json

    session = connection_dict[data['broker_firm_id']]

    account = session.query(ClientAccount).filter_by(
        passport_data=data['passport_data'],
        account_number=data['account_number']).one()

    return jsonify({'balance': str(account.balance)})

if __name__ == '__main__':
    app.run(debug=True)
