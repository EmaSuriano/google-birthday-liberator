"""Integration tests for the complete workflow."""

import csv
import os
import tempfile
from pathlib import Path

import pytest


class TestIntegration:
    """Integration tests for the complete Google Birthday Liberator workflow."""

    def test_complete_workflow(self):
        """Test the complete workflow: filter contacts -> create calendar."""
        # Create test data with mixed contacts
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
                "* myContacts",
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
                "* myContacts",
            ],  # No birthday
            [
                "Bob",
                "M",
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
                "1985-12-01",
                "",
                "",
                "* myContacts",
            ],
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

        # Create temporary files
        original_csv = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv"
        )
        writer = csv.writer(original_csv)

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

        # Write contacts
        for contact in contacts:
            writer.writerow(contact)

        original_csv.close()

        filtered_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name
        calendar_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ics").name

        try:
            import sys

            sys.path.insert(0, ".")
            from filter_contacts import filter_contacts_with_birthdays
            from create_birthday_calendar import create_birthday_ics

            # Step 1: Filter contacts
            kept, removed = filter_contacts_with_birthdays(
                original_csv.name, filtered_csv
            )

            assert kept == 3  # John, Bob, Alice have birthdays
            assert removed == 2  # Jane and Charlie don't have birthdays

            # Step 2: Create calendar
            events_created = create_birthday_ics(filtered_csv, calendar_file)

            assert events_created == 3

            # Verify filtered CSV
            with open(filtered_csv, "r") as f:
                reader = csv.reader(f)
                rows = list(reader)

            assert len(rows) == 4  # Header + 3 contacts
            names = [row[0] for row in rows[1:]]
            assert "John" in names
            assert "Bob" in names
            assert "Alice" in names
            assert "Jane" not in names
            assert "Charlie" not in names

            # Verify calendar file
            with open(calendar_file, "r", encoding="utf-8") as f:
                calendar_content = f.read()

            assert "BEGIN:VCALENDAR" in calendar_content
            assert "END:VCALENDAR" in calendar_content
            assert calendar_content.count("BEGIN:VEVENT") == 3
            assert "🎂 John Doe's Birthday" in calendar_content
            assert "🎂 Bob M Johnson's Birthday" in calendar_content
            assert "🎂 Alice Wilson's Birthday" in calendar_content

            # Verify email reminders
            assert calendar_content.count("BEGIN:VALARM") == 3
            assert calendar_content.count("TRIGGER:-PT6H") == 3
            assert "Today is John Doe's Birthday!" in calendar_content

        finally:
            os.unlink(original_csv.name)
            os.unlink(filtered_csv)
            os.unlink(calendar_file)

    def test_workflow_with_real_file_structure(self):
        """Test workflow using actual file names from the project."""
        # Create a temporary directory to simulate project structure
        with tempfile.TemporaryDirectory() as temp_dir:
            export_csv = os.path.join(temp_dir, "export.csv")
            backup_csv = os.path.join(temp_dir, "export_backup.csv")
            calendar_ics = os.path.join(temp_dir, "birthdays.ics")

            # Create initial export.csv
            contacts = [
                [
                    "Test",
                    "User",
                    "One",
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
                    "1990-01-01",
                    "",
                    "",
                    "",
                ],
                [
                    "Test",
                    "User",
                    "Two",
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
                [
                    "Test",
                    "User",
                    "Three",
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
                    "1995-06-15",
                    "",
                    "",
                    "",
                ],
            ]

            with open(export_csv, "w", newline="") as f:
                writer = csv.writer(f)
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
                for contact in contacts:
                    writer.writerow(contact)

            # Copy to backup
            import shutil

            shutil.copy2(export_csv, backup_csv)

            # Change to temp directory and run workflow
            original_cwd = os.getcwd()
            os.chdir(temp_dir)

            try:
                import sys

                sys.path.insert(0, original_cwd)
                from filter_contacts import filter_contacts_with_birthdays
                from create_birthday_calendar import create_birthday_ics

                # Simulate the filter step (backup -> export)
                kept, removed = filter_contacts_with_birthdays(backup_csv, export_csv)
                assert kept == 2
                assert removed == 1

                # Create calendar
                events = create_birthday_ics(export_csv, calendar_ics)
                assert events == 2

                # Verify files exist and have correct content
                assert os.path.exists(export_csv)
                assert os.path.exists(backup_csv)
                assert os.path.exists(calendar_ics)

                # Check calendar content
                with open(calendar_ics, "r", encoding="utf-8") as f:
                    content = f.read()

                assert "🎂 Test User One's Birthday" in content
                assert "🎂 Test User Three's Birthday" in content
                assert "Test User Two" not in content  # No birthday

            finally:
                os.chdir(original_cwd)

    def test_workflow_handles_unicode_names(self):
        """Test workflow with Unicode characters in names."""
        contacts = [
            [
                "José",
                "",
                "García",
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
                "François",
                "",
                "Müller",
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
                "李",
                "",
                "小明",
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

        input_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        )
        writer = csv.writer(input_file)

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

        for contact in contacts:
            writer.writerow(contact)

        input_file.close()

        filtered_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name
        calendar_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ics").name

        try:
            import sys

            sys.path.insert(0, ".")
            from filter_contacts import filter_contacts_with_birthdays
            from create_birthday_calendar import create_birthday_ics

            # Filter and create calendar
            kept, removed = filter_contacts_with_birthdays(
                input_file.name, filtered_csv
            )
            events = create_birthday_ics(filtered_csv, calendar_file)

            assert kept == 3
            assert removed == 0
            assert events == 3

            # Verify Unicode names in calendar
            with open(calendar_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert "🎂 José García's Birthday" in content
            assert "🎂 François Müller's Birthday" in content
            assert "🎂 李 小明's Birthday" in content

        finally:
            os.unlink(input_file.name)
            os.unlink(filtered_csv)
            os.unlink(calendar_file)
