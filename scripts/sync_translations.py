#!/usr/bin/env python3
import json
import os
import argparse
from pathlib import Path


def load_json_file(file_path):
    """Load a JSON file and return its contents as a dictionary."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file - {file_path}")
        return None


def save_json_file(data, file_path):
    """Save a dictionary as a JSON file with pretty formatting."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print(f"Saved updated file: {file_path}")


def find_translation_files(directory):
    """Find all JSON translation files in the given directory and its subdirectories."""
    translation_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                # Extract language code from filename (assuming format like xx.json or xx_XX.json)
                lang_code = os.path.splitext(file)[0]
                translation_files.append((lang_code, file_path))
    
    return translation_files


def compare_translations(source_data, target_data, source_lang, target_lang):
    """Compare translation keys between source and target languages."""
    if not source_data or not target_data:
        return [], []
    
    # Find keys in source that are missing in target
    missing_in_target = [
        key for key in source_data.keys() 
        if key not in target_data
    ]
    
    # Find keys in target that are missing in source
    missing_in_source = [
        key for key in target_data.keys() 
        if key not in source_data
    ]
    
    if missing_in_target:
        print(f"\n{len(missing_in_target)} keys from {source_lang} missing in {target_lang}:")
        for key in missing_in_target[:10]:  # Show first 10 as example
            print(f"  - {key}")
        if len(missing_in_target) > 10:
            print(f"  ... and {len(missing_in_target) - 10} more")
    
    if missing_in_source:
        print(f"\n{len(missing_in_source)} keys from {target_lang} missing in {source_lang}:")
        for key in missing_in_source[:10]:  # Show first 10 as example
            print(f"  - {key}")
        if len(missing_in_source) > 10:
            print(f"  ... and {len(missing_in_source) - 10} more")
    
    return missing_in_target, missing_in_source


def update_translation_file(file_path, source_data, missing_keys, source_lang):
    """Update a translation file with missing keys from a source file."""
    target_data = load_json_file(file_path)
    if not target_data:
        return
    
    updated = False
    for key in missing_keys:
        target_data[key] = f"[NEEDS TRANSLATION from {source_lang}] {source_data[key]}"
        updated = True
    
    if updated:
        # Create output path with _updated suffix
        base_path = os.path.splitext(file_path)[0]
        extension = os.path.splitext(file_path)[1]
        updated_path = f"{base_path}_updated{extension}"
        save_json_file(target_data, updated_path)


def sync_two_files(file1_path, file2_path, update_files=False):
    """Synchronize two specific translation files."""
    file1_lang = os.path.splitext(os.path.basename(file1_path))[0]
    file2_lang = os.path.splitext(os.path.basename(file2_path))[0]
    
    file1_data = load_json_file(file1_path)
    file2_data = load_json_file(file2_path)
    
    if not file1_data or not file2_data:
        return
    
    print(f"\nComparing {file1_lang} and {file2_lang}...")
    
    missing_in_file2, missing_in_file1 = compare_translations(
        file1_data, file2_data, file1_lang, file2_lang
    )
    
    if update_files:
        if missing_in_file2:
            print(f"\nUpdating {file2_lang} with keys from {file1_lang}...")
            update_translation_file(file2_path, file1_data, missing_in_file2, file1_lang)
        
        if missing_in_file1:
            print(f"\nUpdating {file1_lang} with keys from {file2_lang}...")
            update_translation_file(file1_path, file2_data, missing_in_file1, file2_lang)


def find_specific_lang_file(files, lang_code):
    """Find a file with a specific language code in the list of files."""
    for code, path in files:
        if code == lang_code or code.startswith(f"{lang_code}_"):
            return path
    return None


def get_standard_frontend_apps():
    """Return a list of standard frontend application directories."""
    return [
        "frontend-app-dashboard",
        "frontend-app-course-authoring",
        "frontend-app-staff-dashboard",
        "frontend-app-learning",
        "frontend-app-profile",
        "frontend-app-account",
        "frontend-app-discussions"
    ]


def find_app_directories(base_dir=None):
    """Find existing frontend app directories from the standard list."""
    standard_apps = get_standard_frontend_apps()
    found_apps = []
    
    # If base_dir is provided, look for app directories under it
    if base_dir:
        base_path = Path(base_dir)
        for app in standard_apps:
            app_path = base_path / app
            if app_path.exists() and app_path.is_dir():
                found_apps.append((app, str(app_path)))
            
            # Also check for translations subdirectory
            translations_path = base_path / app / "src" / "i18n" / "messages"
            if translations_path.exists() and translations_path.is_dir():
                found_apps.append((f"{app} (translations)", str(translations_path)))
    
    # If no apps were found or no base_dir provided, just return the standard list
    if not found_apps:
        found_apps = [(app, app) for app in standard_apps]
    
    return found_apps


def select_app_directory():
    """Prompt the user to select from standard frontend app directories."""
    apps = get_standard_frontend_apps()
    
    print("\nSelect a frontend application:")
    for i, app in enumerate(apps):
        print(f"{i+1}. {app}")
    
    try:
        choice = int(input("\nSelect an application (number): ")) - 1
        if 0 <= choice < len(apps):
            return apps[choice]
        else:
            print("Invalid selection")
            return None
    except ValueError:
        print("Please enter a valid number")
        return None


def main():
    parser = argparse.ArgumentParser(description='Synchronize translation files across languages.')
    parser.add_argument('--dir', '-d', help='Directory containing translation files', required=False)
    parser.add_argument('--lang1', '-l1', help='First language code (e.g., es_ES, ar)', required=False)
    parser.add_argument('--lang2', '-l2', help='Second language code (e.g., es_ES, ar)', required=False)
    parser.add_argument('--update', '-u', action='store_true', help='Update files with missing translations')
    parser.add_argument('--file1', '-f1', help='Path to first language file', required=False)
    parser.add_argument('--file2', '-f2', help='Path to second language file', required=False)
    parser.add_argument('--base', '-b', help='Base directory to search for frontend apps', required=False)
    
    args = parser.parse_args()
    
    # Always show the list of standard frontend apps
    print("Standard frontend applications:")
    for i, app in enumerate(get_standard_frontend_apps()):
        print(f"{i+1}. {app}")
    
    if args.file1 and args.file2:
        # Direct file comparison mode
        print(f"\nComparing specific files: {args.file1} and {args.file2}")
        sync_two_files(args.file1, args.file2, args.update)
        return
    
    # Determine which directory to use
    directory = None
    
    if args.dir:
        # Use provided directory
        directory = Path(args.dir)
    elif args.base:
        # Show apps found in the base directory
        app_dirs = find_app_directories(args.base)
        if app_dirs:
            print("\nFound frontend applications:")
            for i, (app_name, app_path) in enumerate(app_dirs):
                print(f"{i+1}. {app_name} ({app_path})")
            
            try:
                choice = int(input("\nSelect an application (number): ")) - 1
                if 0 <= choice < len(app_dirs):
                    _, directory = app_dirs[choice]
                    directory = Path(directory)
                else:
                    print("Invalid selection")
                    return
            except ValueError:
                print("Please enter a valid number")
                return
    else:
        # Interactive selection of standard app
        app_name = select_app_directory()
        if app_name:
            # Default path structure for translations in frontend apps
            directory = Path(app_name) / "src" / "i18n" / "messages"
            print(f"Using default translation path: {directory}")
            
            # If the directory doesn't exist, try to find it
            if not directory.exists():
                # Just use the app name as directory for now
                directory = Path(app_name)
                print(f"Default path not found, using: {directory}")
    
    if not directory or not directory.exists() or not directory.is_dir():
        print(f"Error: {directory} is not a valid directory")
        return
    
    print(f"\nScanning for translation files in {directory}...")
    translation_files = find_translation_files(directory)
    
    if not translation_files:
        print(f"No translation files found in {directory}")
        return
    
    print(f"Found {len(translation_files)} translation files:")
    for lang, path in translation_files:
        print(f"  - {lang}: {path}")
    
    if args.lang1 and args.lang2:
        # Compare specific languages
        lang1_file = find_specific_lang_file(translation_files, args.lang1)
        lang2_file = find_specific_lang_file(translation_files, args.lang2)
        
        if not lang1_file:
            print(f"Error: No translation file found for language {args.lang1}")
            return
        
        if not lang2_file:
            print(f"Error: No translation file found for language {args.lang2}")
            return
        
        sync_two_files(lang1_file, lang2_file, args.update)
    else:
        # Interactive mode if languages not specified
        print("\nPlease select which files to compare:")
        for i, (lang, path) in enumerate(translation_files):
            print(f"{i+1}. {lang}: {path}")
        
        try:
            choice1 = int(input("\nSelect first file (number): ")) - 1
            choice2 = int(input("Select second file (number): ")) - 1
            
            if 0 <= choice1 < len(translation_files) and 0 <= choice2 < len(translation_files):
                _, file1_path = translation_files[choice1]
                _, file2_path = translation_files[choice2]
                sync_two_files(file1_path, file2_path, args.update)
            else:
                print("Invalid selection")
        except ValueError:
            print("Please enter a valid number")


if __name__ == "__main__":
    main()
