# Translation Synchronization Tool

This document explains how to use the `sync_translations.py` script to synchronize translation files across different languages in the Open edX frontend applications.

## Overview

The translation synchronization tool helps you:

1. Find missing translation keys between language files
2. Create updated versions of translation files with placeholders for missing translations
3. Keep translation files consistent across multiple languages
4. Work with any of the standard Open edX frontend applications

## Prerequisites

- Python 3.6 or higher
- Access to the frontend application translation files

## Basic Usage

### Display Help Information

```bash
python scripts/sync_translations.py --help
```

### Compare Two Specific Translation Files

```bash
python scripts/sync_translations.py --file1 translations/frontend-app-staff-dashboard/src/i18n/messages/es_ES.json --file2 translations/frontend-app-staff-dashboard/src/i18n/messages/ar.json
```

This will compare the Spanish and Arabic translation files and report any missing keys in either file.

### Compare and Update Translation Files

```bash
python scripts/sync_translations.py --file1 translations/frontend-app-staff-dashboard/src/i18n/messages/es_ES.json --file2 translations/frontend-app-staff-dashboard/src/i18n/messages/ar.json --update
```

This will compare the files and create updated versions with placeholders for any missing translations.

## Working with Directories

### Scan a Specific Directory

```bash
python scripts/sync_translations.py --dir translations/frontend-app-staff-dashboard/src/i18n/messages
```

This will:
1. Scan the specified directory for all JSON translation files
2. Display a list of found files
3. Prompt you to select which two files to compare

### Compare Specific Languages in a Directory

```bash
python scripts/sync_translations.py --dir translations/frontend-app-staff-dashboard/src/i18n/messages --lang1 es_ES --lang2 ar
```

This will find and compare the Spanish and Arabic translation files in the specified directory.

### Compare and Update Specific Languages

```bash
python scripts/sync_translations.py --dir translations/frontend-app-staff-dashboard/src/i18n/messages --lang1 es_ES --lang2 ar --update
```

This will compare the Spanish and Arabic files and create updated versions with placeholders for missing translations.

## Working with Standard Frontend Applications

The script always displays a list of standard Open edX frontend applications:

- frontend-app-dashboard
- frontend-app-course-authoring
- frontend-app-staff-dashboard
- frontend-app-learning
- frontend-app-profile
- frontend-app-account
- frontend-app-discussions

### Interactive Application Selection

```bash
python scripts/sync_translations.py
```

Without any arguments, the script will:
1. Display the list of standard frontend apps
2. Prompt you to select an application
3. Try to find translation files in the standard location (`app/src/i18n/messages/`)
4. Let you select which files to compare

### Using a Base Directory

```bash
python scripts/sync_translations.py --base /path/to/frontend-repos
```

This will:
1. Search for the standard frontend applications within the specified base directory
2. Display the applications that were found
3. Prompt you to select an application
4. Find and display translation files in that application
5. Let you select which files to compare

## Output Format

When comparing translation files, the script will report:
- The number of keys missing in each file
- Examples of the missing keys (up to 10)
- If using the `--update` flag, it will create new files with the format `[original_filename]_updated.json`

## Examples

### Example 1: Quick Comparison of Spanish and Arabic

```bash
python scripts/sync_translations.py --dir translations/frontend-app-staff-dashboard/src/i18n/messages --lang1 es_ES --lang2 ar
```

### Example 2: Update Missing Translations in All Frontend Apps

```bash
for app in frontend-app-dashboard frontend-app-course-authoring frontend-app-staff-dashboard frontend-app-learning frontend-app-profile frontend-app-account frontend-app-discussions; do
  python scripts/sync_translations.py --dir translations/$app/src/i18n/messages --lang1 es_ES --lang2 ar --update
done
```

### Example 3: Interactive Application Selection and Comparison

```bash
python scripts/sync_translations.py
```

Then follow the prompts to select an application and translation files to compare.

## Tips for Translation Management

1. **Regular Synchronization**: Run this tool regularly to keep translation files in sync
2. **Update Original Files**: After translation, update the original files rather than using the generated `_updated.json` files
3. **Batch Processing**: Use shell scripts to process multiple applications at once
4. **Version Control**: Commit translation updates separately from code changes for clearer history

## Troubleshooting

- **File Not Found**: Ensure the path to translation files is correct
- **Invalid JSON**: Check that your translation files contain valid JSON
- **No Files Found**: Verify that the directory contains `.json` files
- **No Missing Keys**: If the script reports no missing keys, the translation files are already synchronized
