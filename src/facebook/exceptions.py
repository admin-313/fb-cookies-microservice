class FBWebdriverException(Exception):
    pass

class FBWebdriverCouldNotLoginToFb(FBWebdriverException):
    pass

class FBWebdriverHasNotBeenInstanciatedException(FBWebdriverException):
    pass

class FBWebdriverCouldNotParseToken(FBWebdriverException):
    pass

class FBWebdriverInvalidConfigProvided(FBWebdriverException):
    pass