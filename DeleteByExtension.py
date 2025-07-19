import os
import threading
import time
from send2trash import send2trash
from tkinter import Tk, Label
from PIL import Image, ImageTk, ImageSequence

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GIF_PATH = os.path.join(SCRIPT_DIR, "Gif", "106823.gif")

def show_gif_window(stop_event):
    root = Tk()
    root.title("Loading.....")
    width = 500
    height = 500

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")

    lbl = Label(root)
    lbl.pack()

    img = Image.open(GIF_PATH)
    frames = [ImageTk.PhotoImage(frame.copy().convert('RGBA')) for frame in ImageSequence.Iterator(img)]

    def update(index):
        if not stop_event.is_set():
            lbl.configure(image=frames[index])
            root.after(100, update, (index + 1) % len(frames))
        else:
            root.destroy()
            root.quit()

    root.after(0, update, 0)
    root.mainloop()

def send_files_to_trash():
    while True:
        folder = input("Enter the full path to the folder: ").strip()
        if not os.path.isdir(folder):
            print(f"The path '{folder}' is not a valid directory.\n")
            continue

        extensions_input = input("Enter file extensions to delete (comma-separated, e.g. .log, .tmp): ").strip()
        extensions = [ext.strip().lower() if ext.strip().startswith('.') else f".{ext.strip().lower()}"
                      for ext in extensions_input.split(',') if ext.strip()]

        if not extensions:
            print("No valid extensions provided.\n")
            continue

        exclusions = []
        exclude_prompt = input("Do you want to exclude any files? (y/n): ").strip().lower()
        if exclude_prompt == 'y':
            exclude_input = input("Enter filenames to exclude (comma-separated, case-sensitive): ").strip()
            exclusions = [name.strip() for name in exclude_input.split(',') if name.strip()]

            print("\nChecking excluded files:")
            missing = []
            for name in exclusions:
                excluded_path = os.path.join(folder, name)
                if os.path.isfile(excluded_path):
                    print(f"  ✓ Found excluded file: {name}")
                else:
                    print(f"  ✗ Excluded file not found: {name}")
                    missing.append(name)

            if missing:
                print("\nError: One or more excluded files were not found. Aborting deletion.")
                print("Missing files:")
                for m in missing:
                    print(f"  - {m}")
                input("\nPress Enter to retry...")
                continue

        break

    trashed_files = []

    stop_event = threading.Event()
    gif_thread = threading.Thread(target=show_gif_window, args=(stop_event,))
    gif_thread.start()

    start_time = time.time()
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if (
            os.path.isfile(filepath)
            and any(filename.lower().endswith(ext) for ext in extensions)
            and filename not in exclusions
        ):
            try:
                send2trash(filepath)
                trashed_files.append(filename)
                time.sleep(0.3)
            except Exception as e:
                print(f"\nFailed to move {filename} to trash: {e}")

    elapsed = time.time() - start_time
    if elapsed < 5:
        time.sleep(5 - elapsed)

    stop_event.set()
    gif_thread.join()

    print("\nSent the following files to the recycle bin:")
    for f in trashed_files:
        print(f"  - {f}")

    print("\nTrash complete.")

if __name__ == "__main__":
    try:
        send_files_to_trash()
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    finally:
        if os.name == "nt":
            print("\nFinished")


