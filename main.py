#!/usr/bin/python3
# coding=utf-8
###############################################################################
#    Copyright 2023 Michael Ryan Hunsaker, M.Ed., Ph.D.                       #
#    email: hunsakerconsulting@gmail.com                                      #
#                                                                             #
#    Licensed under the Apache License, Version 2.0 (the "License");          #
#    you may not use this file except in compliance with the License.         #
#    You may obtain a copy of the License at                                  #
#                                                                             #
#        http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                             #
#    Unless required by applicable law or agreed to in writing, software      #
#    distributed under the License is distributed on an "AS IS" BASIS,        #
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
#    See the License for the specific language governing permissions and      #
#    limitations under the License.                                           #
###############################################################################

###############################################################################
#    TO DO (LastEdited 2023-04-12):                                                                   #
#    * Make this program Screenreader accessible (move to wxWidgets)          #
#    * Make opening and creating .brf files easier                            #
###############################################################################
import tkinter as tk
import tkinter.scrolledtext
from tkinter import simpledialog, messagebox
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
from tkinter import Menu
import tkinter.scrolledtext as scrolledtext
import random

colorList = [
    '#EFD6C0', 
    '#F1F0E2', 
    '#EEE78E', 
    '#8896C6', 
    '#6BCD9C', 
    '#E0C7D7', 
    '#FF8C55', 
    '#BFCAD6'
    ]

class Root(tk.Tk):
    def __init__(
        self, 
        *args, 
        **kwargs
        ):
        super(
            Root, 
            self
            ).__init__(
                *args, 
                **kwargs
                )
        self.option_add('*Dialog.msg.font', 'JetBrains Mono NL')
        self.geometry(
            '1175x950+20+20'
            )
        self.title(
            "Six-Key Braille Input"
            )
        self.config(
            bg=random.choice(
                colorList
                )
            )
        self.variable = tk.StringVar()
        self.variable.set(
            hold_key_list
            )
        self.position = tk.StringVar()
        self.create_widgets()
        self.create_menus()
        self.bind(
            "<KeyPress>", 
            self.hold_key
            )
        self.bind(
            "<KeyRelease>", 
            self.key_combine
            )
        self.bind(
            "<space>", 
            self.space_bar
            )
        self.bind(
            "<BackSpace>", 
            self.backspace
            )
        self.bind(
            "<Return>", 
            self.new_line
            )

    def create_menus(self):
        self.menubar = Menu()
        self.filemenu = Menu(
            self.menubar, 
            tearoff=0
            )
        self.helpmenu = Menu(
            self.menubar, 
            tearoff=0
            )
        self.menubar.add_cascade(
            label='File', 
            menu=self.filemenu
            )
        self.menubar.add_cascade(
            label='Help', 
            menu=self.helpmenu
            )
        self.filemenu.add_command(
            label="Save", 
            command = self.save_file
            )        
        self.filemenu.add_separator()
        self.filemenu.add_command(
            label="Exit", 
            command = self.destroy
            )
        self.helpmenu.add_command(
            label='About', 
            command = self.about
            )
        self.helpmenu.add_command(
            label='Help', 
            command = self.help
            )
        self.config(
            menu=self.menubar
            )

    def create_widgets(self):
        self.main_frame = tk.Frame(
            self, 
            bg=random.choice(
                colorList
                )
            )
        self.main_frame.grid(
            column=0, 
            row=0, 
            padx=100, 
            pady=10
            )
        self.input_area = scrolledtext.ScrolledText(
            self.main_frame, 
            height=25, 
            width=48, 
            bg="#FFEBEE", 
            cursor = "cross red",
            wrap='word'
            )
        self.input_area.grid(
            column=0, 
            row=6, 
            columnspan=3,
            sticky = tk.N
            )
        self.input_area.config(
            font=(
                "JetBrains Mono NL", 
                24
                ), 
            state="disabled"
            )

        self.label2 = tk.Label(
            self.main_frame, 
            text = f"Line 0, Column 0\n---------------------------------------\nUS Letter = 25 Lines, 32 columns | US Braille = 25 Lines, 40 columns"

            )
        self.label2.config(
            font=(
                "JetBrains Mono NL", 
                18, 
                "bold"
                ), 
            bg="navy", 
            fg="yellow"
            )
        self.label2.grid(
            column=0, 
            row=4, 
            rowspan=2,
            columnspan=3,
            sticky = tk.N
            )
        self.input_area.focus_set()

    @staticmethod
    def hold_key(event):
        try:
            if hold_key_list.index(
                event.keysym
                ):
                # return event.keysym
                pass
        except:
            hold_key_list.append(
                event.keysym
                )

    def key_combine(
        self, event
        ):
        word = "".join(
            sorted(
                hold_key_list
                )
            )
        lower_caps = word.lower()
        # print(lower_caps)
        if lower_caps in letter_combination_mapping:
            output = letter_combination_mapping.get(
                lower_caps
                )
            self.display(
                output
                )
        else:
            hold_key_list.clear()
        pass

    def backspace(
        self, 
        event
        ):
        self.input_area.config(
            state="normal"
            )
        self.input_area.delete(
            "insert -1 chars", 
            "insert"
            )
        self.input_area.config(
            state='disabled'
            )
        curr = self.input_area.index(
            tkinter.INSERT
            )
        self.position.set(
            curr
            )
        new_label_raw = self.position.get()
        new_label_split = new_label_raw.split(
            "."
            )
        new_label = f"Line {new_label_split[0]}, Column {new_label_split[1]}\n---------------------------------------\nUS Letter = 25 Lines, 32 columns | US Braille = 25 Lines, 40 columns"
        self.label2['text'] = new_label
        

    def space_bar(
        self, 
        event
        ):
        self.display(
            event="\u2800"
            )
        curr = self.input_area.index(
            tkinter.INSERT
            )
        self.position.set(
            curr
            )
        new_label_raw = self.position.get()
        new_label_split = new_label_raw.split(
            "."
            )
        new_label = f"Line {new_label_split[0]}, Column {new_label_split[1]}\n---------------------------------------\nUS Letter = 25 Lines, 32 columns | US Braille = 25 Lines, 40 columns"
        self.label2['text'] = new_label
        

    def new_line(
        self, event
        ):
        self.display(
            event="\n"
            )
        curr = self.input_area.index(
            tkinter.INSERT
            )
        self.position.set(
            curr
            )
        new_label_raw = self.position.get()
        new_label_split = new_label_raw.split(
            "."
            )
        new_label = f"Line {new_label_split[0]}, Column {new_label_split[1]}\n---------------------------------------\nUS Letter = 25 Lines, 32 columns | US Braille = 25 Lines, 40 columns"
        self.label2['text'] = new_label

    def save_file(
        event
        ):
        files = [
                (
                'All Files', 
                '*.*'
            ),
                (
                'Braille File', 
                '*.brf'
            ), 
                (
                'Text Files', 
                '*.txt'
            )
        ]
        filename = asksaveasfile(
            filetypes = files, 
            defaultextension = files
            )

    def display(
        self, 
        event
        ):
        self.input_area.config(
            state="normal"
            )
        self.input_area.insert(
            'end', 
            event
            )
        self.input_area.yview(
            'end'
            )
        self.input_area.config(
            state='disabled'
            )
        curr = self.input_area.index(
            tkinter.INSERT
            )
        self.position.set(
            curr
            )
        new_label_raw = self.position.get()
        new_label_split = new_label_raw.split(
            "."
            )
        new_label = f"Line {new_label_split[0]}, Column {new_label_split[1]}\n---------------------------------------\nUS Letter = 25 Lines, 32 columns | US Braille = 25 Lines, 40 columns"
        self.label2['text'] = new_label
        hold_key_list.clear()

    def about(
        event
        ):
        tkinter.messagebox.showinfo(
            title='About', 
            message = '''
            Six Key Braille Input GUI
            --------------------------------------------
            Copyright © 2023 Michael Ryan Hunsaker, M.Ed., Ph.D.
            Davis School District
            hunsakerconsulting@gmail.com
            --------------------------------------------
            Source code available at:
            https://github.com/mrhunsaker/BrailleSixKey
            
            '''
            )

    def help(
        event
        ):
        tkinter.messagebox.showinfo(
            title='Help', 
            message = '''
            This program uses the SDF JKL keys to generate 
            formatted unicode braille.
            --------------------------------------------
            Key Mappings:
            f = dot 1  |  j = dot 4
            d = dot 2  |  k = dot 5
            s = dot 3  |  l = dot 6
            
            <space> adds a single Unicode Space
            <Backspace> deletes one Unicode Character
            <Insert> activates a cursor to move with arrow keys
                - There is NO braille input in this mode
            <esc> turns the cursor off and allows braille input
            --------------------------------------------
            
            '''
            )
        
curr = ''
hold_key_list = []
str(
    hold_key_list
    )
letter_combination_mapping = {
    "f": u'\u2801', 
    "df": u'\u2803', 
    "fj": u'\u2809', 
    "fjk": u'\u2819',
    "fk": u'\u2811',
    "dfj": u'\u280B',
    "dfjk": u'\u281B',
    "dfk": u'\u2813',
    "dj": u'\u280A',
    "djk": u'\u281A',
    "fs": u'\u2805',
    "dfs": u'\u2807',
    "fjs": u'\u280D',
    "fjks": u'\u281D',
    "fks": u'\u2815',
    "dfjs": u'\u280F',
    "dfjks": u'\u281F',
    "dfks": u'\u2817',
    "djs": u'\u280E',
    "djks": u'\u281E',
    "fls": u'\u2825',
    "dfls": u'\u2827',
    "djkl": u'\u283A',
    "fjls": u'\u282D',
    "fjkls": u'\u283D',
    "fkls": u'\u2835',
    "kls": u'\u2834',
    "d": u'\u2802',
    "ds": u'\u2806',
    "dk": u'\u2812',
    "dkl": u'\u2832',
    "dl": u'\u2822',
    "dks": u'\u2816',
    "dkls": u'\u2836',
    "dls": u'\u2826',
    "ks": u'\u2814',
    " ": u'\u2800',
    "djls": u'\u282E', 
    "k": u'\u2810',
    "jkls": u'\u283C',
    "dfjl": u'\u282B',
    "fjl": u'\u2829',
    "dfjls": u'\u282F',
    "s": u'\u2804',
    "dfkls": u'\u2837',
    "djkls": u'\u283E',
    "fl": u'\u2821',
    "jls": u'\u282C',
    "l": u'\u2820',
    "ls": u'\u2824',
    "jl": u'\u2828',
    "js": u'\u280C',
    "fkl": u'\u2831',
    "kl": u'\u2830',
    "dfl": u'\u2823',
    "dfjkls": u'\u283F',
    "jks": u'\u281C',
    "fjkl": u'\u2839',
    "j": u'\u2808',
    "djl": u'\u282A',
    "dfkl": u'\u2833',
    "dfjkl": u'\u283B',
    "jk": u'\u2818',
    "jkl": u'\u2838'
    }

if __name__ == '__main__':
    Root().mainloop()