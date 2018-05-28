from flask import Flask, request
from hashlib import sha256
from json import dumps, loads
from requests import post
from socket import gethostbyname, gethostname
from sys import argv

from src.server import Server

'''
This code represents the public facing interface for a TrustNet network node.  It uses a Server object
to implement the actual function, simply passing data from the endpoints to that instance.  Furhter, it
initializes the Flask application, defines its endpoints, and starts it running.
To run the TrustNet network:
    To start the first node, type in:
        python3 node.py 8001
        
    To start subsequent nodes, type in:
        python3 node.py 800x <hostname> <port>
        
        where <hostname> is the previous node's host, and <port> is its port
        
    Each time a node is added, output from each running node indicates that a new node has joined TrustNet
HTTP response codes:  
  
    200           request handled OK
    201           entity created
    400           bad request, invalid parameters, etc.
'''

transactions = []
users = {}
nodes = set()

if len(argv) > 1:
    port = int(argv[1])
else:
    port = 8001
  
if len(argv) > 3:
    nodes.add(argv[2] + ':' + argv[3])
    body = { 'node' : gethostbyname(gethostname()) + ':' + str(port) }
    addrs = set()
    for node in nodes:
        addr = 'http://{}/node'.format(node)
        response = post(addr, json=body, headers={'Content-type':'application/json'})
        hosts = loads(response.text)
        for host in hosts:
            addrs.add(host)
    nodes.update(addrs)

    for node in nodes:
        if node == body['node']:
            continue
        addr = 'http://{}/node'.format(node)
        response = post(addr, json=body, headers={'Content-type':'application/json'})
    nodes.remove(body['node'])
    
server = Server()

# ==============================================================================
# public interface; ReSTful endpoints mostly following CRUD terminology and usage
# ==============================================================================
app = Flask(__name__)

@app.route('/block', methods=['GET'])
def blockGET():
    return server.readAllBlocks()

@app.route('/block', methods=['POST'])
def blockPOST():
    return server.updateWithNewBlock(request)

@app.route('/block/<index>', methods=['GET'])
def blockIndexGET(index):
    return server.readSingleBlock(index)

@app.route('/mine', methods=['POST'])
def minePOST():
    return server.createNewBlock(request)

@app.route('/node', methods=['GET'])
def nodeGET():
    return server.readAllNodes()

@app.route('/node/', methods=['POST'])
def nodePOST():
    return server.updateWithNewNode(request)

@app.route('/transaction', methods=['POST'])
def transactionPOST():
    return server.createNewTransaction()

# ==============================================================================
# debugging endpoints for prototype use
# ==============================================================================
# endpoint to dump users
@app.route('/user', methods=['GET'])
def getUsers():
    return "/user:getUsers(" + dumps(users) + ")", 200

# endpoint to register a new user
@app.route('/user', methods=['POST'])
def addUser():
    body = request.get_json()
    handle = body['handle']
    ip = body['ip']
    uid = sha256((handle + ip).encode()).hexdigest()
    if uid in users.keys():
        return "id is not unique, try a new handle", 400
    users[id] = body
    return "/user:addUser(" + id + ")", 201

# endpoint to query id of a user by its handle
@app.route('/user/<user>', methods=['GET'])
def getUserIdByHandle(user):
    for uid in users.keys():
        if users[id]['handle'] == user:
            return uid, 200
    return "user " + user + " not registered", 400

# endpoint to dump transactions
@app.route('/transaction', methods=['GET'])
def getTransactions():
    return "/transaction:getTransactions(" + dumps(transactions) + ")", 200

# run Flask application
app.run(port=port, debug=True)
