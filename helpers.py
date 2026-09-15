import os
import shutil
from pathlib import Path
from typing import List, Union

class FileOrchestrator:
    def __init__(self, root: str = '.'):
        self.root = Path(root)

    def purge_patterns(self, patterns: List[str]) -> int:
        deleted_count = 0
        for pattern in patterns:
            for path in self.root.rglob(pattern):
                try:
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path)
                    deleted_count += 1
                except OSError:
                    continue
        return deleted_count

    def reorganize_by_extension(self, target_dir: str = 'archive') -> None:
        target = self.root / target_dir
        target.mkdir(exist_ok=True)
        
        for file in self.root.iterdir():
            if file.is_file() and file.parent != target:
                ext = file.suffix.lstrip('.') or 'no_ext'
                ext_dir = target / ext
                ext_dir.mkdir(exist_ok=True)
                file.rename(ext_dir / file.name)

def sanitize_workspace(base_path: str = '.') -> dict:
    orchestrator = FileOrchestrator(base_path)
    clean_count = orchestrator.purge_patterns(['*.tmp', '__pycache__', '.DS_Store'])
    orchestrator.reorganize_by_extension('storage')
    return {'status': 'success', 'items_removed': clean_count}