import requests
import json
import os
from PIL import Image
import io

class BackendTester:
    def __init__(self):
        self.backend1_url = "http://194.87.46.228:5000"
        self.backend2_url = "http://194.87.46.228:5001"
        self.test_address = "0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab"

    def create_test_image(self):
        """Create a simple test image"""
        img = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr

    def test_backend_connectivity(self):
        """Test if both backends are responding"""
        try:
            response1 = requests.get(self.backend1_url)
            print(f"Backend 1 Status: {response1.status_code}")
            print(f"Backend 1 Response: {response1.text}")
        except requests.exceptions.RequestException as e:
            print(f"Backend 1 Error: {str(e)}")

        try:
            response2 = requests.get(self.backend2_url)
            print(f"Backend 2 Status: {response2.status_code}")
            print(f"Backend 2 Response: {response2.text}")
        except requests.exceptions.RequestException as e:
            print(f"Backend 2 Error: {str(e)}")

    def test_file_handling(self):
        """Test file upload and retrieval"""
        print("\nTesting File Handling:")
        try:
            # Create and upload test image
            test_image = self.create_test_image()
            files = {'file': ('test.png', test_image, 'image/png')}
            response = requests.post(f'{self.backend2_url}/upload', files=files)
            print(f"File Upload Response: {response.status_code}")
            
            if response.status_code == 200:
                file_url = response.json()['file_url']
                filename = file_url.split('/')[-1]
                # Test file retrieval
                response = requests.get(f'{self.backend2_url}/file/{filename}')
                print(f"File Retrieval Response: {response.status_code}")
                return file_url
            return None
        except requests.exceptions.RequestException as e:
            print(f"File Handling Error: {str(e)}")
            return None

    def test_nft_creation(self, file_url):
        """Test NFT creation flow"""
        print("\nTesting NFT Creation:")
        try:
            nft_data = {
                'recipientAddress': self.test_address,
                'image': file_url,
                'text': "Test NFT",
                'tags': ["test", "initial"],
                'reason': "Testing backend connectivity",
                'previousTokenId': 0,
                'isApproveNFT': False
            }
            
            response = requests.post(f'{self.backend2_url}/send-data', json=nft_data)
            print(f"NFT Creation Response: {response.status_code}")
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(f"NFT Creation Error: {str(e)}")

    def test_nft_retrieval(self):
        """Test NFT retrieval"""
        print("\nTesting NFT Retrieval:")
        try:
            response = requests.get(f'{self.backend2_url}/get-valid-nfts', 
                                  params={'userAddress': self.test_address})
            print(f"NFT Retrieval Response: {response.status_code}")
            print(json.dumps(response.json(), indent=2))
        except requests.exceptions.RequestException as e:
            print(f"NFT Retrieval Error: {str(e)}")

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("Starting Backend Tests...")
        print("-" * 50)
        
        self.test_backend_connectivity()
        file_url = self.test_file_handling()
        if file_url:
            self.test_nft_creation(file_url)
        self.test_nft_retrieval()
        
        print("-" * 50)
        print("Tests Complete!")

if __name__ == "__main__":
    tester = BackendTester()
    tester.run_all_tests()