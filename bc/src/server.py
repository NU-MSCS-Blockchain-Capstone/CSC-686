from src.blockchain import Blockchain

'''
This class implements the necessary function for maintaining a blockchain, validating blocks, and generally
handling the details of the endpoints specified by a node in the TrustNet.
'''

class Server:
    def __init__(self):
        self.blockchain = Blockchain()
    
    def readAllBlocks(self):  # todo implement
        pass

    def updateWithNewBlock(self, request):  # todo implement
        pass

    def readSingleBlock(self, index):  # todo implement
        pass

    def createNewBlock(self, request):  # todo implement
        pass

    def readAllNodes(self):  # todo implement
        pass

    def updateWithNewNode(self, request):  # todo implement
        pass

    def createNewTransaction(self):  # todo implement
        pass

'''
hints:
    req = request.get_json()
    rc = 200
    if req['node'] not in nodes:
        nodes.add(req['node'])
        rc = 201
    return dumps(list(nodes)) + '\n', rc
'''