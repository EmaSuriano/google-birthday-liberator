"""Tests for filter_contacts.py functionality."""

import csv
import os
import tempfile

import pytest


def create_test_csv(contacts_data):
    """Helper function to create a temporary CSV file with test data."""
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv")
    writer = csv.writer(temp_file)

    # Write header
    header = [
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
    writer.writerow(header)

    # Write contacts data
    for contact in contacts_data:
        writer.writerow(contact)

    temp_file.close()
    return temp_file.name


class TestFilterContacts:
    """Test cases for contact filtering functionality."""

    def test_filter_contacts_with_birthdays(self):
        """Test filtering contacts to keep only those with birthdays."""
        # Create test data
        contacts = [
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
                "",
            ],
            [
                "Jane",
                "",
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
                "",
                "",
                "",
                "",
            ],  # No birthday
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
                "",
            ],  # No year
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
                "1985-12-01",
                "",
                "",
                "",
            ],
        ]

        input_file = create_test_csv(contacts)
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name

        try:
            # Import and test the function
            import sys

            sys.path.insert(0, ".")
            from filter_contacts import filter_contacts_with_birthdays

            kept, removed = filter_contacts_with_birthdays(input_file, output_file)

            assert kept == 3  # John, Bob, Alice have birthdays
            assert removed == 1  # Jane has no birthday

            # Verify output file content
            with open(output_file, "r") as f:
                reader = csv.reader(f)
                rows = list(reader)

            assert len(rows) == 4  # Header + 3 contacts with birthdays
            assert rows[1][0] == "John"
            assert rows[2][0] == "Bob"
            assert rows[3][0] == "Alice"

        finally:
            os.unlink(input_file)
            os.unlink(output_file)

    def test_filter_empty_file(self):
        """Test filtering an empty CSV file."""
        contacts = []
        input_file = create_test_csv(contacts)
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name

        try:
            import sys

            sys.path.insert(0, ".")
            from filter_contacts import filter_contacts_with_birthdays

            kept, removed = filter_contacts_with_birthdays(input_file, output_file)

            assert kept == 0
            assert removed == 0

        finally:
            os.unlink(input_file)
            os.unlink(output_file)

    def test_filter_all_contacts_have_birthdays(self):
        """Test filtering when all contacts have birthdays."""
        contacts = [
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
                "",
            ],
            [
                "Jane",
                "",
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
                "",
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
                "",
            ],
        ]

        input_file = create_test_csv(contacts)
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name

        try:
            import sys

            sys.path.insert(0, ".")
            from filter_contacts import filter_contacts_with_birthdays

            kept, removed = filter_contacts_with_birthdays(input_file, output_file)

            assert kept == 3
            assert removed == 0

        finally:
            os.unlink(input_file)
            os.unlink(output_file)

    def test_filter_no_contacts_have_birthdays(self):
        """Test filtering when no contacts have birthdays."""
        contacts = [
            ["John", "", "Doe", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            [
                "Jane",
                "",
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
                "   ",
                "",
                "",
                "",
            ],  # Whitespace
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
                "",
                "",
                "",
                "",
            ],
        ]

        input_file = create_test_csv(contacts)
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name

        try:
            import sys

            sys.path.insert(0, ".")
            from filter_contacts import filter_contacts_with_birthdays

            kept, removed = filter_contacts_with_birthdays(input_file, output_file)

            assert kept == 0
            assert removed == 3

            # Verify output file has only header
            with open(output_file, "r") as f:
                reader = csv.reader(f)
                rows = list(reader)

            assert len(rows) == 1  # Only header

        finally:
            os.unlink(input_file)
            os.unlink(output_file)

    def test_filter_handles_whitespace_birthdays(self):
        """Test that whitespace-only birthday fields are treated as empty."""
        contacts = [
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
                "",
            ],
            [
                "Jane",
                "",
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
                "   ",
                "",
                "",
                "",
            ],  # Whitespace
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
                "\t\n",
                "",
                "",
                "",
            ],  # Tabs/newlines
        ]

        input_file = create_test_csv(contacts)
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name

        try:
            import sys

            sys.path.insert(0, ".")
            from filter_contacts import filter_contacts_with_birthdays

            kept, removed = filter_contacts_with_birthdays(input_file, output_file)

            assert kept == 1  # Only John has valid birthday
            assert removed == 2  # Jane and Bob have whitespace

        finally:
            os.unlink(input_file)
            os.unlink(output_file)
