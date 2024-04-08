from typing import Any, Dict, List
import os
import csv
from src.infrastructure.database.database_interface import DatabaseInterface


class CSVDatabase(DatabaseInterface):
    """
    CSVDatabase class is a concrete implementation of DatabaseInterface
    that connects to a CSV file and performs CRUD operations on it.

    Attributes:
        file_path (str): The path to the CSV file.
        data (List[Dict[str, Any]]): A list of dictionaries representing the data in the CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """

    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.data: List[Dict[str, Any]] = []

        self._load_data()

    def _load_data(self) -> None:
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
                writer.writeheader()

        with open(self.file_path, "r") as f:
            reader = csv.DictReader(f)
            self.data = list(reader)

    def _save_data(self) -> None:
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
                writer.writeheader()

        with open(self.file_path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)

    def execute(
            self, operation: str, parameters: List[Any] | None = None
    ) -> List[Any] | None:
        if operation.startswith("SELECT"):
            return self._select(parameters)
        elif operation.startswith("INSERT"):
            return self._insert(parameters)
        elif operation.startswith("UPDATE"):
            return self._update(parameters)
        elif operation.startswith("DELETE"):
            return self._delete(parameters)
        else:
            raise ValueError(f"Invalid operation: {operation}")

    def _select(self, parameters: List[Dict[str, Any]] | None = None) -> List[Any]:
        if parameters is None:
            return self.data

        result = []
        for parameter in parameters:
            for row in self.data:
                if any(row[key] == value for key, value in parameter.items()):
                    result.append(row)

        return result

    def _insert(self, parameters: List[Any] | None = None) -> None:
        if parameters is None:
            raise ValueError("No data provided for insertion")

        self.data = self.data + parameters
        self._save_data()

    def _update(self, parameters: List[Dict[str, Any]] | None = None) -> None:
        if parameters is None:
            raise ValueError("No data provided for update")
        for parameter in parameters:
            for row in self.data:
                if row[list(row.keys())[0]] == parameter[list(parameter.keys())[0]]:
                    for key, value in parameter.items():
                        row[key] = value

        self._save_data()

    def _delete(self, parameters: List[Dict[str, Any]] | None = None) -> None:
        if parameters is None:
            raise ValueError("No data provided for deletion")
        for parameter in parameters:
            self.data = [row for row in self.data if not any(row[key] == value for key, value in parameter.items())]
        self._save_data()

    def transaction(self) -> None:
        pass

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass
