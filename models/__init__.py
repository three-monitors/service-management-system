import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
 
from client import Client
from appointment import Appointment
from service import Service
from order import Order
from patient_profile import PatientProfile
from product import Product
