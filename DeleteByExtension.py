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
    width = 300
    height = 300

    win_width = width
    win_height = height

    # Calculate center position based on screen size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (win_width / 2))
    y = int((screen_height / 2) - (win_height / 2))
    root.geometry(f"{win_width}x{win_height}+{x}+{y}")

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

    root.after(0, update, 0)
    root.mainloop()

def send_files_to_trash():
    folder = input("Enter the full path to the folder: ").strip()
    if not os.path.isdir(folder):
        print(f"The path '{folder}' is not a valid directory.")
        return

    extension = input("Enter the file extension to delete (e.g. .log, .tmp): ").strip()
    if not extension.startswith('.'):
        extension = '.' + extension

    trashed_files = []

    stop_event = threading.Event()
    gif_thread = threading.Thread(target=show_gif_window, args=(stop_event,))
    gif_thread.start()

    start_time = time.time()
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath) and filename.lower().endswith(extension.lower()):
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

    # Output summary
    print("\nSent the following files to the recycle bin:")
    for f in trashed_files:
        print(f"  - {f}")

    print("\nTrash complete.")

if __name__ == "__main__":
    send_files_to_trash()
