import tkinter as tk
from tkinter import CENTER, END, StringVar, font as tkfont
from tkinter import messagebox, PhotoImage, filedialog
from PIL import ImageTk, Image
import os
from spam_identifier import SpamIdentifier

class SpamIdentifierUI(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
		self.title("Spam Mail Identifier")
		self.resizable(False, False)
		self.geometry("700x350")
		self.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.active_name = None
		container = tk.Frame(self)
		container.grid(sticky="nsew")
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		self.frames = {}
		for F in (SMIHomePage, DataSetPage, SpamIdentifyPage):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew")
		self.show_frame("SMIHomePage")

		self.file_path = StringVar()

	def show_frame(self, page_name, **kwargs):
		frame = self.frames[page_name]
		frame.tkraise()
		file_path = kwargs.get("file_path")

		if file_path:
			frame.file_path = file_path

	def on_closing(self):
		if messagebox.askokcancel("Quit", "Are you sure?"):
			self.destroy()

class SMIHomePage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		render = PhotoImage(file="Assets/Images/home_page_icon.png")
		img = tk.Label(self, image=render)
		img.image = render
		img.grid(row=0, rowspan=5, ipadx=50, ipady=50)
		
		label = tk.Label(self, text="        Spam Mail Identifier        ", font=self.controller.title_font, fg="#263942")
		label.grid(row=0, column=5)

		button1 = tk.Button(self, text="   Classify Spam Emails  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("DataSetPage"))
		button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
		button1.grid(row=1, column=5, ipady=3, ipadx=7)
		button3.grid(row=2, column=5, ipady=3, ipadx=32)

	def on_closing(self):
		if messagebox.askokcancel("Quit", "Are you sure?"):
			self.controller.destroy()

class DataSetPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		tk.Label(self, text="Select Dataset File", fg="#263942", font="Helvetica 12 bold").grid(row=0, column=0, pady=10, padx=5)
		self.buttonbrowse = tk.Button(self, text="Browse", bg="#ffffff", fg="#263942", command=self.open_dataset_csv)
		self.buttonbrowse.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)

		self.buttoncanc = tk.Button(self, text="Go Back", bg="#ffffff", fg="#263942", command=lambda: self.controller.show_frame("SMIHomePage"))
		self.buttoncanc.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)

	def open_dataset_csv(self):
		file = filedialog.askopenfile(mode="r", filetypes=[("CSV Files", "*.csv")])

		if file:
			file_path = os.path.abspath(file.name)
			tk.Label(self, text="Selected Dataset :", fg="#263942", font="Helvetica 12 bold").place(x=5, y=120)
			self.selected_file = tk.Label(self, text=str(file_path), fg="#263942", font=("Helvetica 12 bold"), wraplength=680)
			self.selected_file.place(x=5, y=155)

			self.nextbutton = tk.Button(self, text="Next", bg="#ffffff", fg="#263942", command=lambda: self.controller.show_frame("SpamIdentifyPage", file_path=file_path))
			self.nextbutton.config(
				height=2,
				width=8
			)
			self.nextbutton.place(x=600, y=275, anchor=CENTER)

class SpamIdentifyPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.file_path = None

		tk.Label(self, text="Enter/Type Your Email", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)

		self.input_mail = tk.Text(self, height=10, width=60, bg="lightgrey", font='Helvetica 11')
		self.input_mail.grid(row=0, column=1, pady=10, padx=10)
		self.classifybutton = tk.Button(self, text="Classify", bg="#ffffff", fg="#263942", command=self.classify_email)
		self.classifybutton.config(
			height=2,
			width=8
		)
		self.classifybutton.place(x=635, y=215, anchor=CENTER)

	def classify_email(self):
		sidf = SpamIdentifier(
			dataset_path = self.file_path,
			input_mail = self.input_mail.get("1.0", END)
		)
		is_spam_mail = sidf.classify_spam()
		
		if is_spam_mail:
			messagebox.showwarning("Classification Result", "This is a spam mail")
		else:
			messagebox.showinfo("Classification Result", "This is not a spam mail")

if __name__ == "__main__":
	app = SpamIdentifierUI()
	app.iconphoto(False, ImageTk.PhotoImage(Image.open("Assets/Images/smi_icon.ico")))
	app.mainloop()