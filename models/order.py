import sys
import os
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, current_dir)
 
from models.appointment import Appointment


class Order(Appointment):
    """Клас замовлення (успадкує від Appointment)"""

    def __init__(self, id: int, client: str, service: str, master: str, 
                 status: str, date: str, total_price: float):
        super().__init__(id, client, service, master, status, date, total_price)

    @property
    def service(self) -> str:
        """Замінює procedure на service для Order"""
        return self.procedure

    @service.setter
    def service(self, value: str):
        """Замінює procedure на service для Order"""
        self.procedure = value

    def __str__(self) -> str:
        return f"Order: {self.client} | {self.service} | {self.master} | {self.status} | {self.date} | {self.total_price} грн."
