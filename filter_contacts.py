import csv
import os


def filter_contacts_with_birthdays(input_file, output_file):
    """Filter Google Contacts export to keep only those with birthdays assigned."""
    contacts_with_birthdays = []
    total_contacts = 0

    with open(input_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)

        # Find the birthday column index
        birthday_index = header.index("Birthday")

        # Keep the header
        contacts_with_birthdays.append(header)

        for row in reader:
            total_contacts += 1
            # Check if birthday field is not empty
            if len(row) > birthday_index and row[birthday_index].strip():
                contacts_with_birthdays.append(row)

    # Write filtered contacts to output file
    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(contacts_with_birthdays)

    contacts_kept = len(contacts_with_birthdays) - 1  # Subtract header
    contacts_removed = total_contacts - contacts_kept

    print(f"Total contacts processed: {total_contacts}")
    print(f"Contacts with birthdays kept: {contacts_kept}")
    print(f"Contacts without birthdays removed: {contacts_removed}")

    return contacts_kept, contacts_removed


if __name__ == "__main__":
    input_file = "export.csv"
    output_file = "export.csv"  # Overwrite the original file

    # Create backup first
    backup_file = "export_backup.csv"
    os.rename(input_file, backup_file)

    filter_contacts_with_birthdays(backup_file, output_file)
