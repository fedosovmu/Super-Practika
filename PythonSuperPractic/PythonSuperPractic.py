from tkinter import *
from tkinter import ttk
import Searcher

root = Tk()
root.title('������� ����')
root.resizable(False, False)
x = (root.winfo_screenwidth() / 2 - root.winfo_reqwidth())
y = (root.winfo_screenheight() / 2 - root.winfo_reqheight())
root.wm_geometry('+%d+%d' % (x, y))

# 
Label(root, text='�����').grid(row=1, column=1)
searchEntry = Entry(root, width=45)
searchEntry.grid(row=1, column=2)
searchButton = Button(root, text='������', width=10, command=searchButtonDowned).grid(row=1, column=3)

# �������
note = ttk.Notebook(root, width=600, heigh=400) 
f1 = ttk.Frame(note)
listBox = Listbox(f1, width=97, height=23)
scrollBar = Scrollbar(f1, command=listBox.yview).pack(side='right', expand=True)
listBox.pack(side='top')
openButton = Button(f1, text='�������', width=20, command=openButtonDowned).pack(side='left', expand=True)
reloadButton = Button(f1, text='��������', width=20, command=reloadButtonDowned).pack(side='right', expand=True)

f2 = Canvas()
canva = Canvas(f2, width=600, height=370, bg='white')
canva.create_line(0,0, 50, 50)
canva.pack(side='top')

note.add(f1, text='������ ��������')
note.add(f2, text='������')

note.grid(row=2, column=1, columnspan=3)

s = Search()

def searchButtonDowned():
    listBox.delete(0, END)   
    st = searchEntry.get()    
    s.search(st)
    for i in s.searchResults:
        listBox.insert(END, i.title)

def openButtonDowned():
    root.title = 'kek'
    pass

def reloadButtonDowned():
	pass

root.mainloop()

