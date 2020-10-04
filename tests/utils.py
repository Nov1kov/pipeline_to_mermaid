class StubObject:
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [StubObject(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, StubObject(b) if isinstance(b, dict) else b)