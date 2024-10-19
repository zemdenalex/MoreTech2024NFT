const EmployeeNFT = artifacts.require("EmployeeNFT");

module.exports = function (deployer) {
  deployer.deploy(EmployeeNFT);
};
