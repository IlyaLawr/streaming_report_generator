from dataclasses import dataclass
from os import path


@dataclass
class Setting:
    base_dir: str = path.dirname(path.abspath(__file__))
    db_path: str = f'{base_dir}/infrastructure/temp.db'
    file_format: str = '.csv'
