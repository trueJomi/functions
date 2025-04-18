from datetime import datetime

class Predictions:
    def __init__(self, high: float, low: float, timestamp: datetime, symbol: str):
        self.high = high
        self.low = low
        self.timestamp = timestamp
        self.symbol = symbol

    def to_dict(self):
        return {
            "high": self.high,
            "low": self.low,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            "symbol": self.symbol
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            high=data.get("high"),
            low=data.get("low"),
            timestamp=datetime.fromisoformat(data.get("timestamp")) if data.get("timestamp") else None,
            symbol=data.get("symbol")
        )