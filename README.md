# PDF Watcher and Merger

## Overview
The PDF Watcher and Merger is a Python application designed to monitor a specific folder for new PDF files. When a new PDF is detected, it merges this file with a base PDF and moves the new file to an archive folder. This application uses Tkinter for its GUI, Watchdog for monitoring file system changes, and PyPDF2 for handling PDF operations.

## Features
- Monitor a specified folder for new PDF files.
- Merge new PDFs with a base PDF file.
- Archive processed PDFs to a different folder.
- Customizable paths for watched, archive, and base PDF folders through a GUI.
- Real-time logging within the GUI.

## Requirements
- Python 3.12+
- Tkinter (usually included with Python)
- Watchdog
- PyPDF2

You can install Watchdog and PyPDF2 using pip:
```bash
pip install watchdog PyPDF2
```

## Usage
1. Start the application. The GUI window titled "PDF Watcher and Merger" will open.
2. Set the paths for the watched folder, archive folder, and base PDF file using the "Browse" buttons.
3. Click "Update Paths" to save your settings.
4. Click "Start Observer" to begin monitoring the watched folder.
5. When new PDF files are added to the watched folder, they will be automatically merged with the base PDF and moved to the archive folder.
6. Use "Stop Observer" to halt the monitoring process.
7. Close the application using the window's close button, which ensures a clean shutdown of the observer.

## Code Structure
- `WatcherHandler` class: Handles file system events and processes new PDF files.
- `Application` class: Manages the GUI and integrates the watcher functionality.
- The application is initialized and run with a Tkinter event loop.

## Logging
- The application logs all key actions, like file detection, merging, and errors, in the GUI's log area.
- Logging is facilitated through a custom handler that redirects log messages to the Tkinter text widget.

## Limitations
- The application currently only supports PDF files.
- It processes files sequentially, which might not be optimal for high-volume scenarios.

## Customization
- Modify the `watched_folder`, `archive_folder`, and `base_pdf_path` variables for different default paths.
- The logging level and format can be adjusted in the `setup_logging` method of the `Application` class.

## Contributing
Contributions to enhance the functionality or efficiency of this application are welcome. Please adhere to standard Python coding practices for any pull requests.

## License
This project is open-sourced under the [MIT License](LICENSE).
