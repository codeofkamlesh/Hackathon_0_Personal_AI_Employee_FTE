"""
File System Watcher - Monitors a drop folder for new files
Part of Personal AI Employee Bronze Tier Implementation
"""

import shutil
from pathlib import Path
from datetime import datetime
from base_watcher import BaseWatcher


class FileSystemWatcher(BaseWatcher):
    """Watches a drop folder and creates action items for new files"""

    def __init__(self, vault_path: str, drop_folder: str, check_interval: int = 30):
        super().__init__(vault_path, check_interval)
        self.drop_folder = Path(drop_folder)
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        self.processed_files = set()

        self.logger.info(f'Watching drop folder: {self.drop_folder}')

    def check_for_updates(self) -> list:
        """Check drop folder for new files"""
        new_files = []

        try:
            for file_path in self.drop_folder.iterdir():
                # Skip directories and already processed files
                if file_path.is_dir():
                    continue

                file_id = f"{file_path.name}_{file_path.stat().st_mtime}"

                if file_id not in self.processed_files:
                    new_files.append(file_path)
                    self.processed_files.add(file_id)

        except Exception as e:
            self.logger.error(f'Error scanning drop folder: {e}')

        return new_files

    def create_action_file(self, file_path: Path) -> Path:
        """Create action file for dropped file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        action_filename = f'FILE_{timestamp}_{file_path.stem}.md'
        action_filepath = self.needs_action / action_filename

        # Get file metadata
        file_stats = file_path.stat()
        file_size = file_stats.st_size
        file_size_kb = file_size / 1024

        # Create action file content
        content = f"""---
type: file_drop
original_name: {file_path.name}
original_path: {file_path.absolute()}
size_bytes: {file_size}
size_kb: {file_size_kb:.2f}
detected: {datetime.now().isoformat()}
status: pending
priority: medium
---

## New File Detected

A new file has been dropped into the Inbox folder and requires processing.

### File Details
- **Name**: {file_path.name}
- **Size**: {file_size_kb:.2f} KB
- **Type**: {file_path.suffix or 'No extension'}
- **Location**: {file_path.absolute()}

### Suggested Actions
- [ ] Review file contents
- [ ] Determine appropriate action
- [ ] Process or categorize the file
- [ ] Move to appropriate folder when complete

### Processing Notes
_Add notes here during processing_

---
*Created by File System Watcher*
"""

        # Write action file
        action_filepath.write_text(content, encoding='utf-8')

        return action_filepath


if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    vault_path = sys.argv[1] if len(sys.argv) > 1 else '../AI_Employee_Vault'
    drop_folder = sys.argv[2] if len(sys.argv) > 2 else '../AI_Employee_Vault/Inbox'

    # Create and run watcher
    watcher = FileSystemWatcher(
        vault_path=vault_path,
        drop_folder=drop_folder,
        check_interval=30
    )

    try:
        watcher.run()
    except KeyboardInterrupt:
        print('\nWatcher stopped by user')
