import { useEffect, useState } from 'react';
import axios from 'axios';


// Define the expected structure of the data
interface NFT {
  image: string;
  text: string;
  tags: string[];
  reason: string;
  isApproveNFT: boolean;
}

const Home = () => {
  const [NFTChains, setNFTChains] = useState([]);
  const [validNFTs, setValidNFTs] = useState([]);
  const [data, setData] = useState<NFT[] | null>(null); // Store NFT data
  const [loading, setLoading] = useState(false); // Add loading state for the button

  // Fetch NFTs when the component mounts
  useEffect(() => {
    axios
      .post('http://194.87.46.228:5001/get_nft_chains', {
        user_eth_address: '0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab'  // Replace with actual address
      })
      .then((response) => {
        console.log('Fetched NFT data:', response.data); // Log response
        setNFTChains(response.data); // Assuming response.data is an array of NFT objects
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const handleGetActualValidNFTs = () => {
    setLoading(true);

    axios
      .post('http://194.87.46.228:5001/get_actual_valid_nfts', NFTChains)
      .then((response) => {
        console.log('NFT Chains got:', response.data);
        setValidNFTs(response.data)
        setLoading(false); // Stop loading after request completes
        handleGetNFTData;
      })
      .catch((error) => {
        console.error('Error getting NFT Chains:', error);
        setLoading(false);
      });
  }

  const handleGetNFTData = () => {
    setLoading(true);

    axios
      .post('http://194.87.46.228:5001/prepare_nft_list_for_frontend', validNFTs)
      .then((response) => {
        console.log('NFT Data got:', response.data);
        setData(response.data)
        setLoading(false); // Stop loading after request completes
      })
      .catch((error) => {
        console.error('Error getting NFT Data:', error);
        setLoading(false);
      });
  }

  // Function to handle button click and send a request to app.py
  const handleAddNFT = () => {
    setLoading(true); // Start loading

    // Define the data to send (you can modify this data as needed)
    const nftData = {
      recipientAddress: '0x7D4fCE1D01D00baBF24D3a4379D5A7fDCAB77Eab',
      image: 'ipfs://image_link',
      text: 'New NFT',
      tags: ['tag1', 'tag2'],
      reason: 'Created via button',
      previousTokenId: 0,
      isApproveNFT: false,
    };

    

    // Make a POST request to add the NFT
    axios
      .post('http://194.87.46.228:5001/send_data_for_backend', nftData)
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
      <button
        onClick={handleGetActualValidNFTs}
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        disabled={loading} // Disable while loading
      >
        {loading ? 'Getting Data' : 'Get Actual Valid NFTs'}
      </button>
      
      <h1 className="text-4xl font-bold mb-4">NFT Data from Backend</h1>

      {loading ? (
        <p>Loading data...</p>
      ) : data && data.length > 0 ? (
        <div className="w-full max-w-4xl">
          {data.toString()}
        </div>
      ) : (
        <p>No data found.</p>
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