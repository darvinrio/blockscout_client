"""Output formatters for CLI"""

import json
import csv
import io
from typing import List, Any, Dict, Union
from rich.console import Console
from rich.table import Table
from rich.json import JSON
from tabulate import tabulate

console = Console()


class OutputFormatter:
    """Base output formatter"""

    @staticmethod
    def format_table(data: List[Dict[str, Any]], title: str = None) -> str:
        """Format data as a table"""
        if not data:
            return "No data found."

        # Create rich table
        table = Table(title=title, show_header=True, header_style="bold magenta")

        # Add columns
        if data:
            for key in data[0].keys():
                table.add_column(str(key), style="cyan", no_wrap=False)

            # Add rows
            for item in data:
                row = []
                for value in item.values():
                    if isinstance(value, (dict, list)):
                        row.append(
                            str(value)[:50] + "..."
                            if len(str(value)) > 50
                            else str(value)
                        )
                    else:
                        row.append(str(value) if value is not None else "")
                table.add_row(*row)

        with console.capture() as capture:
            console.print(table)
        return capture.get()

    @staticmethod
    def format_json(
        data: Union[List[Dict[str, Any]], Dict[str, Any]], indent: int = 2
    ) -> str:
        """Format data as JSON"""
        return json.dumps(data, indent=indent, default=str)

    @staticmethod
    def format_csv(data: List[Dict[str, Any]]) -> str:
        """Format data as CSV"""
        if not data:
            return ""

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

    @staticmethod
    def format_simple_table(data: List[Dict[str, Any]]) -> str:
        """Format data as simple ASCII table"""
        if not data:
            return "No data found."

        return tabulate(data, headers="keys", tablefmt="grid")


def format_output(data: Any, format_type: str, title: str = None) -> str:
    """Format output based on type"""
    formatter = OutputFormatter()

    # Convert Pydantic models to dicts
    if hasattr(data, "__iter__") and not isinstance(data, (str, dict)):
        try:
            data = [
                item.to_dict() if hasattr(item, "to_dict") else item for item in data
            ]
        except TypeError:
            pass
    elif hasattr(data, "to_dict"):
        data = data.to_dict()

    if format_type == "json":
        return formatter.format_json(data)
    elif format_type == "csv":
        if isinstance(data, list):
            return formatter.format_csv(data)
        else:
            return formatter.format_csv([data])
    elif format_type == "table":
        if isinstance(data, list):
            return formatter.format_table(data, title)
        else:
            return formatter.format_table([data], title)
    else:
        return str(data)
