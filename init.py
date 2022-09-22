import os

import firebase_admin
from firebase_admin import credentials

import shutil


class Init:
    def __init__(self):
        pass

    def bring_file_to_the_front(self):
        ask_for_file_ui = AskForFileUI()

        selected_filepath = ask_for_file_ui.get_selected_file_location()

        if selected_filepath == "":
            return

        current_location = os.getcwd()

        shutil.copy(selected_filepath, current_location)

        # rename the moved file
        selected_filename = os.path.basename(selected_filepath)
        new_name = "fluency-py-private-key.json"
        os.rename(f'{current_location}/{selected_filename}', f'{current_location}/{new_name}')

    def init_firebase_admin(self):
        cred = credentials.Certificate("./fluency-py-private-key.json")
        firebase_admin.initialize_app(cred)


class AskForFileUI:
    def __init__(self):
        try:
            import tkinter as tk
            from tkinter import filedialog

            # create the root window
            self.root = tk.Tk()
            self.root.withdraw()
            self.filetypes = (
                ('json files', '*.json'),
                ('All files', '*.*')
            )

            self.filedialog = filedialog

        except ModuleNotFoundError:
            self.filedialog = None

    def get_selected_file_location(self):
        # show the dialog
        if self.filedialog is None:
            file_path = input('Enter file path location manually: ')
        else:
            file_path = self.filedialog.askopenfilename(filetypes=self.filetypes)

        return file_path


if __name__ == "__main__":
    init = Init()
    print("please select your service key json file (firebase admin), please be sure to select a valid file, to avoid errors.")
    init.bring_file_to_the_front()
