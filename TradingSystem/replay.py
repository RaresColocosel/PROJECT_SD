import json
from datetime import datetime
from events import OrderPlaced, OrderCancelled, TradeExecuted, FundsDebited, FundsCredited
from trading_system import TradingSystem

EVENT_TYPE_MAP = {
    'OrderPlaced': OrderPlaced,
    'OrderCancelled': OrderCancelled,
    'TradeExecuted': TradeExecuted,
    'FundsDebited': FundsDebited,
    'FundsCredited': FundsCredited,
}

def load_event_log(filepath: str):
    with open(filepath, 'r') as f:
        raw_events = json.load(f)
    events = []
    for raw in raw_events:
        etype = raw.get('type')
        cls = EVENT_TYPE_MAP.get(etype)
        if cls is None:
            raise ValueError(f"Unknown event type: {etype}")
        timestamp = datetime.fromisoformat(raw.get('timestamp'))
        kwargs = {k: v for k, v in raw.items() if k not in ('type', 'timestamp')}
        events.append(cls(timestamp=timestamp, **kwargs))
    return events

def save_event_log(system: TradingSystem, filepath: str):
    serial = []
    for event in system.event_store.get_all_events():
        data = {'type': event.__class__.__name__, 'timestamp': event.timestamp.isoformat()}
        for field, value in event.__dict__.items():
            if field != 'timestamp':
                data[field] = value
        serial.append(data)
    with open(filepath, 'w') as f:
        json.dump(serial, f, indent=2)

def reconstruct_from_log(filepath: str) -> TradingSystem:
    events = load_event_log(filepath)
    ts = TradingSystem()
    ts.event_store._events = events
    ts.replay()
    return ts


