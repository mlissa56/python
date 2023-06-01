from typing import Optional, List
from pymongo import MongoClient
from account.model import Account, AccountStatus
from account.storage.protocol import AccountsStorageProtocol

class AccountsMongoStorage(AccountsStorageProtocol):
    def __init__(self):
        self.client = MongoClient("mongodb://localhost/")
        self.db = self.client["bank"]
        self.collection = self.db["accounts"]

    def get_all_accounts(self) -> List[Account]:
        all_accounts = self.collection.find({}, {"_id": 0})
        list_of_accounts = []
        for account_data in all_accounts:
            account = Account(
                id=account_data.get("id"),
                phone_number=account_data.get("phone_number"),
                password=account_data.get("password"),
                status=AccountStatus(account_data.get("status")),
            )
            list_of_accounts.append(account)
        return list_of_accounts

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        account = self.collection.find_one({"id": account_id})
        account_dataclass = Account(
            account['id'],
            account['phone_number'],
            account['password'],
            account['status']
        )
        return account_dataclass

    def mark_account_as_blocked(self, account_id: int):
        self.collection.update_one({"id": account_id}, {"$set": {"status": AccountStatus.BLOCKED.value}})

    def add_account(self) -> int:
        account_data = {"id": self.collection.count_documents({}) + 1, "phone_number": "", "password": "",
                        "status": AccountStatus.PENDING.value}
        self.collection.insert_one(account_data)
        return account_data["id"]

    def set_account_processing(self, account_id: int):
        account_data = self.collection.find_one({"id": account_id})
        if account_data:
            account_data["status"] = AccountStatus.PROCESSING.value
            self.collection.update_one({"id": account_id}, {"$set": {"status": AccountStatus.PROCESSING.value}})

    def set_account_pending(self, account_id: int):
        account_data = self.collection.find_one({"id": account_id})
        if account_data:
            account_data["status"] = AccountStatus.PENDING.value
            self.collection.update_one({"id": account_id}, {"$set": {"status": AccountStatus.PENDING.value}})

    def flush(self):
        self.collection.delete_many({})