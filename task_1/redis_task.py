from typing import Optional, List
from account.model import Account, AccountStatus
from account.storage.protocol import AccountsStorageProtocol

class AccountsRedisStorage(AccountsStorageProtocol):
    def __init__(self):
        self.redis = RedisConnection() # тут подключение к redis

    def clear(self):
        self.redis.flushdb()
        
    def get_all_accounts(self) -> List[Account]:
        account_ids = self.redis.lrange("accounts", 0, -1) # получение всех id
        accounts = []
        return accounts # возвращаем список аккаунтов
    
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        account_data = self.redis.get(str(account_id)) # получение данные по id
        if account_data: # если данные получили
            return Account(id=account_data.get('id'), name=account_data.get('name'))
        return None # если не получили

    def mark_account_as_blocked(self, account_id: int):
        self.redis.set(str(account_id), "status", "blocked")

    def add_account(self) -> int:
        account_id = self.redis.incr("account_counter") #новый id аккаунта
        self.redis.lpush("accounts", account_id) # добавление в список
        return account_id # возвращение идентификатора нового аккаунта
    
    def set_account_processing(self, account_id: int) -> Optional[Account]:
        if self.redis.hexists(str(account_id), "status"): # Returns a boolean indicating if key exists within hash name - Union[Awaitable[bool], bool] (тут проверка существует ли аккаунт)
            self.redis.lset(str(account_id), "status", "processing") # статус
            account_data = self.redis.get(str(account_id)) # получаем данные из redis
            if account_data:
                account = Account() # тут создается новый объект Account и заполняются его данные
                account.id = account_data.get("id")
                account.name = account_data.get("name")
            return account
        return None

    def set_account_pending(self, account_id: int) -> Optional[Account]:
        account_data = self.redis.get(str(account_id)) # проверяем данные аккаунта из redis
        if account_data and "status" in account_data: # проверяем, существует ли аккаунт и имеет ли он статус
            self.redis.lset(str(account_id), "status", "pending") # устанавливаем pending
            account = Account() # то же самое
            account.id = account_data.get("id")
            account.name = account_data.get("name")
            return account
        return account


