import tkinter as tk
from navbar import Navbar
from content_frame import ContentFrame
from file_handler import FileHandler


class App:
    def __init__(self, master, content_frame):
        self.master = master
        self.master.title("Website Emulation")

        # Header
        self.header = Navbar(self.master, bg="lightblue", height=50)
        self.header.pack(fill=tk.X)

        # Content frame
        self.content = content_frame
        self.content.pack(fill=tk.BOTH, expand=True)

    def save_data_and_next(self, num_subsections, section_content):
        # Save section data
        data = {
            'num_subsections': num_subsections,
            'section_content': section_content,
            'subsections': []
        }

        # Save data to file
        FileHandler.save_data(data)

        # Retrieve subsection content iteratively
        self.content.retrieve_subsection_content(0, int(num_subsections))

    def display_html_content(self):
        data = FileHandler.load_data()
        self.content.display_html(data)


def main():
    root = tk.Tk()
    content_frame = ContentFrame(root, App.save_data_and_next)
    app = App(root, content_frame)
    root.mainloop()


if __name__ == "__main__":
    main()
