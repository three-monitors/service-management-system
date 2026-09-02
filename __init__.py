from managers.service_manager import ServiceManager
from models.product import Product
from models.patient_profile import PatientProfile
from models.order import Order
from models.service import Service
from models.appointment import Appointment
from models.client import Client
from exceptions import (
    ClientNotFoundError,
    InvalidPriceError,
    InvalidMenuChoiceError
)
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
