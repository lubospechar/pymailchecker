from abc import ABC, abstractmethod
from typing import Optional
import imaplib

# ✅ CONTRACTS

class EmailCheckerContract(ABC):
    """
    Abstract contract for an email checker.

    This class defines the required methods for any implementation
    of an email checker, such as connecting to the email server,
    retrieving unread message counts, and disconnecting.
    """

    @abstractmethod
    def connect(self) -> None:
        """
        Establish a connection to the email server.

        Raises:
            ConnectionError: If unable to connect to the server.
        """
        ...

    @abstractmethod
    def get_unread_count(self) -> int:
        """
        Retrieve the number of unread emails.

        Returns:
            int: Number of unread emails.
        """
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """
        Disconnect from the email server.
        """
        ...


# ✅ IMPLEMENTATIONS

class ImapEmailChecker(EmailCheckerContract):
    """
    IMAP implementation of the EmailCheckerContract.

    This class provides methods to connect to an email server using IMAP,
    count unread messages in the inbox, and disconnect from the server.
    """

    INBOX_FOLDER = "inbox"  # Constant for the folder name to check

    def __init__(self, server: str, email: str, password: str) -> None:
        """
        Initialize the IMAP email checker with server credentials.

        Args:
            server (str): The IMAP server address.
            email (str): The email address to log in with.
            password (str): The password for authentication.
        """
        self.server: str = server
        self.email: str = email
        self.password: str = password
        self.imap_connection: Optional[imaplib.IMAP4_SSL] = None

    def connect(self) -> None:
        """
        Establish a connection to the IMAP server and log in.

        Raises:
            ConnectionError: If the connection or login fails.
        """
        if self.imap_connection is None:
            try:
                self.imap_connection = imaplib.IMAP4_SSL(self.server)
                self.imap_connection.login(self.email, self.password)
            except imaplib.IMAP4.error as e:
                raise ConnectionError(f"Failed to connect: {e}")

    def _ensure_connection(self) -> None:
        """
        Ensure that the connection to the IMAP server is active.

        If no connection exists, it will attempt to establish one.
        """
        if self.imap_connection is None:
            self.connect()

    def get_unread_count(self) -> int:
        """
        Get the number of unread emails in the inbox.

        Returns:
            int: The count of unread emails.

        Raises:
            RuntimeError: If there is an error accessing messages.
        """
        self._ensure_connection()
        try:
            self.imap_connection.select(ImapEmailChecker.INBOX_FOLDER)
            status, response = self.imap_connection.search(None, "UNSEEN")
            unread_msg_nums = response[0].split()
            return len(unread_msg_nums)
        except imaplib.IMAP4.error as e:
            raise RuntimeError(f"Error while fetching emails: {e}")

    def disconnect(self) -> None:
        """
        Log out and close the connection to the IMAP server.
        """
        if self.imap_connection:
            try:
                self.imap_connection.logout()
            finally:
                self.imap_connection = None
