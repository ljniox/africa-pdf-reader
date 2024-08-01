from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import os
from miner import PDFMiner

class PDFViewer:
    def __init__(self, master):
        self.master = master
        self.master.title('PDF Viewer')
        self.master.geometry('580x520+440+180')
        self.master.resizable(True, True)

        self.path = None
        self.fileisopen = None
        self.author = None
        self.name = None
        self.current_page = 0
        self.numPages = None
        self.zoom_level = 1.0
        self.zoom_step = 0.1

        # Create menu
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open File", command=self.open_file)
        self.filemenu.add_command(label="Exit", command=self.master.destroy)

        # Create frames
        self.top_frame = ttk.Frame(self.master)
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        
        self.bottom_frame = ttk.Frame(self.master)
        self.bottom_frame.grid(row=1, column=0, sticky='ew')
        
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Create widgets for top frame
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        self.scrolly.grid(row=0, column=1, sticky='ns')
        
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        self.scrollx.grid(row=1, column=0, sticky='ew')
        
        self.output = Canvas(self.top_frame, bg='#ECE8F3')
        self.output.grid(row=0, column=0, sticky='nsew')
        
        self.output.config(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.scrolly.config(command=self.output.yview)
        self.scrollx.config(command=self.output.xview)

        # Create widgets for bottom frame
        self.upbutton = ttk.Button(self.bottom_frame, text="Previous", command=self.previous_page)
        self.upbutton.grid(row=0, column=0, padx=5, pady=5)
        
        self.downbutton = ttk.Button(self.bottom_frame, text="Next", command=self.next_page)
        self.downbutton.grid(row=0, column=1, padx=5, pady=5)
        
        self.page_label = ttk.Label(self.bottom_frame, text='Page')
        self.page_label.grid(row=0, column=2, padx=5)
        
        self.zoom_in_button = ttk.Button(self.bottom_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.grid(row=0, column=3, padx=5, pady=5)
        
        self.zoom_out_button = ttk.Button(self.bottom_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.grid(row=0, column=4, padx=5, pady=5)
        
        self.zoom_label = ttk.Label(self.bottom_frame, text="100%")
        self.zoom_label.grid(row=0, column=5, padx=5)

    def open_file(self):
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'),))
        if filepath:
            self.path = filepath
            filename = os.path.basename(self.path)
            self.miner = PDFMiner(self.path)
            data, numPages = self.miner.get_metadata()
            self.current_page = 0
            if numPages:
                self.name = data.get('title', filename[:-4])
                self.author = data.get('author', None)
                self.numPages = numPages
                self.fileisopen = True
                self.display_page()
                self.master.title(self.name)

    def display_page(self):
        if 0 <= self.current_page < self.numPages:
            self.img_file = self.miner.get_page(self.current_page)
            self.output.delete("all")
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            self.page_label['text'] = f'{self.current_page + 1} of {self.numPages}'
            self.output.configure(scrollregion=self.output.bbox(ALL))

    def next_page(self):
        if self.fileisopen and self.current_page < self.numPages - 1:
            self.current_page += 1
            self.display_page()

    def previous_page(self):
        if self.fileisopen and self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def zoom_in(self):
        if self.fileisopen:
            self.zoom_level += self.zoom_step
            self.update_zoom()

    def zoom_out(self):
        if self.fileisopen and self.zoom_level > self.zoom_step:
            self.zoom_level -= self.zoom_step
            self.update_zoom()

    def update_zoom(self):
        self.zoom_label['text'] = f"{int(self.zoom_level * 100)}%"
        self.display_page()

# Create the main window and start the application
root = Tk()
app = PDFViewer(root)
root.mainloop()