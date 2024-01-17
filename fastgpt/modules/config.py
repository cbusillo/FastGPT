import json
from pathlib import Path
from typing import Any


class Config:
    def __init__(self) -> None:
        self.file_path = Path(__file__).parent.parent / "data" / "config.json"
        self.config = self.load_json(self.file_path)

    @staticmethod
    def load_json(file_path: Path) -> dict[str, Any]:
        with open(file_path) as file:
            return json.load(file)

    def save(self) -> None:
        with open(self.file_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def set(self, key: str, value: Any) -> None:
        keys = key.split(".")
        d = self.config
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

    def get(self, key: str, default=None) -> Any:
        keys = key.split(".")
        d = self.config
        for k in keys:
            if k in d:
                d = d[k]
            else:
                raise KeyError(f"Key {key} does not exist in the configuration.")
        return d

    def delete(self, key: str | int) -> None:
        keys = key.split(".")
        d = self.config
        for k in keys[:-1]:
            if k in d:
                d = d[k]
            else:
                raise KeyError(f"Key {key} does not exist in the configuration.")
        if keys[-1] in d:
            del d[keys[-1]]
        else:
            raise KeyError(f"Key {key} does not exist in the configuration.")

    def reload(self) -> None:
        self.config.clear()
        self.config.update(self.load_json(self.file_path))

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        self.delete(key)


config = Config()
