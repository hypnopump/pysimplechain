# -*- coding: utf-8 -*-
""" Code written entirely by Eric Alcaide.

	Simple Blockchain where each block points
	to the previous block. It's a basic implementation
	and does NOT include advanced features like
	proof of work or peer to peer.
"""

import datetime
import hashlib
import time

class Message:
	def __init__(self, data):
		self.hash = None
		self.prev_hash = None
		self.timestamp = time.time()
		self.size = len(data.encode('utf-8'))   # length in bytes
		self.data = data
		self.payload_hash = self._hash_payload()

	def _hash_payload(self):
		return hashlib.sha256(bytearray(str(self.timestamp) + str(self.data), "utf-8")).hexdigest()

	def _hash_message(self):
		return hashlib.sha256(bytearray(str(self.prev_hash) + self.payload_hash, "utf-8")).hexdigest()

	def link(self, message):
		""" Link the message to the previous one via hashes."""
		self.prev_hash = message.hash

	def seal(self):
		""" Get the message hash. """
		self.hash = self._hash_message()

	def validate(self):
		""" Check whether the message is valid or not. """
		if self.payload_hash != self._hash_payload():
			raise InvalidMessage("Invalid payload hash in message: " + str(self))
		if self.hash != self._hash_message():
			raise InvalidMessage("Invalid message hash in message: " + str(self))

	def __repr__(self):
		return 'Message<hash: {}, prev_hash: {}, data: {}>'.format(
			self.hash, self.prev_hash, self.data[:20]
		)


class Block:
	def __init__(self, *args):
		self.messages = []
		self.timestamp = None
		self.prev_hash = None
		self.hash = None
		if args:
			for arg in args:
				self.add_message(arg)

	def _hash_block(self):
		return hashlib.sha256(bytearray(str(self.prev_hash) + str(self.timestamp) + self.messages[-1].hash, "utf-8")).hexdigest()

	def add_message(self, message):
		if len(self.messages) > 0:
			message.link(self.messages[-1])
		message.seal()
		message.validate()
		self.messages.append(message)
 
	def link(self, block):
		""" The block hash only incorporates the head message hash
			which then transitively includes all prior hashes.
		"""
		self.prev_hash = block.hash
        
	def seal(self):
		self.timestamp = time.time()
		self.hash = self._hash_block()

	def validate(self):
		""" Validates each message hash, then chain integrity, then the block hash.
			Calls each message's validate() method.

			If a message fails validation, this method captures the exception and 
			throws InvalidBlock since an invalid message invalidates the whole block.
		"""
		for i, msg in enumerate(self.messages):
			try:
				msg.validate()
				if i > 0 and msg.prev_hash != self.messages[i-1].hash:
					raise InvalidBlock("Invalid block: Message #{} has invalid message link in block: {}".format(i, str(self)))
			except InvalidMessage as ex:
				raise InvalidBlock("Invalid block: Message #{} failed validation: {}. In block: {}".format(
					i, str(ex), str(self))
				)

	def __repr__(self):
		return 'Block<hash: {}, prev_hash: {}, messages: {}, time: {}>'.format(
			self.hash, self.prev_hash, len(self.messages), self.timestamp
		)

class SimpleChain:
	def __init__(self):
		self.chain = []

	def add_block(self, block):
		""" Add a block if valid."""
		if len(self.chain) > 0:
			block.prev_hash = self.chain[-1].hash
		block.seal()
		block.validate()
		self.chain.append(block)

	def validate(self):
		""" Validates each block, in order.
			An invalid block invalidates the chain.
		"""
		for i, block in enumerate(self.chain):
			try:
				block.validate()
			except InvalidBlock as exc:
				raise InvalidBlockchain("Invalid blockchain at block number {} caused by: {}".format(i, str(exc)))
		return True

	def __repr__(self):
		return 'SimpleChain<blocks: {}>'.format(len(self.chain))


class InvalidMessage(Exception):
	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)

class InvalidBlock(Exception):
	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)

class InvalidBlockchain(Exception):
	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)


def manager():
	chain = SimpleChain()
	block = Block()
	msg = """
		Basic implementation of a Blockchain. Changes are inmutable. Be aware.

		Action set:
			- add message to the existing block  (1)
			- add existing block to the chain    (2)
			- show a block (index will be asked) (3)
			- show the whole chain               (4)
			- validate the chain integrity       (5)
			- exit the program                   (6)

		The validate action will kill the program if the integrity if the chain
		is compromised.
		"""

	print(msg)	
	while True:
		print()

		decide = input("Your action: ")

		if decide == "1":
			block.add_message(Message(input("Enter your data:")))
		elif decide == "2":
			if len(block.messages) > 0:
				chain.add_block(block)
				block = Block()
			else: print("Block is empty, try adding some messages")
		elif decide == "3":
			index = int(input("Provide the index: "))
			if len(chain.chain)>0:
				try: print(chain.chain[index])
				except: print("An issue occurred")
		elif decide == "4":
			for b in chain.chain:
				print(b)
				print("----------------")
		elif decide == "5":
			if chain.validate(): print("Integrity validated.")
		else:
			break

if __name__ == "__main__":
	manager()