from datetime import datetime

class Order:
    def __init__(self, order_id: str, user_id: str, side: str,
                 symbol: str, quantity: int, price: float):
        self.order_id = order_id
        self.user_id = user_id
        self.side = side
        self.symbol = symbol
        self.quantity = quantity
        self.price = price

class Trade:
    def __init__(self, trade_id: str, buy_order_id: str,
                 sell_order_id: str, symbol: str,
                 quantity: int, price: float, timestamp: datetime):
        self.trade_id = trade_id
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
