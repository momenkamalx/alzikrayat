import re


class Router:
    def __init__(self):
        self.routes = []

    """
        Register one route
        method: HTTP method string ("GET", "POST")
        pattern: URL pattern
        handler: function to call when this route match
    """
    def add(self, method, pattern, handler):
        param_names = re.findall(r"\{(\w+)(?::int)?\}", pattern)

        def replace(match):
            return r"(\d+)" if match.group(0).endswith(":int}") else r"([^/]+)"

        regex_str = re.sub(r"\{\w+(?::int)?\}", replace, pattern)
        compiled = re.compile("^" + regex_str + "$")
        self.routes.append((method.upper(), compiled, param_names, handler))


        """
        Match an incoming (method, path) against every registered route
        in registration order and calls and returns the first matching
        handler result or None if nothing matches (404)
        """
        
    def dispatch(self, method, path):
        for route_method, regex, param_names, handler in self.routes:
            if route_method != method.upper():
                continue
            match = regex.match(path)
            if match:
                kwargs = dict(zip(param_names, match.groups()))
                return handler(**kwargs)
        return None