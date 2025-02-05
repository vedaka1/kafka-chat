from dataclasses import dataclass


@dataclass(eq=False, init=False)
class ApplicationException(Exception):
    status_code: int = 500
    message: str = "An unknown error occurred"

    def __init__(self, *args, **kwargs):
        return super().__init__(self.message, *args, **kwargs)
