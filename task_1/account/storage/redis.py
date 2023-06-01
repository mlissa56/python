from typing import Optional, List
from account.model import Account, AccountStatus
from account.storage.protocol import AccountsStorageProtocol
import redis

# не работает
class AccountsRedisStorage(AccountsStorageProtocol):
    def __init__(self):
        self.redis = redis.Redis()
        self.next_id = 1

    def get_all_accounts(self) -> List[Account]:
        account_keys = self.redis.keys("account:")
        accounts = []
        for key in account_keys:
            account_data = self.redis.hgetall(key)
            account = Account(
                id=int(account_data["id"]),
                phone_number=account_data["phone_number"],
                password=account_data["password"],
                status=AccountStatus(account_data["status"]),
            )
            accounts.append(account)
        return accounts

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        account_key = f"account:{account_id}"
        account_data = self.redis.hgetall(account_key)
        if account_data:
            account = Account(
                id=int(account_data["id"]),
                phone_number=account_data["phone_number"],
                password=account_data["password"],
                status=AccountStatus(account_data["status"]),
            )
            return account
        return None

    def mark_account_as_blocked(self, account_id: int):
        account_key = f"account:{account_id}"
        self.redis.hset(account_key, "status", AccountStatus.BLOCKED.value)

    def add_account(self) -> int:
        account = Account(id=self.next_id, phone_number='', password='')
        account_key = f"account:{self.next_id}"
        self.redis.hmset(account_key, {
            "id": str(account.id),
            "phone_number": account.phone_number,
            "password": account.password,
            "status": account.status.value,
        })
        self.next_id += 1
        return account.id

    def set_account_processing(self, account_id: int) -> Optional[Account]:
        account = self.get_account_by_id(account_id)
        if account:
            account.status = AccountStatus.PROCESSING
            account_key = f"account:{account_id}"
            self.redis.hset(account_key, "status", AccountStatus.PROCESSING.value)
            return account
        return None

    def set_account_pending(self, account_id: int) -> Optional[Account]:
        account = self.get_account_by_id(account_id)
        if account:
            account.status = AccountStatus.PENDING
            account_key = f"account:{account_id}"
            self.redis.hset(account_key, "status", AccountStatus.PENDING.value)
            return account
        return None
