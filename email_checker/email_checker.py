from abc import ABC, abstractmethod
from typing import Optional, List
import imaplib


# ✅ KONTRAKTY

# Kontrakt pro emailového kontrolera
class EmailCheckerContract(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Připojí se k e-mailovému serveru."""
        ...

    @abstractmethod
    def get_unread_count(self) -> int:
        """Vrátí počet nepřečtených e-mailů."""
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """Odpojí se od serveru."""
        ...


# ✅ PŘÍSLIBY

# Implementace pro IMAP email checker
class ImapEmailChecker(EmailCheckerContract):
    def __init__(self, server: str, email: str, password: str) -> None:
        self.server: str = server
        self.email: str = email
        self.password: str = password
        self.connection: Optional[imaplib.IMAP4_SSL] = None

    def connect(self) -> None:
        """Připojí se k serveru pomocí IMAP."""
        try:
            self.connection = imaplib.IMAP4_SSL(self.server)
            self.connection.login(self.email, self.password)
        except imaplib.IMAP4.error as e:
            raise ConnectionError(f"Chyba při připojování: {e}")

    def get_unread_count(self) -> int:
        """Vrátí počet nepřečtených e-mailů v INBOXu."""
        if self.connection is None:
            self.connect()

        try:
            self.connection.select("inbox")
            status, response = self.connection.search(None, 'UNSEEN')
            unread_msg_nums = response[0].split()
            return len(unread_msg_nums)
        except imaplib.IMAP4.error as e:
            raise RuntimeError(f"Chyba při čtení e-mailů: {e}")
        finally:
            self.disconnect()

    def disconnect(self) -> None:
        """Odhlásí se a zavře spojení."""
        if self.connection:
            self.connection.logout()
            self.connection = None