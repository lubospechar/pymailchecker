#!/usr/bin/env python3

import os
import json
from email_checker import ImapEmailChecker, MultiAccountChecker


# ✅ Funkce pro načtení konfigurace
def load_config():
    config_path = os.path.expanduser("~/.config/pymailchecker/config.json")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Konfigurační soubor {config_path} neexistuje!")

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ✅ Hlavní část programu
if __name__ == "__main__":
    try:
        config = load_config()

        # Vytvoření správce více účtů
        multi_checker = MultiAccountChecker()

        # Projdeme všechny účty v konfiguraci
        for account in config["accounts"]:
            checker = ImapEmailChecker(account["server"], account["email"], account["password"])
            multi_checker.add_account(checker)

        # Kontrola všech účtů
        multi_checker.check_all_unread_counts()

    except Exception as e:
        print(f"Chyba: {e}")
