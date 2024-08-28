import requests


COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

def get_crypto_price(symbol: str):
    response = requests.get(f'{COINGECKO_API_URL}/simple/price', params={
        "ids": symbol,
        "vs_currencies": "usd"
    })
    
    if response.status_code == 200:
        data = response.json()
        return data.get(symbol, {}).get("usd", None)
    else:
        return None