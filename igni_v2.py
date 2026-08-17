@app.route('/transaction', methods=['POST'])
def new_transaction():
    values = request.form  # <- agora pega do formulário
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transação será adicionada ao Bloco {index}'}
    return jsonify(response), 201