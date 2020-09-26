class InvalidArgumentError(Exception):
    '''
    This exception will be thrown when the program argument is invalie
    '''
    def __init__(self, argument_name, argument_value=None):
        if argument_value is not None:
            msg = "'{}' is not a valid value for argument '{}'".format(
                argument_value, argument_name
            )
        else:
            msg = "Argument '{}' should not be empty".format(argument_name)
        super().__init__(msg)


class FileNotFoundException(Exception):
    def __init__(self, filename):
        super().__init__("'{}' does not exist or is inaccessible".format(filename))


class FileWriteError(Exception):
    def __init__(self, filename, reason):
        super().__init__("Error while writing to {} due to {}".format(filename, reason))