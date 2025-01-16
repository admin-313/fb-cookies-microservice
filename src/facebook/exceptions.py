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


class TockenParseException(ConfigException):
    pass


class Socks5ProxyParseFail(ConfigException):
    pass
