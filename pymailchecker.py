#!/usr/bin/env python3

from email_checker import EmailChecker, MultiAccountChecker

# ✅ POUŽITÍ
if __name__ == "__main__":
    # Vytvoření instancí pro různé účty
    checker1 = EmailChecker("", "", "")
    checker2 = EmailChecker("", "", "")

    # Vytvoření správce více účtů
    multi_checker = MultiAccountChecker()
    multi_checker.add_account(checker1)
    multi_checker.add_account(checker2)

    # Kontrola všech účtů
    multi_checker.check_all_unread_counts()
