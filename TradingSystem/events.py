from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    timestamp: datetime

@dataclass
class OrderPlaced(Event):
    order_id: str
    user_id: str
    side: str
    symbol: str
    quantity: int
    price: float

@dataclass
class OrderCancelled(Event):
    order_id: str

@dataclass
class TradeExecuted(Event):
    trade_id: str
    buy_order_id: str
    sell_order_id: str
    symbol: str
    quantity: int
    price: float

@dataclass
class FundsDebited(Event):
    user_id: str
    amount: float

@dataclass
class FundsCredited(Event):
    user_id: str
    amount: float