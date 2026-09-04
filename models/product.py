from exceptions import InvalidPriceError

class Product:
    """Клас продукту Beauty Clinic"""

    def __init__(self, id: int, name: str, price: float, stock: int):
        self._id = id
        self.__name = name
        self.__price = price
        self.__stock = stock

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Product name cannot be empty")
        self.__name = value

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise InvalidPriceError("Price cannot be negative")
        self.__price = value

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, value: int):
        if value < 0:
            raise ValueError("Stock cannot be negative")
        self.__stock = value

    def __str__(self) -> str:
        return f"Product: {self.__name} | Price: {self.__price} грн. | Stock: {self.__stock}"
