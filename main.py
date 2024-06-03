import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv
from datetime import datetime
import threading
from time import sleep


class Program():
    def __init__(self):
        self.root = Tk()

        self.path = ""
        self.find_text = ""

        self.window()
        self.root.mainloop()

    def updater(self, event):
        self.progressbar_1["value"] = self.value
        self.label_1["text"] = f"{self.value} %"

    def open_file(self, *args):
        method = args[1]
        coincidences = []
        with open(self.path, "r", encoding="utf8") as f:
            n = 0
            string_n = 0
            with open(self.path, "rb") as f_2:
                string_count = sum(1 for _ in f_2)
            time_start = datetime.now()

            self.label_2["text"] = "Йде пошук..."

            if method == ".csv": f = csv.reader(f)
            for i in f:
                if method == ".csv": i = (' | '.join(i) + '\n')
                index = 0
                coincidences.append([])
                for x in i:
                    if index >= len(i): break

                    result = i.lower()[index:].find(self.find_text.lower())
                    if result != -1:
                        coincidences[n].append(index + result)
                        index += result + 1
                    else:
                        break

                if len(coincidences[n]) > 0:
                    self.text_1.insert(END, i)
                    for x in coincidences[n]:
                        start = "%s.%s" % (n+1, x)
                        end = "%s.%s" % (n+1, x+len(self.find_text.lower()))

                        self.text_1.tag_add("find %s" % start, start, end)
                        self.text_1.tag_config("find %s" % start, background="#00D8EB", foreground="black")
                else: n -= 1

                string_n += 1
                value = round(100 / string_count * string_n, 1)
                self.value = value
                self.root.event_generate('<<Progress>>')

                n += 1
 
            self.progressbar_1["value"] = 100
            self.label_1["text"] = "100.0 %"
            self.label_2["text"] = "Пошук тривав %s. Знайдено %s строк." % ((datetime.min + (datetime.now() - time_start)).strftime("%H:%M:%S"), n)

    def start_find(self, *args):
        self.find_text = self.entry_1.get()

        if self.path in ["", None]:
            messagebox.showinfo("Увага!", "Файл не обрано")
            return
        if self.find_text == "":
            messagebox.showinfo("Увага!", "Не введено пошукового запиту")
            return

        self.text_1.delete(1.0, END)

        extension = os.path.splitext(self.path)[1]
        threading.Thread(target=self.open_file, args=(self, extension), daemon=True).start()

    def get_file(self):
        filetypes = (
            ('Текстові файли', '*.txt'),
            ('md файли', '*.md'),
            ('csv файли', '*.csv')
        )

        self.path = filedialog.askopenfile(title='Оберіть файл', initialdir='/', filetypes=filetypes).name

    def save_file(self):
        f = filedialog.asksaveasfile(initialfile='%s_%s' % (datetime.now().strftime("%m/%d/%Y_%H:%M"), self.find_text), mode='w', defaultextension=".txt")
        if f is None:
            return
        f.write(str(self.text_1.get(1.0, END)))
        f.close()

    def window(self):
        self.root.geometry("700x500")

        frame_1 = Frame(self.root)
        frame_1.grid(row=0, column=0, sticky='ew', columnspan=3)
        frame_2 = Frame(self.root)
        frame_2.grid(row=1, column=0, sticky='nsew', columnspan=3)
        frame_3 = Frame(self.root)
        frame_3.grid(row=2, column=0, sticky='ew', columnspan=3)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        
        entry_1 = Entry(frame_1, text="Пошук")
        entry_1.grid(row=0, column=1, sticky='we')
        self.entry_1 = entry_1
        
        button_1 = Button(frame_1, text="Вибрати файли", command=self.get_file)
        button_1.grid(row=0, column=2)
        button_2 = Button(frame_1, text="Пошук", command=self.start_find)
        button_2.grid(row=0, column=3)
        
        self.root.bind_all("<Return>", self.start_find)

        frame_1.grid_columnconfigure(1, weight=1)
        
        text_1 = Text(frame_2)
        text_1.grid(row=0, column=0, sticky='nsew')
        self.text_1 = text_1

        scroll_1 = Scrollbar(frame_2, command=text_1.yview)
        scroll_1.grid(row=0, column=1, sticky='nsew')
        text_1['yscrollcommand'] = scroll_1.set

        frame_2.grid_columnconfigure(0, weight=1)
        frame_2.grid_rowconfigure(0, weight=1)

        progressbar_1 = ttk.Progressbar(frame_3, mode="determinate")
        progressbar_1.grid(row=1, column=0, sticky='ew')
        self.progressbar_1 = progressbar_1
        
        label_1 = Label(frame_3, text="0 %")
        label_1.grid(row=1, column=1)
        self.label_1 = label_1

        label_2 = Label(frame_3, text="")
        label_2.grid(row=0, column=0, sticky='w')
        self.label_2 = label_2

        frame_3.grid_columnconfigure(0, weight=1)

        menubar_1 = Menu()
        file_menu = Menu(menubar_1, tearoff=False)
        file_menu.add_command(label="Зберегти", accelerator="", command=self.save_file)
        menubar_1.add_cascade(menu=file_menu, label="Файл")
        self.root.config(menu=menubar_1)

        self.root.bind('<<Progress>>', self.updater)

Program()
