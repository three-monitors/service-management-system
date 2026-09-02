import re
from typing import Dict


class Client:
    """Клас клієнта Beauty Clinic"""

    def __init__(self, id: int, name: str, phone: str, email: str):
        self._id = id
        self.__name = name
        self.__phone = phone
        self.__email = email

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self.__name = value

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str):
        if not re.fullmatch(r"\+\d{3}-\d{2}-\d{3}-\d{2}-\d{2}", value):
            raise ValueError("Invalid phone format. Use +380-XX-XXX-XX-XX")
        self.__phone = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", value):
            raise ValueError("Invalid email format")

        banned_domains = [".ru", ".su", ".рф"]
        email_lower = value.lower()
        for domain in banned_domains:
            if email_lower.endswith(domain):
                raise ValueError(f"The use of email with the {domain} domain is prohibited")
        self.__email = value

    def __str__(self) -> str:
        return f"Client: {self.__name} | Phone: {self.__phone} | Email: {self.__email}"

    def to_dict(self) -> Dict:
        return {
            "id": self._id,
            "name": self.__name,
            "phone": self.__phone,
            "email": self.__email
        }
