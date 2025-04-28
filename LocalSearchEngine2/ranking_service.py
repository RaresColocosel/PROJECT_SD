from datetime import datetime

class RankingService:
    def score(self, file, content_terms):
        score = file.get('index_score') or 0
        raw_content = file.get('file_content') or ''
        text = raw_content.lower()
        for term in content_terms:
            if not term:
                continue
            score += text.count(term.lower())
        try:
            last_str = file.get('last_access_time') or file.get('indexed_at')
            last = datetime.fromisoformat(last_str)
            days = (datetime.now() - last).days
            score += max(0, 7 - days)
        except Exception:
            pass
        return score

    def rank(self, files, content_terms):
        for f in files:
            f['score'] = self.score(f, content_terms)
        return sorted(files, key=lambda x: x['score'], reverse=True)
