import time
import base64
import hashlib
import sys
import secrets


class Block:
    def __init__(self, index, previous_hash, timestamp, encoded_transactions, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.encoded_transactions = encoded_transactions
        self.nonce = nonce

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.encoded_transactions}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()


def proof_of_work(previous_block, encoded_transactions):
    index = previous_block.index + 1
    timestamp = int(time.time())
    nonce = 0

    block = Block(index, previous_block.calculate_hash(),
                  timestamp, encoded_transactions, nonce)
    # creates a new block

    while not is_valid_proof(block):
        nonce += 1
        block.nonce = nonce # we keep changing the nonce until our hash doesn start with "00"

    return block


def is_valid_proof(block):
    guess_hash = block.calculate_hash() #it gets a block_string, converts it into bytes, then hashes it using
    #SHA256 then converts it into hexadecimal srtings
    return guess_hash[:2] == "00" #increases difficulty


def decode_transactions(encoded_transactions):
    return base64.b64decode(encoded_transactions).decode('utf-8')


def get_all_blocks(blockchain):
    return blockchain


def blockchain_to_string(blockchain):
    block_strings = [f"{block.calculate_hash()}" for block in blockchain]
    return '-'.join(block_strings)


def encrypt(plaintext, inner_txt, key):
    midpoint = len(plaintext) // 2

    first_part = plaintext[:midpoint]
    second_part = plaintext[midpoint:]
    modified_plaintext = first_part + inner_txt + second_part # the inner part is what we need
    block_size = 16
    plaintext = pad(modified_plaintext, block_size) # the plain text is now padded bytes
    key_hash = hashlib.sha256(key).digest() #the key is hashed now

    ciphertext = b''

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i + block_size]
        cipher_block = xor_bytes(block, key_hash)
        ciphertext += cipher_block

    return ciphertext


def pad(data, block_size):
    padding_length = block_size - len(data) % block_size
    padding = bytes([padding_length] * padding_length)
    return data.encode() + padding


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def generate_random_string(length):
    return secrets.token_hex(length // 2)


random_string = generate_random_string(64) # 64 long secured string


def main(token):
    key = bytes.fromhex(random_string) # turns into bytes
    
    print("Key:", key)

    genesis_block = Block(0, "0", int(time.time()), "EncodedGenesisBlock", 0)
    blockchain = [genesis_block]

    for i in range(1, 5):
        encoded_transactions = base64.b64encode(
            f"Transaction_{i}".encode()).decode('utf-8')
        #1: .encode turns Transaction_i into bytes
        #2: bas64.b64encode(..,) => encodes the bytes into Base64
        #3: Converts base64 into Python Strings
        
        new_block = proof_of_work(blockchain[-1], encoded_transactions)
        # 4: Creates block based on last block infor and encoded transactions
        # 5: it is based on the time this was created and nonce is always different

        blockchain.append(new_block)
        # 5: We get 5 blocks in total, each block has their encoded transaction crypted except for the first 1 whihc is EncodedGenesisBlock

    all_blocks = get_all_blocks(blockchain) # is a reference to blockchain

    blockchain_string = blockchain_to_string(all_blocks) # returns a string concatenation of all the calculate the hases
    encrypted_blockchain = encrypt(blockchain_string, token, key)

    print("Encrypted Blockchain:", encrypted_blockchain)


if __name__ == "__main__":
    text = sys.argv[1]
    main(text)
