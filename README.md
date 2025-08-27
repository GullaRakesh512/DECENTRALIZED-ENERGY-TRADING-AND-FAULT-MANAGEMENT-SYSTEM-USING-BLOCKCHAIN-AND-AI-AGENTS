Decentralized Energy Trading and Fault Management System
watch the video (https://youtu.be/ZKnaKUDkE3c)
1. Overview
This project introduces a smart, decentralized system for local energy markets. It empowers homeowners with renewable energy sources, like solar panels, to sell their surplus electricity directly to their neighbors. This creates a peer-to-peer (P2P) energy trading network that is more efficient, transparent, and resilient than traditional, centralized power grids.

The system is built on three core pillars: a secure blockchain-based marketplace for trading, an AI-powered fault management system for instant alerts, and an intelligent grid control agent to ensure the stability of the local power network. It effectively creates a self-regulating, community-driven energy ecosystem.

2. Key Features
Peer-to-Peer Energy Trading: A user-friendly web platform allows users to buy and sell energy directly. All transactions are securely recorded on the Ethereum blockchain, eliminating the need for a middleman.

Fair Market Pricing: A Double Auction Mechanism is built into the system's smart contract. It matches the highest bids from buyers with the lowest offers from sellers to determine the fairest market price for everyone in real-time.

Automated Fault Detection: An AI agent continuously monitors the electrical grid (a simulated IEEE 13-bus system). If a fault, like a power outage at a house, is detected, the system instantly reacts.

Instantaneous Alerts: Upon detecting a fault, the system uses n8n automation to send immediate Telegram alerts to both the substation operator (for repairs) and the affected homeowner. The homeowner's alert includes a direct link to the trading platform to buy backup power.

AI-Powered Grid Stability: A second AI agent monitors the energy trading activity. If a high volume of trades threatens to destabilize the grid's voltage, the agent automatically commands a simulated tap changer to adjust and maintain safe voltage levels, protecting the local infrastructure.

3. System Architecture
The system integrates four key components that work in harmony:

OpenDSS Power System: This is the simulation environment that models the physical electrical grid. It includes houses (both producing and consuming energy), solar panels, and grid control equipment like transformers.

Python AI Agents: These are the brains of the operation.

Fault Detection Agent: Watches the grid for abnormalities.

Grid Control Agent: Watches the trading platform for energy imbalances.

Blockchain DApp (Decentralized Application): This is the user-facing marketplace. Built with JavaScript and Ethers.js, it connects to the Ethereum blockchain and allows users to manage their trades using a crypto wallet like MetaMask. The rules of the market are enforced by a Solidity smart contract.

n8n Automation Workflow: This is the notification engine. It receives a signal (a webhook) from the fault detection agent and executes a pre-defined workflow to send out customized Telegram alerts instantly.

4. How It Works: Step-by-Step
Scenario 1: Trading Energy
Seller Lists Energy: A homeowner with excess solar power lists a certain amount of energy (e.g., 3 kWh) for sale on the DApp at their desired price.

Buyer Places Bid: A neighbor who needs power places a bid to buy energy.

Market Matching: The smart contract's double auction algorithm finds the optimal match and calculates the Market Clearing Price (MCP).

Transaction Execution: The trade is automatically executed on the blockchain. The buyer's payment is transferred to the seller, and the energy balance is updated. The entire transaction is transparent and cannot be altered.

Scenario 2: A Power Outage Occurs
Fault Detected: The AI agent monitoring the OpenDSS simulation detects a sudden voltage drop at "House 1," indicating a power failure.

Alert Triggered: The agent immediately sends a signal to the n8n automation workflow.

Notifications Sent: The n8n workflow sends out two simultaneous messages:

To the Substation: "Alert: A fault has been detected at House 1. Please initiate rectification procedures."

To the Homeowner: "A fault has been detected at your house. You can buy backup power from House 2 or House 3 on our trading platform: [link-to-dapp]."

Scenario 3: Grid Voltage Becomes Unstable
Imbalance Detected: The Grid Control AI agent analyzes the blockchain and sees a massive amount of energy being sold, causing the grid voltage to rise to an unsafe level (e.g., 1.056 p.u.).

Control Action Initiated: The agent sends a command to the OpenDSS simulation.

Voltage Stabilized: The command instructs the tap changer transformer to adjust its position to lower the voltage. The simulation confirms the voltage has returned to a safe level (e.g., 1.016 p.u.), and the grid is stable.

5. Technologies Used
Blockchain: Ethereum, Solidity, Hardhat

Frontend & DApp Interaction: JavaScript, Ethers.js

Backend & AI Agents: Python

Power System Simulation: OpenDSS

Automation & Notification: n8n, Webhooks, Telegram API

6. Future Scope
This project lays the foundation for a more advanced smart grid. Future enhancements could include:

Electric Vehicle (V2G) Integration: Allowing EVs to act as mobile batteries that can buy, sell, or store energy.

AI-Powered Forecasting: Using AI to predict energy production and consumption to help users make smarter trading decisions.

Integration with IoT Devices: Connecting with smart meters and home devices for more granular control and real-time data.
