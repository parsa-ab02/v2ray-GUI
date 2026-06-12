from urllib.parse import urlparse, parse_qs, unquote

class ParsedURL:
    def __init__(self, raw_url: str):
        parsed = urlparse(raw_url)

        self.raw_url = raw_url
        self.scheme = parsed.scheme
        self.username = parsed.username
        self.password = parsed.password
        self.hostname = parsed.hostname
        self.port = parsed.port

        self.query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        self.fragment = unquote(parsed.fragment)

    def get_param(self, key: str, default=None):
        return self.query.get(key, default)

    def get_extra_params(self, known_params: list):
        return{ k: v 
                for k, v in self.query.items()
                if k not in known_params
            }