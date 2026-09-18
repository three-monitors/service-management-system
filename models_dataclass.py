from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    CREATED = "Created"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


@dataclass
class Client:
    name: str
    phone: str
    email: str = ""
    notes: str = ""

    def display(self) -> str:
        """Повертає відформатований рядок"""
        return f"{self.name} | {self.phone}"


@dataclass
class Service:
    name: str
    price: float
    duration_minutes: int

    def price_per_hour(self) -> float:
        """Обчислює ціну за годину"""
        return (self.price / self.duration_minutes) * 60 if self.duration_minutes > 0 else 0

    def formatted(self) -> str:
        """Повертає відформатований рядок"""
        return f"{self.name} — {self.price} грн ({self.duration_minutes} хв)"


@dataclass
class Order:
    client: Client
    service: Service
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)  # дата і час створення в системі
    appointment_date: datetime | None = None  # дата і час процедури
    notes: str = ""

    def total_price(self) -> float:
        """Повертає загальну ціну"""
        return self.service.price

    def summary(self) -> str:
        """Повертає короткий опис"""
        return f"[{self.status.value}] {self.client.name} — {self.service.name} — {self.service.price} грн. | {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def is_active(self) -> bool:
        """Перевіряє чи замовлення активне"""
        return self.status in [OrderStatus.CREATED, OrderStatus.IN_PROGRESS]
