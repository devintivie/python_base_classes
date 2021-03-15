class callable_dict(dict):
    def __getitem__(self, key):
        val = super().__getitem__(key)
        if callable(val):
            return val()
        return val