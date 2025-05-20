class IdNotFoundException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class InvalidEmotionResultException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class InsufficientInputDataException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class SQLError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class InvalidGeminiResponseException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

