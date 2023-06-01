import psycopg2
from typing import Optional, List
from account.model import Account
from account.storage.protocol import AccountsStorageProtocol


class AccountsPostgresStorage(AccountsStorageProtocol):
    def __init__(self):
        self.accounts = []  # список для хранения аккаунтов
        self.next_id = 1  # следующий id для нового аккаунта

    def get_all_accounts(self) -> List[Account]:  # получить все аккаунты из хранилища и вернуть их в виде списка.
        return self.accounts

    def get_account_by_id(self, account_id: int) -> Optional[Account]:  # получить аккаунт по id (опционально)
        for account in self.accounts:  # проходимся по списку
            if account.id == account_id:  # проверка соответствия
                return account  # аккаунт с нужным id
        return None  # не нашли

    def mark_account_as_blocked(self, account_id: int):
        account = self.get_account_by_id(account_id)  # получаем аккаунт по id
        if account:
            account.is_blocked = True  # аккаунт заблокирован

    def add_account(self) -> int:
        account = Account(id=self.next_id)  # создаем новый аккаунт с заданным id
        self.accounts.append(account)  # добавление аккаунта в список
        self.next_id += 1  # увеличение счетчика id
        return account.id  # вернуть id нового аккаунта

    def set_account_processing(self, account_id: int) -> Optional[Account]:
        account = self.get_account_by_id(account_id)  #
        if account:
            account.status = "processing"  # статус "в обработке"
            return account  # возвращаем обновленный аккаунт
        return None  # если аккаунт не найден

    def set_account_pending(self, account_id: int) -> Optional[Account]:
        account = self.get_account_by_id(account_id)
        if account:
            account.status = "pending"  # статус "ожидание"
            return account  # обновленный акк
        return None
