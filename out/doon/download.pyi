from typing import Any

class Download:
    category: Any = ...
    save_dir: Any = ...
    root: Any = ...
    def __init__(self, category: str, root: str) -> None: ...
    def get_all_pages(self) -> None: ...
