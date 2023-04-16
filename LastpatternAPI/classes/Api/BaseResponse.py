import json


class BaseResponse:
    def __init__(self, isSuccess: bool, message: str, data) -> None:
        self.isSuccess = isSuccess
        self.message = message
        self.data = data

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def toDict(self):
        return self.__dict__