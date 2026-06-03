// A continuous limit-order book per contract, with price–time priority. This is
// where price discovery happens: the fleet's analyst, the GPU operators, and
// the retail swarm all post orders, and the crossing trades print a last price.

let ORDER_SEQ = 0;

export class OrderBook {
  constructor(contract) {
    this.contract = contract;
    this.bids = []; // resting buys, sorted best (highest) first
    this.asks = []; // resting sells, sorted best (lowest) first
    this.last = null; // last trade price
    this.trades = []; // trade tape
    this.halted = false;
  }

  bestBid() {
    return this.bids[0]?.price ?? null;
  }
  bestAsk() {
    return this.asks[0]?.price ?? null;
  }
  mid() {
    const b = this.bestBid();
    const a = this.bestAsk();
    if (b != null && a != null) return (b + a) / 2;
    return this.last ?? b ?? a ?? null;
  }

  // Submit a limit order; match against the opposite side, rest the remainder.
  // Returns the trades it generated.
  submit({ did, side, qty, price }) {
    if (this.halted) return [];
    const order = {
      id: ++ORDER_SEQ,
      did,
      side,
      qty,
      price: this.contract.roundToTick(price),
      seq: ORDER_SEQ,
    };
    const made = [];
    const opposite = side === "buy" ? this.asks : this.bids;
    const crosses = (resting) =>
      side === "buy" ? order.price >= resting.price : order.price <= resting.price;

    while (order.qty > 0 && opposite.length && crosses(opposite[0])) {
      const resting = opposite[0];
      const fill = Math.min(order.qty, resting.qty);
      const px = resting.price; // resting order sets the price (price-time priority)
      const trade = {
        symbol: this.contract.symbol,
        price: px,
        qty: fill,
        buyer: side === "buy" ? order.did : resting.did,
        seller: side === "buy" ? resting.did : order.did,
      };
      made.push(trade);
      this.trades.push(trade);
      this.last = px;
      order.qty -= fill;
      resting.qty -= fill;
      if (resting.qty === 0) opposite.shift();
    }

    if (order.qty > 0) this.#rest(order);
    return made;
  }

  #rest(order) {
    const book = order.side === "buy" ? this.bids : this.asks;
    book.push(order);
    book.sort((x, y) =>
      order.side === "buy" ? y.price - x.price || x.seq - y.seq : x.price - y.price || x.seq - y.seq,
    );
  }

  // Between rounds the book is cleared of resting liquidity (orders are
  // round-scoped, like quotes minted under a per-round capability). The last
  // price persists as the reference for the next round.
  clearResting() {
    this.bids = [];
    this.asks = [];
  }
}
