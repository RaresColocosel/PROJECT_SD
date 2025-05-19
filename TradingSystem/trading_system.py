import uuid
from datetime import datetime

from event_store import EventStore
from order_book import OrderBook
from accounts import AccountsManager
from events import OrderPlaced, OrderCancelled, TradeExecuted, FundsDebited, FundsCredited

class TradingSystem:
    def __init__(self):
        self.event_store = EventStore()
        self.order_book = OrderBook()
        self.accounts   = AccountsManager()

    def append_and_apply(self, event):
        self.event_store.append(event)
        self.order_book.apply(event)
        self.accounts.apply(event)

    def deposit(self, user_id: str, amount: float):
        e = FundsCredited(user_id=user_id, amount=amount, timestamp=datetime.now())
        self.append_and_apply(e)

    def withdraw(self, user_id: str, amount: float):
        acct = self.accounts.get_account(user_id)
        if acct.balance < amount:
            raise ValueError("Insufficient funds")
        e = FundsDebited(user_id=user_id, amount=amount, timestamp=datetime.now())
        self.append_and_apply(e)

    def place_order(self, user_id: str, side: str, symbol: str, quantity: int, price: float) -> str:
        oid = str(uuid.uuid4())
        e = OrderPlaced(order_id=oid, user_id=user_id, side=side, symbol=symbol, quantity=quantity, price=price, timestamp=datetime.now())
        self.append_and_apply(e)
        self._match_orders(symbol)
        return oid

    def cancel_order(self, order_id: str):
        e = OrderCancelled(order_id=order_id, timestamp=datetime.now())
        self.append_and_apply(e)

    def _match_orders(self, symbol: str):
        while True:
            buys  = [o for o in self.order_book.orders.values() if o.symbol==symbol and o.side=='buy']
            sells = [o for o in self.order_book.orders.values() if o.symbol==symbol and o.side=='sell']
            if not buys or not sells:
                break
            best_buy  = max(buys,  key=lambda o: o.price)
            best_sell = min(sells, key=lambda o: o.price)
            if best_buy.price < best_sell.price:
                break
            qty   = min(best_buy.quantity, best_sell.quantity)
            price = best_sell.price
            tid   = str(uuid.uuid4())
            te = TradeExecuted(trade_id=tid, buy_order_id=best_buy.order_id, sell_order_id=best_sell.order_id, symbol=symbol, quantity=qty, price=price, timestamp=datetime.now())
            self.append_and_apply(te)
            self.append_and_apply(FundsDebited(user_id=best_buy.user_id, amount=qty*price, timestamp=datetime.now()))
            self.append_and_apply(FundsCredited(user_id=best_sell.user_id, amount=qty*price, timestamp=datetime.now()))

    def replay(self):
        new_book     = OrderBook()
        new_accounts = AccountsManager()
        for e in self.event_store.get_all_events():
            new_book.apply(e)
            new_accounts.apply(e)
        self.order_book = new_book
        self.accounts   = new_accounts
