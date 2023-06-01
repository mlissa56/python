from typing import Optional, List
from pymongo import MongoClient
from account.model import Account
from account.storage.protocol import AccountsStorageProtocol


class AccountsMongoStorage(AccountsStorageProtocol):
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['accounts_db']
        self.collection = self.db['accounts']

    def clear(self):
        self.collection.drop()

    def get_all_accounts(self) -> List[Account]:
        account_data = self.collection.find()
        return account_data

    def get_account_by_index(self, account_index: int) -> Optional[Account]:
        account_data = self.collection.find().skip(account_index - 1).limit(1) # тут вроде должно было сработать как пропуск [0] элемента
        account = None
        for data in account_data:
            account = Account()
            account.id = data.get("id")
            account.name = data.get("name")
        return account

    def mark_account_as_blocked(self, account_id: int):
        self.collection.update_one({"id": account_id}, {"$set": {"status": "blocked"}})

    def set_account_pending(self, account_id: int) -> Optional[Account]:
        self.collection.update_one({"id": account_id}, {"$set": {"status": "pending"}})
        account_data = self.collection.find_one({"id": account_id})
        if account_data:
            account = Account()
            account.id = account_data.get("id")
            account.name = account_data.get("name")
            return account
        return account_data
