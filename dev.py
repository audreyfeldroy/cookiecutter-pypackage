"""
Cookiecutter PyPackage Development Watcher

This script watches for changes in the template directory and
automatically regenerates python_boilerplate/ when changes are detected.

Usage:
    1. Run this script from the cookiecutter-pypackage repo root directory
    2. Make changes to files in {{cookiecutter.pypi_package_name}}/
    3. The script will automatically regenerate python_boilerplate/ with your changes
    4. Press Ctrl+C to stop watching

The generated python-boilerplate/ directory will be created in the repo root.
"""

import io
import shutil
import sys
import time
from pathlib import Path

# Flush prints immediately, even when stdout is piped or redirected
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(line_buffering=True)

from cookiecutter.main import cookiecutter
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_run = 0
        self.debounce_period = 2  # seconds

    def on_any_event(self, event):
        # Ignore changes to dev.py itself
        if Path(event.src_path).name == "dev.py":
            return
        if event.is_directory:
            return

        current_time = time.time()
        if current_time - self.last_run > self.debounce_period:
            self.last_run = current_time
            print(f"Detected change in {event.src_path}. Running cookiecutter...")
            try:
                # Output dir matches pypi_package_name in cookiecutter.json
                output_dir = Path("python-boilerplate")
                if output_dir.exists() and output_dir.is_dir():
                    print(f"Removing existing directory: {output_dir}")
                    shutil.rmtree(output_dir)

                # The template is the current directory, output to repo root
                cookiecutter(".", no_input=True, output_dir=".")
                print("Cookiecutter finished successfully.")
            except Exception as e:
                print(f"Error running cookiecutter: {e}")
            print("Waiting for next change...")


if __name__ == "__main__":
    # Watch the template directory where actual changes matter
    path = "{{cookiecutter.pypi_package_name}}"
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Watching for file changes in '{path}'...")
    print("Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping watcher.")
        observer.stop()
    observer.join()
