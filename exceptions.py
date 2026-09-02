class ClientNotFoundError(Exception):
    """Виключення для випадку, коли клієнт не знайдено"""
    pass


class InvalidPriceError(Exception):
    """Виключення для некоректної ціни"""
    pass


class InvalidMenuChoiceError(Exception):
    """Виключення для некоректного вибору меню"""
    pass
