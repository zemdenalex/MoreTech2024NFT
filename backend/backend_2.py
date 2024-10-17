import requests
import json
import logging
import sqlite3
import bcrypt
from http.server import BaseHTTPRequestHandler, HTTPServer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend_1 endpoint
BACKEND_1_URL = "http://localhost:5000"  # Update with the actual backend_1 address

# Database connection for users
def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        wallet_id TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Database connection for images
def create_images_table():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_url TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

create_users_table()
create_images_table()

# Function to send data to backend_1
def send_data_for_backend(frontend_data, is_update=False):
    data = {
        "recipientAddress": frontend_data['recipientAddress'],
        "image": frontend_data['image'],
        "text": frontend_data['text'],
        "tags": frontend_data['tags'],
        "reason": frontend_data['reason'] if is_update else "No reason",
        "previousTokenId": frontend_data['previousTokenId'] if is_update else 0,
        "isApproveNFT": frontend_data['isApproveNFT']
    }

    try:
        response = requests.post(f"{BACKEND_1_URL}/send-data", json=data)
        response.raise_for_status()
        logger.info(f"Data sent successfully: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send data to backend_1: {str(e)}")

# Function to get valid NFTs from backend_1 and organize them into chains
def get_valid_nfts(user_eth_address):
    try:
        response = requests.get(f"{BACKEND_1_URL}/get-valid-nfts", params={"userAddress": user_eth_address})
        response.raise_for_status()

        # Получаем JSON ответ в виде словаря
        data = response.json()

        # Извлекаем список NFT из ключа 'nfts'
        valid_nfts = data.get("nfts", [])
        logger.info(f"Valid NFTs received: {valid_nfts}")

        # Создаем список цепочек NFT
        nft_chains = []

        # Проходим по каждому NFT и распределяем их в цепочки
        for nft in valid_nfts:
            previous_id = nft.get("previousTokenId")
            token_id = nft.get("tokenId")  # Получаем идентификатор токена

            # Флаг, указывающий, добавлен ли NFT в существующую цепочку
            added_to_existing_chain = False

            # Проходим по существующим цепочкам, чтобы найти подходящую
            for chain in nft_chains:
                # Проверяем, если текущий NFT ссылается на последний в цепочке
                if chain[-1].get("tokenId") == previous_id:
                    chain.append(nft)
                    added_to_existing_chain = True
                    break

            # Если ни одна из существующих цепочек не подошла, создаем новую цепочку с текущим NFT
            if not added_to_existing_chain:
                nft_chains.append([nft])

        # Логируем цепочки для отладки
        logger.info(f"NFT chains: {nft_chains}")
        return nft_chains
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get valid NFTs from backend_1: {str(e)}")
        return []

# Function to get the actual valid NFTs (last element in each chain)
def get_actual_valid_nfts(nft_chains):
    # Возвращаем последние элементы каждой цепочки (актуальные версии NFT)
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

# User registration
def register_user(email, username, password, wallet_id):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        # Вставляем нового пользователя в таблицу
        c.execute('INSERT INTO users (email, username, password, wallet_id) VALUES (?, ?, ?, ?)',
                  (email, username, hashed_password, wallet_id))
        conn.commit()
        logger.info("User registered successfully")
    except sqlite3.IntegrityError:
        logger.error("Registration failed: User already exists")
    finally:
        conn.close()

# User login
def login_user(username_or_email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Ищем пользователя по имени или email
    c.execute('SELECT password FROM users WHERE username = ? OR email = ?', (username_or_email, username_or_email))
    result = c.fetchone()

    if result:
        hashed_password = result[0]
        # Проверяем, соответствует ли введённый пароль хешу
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            logger.info("User authenticated successfully")
            return True
        else:
            logger.error("Authentication failed: Incorrect password")
    else:
        logger.error("Authentication failed: User not found")
    return False

# Image saving
def save_image(image_url):
    try:
        conn = sqlite3.connect('images.db')
        c = conn.cursor()
        # Вставляем ссылку на изображение в таблицу
        c.execute('INSERT INTO images (image_url) VALUES (?)', (image_url,))
        conn.commit()
        logger.info("Image saved successfully")
    except sqlite3.Error as e:
        logger.error(f"Failed to save image: {str(e)}")
    finally:
        conn.close()

# Example usage
if __name__ == "__main__":
    # Assume we are getting data from frontend
    frontend_data = {
        'recipientAddress': "0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab",
        'image': "ipfs://image_link",
        'text': "Employee Information 11",
        'tags': ["tag2", "tag3", "tag6"],
        'reason': "Update",
        'previousTokenId': 1,
        'isApproveNFT': True
    }

    # Save image to database
    save_image(frontend_data['image'])

    # Send data to backend_1
    send_data_for_backend(frontend_data, is_update=True)

    # Get valid NFTs from backend_1
    valid_nfts = get_valid_nfts("0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab")
    logger.info(f"Actual valid NFTs: {json.dumps(valid_nfts, indent=2)}")

    # Get actual valid NFTs
    actual_valid_nfts = get_actual_valid_nfts(valid_nfts)
    for nft in actual_valid_nfts:
        logger.info(f"Actual NFT: tokenId={nft.get('tokenId')}, data={json.dumps(nft, indent=2)}")

    # Get strongly filtered actual valid NFTs
    strong_filtered_nfts = get_strong_filtered_actual_valid_nfts(actual_valid_nfts, ["tag1", "tag2"])
    logger.info(f"Strongly filtered NFTs: {json.dumps(strong_filtered_nfts, indent=2)}")

    # Get lightly filtered actual valid NFTs
    lite_filtered_nfts = get_lite_filtered_actual_valid_nfts(actual_valid_nfts, ["tag4", "tag5"])
    logger.info(f"Lightly filtered NFTs: {json.dumps(lite_filtered_nfts, indent=2)}")
