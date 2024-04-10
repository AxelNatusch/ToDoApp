import os
import csv
import pytest

from src.infrastructure.database.implementations.csv_database import CSVDatabase


@pytest.fixture
def csv_database():
    data = [
        {"name": "John Doe", "age": "30"},
        {"name": "Jane Doe", "age": "31"},
        {"name": "Bob Smith", "age": "32"},
    ]
    with open('test.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    db = CSVDatabase('test.csv')
    yield db
    os.remove('test.csv')


def test_load_data(csv_database):
    csv_database._load_data()
    assert csv_database.data == [
        {"name": "John Doe", "age": "30"},
        {"name": "Jane Doe", "age": "31"},
        {"name": "Bob Smith", "age": "32"},
    ]


def test_save_data(csv_database):
    with open('test.csv', 'r') as f:
        reader = csv.DictReader(f)
        actual_data = list(reader)
    assert actual_data == [
        {"name": "John Doe", "age": "30"},
        {"name": "Jane Doe", "age": "31"},
        {"name": "Bob Smith", "age": "32"},
    ]


def test_select(csv_database):
    result = csv_database._select([{"name": "John Doe"}])
    assert result == [{"name": "John Doe", "age": "30"}]


def test_insert(csv_database):
    data_to_be_inserted = [{"name": "New User", "age": "33"}]
    csv_database._insert(data_to_be_inserted)
    assert csv_database.data == [
        {"name": "John Doe", "age": "30"},
        {"name": "Jane Doe", "age": "31"},
        {"name": "Bob Smith", "age": "32"},
        {"name": "New User", "age": "33"},
    ]


def test_update(csv_database):
    csv_database._update([{"name": "John Doe", "age": "31"}])
    assert csv_database.data == [
        {"name": "John Doe", "age": "31"},
        {"name": "Jane Doe", "age": "31"},
        {"name": "Bob Smith", "age": "32"},
    ]


def test_delete(csv_database):
    csv_database._delete([{"name": "John Doe"}])
    assert csv_database.data == [
        {"name": "Jane Doe", "age": "31"},
        {"name": "Bob Smith", "age": "32"},
    ]