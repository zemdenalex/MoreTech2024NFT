require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.27",
  networks: {
<<<<<<< HEAD
    arbitrumTestnet: {
      url: "https://arbitrum-sepolia.infura.io/v3/5012086e2f3449aeb17baa42b6c3b9a1", // Тестовая сеть Arbitrum 
      accounts: ["0xc62c44c60935cf1ae6879263f787ef94f054ec34d8db3e050f04414a59a2c55b"],      
=======
    sepolia: {
      url: "https://sepolia.infura.io/v3/5012086e2f3449aeb17baa42b6c3b9a1",
      accounts: ["0xc62c44c60935cf1ae6879263f787ef94f054ec34d8db3e050f04414a59a2c55b"] // Замените на один из приватных ключей Ganache
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
    }
  }
};