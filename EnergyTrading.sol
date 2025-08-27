// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Energy {
    struct EnergyTransaction {
        address seller;
        address buyer;
        uint amount;
        uint timestamp;
    }

    EnergyTransaction[] public energyTransactions;
    address payable public owner;
    uint public energyPricePerUnit = 1 ether;

    // 🔥 Events to listen from Python
    event EnergySold(address indexed seller, uint256 amount, uint256 timestamp);
    event EnergyBought(address indexed buyer, uint256 amount, uint256 timestamp);

    constructor() {
        owner = payable(msg.sender);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    function setEnergyPrice(uint newPrice) external onlyOwner {
        energyPricePerUnit = newPrice;
    }

    function sellEnergy(uint256 amount) external {
        require(amount > 0, "Amount must be greater than 0");

        energyTransactions.push(EnergyTransaction({
            seller: msg.sender,
            buyer: address(this),
            amount: amount,
            timestamp: block.timestamp
        }));

        emit EnergySold(msg.sender, amount, block.timestamp); // 🔥 Trigger event
    }

    function buyEnergy(uint256 amount) external payable {
        require(amount > 0, "Amount must be greater than 0");
        uint256 totalCost = amount * energyPricePerUnit;
        require(msg.value >= totalCost, "Insufficient payment");

        owner.transfer(totalCost);

        energyTransactions.push(EnergyTransaction({
            seller: owner,
            buyer: msg.sender,
            amount: amount,
            timestamp: block.timestamp
        }));

        emit EnergyBought(msg.sender, amount, block.timestamp); // 🔥 Trigger event

        if (msg.value > totalCost) {
            payable(msg.sender).transfer(msg.value - totalCost);
        }
    }

    function getEnergyTransactions() public view returns (EnergyTransaction[] memory) {
        return energyTransactions;
    }
}
