# importing everything from tkinter
from tkinter import *
# importing ttk for styling widgets from tkinter
from tkinter import ttk
# importing filedialog from tkinter
from tkinter import filedialog as fd
# importing os module
import os
# importing the PDFMiner class from the miner file
from miner import PDFMiner


# creating a class called PDFViewer
class PDFViewer:
    # initializing the __init__ / special method
    def __init__(self, master):
        # path for the pdf doc
        self.path = None
        # state of the pdf doc, open or closed
        self.fileisopen = None
        # author of the pdf doc
        self.author = None
        # name for the pdf doc
        self.name = None
        # the current page for the pdf
        self.current_page = 0
        # total number of pages for the pdf doc
        self.numPages = None    
        # creating the window
        '''
        self.master = master
        # gives title to the main window
        self.master.title('PDF Viewer')
        # gives dimensions to main window
        self.master.geometry('580x520+440+180')
        # this disables the minimize/maximize button on the main window
        # self.master.resizable(width = 0, height = 0)
        self.master.resizable(True, True)
        # loads the icon and adds it to the main window
        #self.master.iconbitmap(self.master, 'pdf_file_icon.ico')

        # Using PhotoImage to set the icon
        try:
            icon = PhotoImage(file='pdf_file_icon.png')
            self.master.iconphoto(False, icon)
        except Exception as e:
            print(f"Error setting icon: {e}")

        # creating the menu
        self.menu = Menu(self.master)
        # adding it to the main window
        self.master.config(menu=self.menu)
        # creating a sub menu
        self.filemenu = Menu(self.menu)
        # giving the sub menu a label
        self.menu.add_cascade(label="File", menu=self.filemenu)
        # adding a two buttons to the sub menus
        self.filemenu.add_command(label="Open File", command=self.open_file)
        self.filemenu.add_command(label="Exit", command=self.master.destroy)
        # creating the top frame
        # self.top_frame = ttk.Frame(self.master, width=580, height=460)
        self.top_frame = ttk.Frame(self.master)
        # placing the frame using inside main window using grid()
        # self.top_frame.grid(row=0, column=0)
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        # the frame will not propagate
        self.top_frame.grid_propagate(False)
        # creating the bottom frame
        # self.bottom_frame = ttk.Frame(self.master, width=580, height=50)
        self.bottom_frame = ttk.Frame(self.master)
        # placing the frame using inside main window using grid()
        # self.bottom_frame.grid(row=1, column=0)
        self.bottom_frame.grid(row=1, column=0, sticky='ew')

        # configuring grid weights
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # the frame will not propagate
        # self.bottom_frame.grid_propagate(False)

        # creating a vertical scrollbar
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        # adding the scrollbar
        # self.scrolly.grid(row=0, column=1, sticky=(N,S))
        self.scrolly.grid(row=0, column=1, sticky='ns')

        # creating a horizontal scrollbar
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        # adding the scrollbar
        # self.scrollx.grid(row=1, column=0, sticky=(W, E))
        self.scrollx.grid(row=1, column=0, sticky='ew')

        # creating the canvas for display the PDF pages
        # self.output = Canvas(self.top_frame, bg='#ECE8F3', width=560, height=435)
        self.output = Canvas(self.top_frame, bg='#ECE8F3')

        # inserting both vertical and horizontal scrollbars to the canvas
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        # adding the canvas
        # self.output.grid(row=0, column=0)
        self.output.grid(row=0, column=0, sticky='nsew')

        # configuring the horizontal scrollbar to the canvas
        # self.scrolly.configure(command=self.output.yview)
        # configuring the vertical scrollbar to the canvas
        # self.scrollx.configure(command=self.output.xview)

        # configuring the scrollbars
        self.output.config(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.scrolly.config(command=self.output.yview)
        self.scrollx.config(command=self.output.xview)
        '''
        self.master = master
        self.master.title('PDF Viewer')
        self.master.geometry('580x520+440+180')
        self.master.resizable(True, True)
        
        # Add zoom level initialization
        self.zoom_level = 1.0  # Default zoom level
        self.zoom_step = 0.1   # Zoom increment/decrement step

        # ... (keep the existing button creation code)

        # Add zoom in and zoom out buttons
        self.zoom_in_button = ttk.Button(self.bottom_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.grid(row=0, column=5, padx=5, pady=8)

        self.zoom_out_button = ttk.Button(self.bottom_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.grid(row=0, column=6, padx=5, pady=8)

        # Add zoom level label
        self.zoom_label = ttk.Label(self.bottom_frame, text="100%")
        self.zoom_label.grid(row=0, column=7, padx=5)
        
        # Using PhotoImage to set the icon
        try:
            icon = PhotoImage(file='pdf_file_icon.png')
            self.master.iconphoto(False, icon)
        except Exception as e:
            print(f"Error setting icon: {e}")
        
        # creating the menu
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        
        # File menu
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open File", command=self.open_file)
        self.filemenu.add_command(label="Exit", command=self.master.destroy)
        
        # creating the top frame
        self.top_frame = ttk.Frame(self.master)
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        
        # creating the bottom frame
        self.bottom_frame = ttk.Frame(self.master)
        self.bottom_frame.grid(row=1, column=0, sticky='ew')
        
        # configuring grid weights
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        
        # creating a vertical scrollbar
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        self.scrolly.grid(row=0, column=1, sticky='ns')
        
        # creating a horizontal scrollbar
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        self.scrollx.grid(row=1, column=0, sticky='ew')
        
        # creating the canvas for displaying the PDF pages
        self.output = Canvas(self.top_frame, bg='#ECE8F3')
        self.output.grid(row=0, column=0, sticky='nsew')
        
        # configuring the scrollbars
        self.output.config(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.scrolly.config(command=self.output.yview)
        self.scrollx.config(command=self.output.xview)


        # loading the button icons
        self.uparrow_icon = PhotoImage(file='uparrow.png')
        self.downarrow_icon = PhotoImage(file='downarrow.png')
        # resizing the icons to fit on buttons
        self.uparrow = self.uparrow_icon.subsample(3, 3)
        self.downarrow = self.downarrow_icon.subsample(3, 3)
        # creating an up button with an icon
        self.upbutton = ttk.Button(self.bottom_frame, image=self.uparrow, command=self.previous_page)
        # adding the button
        self.upbutton.grid(row=0, column=1, padx=(270, 5), pady=8)
        # creating a down button with an icon
        self.downbutton = ttk.Button(self.bottom_frame, image=self.downarrow, command=self.next_page)
        # adding the button
        self.downbutton.grid(row=0, column=3, pady=8)
        # label for displaying page numbers
        self.page_label = ttk.Label(self.bottom_frame, text='page')
        # adding the label
        self.page_label.grid(row=0, column=4, padx=5)
        
    # function for opening pdf files
    def open_file(self):
        # open the file dialog
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'), ))
        # checking if the file exists
        if filepath:
            # declaring the path
            self.path = filepath
            # extracting the pdf file from the path
            filename = os.path.basename(self.path)
            # passing the path to PDFMiner 
            self.miner = PDFMiner(self.path)
            # getting data and numPages
            data, numPages = self.miner.get_metadata()
            # setting the current page to 0
            self.current_page = 0
            # checking if numPages exists
            if numPages:
                # getting the title
                self.name = data.get('title', filename[:-4])
                # getting the author
                self.author = data.get('author', None)
                self.numPages = numPages
                # setting fileopen to True
                self.fileisopen = True
                # calling the display_page() function
                self.display_page()
                # replacing the window title with the PDF document name
                self.master.title(self.name)
    
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

    def display_page(self):
        if 0 <= self.current_page < self.numPages:
            self.img_file = self.miner.get_page(self.current_page, zoom=self.zoom_level)
            self.output.delete("all")  # Clear previous content
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            self.stringified_current_page = self.current_page + 1
            self.page_label['text'] = f"{self.stringified_current_page} of {self.numPages}"
            region = self.output.bbox(ALL)
            self.output.configure(scrollregion=region)      

    # function for displaying next page
    def next_page(self):
        # checking if file is open
        if self.fileisopen:
            # checking if current_page is less than or equal to numPages-1
            if self.current_page <= self.numPages - 1:
                # updating the page with value 1
                self.current_page += 1
                # displaying the new page
                self.display_page()
                            
    # function for displaying the previous page        
    def previous_page(self):
        # checking if fileisopen
        if self.fileisopen:
            # checking if current_page is greater than 0
            if self.current_page > 0:
                # decrementing the current_page by 1
                self.current_page -= 1
                # displaying the previous page
                self.display_page()

  
# creating the root winding using Tk() class
root = Tk()
# instantiating/creating object app for class PDFViewer
app = PDFViewer(root)
# calling the mainloop to run the app infinitely until user closes it
root.mainloop()