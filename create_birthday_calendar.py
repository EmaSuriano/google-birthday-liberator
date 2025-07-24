import csv
from datetime import datetime, date
import uuid


def create_birthday_ics(csv_file, output_file):
    """Create an ICS calendar file with birthday events from Google Contacts CSV export."""

    # ICS file header
    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Google Birthday Liberator//Birthday Events//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]

    contacts_processed = 0

    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)

        # Find column indices
        first_name_idx = header.index("First Name")
        middle_name_idx = header.index("Middle Name")
        last_name_idx = header.index("Last Name")
        birthday_idx = header.index("Birthday")

        for row in reader:
            if len(row) > birthday_idx and row[birthday_idx].strip():
                # Extract name components
                first_name = (
                    row[first_name_idx].strip() if len(row) > first_name_idx else ""
                )
                middle_name = (
                    row[middle_name_idx].strip() if len(row) > middle_name_idx else ""
                )
                last_name = (
                    row[last_name_idx].strip() if len(row) > last_name_idx else ""
                )

                # Build full name
                name_parts = [
                    part for part in [first_name, middle_name, last_name] if part
                ]
                full_name = " ".join(name_parts)

                if not full_name:
                    continue

                birthday_str = row[birthday_idx].strip()

                # Parse birthday - handle different formats
                birthday_date = None
                try:
                    # Try YYYY-MM-DD format first
                    if len(birthday_str) == 10 and birthday_str.count("-") == 2:
                        birthday_date = datetime.strptime(
                            birthday_str, "%Y-%m-%d"
                        ).date()
                    # Try --MM-DD format (no year)
                    elif birthday_str.startswith("--") and len(birthday_str) == 7:
                        month_day = birthday_str[2:]
                        # Use current year as placeholder
                        current_year = datetime.now().year
                        birthday_date = datetime.strptime(
                            f"{current_year}-{month_day}", "%Y-%m-%d"
                        ).date()
                except ValueError:
                    print(
                        f"Skipping {full_name} - invalid birthday format: {birthday_str}"
                    )
                    continue

                if birthday_date:
                    # Create birthday event
                    event_uid = str(uuid.uuid4())
                    event_date = birthday_date.strftime("%Y%m%d")

                    # Create event
                    ics_content.extend(
                        [
                            "BEGIN:VEVENT",
                            f"UID:{event_uid}",
                            f"DTSTART;VALUE=DATE:{event_date}",
                            f"DTEND;VALUE=DATE:{event_date}",
                            f"SUMMARY:🎂 {full_name}'s Birthday",
                            f"DESCRIPTION:Birthday of {full_name} - Remember to call and congratulate!",
                            "RRULE:FREQ=YEARLY",
                            "TRANSP:TRANSPARENT",
                            "CLASS:PUBLIC",
                            f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}",
                            "BEGIN:VALARM",
                            "TRIGGER:PT0S",
                            "ACTION:EMAIL",
                            f"SUMMARY:Today is {full_name}'s Birthday! 🎂",
                            f"DESCRIPTION:Don't forget to call {full_name} today to wish them a happy birthday! 🎂",
                            "END:VALARM",
                            "BEGIN:VALARM",
                            "TRIGGER:PT0S",
                            "ACTION:DISPLAY",
                            f"SUMMARY:🎂 {full_name}'s Birthday!",
                            f"DESCRIPTION:Don't forget to call {full_name} today to wish them a happy birthday! 🎂",
                            "END:VALARM",
                            "END:VEVENT",
                        ]
                    )

                    contacts_processed += 1

    # Close calendar
    ics_content.append("END:VCALENDAR")

    # Write ICS file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(ics_content))

    print(f"Created birthday calendar with {contacts_processed} events")
    print(f"Calendar saved as: {output_file}")

    return contacts_processed


if __name__ == "__main__":
    create_birthday_ics("export.csv", "birthdays.ics")
