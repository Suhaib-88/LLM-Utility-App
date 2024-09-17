
class LLMAppException(Exception):
    __module__="app"

    def __init__(self, message= "Unspecified Error") -> None:
        super().__init__(message)
        self.message= message


class ConfigKeyException(LLMAppException):
    def __init__(self,config_key):
        message= f"{config_key} is not a valid configuration key"
        super().__init__(message)

class HomePathDoesNotExistException(LLMAppException):
    def __init__(self, home_path):
        message= f"`{home_path}` file_path does not exist"
        super().__init__(message)

class DependencyNotInstalledException(LLMAppException):
    def __init__(self, required_library_dependency):
        message= f"`{required_library_dependency}` needs to be installed for this function"
        super().__init__(message)