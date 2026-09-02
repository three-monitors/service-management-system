class PatientProfile:
    """Клас профілю пацієнта Beauty Clinic"""

    def __init__(self, id: int, client_id: int, medical_history: str, allergies: str):
        self._id = id
        self.__client_id = client_id
        self.__medical_history = medical_history
        self.__allergies = allergies

    @property
    def id(self) -> int:
        return self._id

    @property
    def client_id(self) -> int:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: int):
        if value <= 0:
            raise ValueError("Client ID must be positive")
        self.__client_id = value

    @property
    def medical_history(self) -> str:
        return self.__medical_history

    @medical_history.setter
    def medical_history(self, value: str):
        if not value.strip():
            raise ValueError("Medical history cannot be empty")
        self.__medical_history = value

    @property
    def allergies(self) -> str:
        return self.__allergies

    @allergies.setter
    def allergies(self, value: str):
        self.__allergies = value

    def __str__(self) -> str:
        return f"PatientProfile: Client ID {self.__client_id} | History: {self.__medical_history} | Allergies: {self.__allergies}"
