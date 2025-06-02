from collections import Counter
from datetime import datetime

def summarize_by_file_type(results):
    ct = Counter()
    for r in results:
        ft = r.get("file_type") or "unknown"
        ct[ft] += 1
    return ct.most_common()

def summarize_by_year(results):
    ct = Counter()
    for r in results:
        ia = r.get("indexed_at")
        if isinstance(ia, datetime):
            year = ia.year
        else:
            year = "unknown"
        ct[year] += 1
    return ct.most_common()

def summarize_by_language(results):
    ct = Counter()
    for r in results:
        ft = r.get("file_type") or "unknown"
        ct[ft] += 1
    return ct.most_common()
