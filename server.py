from flask import Flask
from flask import request
import datetime as date
import json
from block_chain_components import Block, BlockChain
node = Flask(__name__)


# Create the blockchain
blockchain = BlockChain()

# A completely random address of the owner of this node
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
# Store the transactions that
# this node has in a list
this_nodes_transactions = []
# Store the url data of every
# other node in the network
# so that we can communicate
# with them
peer_nodes = []
# A variable to deciding if we're mining or not
mining = True

@node.route('/transaction', methods=['POST'])
def transaction():
  if request.method == 'POST':
    # On each new POST request,
    # we extract the transaction data
    new_transaction = request.get_json()
    # Then we add the transaction to our list
    this_nodes_transactions.append(new_transaction)
    # Because the transaction was successfully
    # submitted, we log it to our console
    print("New transaction")
    print("FROM: {}".format(new_transaction['from']))
    print("TO: {}".format(new_transaction['to']))
    print("AMOUNT: {}\n".format(new_transaction['amount']))
    # Then we let the client know it worked out
    return "Transaction submission successful\n"

@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_to_send = []
  # Convert our blocks into dictionaries
  # so we can send them as json objects later
  for block in blockchain.chain:
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = block.hash
    chain_to_send.append({
      "index": block_index,
      "timestamp": block_timestamp,
      "data": block_data,
      "hash": block_hash
    })
  # Send our chain to whomever requested it
  chain_to_send = json.dumps(chain_to_send)
  return chain_to_send

@node.route('/mine', methods = ['GET'])
def mine():
  # Get the last proof of work
  last_block = blockchain.last_block()
  last_proof = last_block.data['proof-of-work']
  # Find the proof of work for
  # the current block being mined
  # Note: The program will hang here until a new
  #       proof of work is found
  proof = blockchain.proof_of_work(last_proof)
  # Once we find a valid proof of work,
  # we know we can mine a block so 
  # we reward the miner by adding a transaction
  this_nodes_transactions.append(
    { "from": "network", "to": miner_address, "amount": 1 }
  )
  # Now we can gather the data needed
  # to create the new block
  new_block_data = {
    "proof-of-work": proof,
    "transactions": list(this_nodes_transactions)
  }
  new_block_index = last_block.index + 1
  new_block_timestamp = date.datetime.now()
  last_block_hash = last_block.hash
  # Empty transaction list
  this_nodes_transactions[:] = []
  # Now create the
  # new block!
  mined_block = Block(
    new_block_index,
    new_block_timestamp,
    new_block_data,
    last_block_hash
  )
  blockchain.add_block(mined_block)
  # Let the client know we mined a block
  return json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
  }) + "\n"

node.run()