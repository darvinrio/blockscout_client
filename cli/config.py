"""Configuration management for CLI"""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class Config:
    """CLI configuration"""

    base_url: str = "https://blockscout.com/poa/core/api/v2/"
    timeout: int = 30
    output_format: str = "table"  # table, json, csv
    max_items: int = 50

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        """Load configuration from file"""
        if config_path is None:
            config_path = os.path.expanduser("~/.blockscout/config.yml")

        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, "r") as f:
                data = yaml.safe_load(f) or {}
            return cls(**data)

        return cls()

    def save(self, config_path: Optional[str] = None):
        """Save configuration to file"""
        if config_path is None:
            config_path = os.path.expanduser("~/.blockscout/config.yml")

        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)

        with open(config_file, "w") as f:
            yaml.dump(asdict(self), f, default_flow_style=False)

    def update(self, **kwargs):
        """Update configuration values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
