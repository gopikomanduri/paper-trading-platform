from fyers_api import fyersModel
from app.config import settings

# Initialize FYERS API client
fyers = fyersModel.FyersModel(client_id=settings.fyers_client_id, token=settings.fyers_access_token)

def get_historical_data(symbol: str, resolution: str, range_from: str, range_to: str) -> dict:
    """
    Fetch historical data for a given symbol.
    """
    data = {
        "symbol": symbol,
        "resolution": resolution,  # E.g., "1D", "5m"
        "date_format": 1,
        "range_from": range_from,
        "range_to": range_to,
        "cont_flag": "1",
    }
    response = fyers.history(data)
    return response
