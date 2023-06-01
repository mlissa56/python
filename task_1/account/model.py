from dataclasses import dataclass
from enum import Enum
import json

class AccountStatus(Enum):
    BLOCKED: str = "blocked"
    PENDING: str = "pending"
    PROCESSING: str = "processing"

@dataclass
class Account:
    id: int
    phone_number: str
    password: str
    status: AccountStatus = AccountStatus.PENDING

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "password": self.password,
            "status": self.status.value,
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict())

    @classmethod
    def from_dict(cls, account_dict: dict) -> "Account":
        return cls(
            id=account_dict["id"],
            phone_number=account_dict["phone_number"],
            password=account_dict["password"],
            status=AccountStatus(account_dict["status"]),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "Account":
        account_dict = json.loads(json_str)
        return cls.from_dict(account_dict)