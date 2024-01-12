import os
import shutil
import logging
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import scrolledtext, StringVar, Frame
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyPDF2 import PdfReader, PdfWriter


# Initializing default paths for the watched folder, archive folder, and the base PDF path.
watched_folder = 'default/watched/folder/path'
archive_folder = 'default/archive/folder/path'
base_pdf_path = 'default/base/pdf/path'

# Custom logging handler class to redirect logs to a Tkinter text widget.
class TextHandler(logging.Handler):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        self.text.config(state='normal')
        self.text.insert(tk.END, msg + '\n')
        self.text.config(state='disabled')
        self.text.yview(tk.END)

# Initialize a set with the names of files that are already in the watched folder
#existing_files = {f for f in os.listdir(watched_folder) if os.path.isfile(os.path.join(watched_folder, f))}

# Event handler class
class WatcherHandler(FileSystemEventHandler):
    def __init__(self, existing_files):
        super().__init__()
        self.existing_files = existing_files

    def on_created(self, event):
        if event.is_directory:
            return

        filename = event.src_path
        if filename.endswith('.pdf') and os.path.basename(filename) not in self.existing_files:
            logging.info(f"[{os.path.basename(filename)}] added")  # Log the file name when added
            self.handle_new_pdf(filename)

    def handle_new_pdf(self, filename):
        try:
            merger = PdfWriter()
            with open(base_pdf_path, 'rb') as base_file, open(filename, 'rb') as new_file:
                base_pdf = PdfReader(base_file)
                new_pdf = PdfReader(new_file)

                # Add pages from the base PDF and the new PDF to the merger.
                for i in range(len(base_pdf.pages)):
                    merger.add_page(base_pdf.pages[i])

                for i in range(len(new_pdf.pages)):
                    merger.add_page(new_pdf.pages[i])

            # Write the merged PDF back to the base PDF path and move the new PDF to the archive folder.
            with open(base_pdf_path, 'wb') as f_out:
                merger.write(f_out)

            shutil.move(filename, os.path.join(archive_folder, os.path.basename(filename)))
            logging.info(f"Merged and archived [{os.path.basename(filename)}] successfully.")
        except Exception as e:
            logging.error(f"Error handling [{os.path.basename(filename)}]: {e}")
# Main application class using Tkinter for the GUI.
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.observer = None
        self.setup_logging()
        self.existing_files = set()  # Initialize as an empty set

    def update_paths(self):
        global watched_folder, archive_folder, base_pdf_path
        watched_folder = self.watched_folder_var.get()
        archive_folder = self.archive_folder_var.get()
        base_pdf_path = self.base_pdf_path_var.get()

        # Update existing files set after paths are updated
        self.existing_files = {f for f in os.listdir(watched_folder) if os.path.isfile(os.path.join(watched_folder, f))}

        logging.info("Paths updated.")
        # Method to create widgets for the GUI.
    def create_widgets(self):
        # [Code to create various buttons, labels, entries, and a log area for the GUI]
        self.watched_folder_var = StringVar()
        self.archive_folder_var = StringVar()
        self.base_pdf_path_var = StringVar()

        watched_frame: Frame = tk.Frame(self)
        watched_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(watched_frame, text="Watched Folder").grid(row=0, column=0, sticky="w")
        self.watched_folder_var = StringVar()
        self.watched_folder_entry = tk.Entry(watched_frame, textvariable=self.watched_folder_var)
        self.watched_folder_entry.grid(row=1, column=0, sticky="ew", padx=5)
        self.watched_folder_button = tk.Button(watched_frame, text="Browse",command=lambda: self.browse_folder(self.watched_folder_var))
                                               
        self.watched_folder_button.grid(row=1, column=1, padx=5)

        archive_frame = tk.Frame(self)
        archive_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(archive_frame, text="Archive Folder").grid(row=0, column=0, sticky="w")
        self.archive_folder_var = StringVar()
        self.archive_folder_entry = tk.Entry(archive_frame, textvariable=self.archive_folder_var)
        self.archive_folder_entry.grid(row=1, column=0, sticky="ew", padx=5)
        self.archive_folder_button = tk.Button(archive_frame, text="Browse",command=lambda: self.browse_folder(self.archive_folder_var))

        self.archive_folder_button.grid(row=1, column=1, padx=5)

        base_pdf_frame = tk.Frame(self)
        base_pdf_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(base_pdf_frame, text="Base PDF Path").grid(row=0, column=0, sticky="w")
        self.base_pdf_path_var = StringVar()
        self.base_pdf_path_entry = tk.Entry(base_pdf_frame, textvariable=self.base_pdf_path_var)
        self.base_pdf_path_entry.grid(row=1, column=0, sticky="ew", padx=5)
        self.base_pdf_path_button = tk.Button(base_pdf_frame, text="Browse",command=lambda: self.browse_path(self.base_pdf_path_var,file_type='file'))


        self.base_pdf_path_button.grid(row=1, column=1, padx=5)

        control_frame = tk.Frame(self)
        control_frame.pack(fill="x", padx=5, pady=5)
        self.update_paths_btn = tk.Button(control_frame, text="Update Paths", command=self.update_paths)
        self.update_paths_btn.pack(side="left", padx=5)
        self.start_btn = tk.Button(control_frame, text="Start Observer", command=self.start_observer)
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = tk.Button(control_frame, text="Stop Observer", command=self.stop_observer, state=tk.DISABLED)
        self.stop_btn.pack(side="left", padx=5)

        self.log_area = scrolledtext.ScrolledText(self, state='disabled')
        self.log_area.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

    def browse_folder(self, path_var):
        # Method to open a folder dialog and update the path variable.
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            path_var.set(folder_selected)

    def browse_path(self, path_var, file_type='folder'):
        # Method to open a file dialog and update the path variable.
        if file_type == 'folder':
            selected = filedialog.askdirectory()
        elif file_type == 'file':
            selected = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if selected:
            path_var.set(selected)

    def setup_logging(self):
        # Method to set up logging with a custom format and handler.
        log_format = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        log_handler = TextHandler(self.log_area)
        log_handler.setFormatter(log_format)
        logging.getLogger().addHandler(log_handler)
        logging.getLogger().setLevel(logging.INFO)

    def update_paths(self):
        global watched_folder, archive_folder, base_pdf_path
        watched_folder = self.watched_folder_var.get()
        archive_folder = self.archive_folder_var.get()
        base_pdf_path = self.base_pdf_path_var.get()
        logging.info("Paths updated.")

    def start_observer(self):
        # Method to start the Watchdog observer for the specified folder.
        self.observer = Observer()
        event_handler = WatcherHandler(self.existing_files)
        self.observer.schedule(event_handler, watched_folder, recursive=False)
        self.observer.start()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        logging.info("Observer started.")

    def stop_observer(self):
        # Method to stop the Watchdog observer.
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
            logging.info("Observer stopped.")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def on_closing(self):
        # Method to handle closing of the application, ensuring the observer is stopped.
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
        self.master.destroy()
# Initialize and run the Tkinter application.
root = tk.Tk()
root.title("PDF Watcher and Merger")
app = Application(master=root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()