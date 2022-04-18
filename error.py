class RequestError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


class CrowdedError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        return str(self.message)