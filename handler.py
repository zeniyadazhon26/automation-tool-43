import os
import shutil
from pathlib import Path

class CleanupEngine:
    def __init__(self, target_dir):
        self.target = Path(target_dir)
        self.extensions = {'.tmp', '.log', '.bak', '.swp'}

    def run_sweep(self):
        return [self._process_entry(e) for e in self.target.rglob('*') if e.suffix in self.extensions]

    def _process_entry(self, entry):
        try:
            entry.unlink()
            return f'deleted: {entry.name}'
        except Exception as e:
            return f'failed: {entry.name} - {str(e)}'

class Reorganizer:
    def __init__(self, root):
        self.root = Path(root)

    def structure_by_extension(self):
        files = [f for f in self.root.iterdir() if f.is_file()]
        for f in files:
            target_folder = self.root / (f.suffix.lstrip('.') or 'no_ext')
            target_folder.mkdir(exist_ok=True)
            shutil.move(str(f), str(target_folder / f.name))
        return len(files)

def execute_lifecycle(path):
    sweeper = CleanupEngine(path)
    reorg = Reorganizer(path)
    
    logs = sweeper.run_sweep()
    moved_count = reorg.structure_by_extension()
    
    return {'cleanup_status': logs, 'moved_files': moved_count}