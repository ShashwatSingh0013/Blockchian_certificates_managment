import blockchain_class

import hashlib
from uuid import uuid4
import json
import datetime
from flask import Flask, request , jsonify
from urllib.parse import urlparse
import requests
'''
name = "Shashwat"

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/about')
def about():
   return render_template("home.html",str(obj)=str(chain),name = name)
'''
app=Flask(__name__)


blockchain=blockchain_class.Certification_managment()

###   sample nodes ###########

node_name1= str(uuid4()).replace('-', '')
node_name2= str(uuid4()).replace('-', '')
node_name3= str(uuid4()).replace('-', '')
node_name4= str(uuid4()).replace('-', '')
node_name5= str(uuid4()).replace('-', '')
blockchain.add_to_node_name(node_name1)
blockchain.add_to_node_address('http://127.0.0.1:5001')
blockchain.add_to_node_address('http://127.0.0.1:5002')
blockchain.add_to_node_address('http://127.0.0.1:5003')
blockchain.add_to_node_address('http://127.0.0.1:5004')
blockchain.add_to_node_address('http://127.0.0.1:5005')
blockchain.add_to_node_name(node_name2)
blockchain.add_to_node_name(node_name3)
blockchain.add_to_node_name(node_name5)
blockchain.add_to_node_name(node_name4)

########## sample blocks ###########
certificates=[{
    "id":100,
    "publisher":node_name1
}]

block=blockchain.create_block(certificates,blockchain.hash(blockchain.chain[-1]),node_name1)

print(blockchain.add_block_to_chain(block))


certificates=[{
    "id":200,
    "publisher":node_name2
}]
block2=blockchain.create_block(certificates,blockchain.hash(blockchain.chain[-1]),node_name2)
print(blockchain.add_block_to_chain(block2))


certificates=[{
    "id":300,
    "publisher":node_name3
}]
block3=blockchain.create_block(certificates,blockchain.hash(blockchain.chain[-1]),node_name3)
print(blockchain.add_block_to_chain(block3))


########## sample blocks ###########


print(len(blockchain.chain))
print(blockchain.chain)
print("*******************")
print(blockchain.verify(blockchain.hash(block2),200))


print("*******************")
print(blockchain.is_chain_valid(blockchain.chain))
print("*******************")
print("*******************")

#######################################################
print(blockchain.get_chain())




##### APP #######
@app.route('/home')
def home():
    return   "44HOME44"

@app.route('/get_chain')
def get_chain():
    chain=blockchain.chain
    return str(chain)

'''
@app.route('/update_chain',methods=['GET'])
def update_chain():
    return str(blockchain.update_chain())
   



@app.route('/upgrade_chain',methods=['GET'])
def upgrade_chain():
    status=blockchain.replace_chain()
    response={'status':status}
    return jsonify(response),200
'''



@app.route('/get_latest_block', methods=['GET'])
def get_latest_block():
    response={'block':blockchain.get_chain()[-1]}
    return jsonify(response),200


@app.route('/get_added_block',methods=['GET'])
def get_added_block():
    response={'block':blockchain.get_added()}
    return jsonify(response),200


@app.route('/get_nodes',methods=['GET'])
def get_nodes():
    nodes=blockchain.get_node_address()
    response={'nodes':nodes}
    return jsonify(response), 200


@app.route('/add_block',methods=['POST','GET'])
def add_block():
    json=request.getjson()
    certificates=json.get('certificates')

    if certificates== None:
        return "Not Found",400
    previous_hash=blockchain.hash(blockchain.chain[-1])

    block=blockchain.create_block(certificates)
    status =blockchain.add_block_to_chain(block,previous_hash,publisher)

    response={'status':status}
    return jsonify(response), 200  
app.run()






