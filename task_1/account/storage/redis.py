from typing import Optional, List
from account.model import Account, AccountStatus
from account.storage.protocol import AccountsStorageProtocol
import redis

# тоже с ошибкой
class AccountsRedisStorage(AccountsStorageProtocol):
    def __init__(self):
        self.redis = redis.Redis()
        self.next_id = 1

    def clear(self):
        self.redis.flushdb()

    def get_all_accounts(self) -> List[Account]:
        account_ids = self.redis.lrange("accounts", 0, -1)
        accounts = []
        for account_id in account_ids:
            account_data = self.redis.hgetall(str(account_id))
            account = Account(
                id=int(account_data.get("id", 0)),
                phone_number=account_data.get("phone_number"),
                password=account_data.get("password"),
                status=AccountStatus(account_data.get("status")),
            )
            accounts.append(account)
        return accounts

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        account_data = self.redis.hgetall(str(account_id))
        if account_data:
            account = Account(
                id=int(account_data.get("id", 0)),
                phone_number=account_data.get("phone_number"),
                password=account_data.get("password"),
                status=AccountStatus(account_data.get("status")),
            )
            return account
        return None

    def mark_account_as_blocked(self, account_id: int):
        self.redis.hset(str(account_id), "status", AccountStatus.BLOCKED.value)

    def add_account(self) -> int:
        account_id = self.redis.incr("account_counter")
        self.redis.lpush("accounts", str(account_id))
        return account_id

    def set_account_processing(self, account_id: int) -> Optional[Account]:
        if self.redis.hexists(str(account_id), "status"):
            self.redis.hset(str(account_id), "status", AccountStatus.PROCESSING.value)
            account_data = self.redis.hgetall(str(account_id))
            if account_data:
                account = Account(
                    id=int(account_data.get("id", 0)),
                    phone_number=account_data.get("phone_number"),
                    password=account_data.get("password"),
                    status=AccountStatus(account_data.get("status")),
                )
                return account
        return None

    def set_account_pending(self, account_id: int) -> Optional[Account]:
        account_data = self.redis.hgetall(str(account_id))
        if account_data and "status" in account_data:
            self.redis.hset(str(account_id), "status", AccountStatus.PENDING.value)
            account = Account(
                id=int(account_data.get("id", 0)),
                phone_number=account_data.get("phone_number"),
                password=account_data.get("password"),
                status=AccountStatus(account_data.get("status")),
            )
            return account
        return None
