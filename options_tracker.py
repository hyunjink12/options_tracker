import yfinance as yf

symbol = input("Enter ticker symbol: ").upper().strip()
t = yf.Ticker(symbol)

# expiries
expiries = t.options
print(f"\nAvailable expiries ({len(expiries)} total):")
for i, exp in enumerate(expiries[:10]):
    print(f"  [{i}] {exp}")
if len(expiries) > 10:
    print(f"  ... and {len(expiries) - 10} more")

idx = int(input("\nSelect expiry index: "))
expiry = expiries[idx]

current_price = t.fast_info.last_price
print(f"\n{symbol} current price: ${current_price:.2f}")

# depth
depth = int(input("Contracts to show each side of ATM (e.g. 5 = 5 ITM, 1 ATM, 5 OTM): "))

# fetch
chain = t.option_chain(expiry)
calls = chain.calls.copy().reset_index(drop=True)
puts  = chain.puts.copy().reset_index(drop=True)

def slice_chain(df, current_price, option_type, depth):
    """Label ATM/ITM/OTM and return `depth` contracts on each side of ATM."""
    atm_idx = (df["strike"] - current_price).abs().idxmin()
    df["moneyness"] = df["strike"].apply(
        lambda s: "ITM" if (s < current_price if option_type == "call" else s > current_price) else "OTM"
    )
    df.loc[atm_idx, "moneyness"] = "ATM"
    return df.loc[max(0, atm_idx - depth): atm_idx + depth].reset_index(drop=True)

calls = slice_chain(calls, current_price, "call", depth)
puts  = slice_chain(puts,  current_price, "put",  depth)

cols = ["strike", "moneyness", "lastPrice", "bid", "ask", "volume", "openInterest", "impliedVolatility"]

print(f"\n--- CALLS (expiry: {expiry}) ---")
print(calls[cols].to_string(index=False))

print(f"\n--- PUTS (expiry: {expiry}) ---")
print(puts[cols].to_string(index=False))
