# Google Birthday Liberator
# Simple task runner for liberating birthdays from Google Contacts and creating reliable calendars

.PHONY: help filter calendar all backup restore clean stats

# Default target
help: ## Show this help message
	@echo "Google Birthday Liberator - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Files:"
	@echo "  export.csv           - Main contacts file (filtered)"
	@echo "  export_backup.csv    - Backup of original contacts"
	@echo "  birthdays.ics        - Generated calendar file"
	@echo ""

filter: ## Remove contacts without birthdays from export.csv
	@echo "🔍 Filtering contacts to keep only those with birthdays..."
	python filter_contacts.py
	@echo "✅ Contacts filtered successfully"

calendar: ## Generate ICS calendar file from filtered contacts
	@echo "📅 Creating birthday calendar from contacts..."
	python create_birthday_calendar.py
	@echo "✅ Calendar created: birthdays.ics"

all: filter calendar ## Run complete workflow: filter contacts and create calendar
	@echo "✅ Complete workflow finished"
	@echo "📧 Import birthdays.ics into your calendar app"

backup: ## Create backup of current export.csv
	@if [ -f export.csv ]; then \
		cp export.csv export_backup_$(shell date +%Y%m%d_%H%M%S).csv; \
		echo "✅ Backup created: export_backup_$(shell date +%Y%m%d_%H%M%S).csv"; \
	else \
		echo "❌ No export.csv file found to backup"; \
	fi

restore: ## Restore from backup (restores export_backup.csv to export.csv)
	@if [ -f export_backup.csv ]; then \
		cp export_backup.csv export.csv; \
		echo "✅ Restored export.csv from backup"; \
	else \
		echo "❌ No backup file found (export_backup.csv)"; \
	fi

clean: ## Remove generated files (birthdays.ics)
	@echo "🧹 Cleaning generated files..."
	@rm -f birthdays.ics
	@echo "✅ Cleaned up generated files"

stats: ## Show statistics about contacts and birthdays
	@echo "📊 Contact Statistics:"
	@echo "===================="
	@if [ -f export.csv ]; then \
		total_contacts=$$(tail -n +2 export.csv | wc -l | tr -d ' '); \
		echo "📊 Total contacts with birthdays: $$total_contacts"; \
	else \
		echo "❌ No export.csv file found"; \
	fi
	@if [ -f export_backup.csv ]; then \
		original_contacts=$$(tail -n +2 export_backup.csv | wc -l | tr -d ' '); \
		echo "📊 Original total contacts: $$original_contacts"; \
	fi
	@if [ -f birthdays.ics ]; then \
		calendar_events=$$(grep -c "BEGIN:VEVENT" birthdays.ics); \
		echo "📅 Calendar events created: $$calendar_events"; \
	fi