from typing import Optional, List
from account.model import Account, AccountStatus
from account.storage.protocol import AccountsStorageProtocol

# рабочее решение

class AccountsPostgresStorage(AccountsStorageProtocol):
    def __init__(self):
        self.accounts = []
        self.next_id = 1

    def get_all_accounts(self) -> List[Account]:
        return self.accounts

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        for account in self.accounts:
            if account.id == account_id:
                return account
        return None

    def mark_account_as_blocked(self, account_id: int):
        account = self.get_account_by_id(account_id)
        if account:
            account.status = AccountStatus.BLOCKED

    def add_account(self) -> int:
        account = Account(id=self.next_id, phone_number='', password='')
        self.accounts.append(account)
        self.next_id += 1
        return account.id

    def set_account_processing(self, account_id: int) -> Optional[Account]:
        account = self.get_account_by_id(account_id)
        if account:
            account.status = AccountStatus.PROCESSING
            return account
        return None

    def set_account_pending(self, account_id: int) -> Optional[Account]:
        account = self.get_account_by_id(account_id)
        if account:
            account.status = AccountStatus.PENDING
            return account
        return None
