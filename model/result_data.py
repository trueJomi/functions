from datetime import datetime
from dateutil import parser

class ResultAlpaca:
    def __init__(self, close, high, low, numberOfTrades, open, timestamp, volume, volumeWeightedAveragePrice, symbol):
        self.close = close
        self.high = high
        self.low = low
        self.numberOfTrades = numberOfTrades
        self.open = open
        self.timestamp = timestamp
        self.volume = volume
        self.volumeWeightedAveragePrice = volumeWeightedAveragePrice
        self.symbol = symbol

    def to_dict(self):
        return {
            "close": self.close,
            "high": self.high,
            "low": self.low,
            "numberOfTrades": self.numberOfTrades,
            "open": self.open,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            "volume": self.volume,
            "volumeWeightedAveragePrice": self.volumeWeightedAveragePrice,
            "symbol": self.symbol
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            close=data.get("close"),
            high=data.get("high"),
            low=data.get("low"),
            numberOfTrades=data.get("numberOfTrades"),
            open=data.get("open"),
            timestamp=data.get("timestamp") if data.get("timestamp") else None,
            volume=data.get("volume"),
            volumeWeightedAveragePrice=data.get("volumeWeightedAveragePrice"),
            symbol=data.get("symbol")
        )