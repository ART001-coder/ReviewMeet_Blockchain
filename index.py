import hashlib
import time
import json

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = (
            str(self.index)
            + str(self.timestamp)
            + json.dumps(self.data, sort_keys=True)
            + self.previous_hash
            + str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        print(f"Mining block {self.index}...")

        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Nonce found: {self.nonce}")
        print(f"Hash: {self.hash}\n")


class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        target = "0" * self.difficulty

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

            if current.hash[:self.difficulty] != target:
                return False

        return True


if __name__ == "__main__":
    my_blockchain = Blockchain(difficulty=4)

    my_blockchain.add_block(Block(1, {"sender": "Alice", "receiver": "Bob", "amount": 50}, ""))
    my_blockchain.add_block(Block(2, {"sender": "Bob", "receiver": "Charlie", "amount": 30}, ""))
    my_blockchain.add_block(Block(3, {"sender": "Charlie", "receiver": "David", "amount": 20}, ""))

    print("Blockchain valid?", my_blockchain.is_chain_valid())