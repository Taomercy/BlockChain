import argparse
import sys
from flask import Flask, jsonify, request, render_template
from uuid import uuid4
sys.path.append('./')
import blockchain as bc
import requests
import json, time

app = Flask(__name__, template_folder='./',static_folder="",static_url_path="")
node_id = str(uuid4()).replace('-', '')
blockchain = bc.BlockChain()

hash_list = []
@app.route('/mine', methods=['GET'])
def mine(self, sender: str, recipient: str, timestart: str, timeend: str, data: str):
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.pow(last_proof)  #long time to get the result depend on power
    # Deliver bonus
    blockchain.new_transaction(sender=sender, # From system
                               recipient=recipient,
							   timestart=timestart,
							   timeend=timeend,
                               data=data)
    block = blockchain.new_block(proof)
    response = {'message': 'New block forged',
                'index': block['index'],
                'transactions': block['transactions'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Use raw data format
# {
#     "sender": "6a1ce48188d64010b485dcddba06d4e1",
#     "recipient": "731e01b33dc84df49392e6079b7c1be9",
#     "amount": 1
# }
# Set Content-type to application/json
@app.route('/transaction/new', methods=['post'])
def new_transaction():
    values = request.get_json()
    keys = values.keys()
    required = ['sender', 'recipient', 'timestart', 'timeend', 'data']
    for r in required:
        if not (r in keys):
            return 'Missing value for %s ' % r, 400
    
#    response = {'message': 'Transaction will be added to block {index}'}
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.pow(last_proof)  #long time to get the result depend on power
    # Deliver bonus
    blockchain.new_transaction(values['sender'],
                                       values['recipient'],
                                       values['timestart'],
                                       values['timeend'],
                                       values['data'])
    hash_data = values.get('data')
    print(hash_data)
#    for i in range(0, 100):
    if existRecord(hash_data):
        block = blockchain.new_block(proof)
        response = {'message': 'New block forged',
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']}
        return jsonify(response), 201
    else:
        putIntoRecords(hash_data)
        time.sleep(1)
            
    response = {'message': 'timeout'
                }
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/nodes', methods=['GET'])
def all_nodes():
    response = {'total_nodes': list(blockchain.nodes),
                'length': len(list(blockchain.nodes))}
    return jsonify(response), 200
	
@app.route('/transactions', methods=['GET'])
def full_transaction():
    response = {'transaction': blockchain.transactions,
                'length': len(blockchain.transactions)}
    return jsonify(response), 200

# Use raw data format
# {
#     "nodes": ["http://localhost:5000"]
# }
# Set Content-type to application/json
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json(force=True)
    nodes = values.get('nodes')
    if not nodes:
        return 'Error: Please supply a valid list of nodes', 400
    for node in nodes:
        blockchain.register_node(node)
    response = {'message': 'New nodes added',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conficts()
    response = {'message': 'Our chain is authoritative',
                'chain': blockchain.chain}
    if replaced:
        response['message'] = 'Our chain was replaced'
    return jsonify(response), 200
	
@app.route('/nodes/resolve_transaction', methods=['GET'])
def consensus_trans():
    replaced = blockchain.resolve_conficts_transaction()
    response = {'message': 'Our transactions is authoritative',
                'transactions': blockchain.transactions}
    if replaced:
        response['message'] = 'Our transactions was replaced'
    return jsonify(response), 200

@app.route('/')
def index():
    my_host = args.host_addr
    my_port = args.port
    return render_template('demo.html', my_host=my_host, my_port=my_port)

@app.route('/register', methods=['POST'], strict_slashes=False)
def reg_nodes():
   headers = {'content-type': 'application/json'}
   nodes_reg = request.form['nodes']   
   print (nodes_reg)
   nodes = eval(nodes_reg)['nodes']
   if not nodes:
     return 'Error: Please supply a valid list of nodes', 400
   for node in nodes:
      sendurl=node + "/nodes/register"
   #data = {'nodes': ['http://10.120.72.156:5000','http://10.120.72.156:5001','http://10.120.72.156:5002']}
   #response = requests.post('http://10.120.72.156:5000/nodes/register',data=json.dumps(nodes_reg), headers=headers)
      response = requests.post(sendurl,data=nodes_reg, headers=headers) 
      print (response.text)
   return response.text, 201
 
def existRecord(target_hash):
    print("begin to check")
    for a in hash_list:
        if a==target_hash:
            hash_list.remove(a)
            return True
    return False
     

def putIntoRecords(target_hash):
    print("this is the first one")
    hash_list.append(target_hash)
    return 

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        '--port',
                        help='port to listen',
                        type=int,
                        default=5000)
    parser.add_argument('-a',
                        '--host_addr',
                        help='host to listen',
                        type=str,
                        default='localhost')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    app.run(host=args.host_addr,
            port=args.port,
            debug=True,
            threaded=True) # If not True, on Windows ther server will be fucking slow.
