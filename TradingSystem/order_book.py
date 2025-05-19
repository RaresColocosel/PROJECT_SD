from typing import Dict, List
from events import OrderPlaced, OrderCancelled, TradeExecuted
from models import Order, Trade

class OrderBook:
    def __init__(self):
        self.orders: Dict[str, Order] = {}
        self.trades: List[Trade] = []

    def apply(self, event):
        if isinstance(event, OrderPlaced):
            o = Order(event.order_id, event.user_id, event.side,
                      event.symbol, event.quantity, event.price)
            self.orders[event.order_id] = o
        elif isinstance(event, OrderCancelled):
            self.orders.pop(event.order_id, None)
        elif isinstance(event, TradeExecuted):
            t = Trade(event.trade_id, event.buy_order_id,
                      event.sell_order_id, event.symbol,
                      event.quantity, event.price, event.timestamp)
            self.trades.append(t)
            b = self.orders.get(t.buy_order_id)
            if b:
                b.quantity -= t.quantity
                if b.quantity <= 0:
                    self.orders.pop(b.order_id)
            s = self.orders.get(t.sell_order_id)
            if s:
                s.quantity -= t.quantity
                if s.quantity <= 0:
                    self.orders.pop(s.order_id)
