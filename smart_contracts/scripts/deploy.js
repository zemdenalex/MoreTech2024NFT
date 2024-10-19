async function main() {
    const [deployer] = await ethers.getSigners();
  
    console.log("Развертывание контрактов с аккаунта:", deployer.address);
  
    const EmployeeNFT = await ethers.getContractFactory("EmployeeNFT");
    const employeeNFT = await EmployeeNFT.deploy(/* аргументы конструктора, если есть */);
  
    await employeeNFT.deployed();
  
    const contractAddress = await employeeNFT.address;
    console.log("EmployeeNFT deployed to:", contractAddress);
  }
  
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
  