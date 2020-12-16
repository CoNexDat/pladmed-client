class InvalidParam(Exception):
    pass


class AnyValidator:
    def validate(self, param):
        pass


class BetweenValidator(AnyValidator):
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, param):
        if float(param) > self.max_val or float(param) < self.min_val:
            raise InvalidParam()


class MultiValueValidator(AnyValidator):
    def __init__(self, values):
        self.values = values

    def validate(self, param):
        if param not in self.values:
            raise InvalidParam()


class EmptyValidator(AnyValidator):
    def validate(self, param):
        if param != '':
            raise InvalidParam()
