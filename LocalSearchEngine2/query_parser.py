class QueryParser:
    @staticmethod
    def parse(input_str):
        paths = []
        contents = []
        for tok in input_str.strip().split():
            if tok.lower().startswith('path:'):
                val = tok[5:];
                if val: paths.append(val)
            elif tok.lower().startswith('content:'):
                val = tok[8:];
                if val: contents.append(val)
            else:
                contents.append(tok)
        return paths, contents