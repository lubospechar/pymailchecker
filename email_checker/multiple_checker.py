from abc import ABC, abstractmethod
from typing import List
from email_checker.email_checker import EmailCheckerContract


# ✅ KONTRAKTY

# Kontrakt pro správu více účtů
class MultiAccountCheckerContract(ABC):
    @abstractmethod
    def add_account(self, checker: EmailCheckerContract) -> None:
        """Přidá nový e-mailový účet do správce."""
        pass

    @abstractmethod
    def check_all_unread_counts(self) -> None:
        """Zkontroluje všechny přidané účty a vrátí počet nepřečtených e-mailů pro každý účet."""
        pass


# ✅ PŘÍSLIBY


# Implementace správce více účtů
class MultiAccountChecker(MultiAccountCheckerContract):
    def __init__(self) -> None:
        self.accounts: List[EmailCheckerContract] = []

    def add_account(self, checker: EmailCheckerContract) -> None:
        """Přidá nový účet."""
        self.accounts.append(checker)

    def check_all_unread_counts(self) -> None:
        """Zkontroluje všechny účty a vypíše počet nepřečtených e-mailů."""
        for account in self.accounts:
            try:
                unread_count = account.get_unread_count()
                print(f"Účet {account.email}: {unread_count} nepřečtených e-mailů.")
            except Exception as e:
                print(f"Chyba při kontrole účtu {account.email}: {e}")
