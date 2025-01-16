class FBWebdriverException(Exception):
    pass


class ConfigException(Exception):
    pass


class FBWebdriverCouldNotLoginToFb(FBWebdriverException):
    pass


class FBWebdriverHasNotBeenInstanciated(FBWebdriverException):
    pass


class FBWebdriverInvalidConfigProvided(ConfigException):
    pass


class TokenParseException(ConfigException):
    pass


class Socks5ProxyParseFail(ConfigException):
    pass
