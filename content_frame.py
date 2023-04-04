import tkinter as tk
from file_handler import FileHandler


def create_content_block(section):
    content = ""
    lines = section.strip().split('\n')
    for line in lines:
        if (line.startswith("Heading ") or line.startswith("heading ")) and ":" in line:
            heading_number = line.split(":", 1)[0][7:].strip()
            content += f"<h{heading_number}>{line.split(':', 1)[1].strip()}</h{heading_number}>"
        elif line.startswith("p :") or line.startswith("P :"):
            content += f"<p>{line[3:].strip()}</p>"
        else:
            content += f"<br>{line.strip()}"
    return content


class ContentFrame(tk.Frame):
    def __init__(self, master, save_callback):
        super().__init__(master)
        self.save_callback = save_callback

        # Create widgets
        self.add_section_label = tk.Label(self, text="Add Section")
        self.add_section_label.pack(anchor="nw", padx=10, pady=(10, 0))

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.subsections_label = tk.Label(self.content_frame, text="Number of subsections:")
        self.subsections_label.grid(row=0, column=0, padx=(20, 0), pady=(10, 0), sticky=tk.W)

        self.subsections_spinbox = tk.Spinbox(self.content_frame, from_=0, to=3, width=3)
        self.subsections_spinbox.delete(0, tk.END)
        self.subsections_spinbox.insert(0, "1")
        self.subsections_spinbox.grid(row=0, column=1, padx=(0, 20), pady=(10, 0), sticky=tk.W)

        self.section_content_label = tk.Label(self.content_frame, text="Section content:")
        self.section_content_label.grid(row=1, column=0, padx=(20, 0), pady=(10, 0), sticky=tk.W)

        self.section_content_text = tk.Text(self.content_frame, width=40, height=10)
        self.section_content_text.grid(row=1, column=1, padx=(0, 20), pady=(10, 0), sticky=tk.W)

        self.next_btn = tk.Button(self.content_frame, text="Next", command=self.save_section_data)
        self.next_btn.grid(row=2, column=1, pady=(10, 0), sticky=tk.E)

        # Initialize variables
        self.subsection_widgets = []
        self.num_subsections = 0

    def save_section_data(self):
        self.num_subsections = int(self.subsections_spinbox.get())
        section_content = self.section_content_text.get(1.0, tk.END).strip()

        # Save section data
        data = {
            'num_subsections': self.num_subsections,
            'section_content': section_content,
            'subsections': []
        }
        FileHandler.save_data(data)

        # Destroy all widgets in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Retrieve subsection content iteratively
        self.retrieve_subsection_content(0)

    def retrieve_subsection_content(self, subsection_index):
        if subsection_index >= self.num_subsections:
            self.display_html_content()
            return

        subsection_label = tk.Label(self.content_frame, text=f"Subsection {subsection_index + 1} content:")
        subsection_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky=tk.W)

        subsection_content_text = tk.Text(self.content_frame, width=40, height=10)
        subsection_content_text.grid(row=0, column=1, padx=(0, 20), pady=(20, 0), sticky=tk.W)

        next_subsection_btn_text = "Next Subsection" if subsection_index < self.num_subsections - 1 else "Generate"
        next_subsection_btn = tk.Button(self.content_frame, text=next_subsection_btn_text,
                                        command=lambda: self.save_subsection_data(subsection_content_text,
                                                                                  subsection_index))
        next_subsection_btn.grid(row=1, column=1, pady=(10, 0), sticky=tk.E)
        self.subsection_widgets.append(subsection_label)
        self.subsection_widgets.append(subsection_content_text)
        self.subsection_widgets.append(next_subsection_btn)

    def save_subsection_data(self, subsection_content_text, subsection_index):
        subsection_content = subsection_content_text.get(1.0, tk.END).strip()
        data = FileHandler.load_data()

        # Add subsection content to data
        data['subsections'].append(subsection_content)
        FileHandler.save_data(data)

        # Clear the frame
        for widget in self.subsection_widgets:
            widget.destroy()

        # Retrieve the next subsection content
        self.retrieve_subsection_content(subsection_index + 1)

    def display_html_content(self):
        data = FileHandler.load_data()

        main_section_content = create_content_block(data['section_content'])

        subsection_blocks = ""
        for subsection_content in data['subsections']:
            subsection_blocks += f'<div class="sub">{create_content_block(subsection_content)}</div>'

        html_content = (
            '<!DOCTYPE html>\n'
            '<html>\n'
            '  <head>\n'
            '    <title></title>\n'
            '  </head>\n'
            '  <body>\n'
            '    <section id="mainsection">\n'
            f'      <div class="heading">\n'
            f'        {main_section_content}\n'
            '      </div>\n'
            '      <div class="subsection">\n'
            f'        {subsection_blocks}\n'
            '      </div>\n'
            '    </section>\n'
            '  </body>\n'
            '  <style>\n'
            '    body {\n'
            '      margin: 0;\n'
            '    }\n'
            '    #mainsection {\n'
            '      width: 100%;\n'
            '      height: 500px;\n'
            '      background-color: goldenrod;\n'
            '      text-align: center;\n'
            '    }\n'
            '    #mainsection h1 {\n'
            '      margin-top: 0;\n'
            '    }\n'
            '    .subsection {\n'
            '      width: 80%;\n'
            '      height: 400px;\n'
            '      background-color: black;\n'
            '      color: gold;\n'
            '      margin: 0 10%;\n'
            '    }\n'
            '    .sub {\n'
            '      background-color: brown;\n'
            '      color: white;\n'
            '      width: 45%;\n'
            '      float: left;\n'
            '      margin-top: 2%;\n'
            '      margin-left: 3%;\n'
            '      margin-right: 2%;\n'
            '    }\n'
            '    .sub1, .sub {\n'
            '      margin-left: 3%;\n'
            '      margin-right: 2%;\n'
            '    }\n'
            '    .sub2 {\n'
            '      margin-right: 3%;\n'
            '      margin-left: 2%;\n'
            '    }\n'
            '  </style>\n'
            '</html>\n'
        )

        print(html_content)
        with open('section.html', 'w') as f:
            f.write(html_content)

        #TODO: display on frame
