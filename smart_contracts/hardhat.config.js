require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-ethers");
require("dotenv").config({ path: "../.env" }); // Явное указание на расположение файла .env

module.exports = {
  solidity: {
    compilers: [
      {
        version: "0.8.1",
      },
      {
        version: "0.8.27",
      },
      {
        version: "0.8.0",
      }
    ]
  },
  networks: {
    arbitrumSepolia: { // Одна сеть: Arbitrum Sepolia
      url: process.env.ARBITRUM_RPC_URL, // Используем ARBITRUM_RPC_URL из .env
      accounts: [process.env.PRIVATE_KEY] // Приватный ключ из .env
    }
  }
};
