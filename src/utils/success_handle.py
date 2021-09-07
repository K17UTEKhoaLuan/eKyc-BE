class Success_Handle:
    def __init__(self, result: str, code: int, message: str, data: dict):
        self.result = result
        self.code = code
        self.messsage = message
        self.data = data
    def success_return(self):
        return {
            "result": self.result,
            "message": self.messsage,
            "data": self.data
        }