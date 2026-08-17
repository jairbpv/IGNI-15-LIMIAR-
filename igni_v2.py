@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    proof = 123
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': "BLOCO MINERADO!",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200