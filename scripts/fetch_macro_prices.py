import json, time, urllib.request, sys
import pandas as pd

INFO = "https://api.hyperliquid.xyz/info"
end_ms = int(time.time() * 1000)
start_ms = end_ms - 180 * 24 * 60 * 60 * 1000  # 180 days

MACROS = {
    "BTC": "BTC", "ETH": "ETH", "SOL": "SOL",
    "NATGAS": "xyz:NATGAS",
    "CL_WTI": "xyz:CL",
    "BRENT":  "xyz:BRENTOIL",
    "COPPER": "xyz:COPPER", "PLATINUM": "xyz:PLATINUM", "PALLADIUM": "xyz:PALLADIUM",
    "GOLD":   "xyz:GOLD",  "SILVER":   "xyz:SILVER",
    "EUR":    "xyz:EUR",   "JPY":      "xyz:JPY",
}
DEPIN = {"RENDER": "RENDER", "TAO": "TAO", "IO": "IO"}

def candles(coin):
    body = {
        "type": "candleSnapshot",
        "req": {
            "coin": coin,
            "interval": "1d",
            "startTime": start_ms,
            "endTime": end_ms,
        },
    }
    data = json.dumps(body).encode()
    req = urllib.request.Request(INFO, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

frames = {}
failures = {}
all_symbols = list(MACROS.items()) + list(DEPIN.items())

for label, coin in all_symbols:
    try:
        c = candles(coin)
        if not c:
            failures[label] = "empty"
            print(f"  {label}: empty", file=sys.stderr)
            continue
        s = pd.Series(
            {pd.Timestamp(x["T"], unit="ms", tz="UTC").normalize(): float(x["c"]) for x in c},
            name=label,
        )
        frames[label] = s
        print(f"  {label}: {len(s)} candles")
    except Exception as e:
        failures[label] = str(e)[:120]
        print(f"  {label}: FAIL {str(e)[:80]}", file=sys.stderr)
    time.sleep(0.1)

print(f"\nSucceeded: {sorted(frames.keys())}")
print(f"Failed: {failures}")

missing = [m for m in ("BTC", "SOL", "NATGAS") if m in failures]
if missing:
    print(f"FATAL: missing primary assets {missing}")
    sys.exit(1)

prices = pd.concat(list(frames.values()), axis=1).sort_index()
prices.to_csv(".macro-cache/prices.csv")
print(f"\nPrices saved: {prices.shape[0]} rows x {prices.shape[1]} cols")
print(f"Date range: {prices.index[0].date()} => {prices.index[-1].date()}")
