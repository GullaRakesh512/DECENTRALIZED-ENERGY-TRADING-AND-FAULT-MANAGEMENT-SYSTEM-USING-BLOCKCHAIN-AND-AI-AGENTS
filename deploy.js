const hre = require("hardhat");

async function main() {
  // Get the contract factory - MUST match your contract name "Energy"
  const Energy = await hre.ethers.getContractFactory("Energy");
  
  // Deploy the contract
  const energy = await Energy.deploy();
  
  // Wait for deployment to complete
  await energy.waitForDeployment();

  // Get the contract address
  const contractAddress = await energy.getAddress();
  console.log("Energy contract deployed to:", contractAddress);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
