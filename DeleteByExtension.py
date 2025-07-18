import os
from send2trash import send2trash

def send_files_to_trash():
    folder = input("Enter the full path to the folder: ").strip()
    if not os.path.isdir(folder):
        print(f" The path '{folder}' is not a valid directory.")
        return

    extension = input("Enter the file extension to delete (e.g. .log, .tmp): ").strip()
    if not extension.startswith('.'):
        extension = '.' + extension

    trashed_files = []

    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath) and filename.lower().endswith(extension.lower()):
            try:
                send2trash(filepath)
                trashed_files.append(filename)
            except Exception as e:
                print(f" Failed to move {filename} to trash: {e}")

    if trashed_files:
        print("\n Sent the following files to the recycle bin:")
        for f in trashed_files:
            print(f"  - {f}")
    else:
        print(f"\nNo files with extension '{extension}' found in '{folder}'.")

if __name__ == "__main__":
    send_files_to_trash()