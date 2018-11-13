from block_chain_components import Block, BlockChain

# Create the blockchain and add the genesis block
blockchain = BlockChain()
previous_block = blockchain.last_block()

# How many blocks should we add to the chain
# after the genesis block
num_of_blocks_to_add = 20

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
  block_to_add = blockchain.next_block(previous_block)
  blockchain.add_block(block_to_add)
  previous_block = block_to_add
  # Tell everyone about it!
  print("Block #{} has been added to the blockchain!".format(block_to_add.index))
  print("Hash: {}\n".format(block_to_add.hash))
  print("Timestamp: {}\n".format(block_to_add.timestamp))