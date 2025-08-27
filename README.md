# Decentralized Energy Trading and Fault Management System
Youtube video(https://youtu.be/ZKnaKUDkE3c)
Project link(https://dynamic-sprinkles-93c228.netlify.app/)
## **Overview**
This project introduces a smart, decentralized system for local energy markets. It empowers homeowners with renewable energy sources, like solar panels, to sell their surplus electricity directly to their neighbors.

This creates a peer-to-peer (P2P) energy trading network that is more efficient, transparent, and resilient than traditional centralized power grids.

The system is built on three core pillars:
- A secure blockchain-based marketplace for trading  
- An AI-powered fault management system for instant alerts  
- An intelligent grid control agent to ensure local power stability  

Together, these pillars create a self-regulating, community-driven energy ecosystem.

---

## **Key Features**
- **Peer-to-Peer Energy Trading**  
  A user-friendly web platform where users buy and sell energy directly. Transactions are securely recorded on the Ethereum blockchain for a tamper-proof ledger.

- **Fair Market Pricing with Double Auction**  
  A double auction mechanism in the smart contract matches highest bids with lowest asks and computes a market clearing price (MCP) for fair, real-time pricing.

- **Automated Fault Detection**  
  An AI agent monitors the IEEE 13-bus system simulation in OpenDSS. If a fault (e.g., power outage) occurs, the system reacts instantly without human intervention.

- **Instantaneous Alerts**  
  Using n8n automation, the system sends Telegram alerts to the substation operator and the affected homeowner (with a direct link to buy backup power on the DApp).

- **AI-Powered Grid Stability**  
  A second AI agent monitors trading activity. If energy imbalance threatens grid voltage stability, it automatically controls a tap changer transformer in OpenDSS to restore safe levels.

---

## **Double Auction Mechanism (How Pricing & Matching Work)**
**Order Types**  
- **Bids (Buy orders):** price (per kWh), quantity (kWh), expiry.  
- **Asks (Sell orders):** price (per kWh), quantity (kWh), expiry.  
Orders may be **partially fillable** and include a **settlement deposit** used for penalties if delivery/receipt fails.

**Matching Rules**  
1. **Sort** bids by price descending; **sort** asks by price ascending.  
2. **Accumulate quantities** until the first crossing where cumulative bid ≥ cumulative ask.  
3. **Winning set** = all fully matched orders up to the crossing and the marginal (partially filled) pair.  
4. **Uniform Pricing (pay-as-clear):**  
   - Let \( p_b^* \) = price of the marginal winning bid, \( p_a^* \) = price of the marginal winning ask.  
   - **MCP** \( = \frac{p_b^* + p_a^*}{2} \) (midpoint).  
   - All matched trades settle at MCP.  
   - Optional parameter can switch to **pay-as-bid** if desired.

**Partial Fills & Ties**  
- If the marginal order only needs a portion, it is partially filled; the remainder stays on the book until expiry.  
- Ties (same price): break by **earliest timestamp** (FIFO).

**Validity & Timeouts**  
- Each order includes an **expiry (TTL)**; unmatched orders auto-cancel after expiry.  
- A matched trade has a **settlement window** (e.g., N minutes/blocks) to confirm transfer.  
- If not settled in time, the non-performing side is **slashed** (forfeits deposit) and the engine attempts **next-best rematch**.

**Penalties & Safety**  
- **Seller no-delivery:** seller deposit slashed; buyer refunded; reputation strike.  
- **Buyer no-payment/receipt:** buyer deposit slashed; seller made whole up to deposit; reputation strike.  
- **Min trade size** and **price tick** enforce reasonable on-chain economics.  
- **Pausable** market and **admin cancel** for abnormal events.

**On-Chain Data Structures (Simplified)**
- `struct Order { id, trader, isBid, price, qty, qtyFilled, expiry, deposit, createdAt }`  
- `mapping(uint256 => Order)` plus indexed heaps/arrays for bids/asks (price-sorted).  
- **Events:** `OrderPlaced`, `OrderCancelled`, `TradeMatched`, `TradeSettled`, `TradeExpired`, `PenaltyApplied`, `MarketPaused`.

**Settlement Flow**  
1. `matchOrders()` forms the winning set and computes MCP.  
2. For each matched pair, **escrowed deposits** are checked; trade is marked **Pending**.  
3. Within the settlement window, off-chain energy delivery (microgrid/OpenDSS) occurs.  
4. Oracle/agent posts a **settlement proof** (meter reading or signed message).  
5. Contract calls `settle(tradeId)` → releases funds at MCP to seller, returns deposits.  
6. If proof not received by deadline → `expire(tradeId)` applies penalties and attempts rematch.

**Key Parameters (Configurable)**
- `minQty`, `priceTick`, `orderTTL`, `settlementTTL`, `depositRate`, `maxSlippage` (optional user-protection), `pricingMode` (uniform/pay-as-bid).

**Security & Gas Notes**
- Use OpenZeppelin `ReentrancyGuard`, `Pausable`, `Ownable`, `SafeERC20`.  
- Keep the **order book compact** (heaps/queues) and consider **batch matching** to control gas.  
- Off-chain sorting/matching with **on-chain verification** is an alternative for heavy loads.

**Interface Sketch (Solidity)**
```solidity
interface IEnergyDoubleAuction {
    struct Order {
        uint256 id;
        address trader;
        bool isBid;
        uint256 price;    // wei per kWh (or token decimals)
        uint256 qty;      // in Wh or kWh * 1eDecimals
        uint256 qtyFilled;
        uint64  expiry;   // block.timestamp deadline
        uint256 deposit;  // escrowed collateral
    }

    event OrderPlaced(uint256 id, address trader, bool isBid, uint256 price, uint256 qty, uint64 expiry);
    event OrderCancelled(uint256 id);
    event TradeMatched(uint256 bidId, uint256 askId, uint256 qty, uint256 mcp);
    event TradeSettled(uint256 tradeId, uint256 qty, uint256 mcp);
    event TradeExpired(uint256 tradeId, address penalized);
    event PenaltyApplied(address trader, uint256 amount);

    function placeBid(uint256 price, uint256 qty, uint64 expiry) external payable returns (uint256);
    function placeAsk(uint256 price, uint256 qty, uint64 expiry) external payable returns (uint256);
    function cancelOrder(uint256 orderId) external;
    function matchOrders(uint256 maxMatches) external returns (uint256 matched, uint256 mcp);
    function settle(uint256 tradeId, bytes calldata proof) external;
    function expire(uint256 tradeId) external;
}
