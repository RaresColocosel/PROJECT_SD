import re

class QueryParser:
    def __init__(self):
        pass

    def parse(self, raw_query):
        tokens = re.findall(r"\S+", raw_query)
        paths = []
        contents = []
        for t in tokens:
            low = t.lower()
            if low.startswith("path:"):
                val = t[len("path:"):]
                paths.append(val)
            elif low.startswith("content:"):
                val = t[len("content:"):]
                contents.append(val)
            else:
                # treat any “bare” word as a content term
                contents.append(t)
        return paths, contents
