"""Utility functions"""

import pandas as pd
from typing import List, Any, Optional

def to_pandas_dataframe(items: List[Any]) -> pd.DataFrame:
    """Convert list of Pydantic models to pandas DataFrame"""
    if not items:
        return pd.DataFrame()
    
    # Convert to list of dicts
    data = [item.to_dict() if hasattr(item, 'to_dict') else item for item in items]
    return pd.DataFrame(data)

def to_polars_dataframe(items: List[Any]) -> 'pl.DataFrame':
    """Convert list of Pydantic models to polars DataFrame"""
    try:
        import polars as pl
    except ImportError:
        raise ImportError("polars is required for this function. Install with: pip install polars")
    
    if not items:
        return pl.DataFrame()
    
    # Convert to list of dicts
    data = [item.to_dict() if hasattr(item, 'to_dict') else item for item in items]
    return pl.DataFrame(data)

def flatten_nested_dict(data: dict, parent_key: str = '', sep: str = '_') -> dict:
    """Flatten nested dictionary for DataFrame compatibility"""
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_nested_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
            # Handle list of dicts by taking first item or converting to string
            items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
    return dict(items)