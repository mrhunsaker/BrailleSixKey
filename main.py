import tkinter as tk
import tkinter.scrolledtext
from tkinter import simpledialog, messagebox 
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
from tkinter import Menu 

class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(Root, self).__init__(*args, **kwargs)
        self.title("Six Key Braille Input: Unicode Braille")
        self.config(bg="grey20")
        self.menubar = Menu()
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)
        self.filemenu.add_command(label="Open", command = self.open_file)
        self.filemenu.add_command(label="Save", command = self.save_file)
        self.helpmenu.add_command(label='About', command = self.about)
        self.helpmenu.add_command(label='About', command = self.help)
        self.filemenu.add_command(label="Exit", command = self.destroy)

        self.config(menu=self.menubar)
        self.variable = tk.StringVar()
        self.variable.set(hold_key_list)
        self.create_widgets()
        self.bind("<KeyPress>", self.hold_key)
        self.bind("<KeyRelease>", self.key_combine)
        self.bind("<space>", self.space_bar)
        self.bind("<BackSpace>", self.backspace)
        self.bind("<Return>", self.new_line)
        self.bind("<Control-s>", self.save_file)
        self.mainloop()
    
    def create_widgets(self):
        self.main_frame = tk.Frame(self, bg="grey20")
        self.main_frame.grid(column=0, row=0, padx=10, pady=10)
        self.label2 = tk.Label(self.main_frame, text="Use S-D-F J-K-L to type Braille")
        self.label2.config(font=("Arial", 24, "bold"), bg="grey20", fg="snow")
        self.label2.grid(column=0, row=4, columnspan=3)
        self.input_area = tk.Text(self.main_frame, height=25, width=50, bg="lavender", blockcursor=True, insertbackground="yellow")
        self.input_area.grid(column=0, row=5, columnspan=2)
        self.input_area.config(font=("Calibri", 24), state="disabled")
        self.input_area.focus_set()

    @staticmethod
    def hold_key(event):
        try:
            if hold_key_list.index(event.keysym):
                # return event.keysym
                pass
        except:
            hold_key_list.append(event.keysym)
            
    def key_combine(self, event):
        word = "".join(sorted(hold_key_list))
        lower_caps = word.lower()
        # print(lower_caps)
        if lower_caps in letter_combination_mapping:
            output = letter_combination_mapping.get(lower_caps)
            self.display(output)
        else:
            hold_key_list.clear()
        pass
    
    def backspace(self, event):
        self.input_area.config(state="normal")
        self.input_area.delete("insert -1 chars", "insert")
        self.input_area.config(state='disabled')     
         
    def space_bar(self, event):
        self.display(event="\u2800")
        
    def new_line(self, event):
        self.display(event="\n")
        
    def save_file(event):
        files = [('All Files', '*.*'),
                ('Braille File', '*.brf'), 
                ('Text Files', '*.txt')]
        filename = asksaveasfile(filetypes = files, defaultextension = files)
    
    def open_file(event):
        files = [('All Files', '*.*'),
                ('Braille File', '*.brf'), 
                ('Text Files', '*.txt')]
        filename = askopenfilename(filetypes = files, defaultextension = files)
        
    def display(self, event):
        self.input_area.config(state="normal")
        self.input_area.insert('end', event)
        self.input_area.yview('end')
        self.input_area.config(state='disabled')
        hold_key_list.clear()

    def about(event):
        tkinter.messagebox.showinfo(title='About', message = 'testing')
        
    def help(event):
        tkinter.messagebox.showinfo(title='Help', message = 'testing')
        
hold_key_list = []
str(hold_key_list)
letter_combination_mapping = {"f": u'\u2801', "df": u'\u2803', "fj": u'\u2809', "fjk": u'\u2819', "fk": u'\u2811', "dfj": u'\u280B', "dfjk": u'\u281B', "dfk": u'\u2813', "dj": u'\u280A', "djk": u'\u281A', "fs": u'\u2805', "dfs": u'\u2807', "fjs": u'\u280D', "fjks": u'\u281D', "fks": u'\u2815', "dfjs": u'\u280F', "dfjks": u'\u281F', "dfks": u'\u2817', "djs": u'\u280E', "djks": u'\u281E', "fls": u'\u2825', "dfls": u'\u2827', "djkl": u'\u283A', "fjls": u'\u282D', "fjkls": u'\u283D', "fkls": u'\u2835', "kls": u'\u2834', "d": u'\u2802', "ds": u'\u2806', "dk": u'\u2812', "dkl": u'\u2832', "dl": u'\u2822', "dks": u'\u2816', "dkls": u'\u2836', "dls": u'\u2826', "ks": u'\u2814', " ": u'\u2800', "djls": u'\u282E', 'k': u'\u2810', "jkls": u'\u283C', "dfjl": u'\u282B', "fjl": u'\u2829', "dfjls": u'\u282F', "s": u'\u2804', "dfkls": u'\u2837', "djkls": u'\u283E', "fl": u'\u2821', "jls": u'\u282C', "l": u'\u2820', "ls": u'\u2824', "jl": u'\u2828', "js": u'\u280C', "fkl": u'\u2831', "kl": u'\u2830', "dfl": u'\u2823', "dfjkls": u'\u283F', "jks": u'\u281C', "fjkl": u'\u2839', "j": u'\u2808', "djl": u'\u282A', "dfkl": u'\u2833', "dfjkl": u'\u283B', "jk": u'\u2818', "jkl": u'\u2838'}



Root()