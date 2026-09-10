import os
import shutil
from pathlib import Path
from typing import Union, List

class CleanupEngine:
    def __init__(self, target_dir: Union[str, Path]):
        self.target = Path(target_dir)

    def purge_by_extension(self, extensions: List[str]) -> int:
        count = 0
        for item in self.target.rglob('*'):
            if item.suffix.lower() in extensions:
                try:
                    item.unlink()
                    count += 1
                except OSError:
                    continue
        return count

    def reorg_files(self, mapping: dict) -> None:
        for file_path in self.target.iterdir():
            if file_path.is_file():
                dest_folder = mapping.get(file_path.suffix.lower(), 'misc')
                target_dir = self.target / dest_folder
                target_dir.mkdir(exist_ok=True)
                shutil.move(str(file_path), str(target_dir / file_path.name))

def run_maintenance(path: str):
    engine = CleanupEngine(path)
    purged = engine.purge_by_extension(['.tmp', '.log', '.bak'])
    engine.reorg_files({'.jpg': 'images', '.pdf': 'docs', '.py': 'src'})
    return {'purged_count': purged, 'status': 'optimized'}