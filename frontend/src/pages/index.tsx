import { useEffect, useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    // Make a request to your backend
    axios.get('http://194.87.46.228:5000/get-valid-nfts?userAddress=0xYourAddressHere')
      .then((response) => {
        setData(response.data); // Store the response data in state
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-4xl font-bold mb-4">Data from Backend</h1>
      {data ? (
        <pre className="bg-gray-100 p-4 rounded-lg w-full max-w-4xl overflow-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      ) : (
        <p>Loading data...</p>
      )}
    </div>
  );
};

export default Home;