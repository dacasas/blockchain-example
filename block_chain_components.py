import hashlib as hasher
import datetime as date
import json
import requests

class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
  
  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.index).encode('utf-8') + 
               str(self.timestamp).encode('utf-8') + 
               str(self.data).encode('utf-8') + 
               str(self.previous_hash).encode('utf-8'))
    return sha.hexdigest()
  
class BlockChain:
  def __init__(self):
    self.chain = [self.create_genesis_block()]

  def last_block(self):
    return self.chain[-1]
  
  def add_block(self, block):
    self.chain.append(block)

  def create_genesis_block(self):
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), {
    "proof-of-work": 9,
    "transactions": None
    }, "0")

  def next_block(self, last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)
  
  def proof_of_work(self, last_proof):
    # Create a variable that we will use to find
    # our next proof of work
    incrementor = last_proof + 1
    # Keep incrementing the incrementor until
    # it's equal to a number divisible by 9
    # and the proof of work of the previous
    # block in the chain
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
      incrementor += 1
    # Once that number is found,
    # we can return it as a proof
    # of our work
    return incrementor

  def find_new_chains(self, peer_nodes):
    # Get the blockchains of every
    # other node
    other_chains = []
    for node_url in peer_nodes:
      # Get their chains using a GET request
      block = requests.get(node_url + "/blocks").content
      # Convert the JSON object to a Python dictionary
      block = json.loads(block)
      # Add it to our list
      other_chains.append(block)
    return other_chains

  def consensus(self, peer_nodes):
    # Get the blocks from other nodes
    other_chains = self.find_new_chains(peer_nodes)
    # If our chain isn't longest,
    # then we store the longest chain
    longest_chain = self.chain
    for chain in other_chains:
      if len(longest_chain) < len(chain):
        longest_chain = chain
    # If the longest chain wasn't ours,
    # then we set our chain to the longest
    self.chain = longest_chain