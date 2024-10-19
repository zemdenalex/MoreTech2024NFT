from flask import Flask, request, jsonify
from web3 import Web3
import json
import time
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your actual Arbitrum RPC server
ARBITRUM_RPC_URL = "https://arbitrum-sepolia.infura.io/v3/5012086e2f3449aeb17baa42b6c3b9a1"
CONTRACT_ADDRESS = "0xeDEF0d73424d8623EF8adcB0E5807365e7F560a7"

# Connect to Arbitrum
web3 = Web3(Web3.HTTPProvider(ARBITRUM_RPC_URL))
assert web3.is_connected(), "Could not connect to Arbitrum"
logger.info("Connected to Arbitrum Testnet")

# Load the contract ABI
with open('artifacts/contracts/EmployeeNFT.sol/EmployeeNFT.json') as f:
    contract_json = json.load(f)
    CONTRACT_ABI = contract_json['abi']

# Load the smart contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Endpoint for function in backend_2 send_data_for_backend
@app.route('/send-data', methods=['POST'])
def send_data():
    data = request.get_json()
    if data:
        # Mint the NFT to the blockchain


        # Получить текущий timestamp
        timestamp = int(time.time())
        # Reformate in uint256
        # Преобразовать в uint256
        uint256_timestamp = timestamp

        # This address pays for new mint in blockchain 
        # Адрес с котороого будет браться комиссия за выпуск новых NFT
        address_key_for_pay_comisions = "0xc62c44c60935cf1ae6879263f787ef94f054ec34d8db3e050f04414a59a2c55b"
        receipt = send_format_data_for_make_certificate(data, uint256_timestamp, data['recipientAddress'], address_key_for_pay_comisions)
        if receipt:
            return jsonify({"message": "Data received and NFT minted successfully"}), 200
        return jsonify({"error": "Failed to mint NFT on blockchain"}), 500
    return jsonify({"error": "Invalid data"}), 400

# Endpoint for function in backend_2 get-valid-nfts
@app.route('/get-valid-nfts', methods=['GET'])
def get_valid_nfts():
    user_address = request.args.get('userAddress')
    logger.info(f"Getting valid NFTs for user: {user_address}")
    if user_address:
        valid_nfts_for_user = get_right_address_NFT(user_address)

        # Объединяем список valid_nfts_for_user в один JSON-объект
        result = {"nfts": valid_nfts_for_user}

        logger.info(f"Valid NFTs found: {valid_nfts_for_user}")
        return jsonify(result)
    logger.error("User address not provided")
    return jsonify({"error": "User address not provided"}), 400

# Endpoint for function in backend_2 get NFTs by token IDs
@app.route('/get-nfts-by-token-ids', methods=['POST'])
def get_nfts_by_token_ids():
    data = request.get_json()
    user_address = data.get('userAddress')
    token_ids = data.get('tokenIds', [])

    if user_address and token_ids:
        logger.info(f"Getting NFTs for user: {user_address} with token IDs: {token_ids}")
        nfts = get_right_address_NFT_by_token_ids(user_address, token_ids)
        return jsonify({"nfts": nfts}), 200
    return jsonify({"error": "User address or token IDs not provided"}), 400

# Function to send data to smart contract
def send_format_data_for_make_certificate(data, time_stamp, user_eth_address, private_key):
    try:
        current_gas_price = web3.eth.gas_price

        tx = contract.functions.mintEmployeeNFT(
            data['recipientAddress'],
            data['image'],
            data['text'],
            time_stamp,
            data['tags'],
            data['isApproveNFT'],
            data['reason'],
            data['previousTokenId'],
            data['dataHashFromBackend']
            
        ).build_transaction({
            'from': user_eth_address,
            'nonce': web3.eth.get_transaction_count(user_eth_address),
            'gas': 500000,
            'gasPrice': current_gas_price + web3.to_wei('2', 'gwei')
        })

        # Sign the transaction with the sender's private key
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logger.info(f"Transaction successful with hash: {tx_hash.hex()}")
        return receipt

    except Exception as e:
        logger.error(f"Error while sending data to smart contract: {str(e)}")
        return None

# # Function to receive data for minting certificate
# def get_data_for_make_certificate(image, text_message, tags, data_hash_from_backend, reason="", previous_token_id=0, is_approve_NFT=False):
#     return {
#         'recipientAddress': web3.eth.default_account,
#         'image': image,
#         'text': text_message,
#         'tags': tags,
#         'reason': reason,
#         'previousTokenId': previous_token_id,
#         'isApproveNFT': is_approve_NFT,
#         'dataHashFromBackend': data_hash_from_backend
#     }

# Function to check NFT data against its hash
def check_NFT_data_and_NFT_hash(employee_data):
    try:
        # Extract employee data fields for hash generation
        recipient_address = employee_data[0]
        image = employee_data[1]
        text = employee_data[2]
        time_stamp = employee_data[3]
        tags = employee_data[4]
        is_approve_nft = employee_data[5]
        reason = employee_data[6]
        previous_token_id = employee_data[7]
        data_hash_from_backend = employee_data[8]
        data_hash_from_contract = employee_data[9]

        # Generate hash from employee data
        generated_data_hash = contract.functions.generateDataHash(
            recipient_address, 
            image, 
            text, 
            time_stamp, 
            tags, 
            is_approve_nft, 
            reason, 
            previous_token_id,
            data_hash_from_backend
        ).call()

        # Compare generated hash with the stored hash
        return generated_data_hash == data_hash_from_contract
    except Exception as e:
        logger.error(f"Error while checking NFT data: {str(e)}")
        return False

# Function to get the list of valid NFTs for a user and return their data
def get_right_address_NFT(user_address):
    valid_nfts = []
    try:
        total_tokens = contract.functions.tokenCounter().call()
        for token_id in range(total_tokens):
            employee_data = contract.functions.getEmployeeData(token_id).call()

            # Extracting employee data fields
            recipient_address = employee_data[0]

            # Only proceed if the recipientAddress matches the given user address
            if recipient_address.strip().lower() == user_address.strip().lower():
                # Check the hash to verify the integrity of the data
                if check_NFT_data_and_NFT_hash(employee_data):
                    # Convert data to a format suitable for JSON serialization
                    employee_data_dict = {
                        "tokenId": token_id,
                        "recipientAddress": employee_data[0],
                        "image": employee_data[1],
                        "text": employee_data[2],
                        "tags": employee_data[4],
                        "isApproveNFT": employee_data[5],
                        "reason": employee_data[6],
                        "previousTokenId": employee_data[7],
                        "dataHashFromBackend": employee_data[8]
                    }
                    valid_nfts.append(employee_data_dict)

    except Exception as e:
        logger.error(f"Error while getting valid NFTs: {str(e)}")
    return valid_nfts

# Function to get the list of NFTs by token IDs and user address
def get_right_address_NFT_by_token_ids(user_address, token_ids):
    valid_nfts = []
    try:
        for token_id in token_ids:
            employee_data = contract.functions.getEmployeeData(token_id).call()

            # Extracting employee data fields
            recipient_address = employee_data[0]

            # Only proceed if the recipientAddress matches the given user address
            if recipient_address.strip().lower() == user_address.strip().lower():
                # Check the hash to verify the integrity of the data
                if check_NFT_data_and_NFT_hash(employee_data):
                    # Convert data to a format suitable for JSON serialization
                    employee_data_dict = {
                        "tokenId": token_id,
                        "recipientAddress": employee_data[0],
                        "image": employee_data[1],
                        "text": employee_data[2],
                        "tags": employee_data[4],
                        "isApproveNFT": employee_data[5],
                        "reason": employee_data[6],
                        "previousTokenId": employee_data[7],
                        "dataHashFromBackend": employee_data[8]
                    }
                    valid_nfts.append(employee_data_dict)

    except Exception as e:
        logger.error(f"Error while getting NFTs by token IDs: {str(e)}")
    return valid_nfts

# Example usage
if __name__ == "__main__":
    app.run(port=5000, debug=True)
