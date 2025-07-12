from cookiecutter.main import cookiecutter
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from pathlib import Path

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_run = 0
        self.debounce_period = 2 # seconds

    def on_any_event(self, event):
        # Ignore changes to run.py itself
        if Path(event.src_path).name == 'run.py':
            return
        if event.is_directory:
            return

        current_time = time.time()
        if current_time - self.last_run > self.debounce_period:
            self.last_run = current_time
            print(f"Detected change in {event.src_path}. Running cookiecutter...")
            try:
                # The output directory is now in the parent folder
                output_dir = Path("../python_boilerplate")
                if output_dir.exists() and output_dir.is_dir():
                    print(f"Removing existing directory: {output_dir}")
                    shutil.rmtree(output_dir)

                # The template is the current directory, output to parent
                cookiecutter('.', no_input=True, output_dir='..')
                print("Cookiecutter finished successfully.")
            except Exception as e:
                print(f"Error running cookiecutter: {e}")
            print("Waiting for next change...")


if __name__ == "__main__":
    # Watch the current directory
    path = "."
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
