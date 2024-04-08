import unittest
import os
from src.infrastructure.database.implementations.csv_database import CSVDatabase
import csv


class CSVDatabaseTests(unittest.TestCase):

    def setUp(self):
        self.data = [
            {"name": "John Doe", "age": "30"},
            {"name": "Jane Doe", "age": "31"},
            {"name": "Bob Smith", "age": "32"},
        ]
        with open('test.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)
        self.db = CSVDatabase('test.csv')

    def tearDown(self):
        os.remove('test.csv')

    def test_load_data(self):
        self.db._load_data()
        self.assertEqual(self.db.data, self.data)

    def test_save_data(self):
        self.db.data = self.data
        self.db._save_data()
        with open('test.csv', 'r') as f:
            reader = csv.DictReader(f)
            actual_data = list(reader)
        self.assertEqual(actual_data, self.data)

    def test_select(self):
        self.db.data = self.data
        result = self.db._select([{"name": "John Doe"}])
        self.assertEqual(result, [self.data[0]])

    def test_insert(self):
        self.db.data = []
        self.db._insert([{"name": "New User", "age": "33"}])
        self.assertEqual(self.db.data, [{"name": "New User", "age": "33"}])

    def test_update(self):
        self.db._update([{"name": "John Doe", "age": "31"}])
        self.assertEqual(self.db.data, [{"name": "John Doe", "age": "31"}, {"name": "Jane Doe", "age": "31"},
                                        {"name": "Bob Smith", "age": "32"}])

    def test_delete(self):
        self.db.data = self.data
        self.db._delete([{"name": "John Doe"}])
        self.assertEqual(self.db.data, [{"name": "Jane Doe", "age": "31"}, {"name": "Bob Smith", "age": "32"}])
