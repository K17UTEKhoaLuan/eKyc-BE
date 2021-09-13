
class Exception_Handle(Exception):
    def __init__(self, code: int, message: str, result: bool, field: str):
        self.code = code
        self.result = result
        self.field = field
        self.message = message
