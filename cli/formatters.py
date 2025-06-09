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
    def format_table(data: List[Dict[str, Any]], title: str = None) -> Table:
        """Format data as a Rich Table object"""
        if not data:
            return Table(title="No data found.")

        # Ensure data is a list of dictionaries
        if not isinstance(data, list):
            data = [data]

        # Convert any non-dict items to dicts
        processed_data = []
        for item in data:
            if hasattr(item, "to_dict"):
                processed_data.append(item.to_dict())
            elif isinstance(item, dict):
                processed_data.append(item)
            else:
                processed_data.append({"value": str(item)})

        if not processed_data:
            return Table(title="No data found.")

        # Create rich table
        table = Table(title=title, show_header=True, header_style="bold magenta")

        # Add columns
        first_item = processed_data[0]
        for key in first_item.keys():
            table.add_column(str(key), style="cyan", no_wrap=True)

        # Add rows
        for item in processed_data:
            row = []
            for key in first_item.keys():
                value = item.get(key)
                if isinstance(value, (dict, list)):
                    # Truncate complex objects
                    str_value = str(value)
                    row.append(
                        str_value[:30] + "..." if len(str_value) > 30 else str_value
                    )
                else:
                    row.append(str(value) if value is not None else "")
            table.add_row(*row)

        return table

    @staticmethod
    def format_json(
        data: Union[List[Dict[str, Any]], Dict[str, Any]], indent: int = 2
    ) -> str:
        """Format data as JSON"""
        # Convert Pydantic models to dicts if needed
        if hasattr(data, "to_dict"):
            data = data.to_dict()
        elif isinstance(data, list) and data and hasattr(data[0], "to_dict"):
            data = [
                item.to_dict() if hasattr(item, "to_dict") else item for item in data
            ]

        return json.dumps(data, indent=indent, default=str)

    @staticmethod
    def format_csv(data: List[Dict[str, Any]]) -> str:
        """Format data as CSV"""
        if not data:
            return ""

        # Ensure data is a list
        if not isinstance(data, list):
            data = [data]

        # Convert Pydantic models to dicts if needed
        processed_data = []
        for item in data:
            if hasattr(item, "to_dict"):
                processed_data.append(item.to_dict())
            elif isinstance(item, dict):
                processed_data.append(item)
            else:
                processed_data.append({"value": str(item)})

        if not processed_data:
            return ""

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=processed_data[0].keys())
        writer.writeheader()
        for row in processed_data:
            # Convert complex objects to strings for CSV
            csv_row = {}
            for key, value in row.items():
                if isinstance(value, (dict, list)):
                    csv_row[key] = json.dumps(value, default=str)
                else:
                    csv_row[key] = str(value) if value is not None else ""
            writer.writerow(csv_row)
        return output.getvalue()


def format_output(data: Any, format_type: str, title: str = None) -> Union[str, Table]:
    """Format output based on type"""
    formatter = OutputFormatter()

    # Convert Pydantic models to dicts
    if hasattr(data, "to_dict"):
        converted_data = data.to_dict()
    elif hasattr(data, "__iter__") and not isinstance(data, (str, dict)):
        try:
            converted_data = []
            for item in data:
                if hasattr(item, "to_dict"):
                    converted_data.append(item.to_dict())
                elif isinstance(item, dict):
                    converted_data.append(item)
                else:
                    converted_data.append({"value": str(item)})
        except (TypeError, AttributeError):
            converted_data = [{"value": str(data)}]
    elif isinstance(data, dict):
        converted_data = data
    else:
        converted_data = {"value": str(data)}

    # Format based on requested type
    if format_type == "json":
        return formatter.format_json(converted_data)
    elif format_type == "csv":
        if isinstance(converted_data, list):
            return formatter.format_csv(converted_data)
        else:
            return formatter.format_csv([converted_data])
    elif format_type == "table":
        if isinstance(converted_data, list):
            return formatter.format_table(converted_data, title)
        else:
            return formatter.format_table([converted_data], title)
    else:
        return str(converted_data)
