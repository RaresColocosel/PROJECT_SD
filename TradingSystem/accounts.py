from typing import Dict
from events import FundsDebited, FundsCredited

class Account:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.balance = 0.0

class AccountsManager:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}

    def apply(self, event):
        if not isinstance(event, (FundsDebited, FundsCredited)):
            return
        acct = self.accounts.get(event.user_id)
        if acct is None:
            acct = Account(event.user_id)
            self.accounts[event.user_id] = acct
        if isinstance(event, FundsDebited):
            acct.balance -= event.amount
        else:
            acct.balance += event.amount

    def get_account(self, user_id: str) -> Account:
        acct = self.accounts.get(user_id)
        if acct is None:
            acct = Account(user_id)
            self.accounts[user_id] = acct
        return acct
