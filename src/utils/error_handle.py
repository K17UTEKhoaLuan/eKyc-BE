
class Exception_Handle(Exception):
    def __init__(self, name: str, code: int, message: str, result: bool, field: str, step: int):
        self.name = name
        self.code = code
        self.step = step
        self.result = result
        self.field = field
        self.message = message
