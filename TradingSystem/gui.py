import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from trading_system import TradingSystem
from replay import save_event_log, reconstruct_from_log

class TradingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Event-Sourced Trading System")
        self.geometry("800x600")
        self.ts = TradingSystem()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        self.create_account_tab()
        self.create_order_tab()
        self.create_cancel_tab()
        self.create_view_tab()

    def create_account_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Accounts')
        ttk.Label(frame, text='Deposit (user, amount):').grid(row=0, column=0, padx=5, pady=5)
        self.dep_user = ttk.Entry(frame);
        self.dep_user.grid(row=0, column=1, padx=5)
        self.dep_amt  = ttk.Entry(frame);
        self.dep_amt.grid(row=0, column=2, padx=5)
        ttk.Button(frame, text='Deposit', command=self.do_deposit).grid(row=0, column=3, padx=5)
        ttk.Label(frame, text='Withdraw (user, amount):').grid(row=1, column=0, padx=5, pady=5)
        self.wd_user = ttk.Entry(frame);
        self.wd_user.grid(row=1, column=1, padx=5)
        self.wd_amt  = ttk.Entry(frame);
        self.wd_amt.grid(row=1, column=2, padx=5)
        ttk.Button(frame, text='Withdraw', command=self.do_withdraw).grid(row=1, column=3, padx=5)
        ttk.Button(frame, text='Refresh Balances', command=self.refresh_balances).grid(row=2, column=0, padx=5, pady=10)
        ttk.Button(frame, text='Save Event Log', command=self.do_save_log).grid(row=2, column=1, padx=5, pady=10)
        ttk.Button(frame, text='Load Event Log', command=self.do_load_log).grid(row=2, column=2, padx=5, pady=10)
        self.bal_tree = ttk.Treeview(frame, columns=('user','balance'), show='headings')
        self.bal_tree.heading('user', text='User'); self.bal_tree.heading('balance', text='Balance')
        self.bal_tree.grid(row=3, column=0, columnspan=4, sticky='nsew')
        frame.rowconfigure(3, weight=1); frame.columnconfigure(2, weight=1)

    def create_order_tab(self):
        frame = ttk.Frame(self.notebook);
        self.notebook.add(frame, text='Place Order')
        labels = ['User ID','Side (buy/sell)','Symbol','Quantity','Price']
        self.order_entries = {}
        for i, lbl in enumerate(labels):
            ttk.Label(frame, text=lbl+':').grid(row=i, column=0, padx=5, pady=3, sticky='w')
            ent = ttk.Entry(frame); ent.grid(row=i, column=1, padx=5, sticky='ew')
            self.order_entries[lbl] = ent
        frame.columnconfigure(1, weight=1)
        ttk.Button(frame, text='Place Order', command=self.do_place_order).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def create_cancel_tab(self):
        frame = ttk.Frame(self.notebook);
        self.notebook.add(frame, text='Cancel Order')
        ttk.Label(frame, text='Order ID:').grid(row=0, column=0, padx=5, pady=5)
        self.cancel_id = ttk.Entry(frame);
        self.cancel_id.grid(row=0, column=1, padx=5)
        ttk.Button(frame, text='Cancel', command=self.do_cancel).grid(row=0, column=2, padx=5)

    def create_view_tab(self):
        frame = ttk.Frame(self.notebook); self.notebook.add(frame, text='View State')
        sub = ttk.Notebook(frame); sub.pack(fill='both', expand=True)
        obf = ttk.Frame(sub); sub.add(obf, text='Order Book'); ttk.Button(obf, text='Refresh Orders', command=self.refresh_orders).pack(padx=5, pady=5)
        self.ob_tree = ttk.Treeview(obf, columns=('id','user','side','sym','qty','price'), show='headings')
        for col, hd in zip(self.ob_tree['columns'], ['ID','User','Side','Symbol','Qty','Price']): self.ob_tree.heading(col, text=hd)
        self.ob_tree.pack(fill='both', expand=True)
        trf = ttk.Frame(sub); sub.add(trf, text='Trades'); ttk.Button(trf, text='Refresh Trades', command=self.refresh_trades).pack(padx=5, pady=5)
        self.tr_tree = ttk.Treeview(trf, columns=('tid','buy','sell','sym','qty','price','time'), show='headings')
        for col, hd in zip(self.tr_tree['columns'], ['Trade ID','BuyID','SellID','Symbol','Qty','Price','Time']): self.tr_tree.heading(col, text=hd)
        self.tr_tree.pack(fill='both', expand=True)

    def do_deposit(self):
        u, a = self.dep_user.get().strip(), float(self.dep_amt.get())
        self.ts.deposit(u, a); messagebox.showinfo("Success", f"Deposited {a} to {u}"); self.refresh_balances()

    def do_withdraw(self):
        u, a = self.wd_user.get().strip(), float(self.wd_amt.get())
        self.ts.withdraw(u, a); messagebox.showinfo("Success", f"Withdrew {a} from {u}"); self.refresh_balances()

    def do_place_order(self):
        vals = {lbl: ent.get().strip() for lbl, ent in self.order_entries.items()}
        oid = self.ts.place_order(vals['User ID'], vals['Side (buy/sell)'], vals['Symbol'], int(vals['Quantity']), float(vals['Price']))
        messagebox.showinfo("Order Placed", f"Order ID: {oid}");
        self.refresh_orders()

    def do_cancel(self):
        oid = self.cancel_id.get().strip()
        self.ts.cancel_order(oid)
        messagebox.showinfo("Cancelled", f"Cancelled order {oid}")
        self.refresh_orders()

    def do_save_log(self):
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files', '*.json')])
        if path:
            try:
                save_event_log(self.ts, path)
                messagebox.showinfo("Saved", f"Event log saved to {path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def do_load_log(self):
        path = filedialog.askopenfilename(defaultextension='.json', filetypes=[('JSON files', '*.json')])
        if path:
            try:
                self.ts = reconstruct_from_log(path)
                messagebox.showinfo("Loaded", f"Event log loaded from {path}")
                self.refresh_balances()
                self.refresh_orders()
                self.refresh_trades()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def refresh_balances(self):
        for i in self.bal_tree.get_children():
            self.bal_tree.delete(i)
        for uid, acct in self.ts.accounts.accounts.items():
            self.bal_tree.insert('', 'end', values=(uid, acct.balance))

    def refresh_orders(self):
        for i in self.ob_tree.get_children():
            self.ob_tree.delete(i)
        for o in self.ts.order_book.orders.values():
            self.ob_tree.insert('', 'end', values=(o.order_id, o.user_id, o.side, o.symbol, o.quantity, o.price))

    def refresh_trades(self):
        for i in self.tr_tree.get_children():
            self.tr_tree.delete(i)
        for t in self.ts.order_book.trades:
            self.tr_tree.insert('', 'end', values=(t.trade_id, t.buy_order_id, t.sell_order_id, t.symbol, t.quantity, t.price, t.timestamp))

if __name__ == '__main__':
    TradingApp().mainloop()
