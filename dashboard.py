"""Simple command-line dashboard for DVS Quantum Bot."""

from __future__ import annotations

import sys
from typing import Callable, Dict

import main
from journal.emotional_journal import EmotionalJournal


journal = EmotionalJournal()

def start_bot() -> None:
    """Run the main trading loop."""
    try:
        main.main()
    except KeyboardInterrupt:
        print("\nTrading loop stopped.")


def show_journal() -> None:
    """Display stored journal entries."""
    if journal.entries:
        print("\n".join(journal.entries))
    else:
        print("No journal entries yet.")


def menu() -> None:
    actions: Dict[str, Callable[[], None]] = {
        "1": start_bot,
        "2": show_journal,
        "0": lambda: sys.exit(0),
    }

    while True:
        print("\nDVS Quantum Bot Dashboard")
        print("1. Start Trading Bot")
        print("2. Show Journal")
        print("0. Exit")
        choice = input("Select option: ").strip()
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    menu()
