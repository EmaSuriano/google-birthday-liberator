# Google Birthday Liberator

**Take control of your birthday reminders and fix Google Contacts' broken integration.**

Google Contacts' birthday reminders are notoriously unreliable - they often fail to display properly in your calendar, show incomplete information, or disappear entirely. This tool liberates your birthday data from Google's flaky integration and creates a reliable, self-owned calendar that actually works.

**Stop depending on Google Contacts. Own your birthday calendar.**

## Why This Project Exists

🚫 **Google Contacts birthday reminders are broken:**
- Events randomly disappear from your calendar
- Incomplete contact information displayed  
- Unreliable notifications that don't trigger
- No control over reminder timing or format
- Dependent on Google's flaky integration

✅ **This tool gives you:**
- **Complete ownership** of your birthday calendar
- **Reliable reminders** that actually work
- **Custom formatting** with emojis and detailed info
- **Morning email notifications** (6 hours before)
- **Independence** from Google's broken system

## Features

✅ **Export & Filter** - Extract contacts with birthdays from Google Contacts  
✅ **Self-Owned Calendar** - Generate your own ICS calendar file  
✅ **Morning Email Alerts** - Reliable same-day notifications  
✅ **Yearly Recurring** - Events repeat automatically  
✅ **Rich Formatting** - Cake emoji 🎂 and call reminders  

## Quick Start

1. **Export your contacts** from Google Contacts to `export.csv`
2. **Filter contacts** to keep only those with birthdays:
   ```bash
   make filter
   ```
3. **Generate calendar** file:
   ```bash
   make calendar
   ```
4. **Import** `birthdays.ics` into your calendar app
5. **Delete Google Contacts integration** from your calendar (optional but recommended)

## Commands

### Using Make (Simple)

| Command | Description |
|---------|-------------|
| `make help` | Show available commands |
| `make filter` | Filter contacts to keep only those with birthdays |
| `make calendar` | Generate ICS calendar file from filtered contacts |
| `make all` | Run complete workflow (filter + calendar) |
| `make stats` | Show project statistics |
| `make backup` | Create timestamped backup of export.csv |
| `make restore` | Restore from backup (export_backup.csv) |
| `make clean` | Remove generated files |

### Using uv (Recommended)

```bash
# Core functionality
uv run python filter_contacts.py          # Filter contacts
uv run python create_birthday_calendar.py # Create calendar

# Development commands
uv run pytest tests/ -v                   # Run tests
uv run pytest tests/ --cov=. --cov-report=term-missing  # Run tests with coverage
uv run black .                            # Format code
uv run ruff check .                       # Lint code

# Quick stats (if you have the files)
uv run python -c "import csv, os; print('📊 Contacts:', sum(1 for _ in open('export.csv')) - 1 if os.path.exists('export.csv') else 0); print('📅 Events:', open('birthdays.ics').read().count('BEGIN:VEVENT') if os.path.exists('birthdays.ics') else 0)"
```

### Direct Python Usage

```bash
# Filter contacts
python filter_contacts.py

# Create calendar
python create_birthday_calendar.py
```

## Files

- **`export.csv`** - Your contacts file (filtered to include only contacts with birthdays)
- **`export_backup.csv`** - Backup of original contacts file
- **`birthdays.ics`** - Generated calendar file for import
- **`filter_contacts.py`** - Script to filter contacts
- **`create_birthday_calendar.py`** - Script to generate calendar

## Calendar Features

The generated `birthdays.ics` file includes:

- 🎂 **Cake emoji** in event titles (e.g., "🎂 John Doe's Birthday")
- 📧 **Email reminders** 6 hours before each birthday (morning of the same day)
- 🔄 **Yearly recurring** events
- 📱 **All-day events** that work with any calendar app
- 📞 **Call reminders** in descriptions ("Remember to call and congratulate!")

## Supported Date Formats

- `YYYY-MM-DD` (e.g., 1990-05-15)
- `--MM-DD` (e.g., --05-15 for birthdays without year)

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip for package management
- No external dependencies for core functionality

## Development Setup

Google Birthday Liberator uses `uv` as the preferred package manager for fast, reliable dependency management:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install development dependencies
uv sync

# Run all commands through uv
uv run python filter_contacts.py
uv run python create_birthday_calendar.py
```

## Example Output

After running `make stats`:
```
📊 Contact Statistics:
====================
📊 Total contacts with birthdays: 35
📊 Original total contacts: 478
📅 Calendar events created: 35
```

## Export Instructions (Google Contacts)

1. Go to [Google Contacts](https://contacts.google.com)
2. Click **Export** (in the left sidebar)
3. Select **All contacts** or specific label
4. Choose **Google CSV** format
5. Save as `export.csv` in this project directory

## Import Instructions

1. **Google Calendar**: Import > Select file > Upload `birthdays.ics`
2. **Apple Calendar**: File > Import > Select `birthdays.ics`
3. **Outlook**: File > Import and Export > Import an iCalendar file
4. **Any calendar app**: Look for "Import" or "Add calendar" options

## Bonus: Disable Google Contacts Integration

After importing your self-owned birthday calendar, you can safely disable Google Contacts' unreliable birthday integration:

1. **Google Calendar**: Settings > Events from Gmail > Birthdays > Turn off
2. **Apple Calendar**: Preferences > Accounts > Google > Uncheck "Calendars"
3. **Outlook**: Remove Google Contacts birthday calendar subscription

**You're now free from Google's broken birthday reminders! 🎉**

## Testing

Google Birthday Liberator includes comprehensive tests to ensure reliability:

```bash
# Run all tests
uv run pytest tests/ -v

# Run tests with coverage report
uv run pytest tests/ --cov=. --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_filter_contacts.py -v
```

### Test Coverage

- **Unit tests** for contact filtering logic
- **Unit tests** for calendar generation
- **Integration tests** for complete workflow
- **Edge case handling** (empty files, invalid dates, Unicode names)
- **94% code coverage** across all modules

## Contributing

1. Install development dependencies: `uv sync`
2. Run tests: `uv run pytest tests/ -v`
3. Format code: `uv run black .`
4. Lint code: `uv run ruff check .`
5. Ensure tests pass and coverage remains high