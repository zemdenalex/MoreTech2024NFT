import { useEffect, useState } from 'react';
import axios from 'axios';

// Define the expected structure of the data
interface NFT {
  tokenId: number;
  recipientAddress: string;
  image: string;
  text: string;
  tags: string[];
  isApproveNFT: boolean;
  reason: string;
  previousTokenId: number;
  hash_from_backend: string;
}

const Home = () => {
  const [data, setData] = useState<NFT[] | null>(null); // Store NFT data
  const [loading, setLoading] = useState(false); // Add loading state for the button

  // Fetch NFTs when the component mounts
  useEffect(() => {
    axios
      .get('http://194.87.46.228:5001/get-valid-nfts?userAddress=0xYourAddressHere')
      .then((response) => {
        setData(response.data); // Store response data
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);

  // Function to handle button click and send a request to app.py
  const handleAddNFT = () => {
    setLoading(true); // Start loading

    // Define the data to send (you can modify this data as needed)
    const nftData = {
      recipientAddress: '0xYourAddressHere',
      image: 'ipfs://image_link',
      text: 'New NFT',
      tags: ['tag1', 'tag2'],
      reason: 'Created via button',
      previousTokenId: 0,
      isApproveNFT: false,
    };

    // Make a POST request to add the NFT
    axios
      .post('http://194.87.46.228:5001/send-data', nftData)
      .then((response) => {
        console.log('NFT added:', response.data);
        setLoading(false); // Stop loading after request completes
      })
      .catch((error) => {
        console.error('Error adding NFT:', error);
        setLoading(false);
      });
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-4xl font-bold mb-4">NFT Data from Backend</h1>

      {data ? (
        <div className="w-full max-w-4xl">
          {data.map((nft) => (
            <div key={nft.tokenId} className="p-4 bg-gray-100 rounded-lg mb-4">
              <h2 className="text-2xl font-bold">NFT #{nft.tokenId}</h2>
              <p><strong>Recipient Address:</strong> {nft.recipientAddress}</p>
              <p><strong>Text:</strong> {nft.text}</p>
              <p><strong>Tags:</strong> {nft.tags.join(', ')}</p>
              <p><strong>Reason:</strong> {nft.reason}</p>
              <img src={nft.image} alt={`NFT ${nft.tokenId}`} className="w-32 h-32 object-cover mt-4" />
            </div>
          ))}
        </div>
      ) : (
        <p>Loading data...</p>
      )}

      {/* Button to add an NFT */}
      <button
        onClick={handleAddNFT}
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        disabled={loading} // Disable while loading
      >
        {loading ? 'Adding NFT...' : 'Add NFT'}
      </button>
    </div>
  );
};

export default Home;
