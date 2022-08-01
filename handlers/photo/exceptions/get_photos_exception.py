class GetPhotosException(Exception):
    def __init__(self, message: str = None):
        self.__message = message

    def __str__(self):
        return self.__message
