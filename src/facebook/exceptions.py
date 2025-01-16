class FBWebdriverException(Exception):
    pass

class FBWebdriverCouldNotLoginToFb(FBWebdriverException):
    pass

class FBWebdriverHasNotBeenInstanciated(FBWebdriverException):
    pass

class FBWebdriverCouldNotParseToken(FBWebdriverException):
    pass

class FBWebdriverInvalidConfigProvided(FBWebdriverException):
    pass