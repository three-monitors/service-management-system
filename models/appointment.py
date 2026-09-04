import re
from typing import Dict
from exceptions import InvalidPriceError


class Appointment:
    """Клас запису на процедуру"""

    def __init__(self, id: int, client: str, procedure: str, master: str,
                 status: str, date: str, total_price: float):
        self._id = id
        self.__client = client
        self.__procedure = procedure
        self.__master = master
        self.__status = status
        self.__date = date
        self.__total_price = total_price

    @property
    def id(self) -> int:
        return self._id

    @property
    def client(self) -> str:
        return self.__client

    @client.setter
    def client(self, value: str):
        if not value.strip():
            raise ValueError("Client name cannot be empty")
        self.__client = value

    @property
    def procedure(self) -> str:
        return self.__procedure

    @procedure.setter
    def procedure(self, value: str):
        if not value.strip():
            raise ValueError("Procedure cannot be empty")
        self.__procedure = value

    @property
    def master(self) -> str:
        return self.__master

    @master.setter
    def master(self, value: str):
        if not value.strip():
            raise ValueError("Master name cannot be empty")
        self.__master = value

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str):
        valid_statuses = ["Scheduled", "In Progress", "Done", "Cancelled"]
        if value not in valid_statuses:
            raise ValueError(
                f"Invalid status. Must be one of: {valid_statuses}")
        self.__status = value

    @property
    def date(self) -> str:
        return self.__date

    @date.setter
    def date(self, value: str):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        self.__date = value

    @property
    def total_price(self) -> float:
        return self.__total_price

    @total_price.setter
    def total_price(self, value: float):
        if value < 0:
            raise InvalidPriceError("Price cannot be negative")
        self.__total_price = value

    def __str__(self) -> str:
        return f"{self.__client} | {self.__procedure} | {self.__master} | {self.__status} | {self.__date} | {self.__total_price} грн."

    def to_dict(self) -> Dict:
        return {
            "id": self._id,
            "client": self.__client,
            "procedure": self.__procedure,
            "master": self.__master,
            "status": self.__status,
            "date": self.__date,
            "total_price": self.__total_price
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Класовий метод: створює об'єкт Appointment зі словника"""
        return cls(
            data["id"],
            data["client"],
            data["procedure"],
            data["master"],
            data["status"],
            data["date"],
            data["total_price"]
        )
