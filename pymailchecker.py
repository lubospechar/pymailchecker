#!/usr/bin/env python3

import os
import json
from email_checker import ImapEmailChecker, MultiAccountChecker

CONFIG_FILE_PATH = os.path.expanduser("~/.config/pymailchecker/config.json")  # Configuration file path


def read_config():
    """
    Reads the configuration file in JSON format.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
    Returns:
        dict: The parsed content of the configuration file.
    """
    if not os.path.exists(CONFIG_FILE_PATH):
        raise FileNotFoundError(f"Configuration file {CONFIG_FILE_PATH} does not exist!")

    # Open and read the configuration JSON file
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


def initialize_accounts(config):
    """Initializes and returns account checkers based on the given configuration."""
    account_checker = MultiAccountChecker()
    for account in config["accounts"]:
        email_checker = ImapEmailChecker(
            server=account["server"],
            email=account["email"],
            password=account["password"]
        )
        account_checker.add_account(email_checker)
    return account_checker


if __name__ == "__main__":
    try:
        config = load_config()
        account_checker = initialize_accounts(config)
        account_checker.check_all_unread_counts()
    except Exception as error:
        print(f"Error: {error}")
