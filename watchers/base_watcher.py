"""
Base Watcher Class - Template for all watchers
Part of Personal AI Employee Bronze Tier Implementation
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime


class BaseWatcher(ABC):
    """Abstract base class for all watcher implementations"""

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = self._setup_logger()

        # Ensure required directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)

    def _setup_logger(self):
        """Configure logging for this watcher"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        # Console handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items to process.
        Returns: List of items that need action
        """
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create a .md file in Needs_Action folder for the item.
        Returns: Path to created file
        """
        pass

    def run(self):
        """Main loop - continuously check for updates"""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Monitoring vault at: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval} seconds')

        while True:
            try:
                items = self.check_for_updates()

                if items:
                    self.logger.info(f'Found {len(items)} new item(s) to process')

                for item in items:
                    try:
                        filepath = self.create_action_file(item)
                        self.logger.info(f'Created action file: {filepath.name}')
                    except Exception as e:
                        self.logger.error(f'Error creating action file: {e}')

            except Exception as e:
                self.logger.error(f'Error in check loop: {e}')

            time.sleep(self.check_interval)
