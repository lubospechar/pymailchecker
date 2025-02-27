from abc import ABC
from typing import List
from email_checker.email_checker import EmailCheckerContract


# ✅ CONTRACTS


# Contract for managing multiple email accounts
class MultiAccountCheckerContract(ABC):
    @abstractmethod
    def add_account(self, checker: EmailCheckerContract) -> None:
        """Adds a new email account to the manager."""
        pass

    @abstractmethod
    def check_all_unread_counts(self) -> None:
        """Checks all added accounts and returns the unread email count for each account."""
        pass


# ✅ IMPLEMENTATIONS


# Manager implementation for multiple accounts
class MultiAccountChecker(MultiAccountCheckerContract):
    def __init__(self) -> None:
        # Stores the list of all added email checkers
        self.email_checkers: List[EmailCheckerContract] = []

    def add_account(self, checker: EmailCheckerContract) -> None:
        """Adds a new email account to the list of managed accounts."""
        self.email_checkers.append(checker)

    def check_all_unread_counts(self) -> None:
        """Checks unread emails for all managed accounts and displays the results."""
        unread_emails_info = self.get_unread_emails_info()  # Retrieve unread email information
        self.display_unread_counts(unread_emails_info)  # Display formatted results

    def get_unread_emails_info(self) -> List[str]:
        """
        Checks unread emails for all accounts.

        Returns:
            A list describing the results of the email checks for each account.
        """
        results = []
        for checker in self.email_checkers:
            try:
                unread_count = checker.get_unread_count()  # Retrieve the unread email count
                results.append(f"Account {checker.email}: {unread_count} unread emails.")
            except Exception as e:
                # If an error occurs during data retrieval, add an error message
                results.append(f"Error checking account {checker.email}: {e}")
        return results

    @staticmethod
    def display_unread_counts(unread_emails_info: List[str]) -> None:
        """
        Displays the formatted results of unread email checks.

        Args:
            unread_emails_info (List[str]): A list of strings describing the results of the check.
        """
        for info in unread_emails_info:
            print(info)
