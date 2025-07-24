"""Tests for create_birthday_calendar.py functionality."""

import csv
import os
import tempfile
from datetime import datetime

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


class TestCreateCalendar:
    """Test cases for calendar creation functionality."""

    def test_create_birthday_ics_basic(self):
        """Test creating ICS calendar with basic birthday data."""
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
                "M",
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
        ]

        input_file = create_test_csv(contacts)
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ics").name

        try:
            import sys

            sys.path.insert(0, ".")
            from create_birthday_calendar import create_birthday_ics

            events_created = create_birthday_ics(input_file, output_file)

            assert events_created == 2

            # Verify ICS file content
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert "BEGIN:VCALENDAR" in content
            assert "END:VCALENDAR" in content
            assert content.count("BEGIN:VEVENT") == 2
            assert content.count("END:VEVENT") == 2
            assert "🎂 John Doe's Birthday" in content
            assert "🎂 Jane M Smith's Birthday" in content
            assert "DTSTART;VALUE=DATE:19900515" in content
            assert "DTSTART;VALUE=DATE:19920820" in content
            assert "RRULE:FREQ=YEARLY" in content
            assert "TRIGGER:-PT6H" in content
            assert "ACTION:EMAIL" in content

        finally:
            os.unlink(input_file)
            os.unlink(output_file)

    def test_create_ics_with_no_year_birthday(self):
        """Test creating ICS calendar with --MM-DD format birthdays."""
        contacts = [
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
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ics").name

        try:
            import sys

            sys.path.insert(0, ".")
            from create_birthday_calendar import create_birthday_ics

            events_created = create_birthday_ics(input_file, output_file)

            assert events_created == 1

            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert "🎂 Bob Johnson's Birthday" in content
            current_year = datetime.now().year
            expected_date = f"DTSTART;VALUE=DATE:{current_year}0322"
            assert expected_date in content

        finally:
            os.unlink(input_file)
            os.unlink(output_file)

    def test_create_ics_empty_file(self):
        """Test creating ICS calendar from empty CSV."""
        contacts = []

        input_file = create_test_csv(contacts)
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ics").name

        try:
            import sys

            sys.path.insert(0, ".")
            from create_birthday_calendar import create_birthday_ics

            events_created = create_birthday_ics(input_file, output_file)

            assert events_created == 0

            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert "BEGIN:VCALENDAR" in content
            assert "END:VCALENDAR" in content
            assert content.count("BEGIN:VEVENT") == 0

        finally:
            os.unlink(input_file)
            os.unlink(output_file)

    def test_create_ics_contacts_without_birthdays(self):
        """Test creating ICS calendar with contacts that have no birthdays."""
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
                "   ",
                "",
                "",
                "",
            ],
        ]

        input_file = create_test_csv(contacts)
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ics").name

        try:
            import sys

            sys.path.insert(0, ".")
            from create_birthday_calendar import create_birthday_ics

            events_created = create_birthday_ics(input_file, output_file)

            assert events_created == 1  # Only Jane has birthday

            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert content.count("BEGIN:VEVENT") == 1
            assert "🎂 Jane Smith's Birthday" in content
            assert "John Doe" not in content
            assert "Bob Johnson" not in content

        finally:
            os.unlink(input_file)
            os.unlink(output_file)

    def test_create_ics_invalid_birthday_format(self):
        """Test creating ICS calendar with invalid birthday formats."""
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
                "invalid-date",
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
                "05/15/1990",
                "",
                "",
                "",
            ],
        ]

        input_file = create_test_csv(contacts)
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ics").name

        try:
            import sys

            sys.path.insert(0, ".")
            from create_birthday_calendar import create_birthday_ics

            events_created = create_birthday_ics(input_file, output_file)

            assert events_created == 1  # Only John has valid format

            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert content.count("BEGIN:VEVENT") == 1
            assert "🎂 John Doe's Birthday" in content

        finally:
            os.unlink(input_file)
            os.unlink(output_file)

    def test_create_ics_email_reminder_content(self):
        """Test that email reminders have correct content."""
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
        ]

        input_file = create_test_csv(contacts)
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ics").name

        try:
            import sys

            sys.path.insert(0, ".")
            from create_birthday_calendar import create_birthday_ics

            create_birthday_ics(input_file, output_file)

            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Check email reminder properties
            assert "BEGIN:VALARM" in content
            assert "END:VALARM" in content
            assert "TRIGGER:-PT6H" in content
            assert "ACTION:EMAIL" in content
            assert "SUMMARY:Today is John Doe's Birthday! 🎂" in content
            assert "DESCRIPTION:Don't forget to call John Doe today" in content

        finally:
            os.unlink(input_file)
            os.unlink(output_file)

    def test_create_ics_multiple_names(self):
        """Test creating ICS calendar with various name combinations."""
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
                "",
            ],
            [
                "",
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
                "1985-03-10",
                "",
                "",
                "",
            ],  # Only last name
            [
                "Bob",
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
                "1988-12-25",
                "",
                "",
                "",
            ],  # Only first name
        ]

        input_file = create_test_csv(contacts)
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ics").name

        try:
            import sys

            sys.path.insert(0, ".")
            from create_birthday_calendar import create_birthday_ics

            events_created = create_birthday_ics(input_file, output_file)

            assert events_created == 4

            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert "🎂 John Doe's Birthday" in content
            assert "🎂 Jane Marie Smith's Birthday" in content
            assert "🎂 Johnson's Birthday" in content
            assert "🎂 Bob's Birthday" in content

        finally:
            os.unlink(input_file)
            os.unlink(output_file)
