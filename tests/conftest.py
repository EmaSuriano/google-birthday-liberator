"""Pytest configuration and fixtures for Google Birthday Liberator tests."""

import os
import tempfile

import pytest


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file for testing."""
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv")
    yield temp_file
    temp_file.close()
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def temp_ics_file():
    """Create a temporary ICS file for testing."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ics")
    temp_file.close()
    yield temp_file.name
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def sample_contacts():
    """Sample contact data for testing."""
    return [
        [
            "John",
            "",
            "Doe",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "1990-05-15",
            "",
            "",
            "* myContacts",
        ],
        [
            "Jane",
            "Marie",
            "Smith",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "1992-08-20",
            "",
            "",
            "* myContacts",
        ],
        [
            "Bob",
            "",
            "Johnson",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "--03-22",
            "",
            "",
            "* myContacts",
        ],
        [
            "Alice",
            "",
            "Wilson",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "* myContacts",
        ],  # No birthday
        [
            "Charlie",
            "",
            "Brown",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "   ",
            "",
            "",
            "* myContacts",
        ],  # Whitespace
    ]


@pytest.fixture
def csv_header():
    """Standard CSV header for contact exports."""
    return [
        "First Name",
        "Middle Name",
        "Last Name",
        "Phonetic First Name",
        "Phonetic Middle Name",
        "Phonetic Last Name",
        "Name Prefix",
        "Name Suffix",
        "Nickname",
        "File As",
        "Organization Name",
        "Organization Title",
        "Organization Department",
        "Birthday",
        "Notes",
        "Photo",
        "Labels",
    ]


@pytest.fixture(autouse=True)
def setup_python_path():
    """Add current directory to Python path for imports."""
    import sys

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    yield
    if current_dir in sys.path:
        sys.path.remove(current_dir)
