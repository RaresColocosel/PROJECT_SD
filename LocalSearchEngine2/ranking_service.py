class RankingService:
    def __init__(self):
        pass

    def rank(self, rows, content_terms):
        scored = []
        for r in rows:
            # Lower‐case the text fields
            content_text = (r.get("file_content") or "").lower()
            name_text    = (r.get("file_name")    or "").lower()

            score = 0
            for term in content_terms:
                term_low = term.lower()
                score += content_text.count(term_low)
                score += name_text.count(term_low)

            if not content_terms:
                score = 1

            new_r = dict(r)
            new_r["score"] = score
            scored.append(new_r)

        # Sort by score descending
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored
