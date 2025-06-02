from cachetools import LRUCache

class DatabaseSearchService:
    def __init__(self, db_handler, parser, ranker, widget_factory):
        self._db             = db_handler
        self._parser         = parser
        self._ranker         = ranker
        self._widget_factory = widget_factory

    def search(self, raw_query):
        paths, content_terms = self._parser.parse(raw_query)

        all_rows = self._db.list_all()

        def norm_path(p):
            return (p or "").replace("\\", "/").lower()

        filtered = all_rows
        for p in paths:
            lower_p = p.replace("\\", "/").lower()
            filtered = [
                r for r in filtered
                if lower_p in norm_path(r.get("file_path"))
            ]

        for term in content_terms:
            tlow = term.lower()
            tmp = []
            for r in filtered:
                content_text = (r.get("file_content") or "").lower()
                name_text    = (r.get("file_name") or "").lower()
                if tlow in content_text or tlow in name_text:
                    tmp.append(r)
            filtered = tmp

        ranked = self._ranker.rank(filtered, content_terms)

        widget_html_list = self._widget_factory.get_widgets(raw_query, ranked)

        return {
            "results": ranked,
            "widgets":  widget_html_list
        }


class CachingSearchService:
    def __init__(self, underlying, max_cache_size=128):
        self._underlying = underlying
        self._cache      = LRUCache(maxsize=max_cache_size)
        self.hits        = 0
        self.misses      = 0

    def search(self, query):
        if query in self._cache:
            self.hits += 1
            return self._cache[query]
        else:
            self.misses += 1
            result = self._underlying.search(query)
            self._cache[query] = result
            return result

    def cache_info(self):
        return {
            "hits":    self.hits,
            "misses":  self.misses,
            "currsize": len(self._cache),
            "maxsize":  self._cache.maxsize
        }
