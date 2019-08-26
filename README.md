# Pysimplechain
## Python implementation of a blockchain in less than 200 lines of code
A Python Implementation of a simple blockchain. Less than 200 lines of code.

![Build Status][build-image]

## Description

The Pysimplechain implementation is focused almost exclusively in the hashed ledger feature. It does not include any advanced feature like a distributed ledger or a consensus protocol via proof of work. Here you'll also find that the idea of the "transaction" is abstracted to a more general concept of "`message`" that can contain any type of data.

For that reason, the goal of this project is to explain and to make clearer how is a blockchain structured at the very core. It's not built with the intention to replicate an advanced blockchain like Bitcoin or Ethereum.

The following blockchain implemented in the simple_chain.py file is composed of 3 classes. The `Message()` class, the `Block()` class and the `Chain()`.

A `message` is the basic data container. It is sealed when added to a block and has 2 hashes that identify it: the payload hash and the block hash.
Each message is linked to the previous message via hash pointers (the `prev_hash` attribute). The `validate` message method will ensure the integrity of each message, but will not check if the hash pointers are correct. This is left to the `validate` method in the `Block()` class.

A `block` can contain 1,...,n messages that are linked sequentially one after the other. When a `block` is added to the `chain`, it's sealed and validated to
ensure that the messages are correctly ordered and the hash pointers match. Once the block is sealed and hashed, it is validated by checking the expected vs the actual.

A `chain` can contain 1,...,m blocks that are linked sequentially one after another. The chain integrity can be validated at any time calling the `validate` method, which will call each block's validate method and will raise an `InvalidBlockchain` exception.

## Interactivity:

A `manager()` function is provided to interact with the blockchain via the Terminal/Console. The basic actions are:

* **Add Message to Block:** Allows to add a message to the current block.
* **Add Block to Chain:** Allows to add the current block to the chain if it's not empty.
* **Show Block:** Asks for an index and if exists a block with that index, returns some of the block attributes.
* **Show Chain:** Returns some of the block attributes for each block in the chain.
* **Validate Integrity:** Returns True if the integrity is validated, terminates the program raisiing the appropriate exception otherwise.
* **Exit:** Terminates the program and deletes the blockchain.


## Contribute
Hey there! New ideas are welcome: open/close issues, fork the repo and share your code with a Pull Request.

Clone this project to your computer:

`git clone https://github.com/EricAlcaide/pysimplechain`

## Meta
[Eric Alcaide](https://github.com/EricAlcaide/) – [@eric_alcaide](https://twitter.com/eric_alcaide) – ericalcaide1@gmail.com

[build-image]: https://img.shields.io/travis/rust-lang/rust/master.svg "Build Status"
