from web3 import Web3
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your actual Sepolia RPC server
SEPOLIA_RPC_URL = "https://sepolia.infura.io/v3/5012086e2f3449aeb17baa42b6c3b9a1"
CONTRACT_ADDRESS = "0x03681Be3600789819c24F5EC04214809aA76F4F7"

# Connect to Sepolia
web3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
assert web3.is_connected(), "Could not connect to Sepolia"
logger.info("Connected to Sepolia")

# Load the contract ABI
with open('artifacts/contracts/EmployeeNFT.sol/EmployeeNFT.json') as f:
    contract_json = json.load(f)
    CONTRACT_ABI = contract_json['abi']

# Load the smart contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Function to send data to smart contract
def send_format_data_for_make_sertificate(data, time_stamp, user_eth_address):
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
            data['previousNFTAddress']
        ).build_transaction({
            'from': user_eth_address,
            'nonce': web3.eth.get_transaction_count(user_eth_address),
            'gas': 500000,
            'gasPrice': current_gas_price + web3.to_wei('2', 'gwei')  # Добавляем немного к текущей цене газа
        })

        # Sign the transaction with the sender's private key
        private_key = "0xc62c44c60935cf1ae6879263f787ef94f054ec34d8db3e050f04414a59a2c55b"  # Replace with your private key
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logger.info(f"Transaction successful with hash: {tx_hash.hex()}")
        return receipt

    except Exception as e:
        logger.error(f"Error while sending data to smart contract: {str(e)}")
        return None

# Function to receive data from another backend
def get_data_for_make_sertificate(image, text_message, tags, reason=0, previous_nft_address="0x0000000000000000000000000000000000000000", is_approve_NFT=False):
    return {
        'recipientAddress': web3.eth.default_account,
        'image': image,
        'text': text_message,
        'tags': tags,
        'reason': reason,
        'previousNFTAddress': previous_nft_address,
        'isApproveNFT': is_approve_NFT
    }

# Function to check NFT data against its hash
def check_NFT_data_and_NFT_hash(nft_address, user_address):
    try:
        token_id = get_token_id_from_address(nft_address)
        employee_data = contract.functions.getEmployeeData(token_id).call()
        data_hash = contract.functions.generateDataHash(
            employee_data["recipientAddress"],
            employee_data["image"],
            employee_data["text"],
            employee_data["timeStamp"],
            employee_data["tags"],
            employee_data["isApproveNFT"],
            employee_data["reason"],
            employee_data["previousNFTAddress"]
        ).call()
        return data_hash == employee_data["dataHash"] and employee_data["recipientAddress"] == user_address
    except Exception as e:
        logger.error(f"Error while checking NFT data: {str(e)}")
        return False

# Function to get the list of valid NFTs for a user
def get_right_address_NFT(user_address):
    valid_nfts = []
    try:
        for token_id in range(contract.functions.tokenCounter().call()):
            employee_data = contract.functions.getEmployeeData(token_id).call()
            if employee_data["recipientAddress"] == user_address:
                if check_NFT_data_and_NFT_hash(employee_data["recipientAddress"], user_address):
                    valid_nfts.append(token_id)
    except Exception as e:
        logger.error(f"Error while getting valid NFTs: {str(e)}")
    return valid_nfts

# Example usage
def get_token_id_from_address(nft_address):
    # Implement the logic to get token_id from the NFT address
    logger.info(f"Getting token ID from address: {nft_address}")
    pass

if __name__ == "__main__":
    # Assume we are getting data from another backend
    data = {
        'recipientAddress': "0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab",  # Valid Ethereum address
        'image': "ipfs://image_link",  # IPFS image link
        'text': "Employee Information",  # Employee information text
        'tags': ["tag1", "tag2"],  # Tags list
        'reason': "Update",  # Reason for creating NFT
        'previousNFTAddress': "0x0000000000000000000000000000000000000000",  # Previous NFT address
        'isApproveNFT': True  # Boolean indicating approval
    }

    # Send the data to smart contract
    receipt = send_format_data_for_make_sertificate(data, 1234567890, "0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab")
    if receipt:
        logger.info(f"Transaction receipt: {receipt}")

    # Get valid NFTs for a user
    valid_nfts = get_right_address_NFT("0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab")
    logger.info(f"Valid NFTs: {valid_nfts}")