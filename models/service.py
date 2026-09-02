class Service:
    """Клас послуги Beauty Clinic"""

    def __init__(self, id: int, name: str, price: float, duration: int):
        self._id = id
        self.__name = name
        self.__price = price
        self.__duration = duration

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Service name cannot be empty")
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
    def duration(self) -> int:
        return self.__duration

    @duration.setter
    def duration(self, value: int):
        if value <= 0:
            raise ValueError("Duration must be positive")
        self.__duration = value

    def __str__(self) -> str:
        return f"Service: {self.__name} | Price: {self.__price} грн. | Duration: {self.__duration} min"
