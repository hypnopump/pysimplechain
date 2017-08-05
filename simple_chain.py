# -*- coding: utf-8 -*-
""" Code written entirely by Eric Alcaide.

	Simple Blockchain where each block points
	to the previous block. It's a basic implementation
	and does NOT include advanced features like
	prove of work or peer to peer.

"""

import hashlib
import datetime

class Chain():
	def __init__(self):
		self.chain = []

	# Create the first block
	def genesis(self):
		index = 0
		timestamp = datetime.datetime.now()
		data = "I'm the first Block! Feels good to start a Blockchain."
		previous_hash = " "

		self.chain.append(Block(index, timestamp, data, previous_hash))
		return

	# Add a block if valid
	def add_block(self, block):
		if self.check_block(block) == True:
			self.chain.append(block)
			print()
			print("Block #"+str(block.index)+" added to the blockchain")
			print("Hash: ", block.hash)
		else:
			print("Block not added. Invalid block so far.")

	def new(self):
		prev = self.chain[-1]

		index = prev.index+1
		timestamp = datetime.datetime.now()
		data = str(input("Data to be stored: "))
		previous_hash = prev.hash

		return Block(index, timestamp, data, previous_hash)

	# check if the block recieved is valid
	def check_block(self,block):
		prev = self.chain[-1]
		if block.previous_hash == prev.hash and block.index == prev.index+1:
			return True
		else:
			return False

	# Print block
	def show_block(self, block):
		print("--------------------------")
		print("Showing Block")
		print("Index: ", block.index)
		# print("Timestamp: ", block.timestamp)
		print("Data: ", block.data)
		print("Hash: ", block.hash)
		print("Previous hash: ", block.previous_hash)

	# Show a node provided its index
	def show_n_block(self, index):
		try: 
			block = self.chain[index]
			return self.show_block(block)
		except: 
			print("Index out of range")

	# Show latest block
	def last_block(self):
		last = self.chain[-1]
		return self.show_block(last)

	# Show latest block
	def first_block(self):
		first = self.chain[0]
		return self.show_block(first)

	# Show the entire chain
	def show_chain(self):
		print("/////////////////////////////////")
		print("SHOWING CHAIN")
		for block in self.chain:
			self.show_block(block)

	def manager(self):
		self.genesis()
		print()
		print("Basic implementation of a Blockchain. Changes are inmutable. Be aware.")
		print()
		print("Action set:")
		print()
		print("- add_block (1)")
		print("- show_block (2)")
		print("- last_block (3)")
		print("- first_block (4)")
		print("- show_chain (5)")
		print("- shutdown (6)")
		while True:
			print()

			decide = str(input("Your action: "))

			if decide == "1":
				self.add_block(self.new())
			elif decide == "2":
				index = int(input("Block Index: "))
				self.show_n_block(index)
			elif decide == "3":
				self.last_block()
			elif decide == "4":
				self.first_block()
			elif decide == "5":
				self.show_chain()
			elif decide == "6":
				break
			else:
				print("Invalid action")

class Block():
	def __init__(self, index, timestamp, data, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.previous_hash = previous_hash
		self.hash = self.encrypt_block()

	# Returns the hash of the block
	def encrypt_block(self):
		sha = hashlib.sha256()

		sha.update(str(self.index).encode('utf-8') +
			str(self.timestamp).encode('utf-8') +
			str(self.data).encode('utf-8') +
			str(self.previous_hash).encode('utf-8'))

		return sha.hexdigest()


if __name__ == "__main__":
	chain = Chain()
	chain.manager()