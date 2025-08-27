# 🚀 Decentralized Energy Trading and Fault Management System
youtube video of project(https://youtu.be/ZKnaKUDkE3c)
## 📌 Overview
This project introduces a **smart, decentralized system for local energy markets**.  
It empowers homeowners with renewable energy sources, like **solar panels**, to sell their surplus electricity directly to their neighbors.  

This creates a **peer-to-peer (P2P) energy trading network** that is more efficient, transparent, and resilient than traditional centralized power grids.

The system is built on three core pillars:
- ✅ A **secure blockchain-based marketplace** for trading  
- 🤖 An **AI-powered fault management system** for instant alerts  
- ⚡ An **intelligent grid control agent** to ensure local power stability  

Together, these pillars create a **self-regulating, community-driven energy ecosystem**.

---

## ✨ Key Features
- **🔗 Peer-to-Peer Energy Trading**  
  A user-friendly web platform where users buy and sell energy directly.  
  Transactions are securely recorded on the **Ethereum blockchain** for a tamper-proof ledger.  

- **⚖️ Fair Market Pricing with Double Auction**  
  A **double auction mechanism** in the smart contract matches highest bids with lowest asks.  
  This ensures **real-time, fair, and competitive energy pricing**.  

- **⚡ Automated Fault Detection**  
  An AI agent monitors the **IEEE 13-bus system simulation** in OpenDSS.  
  If a **fault (e.g., power outage)** occurs, the system reacts instantly without human intervention.  

- **📲 Instantaneous Alerts**  
  Using **n8n automation**, the system sends **Telegram alerts**:  
  - 🔧 To the **substation operator** (for repair action)  
  - 🏠 To the **affected homeowner** (with a direct link to buy backup power on the DApp)  

- **🤖 AI-Powered Grid Stability**  
  Another AI agent monitors blockchain trading activity.  
  If energy imbalance threatens **grid voltage stability**, it automatically controls a **tap changer transformer** in OpenDSS to restore safe levels.  

---

## 🏗️ System Architecture
The system integrates **four key components** working in harmony:

1. **OpenDSS Power System**  
   - Simulates houses, loads, solar panels, transformers, and grid behavior.  

2. **Python AI Agents**  
   - **Fault Detection Agent** → Detects faults (voltage drops, current surges).  
   - **Grid Control Agent** → Monitors trading platform & triggers tap changer control.  

3. **Blockchain DApp**  
   - Built with **Solidity smart contracts, Hardhat, JavaScript, and Ethers.js**.  
   - Provides a **web interface** for prosumers via MetaMask.  

4. **n8n Automation Workflow**  
   - Receives signals from agents via **webhooks**.  
   - Sends **custom Telegram notifications** in real-time.  

---

## 🔄 How It Works: Step-by-Step

### **Scenario 1: Trading Energy**
1. 🏠 **Seller lists energy** (e.g., 3 kWh) on the DApp.  
2. 💡 **Buyer places a bid** for required energy.  
3. ⚖️ **Smart contract runs double auction** → finds market clearing price (MCP).  
4. 🔗 **Blockchain executes trade** → payment transferred, energy balances updated.  

---

### **Scenario 2: A Power Outage Occurs**
1. ⚡ **Fault detected** at House 1 by AI agent in OpenDSS.  
2. 🔔 **Alert triggered** via webhook → n8n workflow.  
3. 📲 **Notifications sent**:  
   - Substation → *“Fault detected at House 1. Please initiate repair.”*  
   - Homeowner → *“Fault at your house. Buy backup power here: [DApp Link]”*  

---

### **Scenario 3: Grid Voltage Becomes Unstable**
1. 📉 **Trading imbalance detected** (e.g., high energy sale spikes voltage to 1.056 p.u.).  
2. 🤖 **Grid Control Agent commands tap changer** in OpenDSS.  
3. ✅ **Voltage restored** to safe level (e.g., 1.016 p.u.).  

---

## 🛠️ Technologies Used
- **Blockchain** → Ethereum, Solidity, Hardhat  
- **Frontend** → JavaScript, Ethers.js  
- **Backend & AI Agents** → Python  
- **Power System Simulation** → OpenDSS  
- **Automation & Alerts** → n8n, Webhooks, Telegram API  

---

## 🔮 Future Scope
This project lays the **foundation for advanced smart grids**. Future improvements include:  

- 🚗 **EV (Vehicle-to-Grid) Integration** → EVs as mobile energy storage.  
- 📊 **AI Forecasting** → Predict energy generation & consumption.  
- 📡 **IoT Integration** → Smart meters & home devices for real-time data & granular control.  

---

## 📖 Summary
This project combines **blockchain, AI, power system simulation, and automation** to build a **next-generation decentralized smart grid** that is:  
✅ Transparent  
✅ Efficient  
✅ Resilient  
✅ Community-driven  
