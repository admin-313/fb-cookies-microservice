class FBWebdriverException(Exception):
    pass

class FBWebdriverCouldNotLoginToFb(FBWebdriverException):
    pass

class FBWebdriverHasNotBeenInstanciatedException(FBWebdriverException):
    pass