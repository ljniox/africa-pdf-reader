from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import os
from miner import PDFMiner

class PDFViewer:
    def __init__(self, master):
        self.master = master
        self.master.title('PDF Viewer')
        self.master.geometry('580x520')

        self.path = None
        self.current_page = 0
        self.numPages = 0
        self.zoom_level = 1.0

        self.create_frames()
        self.create_widgets()

    def create_frames(self):
        self.top_frame = ttk.Frame(self.master)
        self.top_frame.pack(side=TOP, fill=BOTH, expand=True)

        self.bottom_frame = ttk.Frame(self.master)
        self.bottom_frame.pack(side=BOTTOM, fill=X)

    def create_widgets(self):
        # Top frame widgets
        self.canvas = Canvas(self.top_frame, bg='#ECE8F3')
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrolly.pack(side=RIGHT, fill=Y)

        self.scrollx = Scrollbar(self.master, orient=HORIZONTAL, command=self.canvas.xview)
        self.scrollx.pack(side=BOTTOM, fill=X)

        self.canvas.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)

        # Bottom frame widgets
        self.open_button = ttk.Button(self.bottom_frame, text="Open PDF", command=self.open_file)
        self.open_button.pack(side=LEFT, padx=5, pady=5)

        self.prev_button = ttk.Button(self.bottom_frame, text="Previous", command=self.previous_page)
        self.prev_button.pack(side=LEFT, padx=5, pady=5)

        self.next_button = ttk.Button(self.bottom_frame, text="Next", command=self.next_page)
        self.next_button.pack(side=LEFT, padx=5, pady=5)

        self.page_label = ttk.Label(self.bottom_frame, text='Page 0 of 0')
        self.page_label.pack(side=LEFT, padx=5, pady=5)

    def open_file(self):
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'),))
        if filepath:
            self.path = filepath
            self.miner = PDFMiner(self.path)
            self.numPages = self.miner.get_metadata()[1]
            self.current_page = 0
            self.display_page()

    def display_page(self):
        if 0 <= self.current_page < self.numPages:
            self.img_file = self.miner.get_page(self.current_page)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=self.img_file)
            self.page_label['text'] = f'Page {self.current_page + 1} of {self.numPages}'
            self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def next_page(self):
        if self.current_page < self.numPages - 1:
            self.current_page += 1
            self.display_page()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()

root = Tk()
app = PDFViewer(root)
root.mainloop() 