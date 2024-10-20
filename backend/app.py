import hashlib
import requests
import json
import logging
import psycopg2
import bcrypt
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend_1 endpoint
BACKEND_1_URL = os.getenv('BACKEND_1_URL')

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database connection for users
user_db_connection = psycopg2.connect(
    host="194.87.46.228",
    database="user_database",
    user="admin",
    password="ghjnjnbg"
)
user_cursor = user_db_connection.cursor()

# Database connection for files
files_db_connection = psycopg2.connect(
    host="194.87.46.228",
    database="files_database",
    user="admin",
    password="ghjnjnbg"
)
files_cursor = files_db_connection.cursor()

# Function to create a hash from NFT data
def make_hash_from_backend(data):
    hash_input = f"{data['recipientAddress']}{data['image']}{data['text']}{','.join(data['tags'])}{data['reason']}{data['previousTokenId']}{data['isApproveNFT']}"
    hash_output = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
    logger.info(f"Generated hash: {hash_output}")
    return hash_output

# Function to check if the given hash matches the generated hash
def check_hash_with_hash_from_backend(nft_data):
    data_for_hash = {
        "recipientAddress": nft_data["recipientAddress"],
        "image": nft_data["image"],
        "text": nft_data["text"],
        "tags": nft_data["tags"],
        "reason": nft_data["reason"],
        "previousTokenId": nft_data["previousTokenId"],
        "isApproveNFT": nft_data["isApproveNFT"]
    }

    generated_hash = make_hash_from_backend(data_for_hash)
    hash_from_backend = nft_data.get("hash_from_backend", "")

    if generated_hash == hash_from_backend:
        logger.info("Hash matches.")
        return True
    else:
        logger.error("Hash mismatch.")
        return False

# Function to send data to backend_1
def send_data_for_backend(frontend_data, is_update=False):
    image_url = save_file_and_get_url(frontend_data['image'])
    
    data = {
        "recipientAddress": frontend_data['recipientAddress'],
        "image": image_url,  # Send URL instead of actual image
        "text": frontend_data['text'],
        "tags": frontend_data['tags'],
        "reason": frontend_data['reason'] if is_update else "No reason",
        "previousTokenId": frontend_data['previousTokenId'] if is_update else 0,
        "isApproveNFT": frontend_data['isApproveNFT']
    }

    # Generate hash for data
    data_hash = make_hash_from_backend(data)
    data['hash_from_backend'] = data_hash

    try:
        response = requests.post(f"{BACKEND_1_URL}/send-data", json=data)
        response.raise_for_status()
        logger.info(f"Data sent successfully: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send data to backend_1: {str(e)}")

# Function to get NFTs by token IDs from backend_1
def get_nfts_by_token_ids(user_eth_address, token_ids):
    try:
        response = requests.post(f"{BACKEND_1_URL}/get-nfts-by-token-ids", json={"userAddress": user_eth_address, "tokenIds": token_ids})
        response.raise_for_status()

        data = response.json()
        valid_nfts = [nft for nft in data.get("nfts", []) if check_hash_with_hash_from_backend(nft)]
        nft_chains = get_nft_chains(valid_nfts)
        return nft_chains
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get NFTs by token IDs from backend_1: {str(e)}")
        return []

# Function to get NFT chains
def get_nft_chains(valid_nfts):
    nft_chains = []
    for nft in valid_nfts:
        previous_id = nft.get("previousTokenId")
        token_id = nft.get("tokenId")
        added_to_existing_chain = False

        for chain in nft_chains:
            if chain[-1].get("tokenId") == previous_id:
                chain.append(nft)
                added_to_existing_chain = True
                break

        if not added_to_existing_chain:
            nft_chains.append([nft])

    logger.info(f"NFT chains: {nft_chains}")
    return nft_chains

# Function to get valid NFTs from backend_1
def get_valid_nfts(user_eth_address):
    try:
        response = requests.get(f"{BACKEND_1_URL}/get-valid-nfts", params={"userAddress": user_eth_address})
        response.raise_for_status()

        data = response.json()
        valid_nfts = data.get("nfts", [])
        logger.info(f"Valid NFTs received: {valid_nfts}")

        valid_nfts = [nft for nft in valid_nfts if check_hash_with_hash_from_backend(nft)]
        nft_chains = get_nft_chains(valid_nfts)
        return nft_chains
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get valid NFTs from backend_1: {str(e)}")
        return []

# Function to get the actual valid NFTs (last element in each chain)
def get_actual_valid_nfts(nft_chains):
    actual_valid_nfts = [chain[-1] for chain in nft_chains]
    return actual_valid_nfts

# Function to get strongly filtered actual valid NFTs
def get_strong_filtered_actual_valid_nfts(actual_valid_nfts, tags):
    filtered_nfts = [
        nft for nft in actual_valid_nfts
        if all(tag in nft["tags"] for tag in tags)
    ]
    return filtered_nfts

# Function to get lightly filtered actual valid NFTs
def get_lite_filtered_actual_valid_nfts(actual_valid_nfts, tags):
    filtered_nfts = [
        nft for nft in actual_valid_nfts
        if any(tag in nft["tags"] for tag in tags)
    ]
    return filtered_nfts

# Function to prepare NFT list to send to frontend
def prepare_nft_list_for_frontend(nft_list):
    updated_nft_list = []
    for nft in nft_list:
        # Извлекаем фактический файл вместо ссылки
        image_file_path = nft.get("image")
        if image_file_path:
            image_file_data = get_file_data_base(image_file_path.split('/')[-1])
            updated_nft = {
                "image": image_file_data,  # Добавляем файл изображения
                "text": nft.get("text"),
                "tags": nft.get("tags"),
                "reason": nft.get("reason"),
                "isApproveNFT": nft.get("isApproveNFT")
            }
            updated_nft_list.append(updated_nft)
    return updated_nft_list

# User registration
def register_user(email, username, password, wallet_id):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        user_cursor.execute('INSERT INTO users (email, username, password, wallet_id) VALUES (%s, %s, %s, %s)',
                            (email, username, hashed_password, wallet_id))
        user_db_connection.commit()
        logger.info("User registered successfully")
    except psycopg2.IntegrityError:
        logger.error("Registration failed: User already exists")

# User login
def login_user(username_or_email, password):
    user_cursor.execute('SELECT password FROM users WHERE username = %s OR email = %s', (username_or_email, username_or_email))
    result = user_cursor.fetchone()

    if result:
        hashed_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            logger.info("User authenticated successfully")
            return True
        else:
            logger.error("Authentication failed: Incorrect password")
    else:
        logger.error("Authentication failed: User not found")
    return False

# Image saving
def save_file_and_get_url(file_path):
    try:
        files_cursor.execute('INSERT INTO files (filename, file_path) VALUES (%s, %s)', (os.path.basename(file_path), file_path))
        files_db_connection.commit()
        logger.info("File saved successfully")
        return f"/file/{os.path.basename(file_path)}"
    except psycopg2.Error as e:
        logger.error(f"Failed to save file: {str(e)}")
    return None

# Flask routes for handling files
@app.route('/upload', methods=['POST'])
def upload_file_data_base():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        save_file_and_get_url(file_path)
        return jsonify({"message": "File uploaded successfully", "file_url": file_path})

@app.route('/')
def index():
    return "Welcome to the frontend server!"

@app.route('/file/<filename>', methods=['GET'])
def get_file_data_base(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    # Create several unique NFTs and send them to backend_1
    nft_data_list = [
        {
            'recipientAddress': "0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab",
            'image': "ipfs://image_link_1",
            'text': "NFT #1",
            'tags': ["tag1", "tag2"],
            'reason': "Initial creation",
            'previousTokenId': 0,
            'isApproveNFT': False
        },
        {
            'recipientAddress': "0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab",
            'image': "ipfs://image_link_2",
            'text': "NFT #2",
            'tags': ["tag3", "tag4"],
            'reason': "Initial creation",
            'previousTokenId': 0,
            'isApproveNFT': False
        },
        {
            'recipientAddress': "0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab",
            'image': "ipfs://image_link_3",
            'text': "NFT #3",
            'tags': ["tag5", "tag6"],
            'reason': "Initial creation",
            'previousTokenId': 0,
            'isApproveNFT': False
        },
        {
            'recipientAddress': "0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab",
            'image': "ipfs://image_link_2",
            'text': "NFT #2",
            'tags': ["tag3", "tag4"],
            'reason': "Trying to update NFT #2",
            'previousTokenId': 2,
            'isApproveNFT': False
        }
    ]
    for nft_data in nft_data_list:
        send_data_for_backend(nft_data)
    app.run(host='194.87.46.228', port=5001, debug=True)
