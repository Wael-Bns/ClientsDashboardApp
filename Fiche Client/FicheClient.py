from tkinter import*
from tkinter import ttk
import sqlite3
from tkinter import messagebox

fen=Tk()
width, height= fen.winfo_screenwidth(),fen.winfo_screenheight()
fen.title("Fiche Patient")
fen.iconbitmap("icon.ico")
fen.geometry('%dx%d+0+0' % (width,height))

def rechercher():
    typed=searchentry.get()
    for record in tree.get_children():
        tree.delete(record)
    conn = sqlite3.connect('clients.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE if not exists customers(nom text, prenom text, date text, telephone integer, adresse text, correspondant text, cnam integer, nclient integer)''')
    count = 0
    c.execute("SELECT rowid, * FROM customers WHERE nom like ?", (typed.strip(" "),))
    newdata = c.fetchall()
    c.execute("SELECT rowid, * FROM customers WHERE date like ?",(typed.strip(" "),))
    newdata1 = c.fetchall()
    for dt1 in newdata:
        tree.insert(parent='', index=0, iid=str(count), text=str(dt1[0]),
                        values=(dt1[1], dt1[2], dt1[3], dt1[4], dt1[5], dt1[6], dt1[7], dt1[8]))
        count += 1
    for dt2 in newdata1:
        tree.insert(parent='', index=0, iid=str(count), text=str(dt2[0]),
                        values=(dt2[1], dt2[2], dt2[3], dt2[4], dt2[5], dt2[6], dt2[7], dt2[8]))

        count += 1
    conn.commit()
    conn.close()

#search bar
searchframe =Frame(fen)
searchframe.pack()
searchbutton=Button(searchframe,text="Rechercher",font=("calibri",14),command=rechercher)
searchlabel=Label(searchframe,text="Tapez le prénom du Patient :",font=("calibri",16))
searchentry=Entry(searchframe,width=100,font=("calibri",16))
searchlabel.grid(row=0,column=0,padx=10,pady=10)
searchbutton.grid(row=0,column=2,padx=10,pady=10)
searchentry.grid(row=0,column=1,padx=10,pady=10)
#tree view
treeframe=Frame(fen)
treeframe.pack()

frame = Frame(fen)
frame.pack(padx=20,pady=20)
#tree view configurations
scrollbar=Scrollbar(treeframe)
scrollbar.pack(side= RIGHT, fill=Y)

tree=ttk.Treeview(treeframe,yscrollcommand=scrollbar.set,selectmode="extended")
tree.pack()
ttk.Style().theme_use("clam")
ttk.Style().configure("Treeview.Heading", background="silver",font=18)
ttk.Style().configure("Treeview",font=("Calibri",16))
#create database
conn=sqlite3.connect('clients.db')
c=conn.cursor()
c.execute('''CREATE TABLE if not exists customers(nom text, prenom text, date text, telephone integer, adresse text, correspondant text, cnam integer, nclient integer)''')


count=1
c.execute("SELECT rowid, * from customers")
data = c.fetchall()
for dt in data :
    tree.insert(parent='', index='end',iid=str(count), text=str(dt[0]),
    values=( dt[1], dt[2], dt[3], dt[4],dt[5],dt[6],dt[7],dt[8]))
    count+=1
conn.commit()

#columns configurations
scrollbar.config(command=tree.yview)
tree['columns']=("Nom","Prénom","Date de naissance","N° de téléphone","Adresse","Correspondant","CNAM","N° client")
tree.column("#0",width=160,minwidth=0)
tree.column("Nom",anchor=CENTER,width=170)
tree.column("Prénom",anchor=CENTER,width=170)
tree.column("Date de naissance",anchor=CENTER,width=190)
tree.column("N° de téléphone",anchor=CENTER,width=170)
tree.column("Adresse",anchor=CENTER,width=170)
tree.column("Correspondant",anchor=CENTER,width=170)
tree.column("CNAM",anchor=CENTER,width=170)
tree.column("N° client",anchor=CENTER,width=170)
#headings
tree.heading("#0",text="#0")
tree.heading("Prénom",text="Prénom",anchor=CENTER)
tree.heading("Nom",text="Nom",anchor=CENTER)
tree.heading("Date de naissance",text="Date de naissance",anchor=CENTER)
tree.heading("N° de téléphone",text="N° de téléphone",anchor=CENTER)
tree.heading("Adresse",text="Adresse",anchor=CENTER)
tree.heading("Correspondant",text="Correspondant",anchor=CENTER)
tree.heading("CNAM",text="CNAM",anchor=CENTER)
tree.heading("N° client",text="N° Dossier",anchor=CENTER)


#fiche client configurations
info = LabelFrame(frame, text="Fiche Patient",font=("Calibri",20))
info.grid(row=1,column=0, padx=20,pady=20)

buttonsframe =LabelFrame(frame,font=19)
buttonsframe.grid(row= 3,column=0, padx=20,pady=20)

#nclient function
def n_client():
    firstname =chnom.get()
    lastname =chprenom.get()
    naissance =chdate.get()
    address = chaddress.get()
    telephone = chtel.get()
    correspondant = chcorresp.get()
    client =chnclient.get()
    ncnam =chcnam.get()
    if firstname and lastname  :
        c.execute("INSERT INTO customers(nom, prenom, date, telephone, adresse, correspondant, cnam, nclient) VALUES(?,?,?,?,?,?,?,?)",
                  (firstname.strip((" ")), lastname.strip(" "),naissance,telephone,address,correspondant,ncnam,client))
        conn.commit()
        global count
        tree.insert(parent='',index='end',iid=str(count),text=str(count),values=(firstname,lastname,naissance,telephone,address,correspondant,ncnam,client))
        count += 1
        chnom.delete(0,END)
        chprenom.delete(0,END)
        chtel.delete(0,END)
        chcnam.delete(0,END)
        chdate.delete(0,END)
        chaddress.delete(0,END)
        chcorresp.delete(0,END)
        chnclient.delete(0,END)
        chnom.focus()

    else:
        messagebox.showerror("Erreur","Quelques informations sont nécessaires !")

newclient=Button(buttonsframe, text="Enregistrer la fiche",font=("Calibri",15), command=n_client)
newclient.grid(row=0,column=0,pady=10,padx=10)



def afficher():
    for record in tree.get_children():
        tree.delete(record)
    conn = sqlite3.connect('clients.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE if not exists customers(nom text, prenom text, date text, telephone integer, adresse text, correspondant text, cnam integer, nclient integer)''')
    count = 1
    c.execute("SELECT rowid,* from customers")
    data = c.fetchall()
    for dt in data:
        tree.insert(parent='', index="end", iid=str(count), text=str(dt[0]),
                    values=( dt[1], dt[2], dt[3], dt[4], dt[5], dt[6], dt[7],dt[8]))
        count += 1
    conn.commit()
    conn.close()



#modele de recherche client button
listeclients=Button(buttonsframe, text="Afficher la liste des clients",font=("Calibri",15),command=afficher)
listeclients.grid(row=0,column=1,pady=10,padx=10)

#nom
nompass=StringVar()
nom =Label(info, text="Nom :",font=("Times New Roman",17))
chnom= Entry(info,textvariable=nompass,width=17,font=("Calibri",15))
chnom.focus()

#prenom
prenompass=StringVar()
prenom = Label(info, text="Prénom :",font=("Times New Roman",17))
chprenom= Entry(info,textvariable=prenompass,width=17,font=("Calibri",15))

#date de naissance
datepass=StringVar()
date =Label(info, text="Date de naissance :",font=("Times New Roman",17))
chdate= Entry(info,textvariable=datepass,width=17,font=("Calibri",15))

#adresse
adrespass=StringVar()
adresse=Label(info,text="Adresse :",font=("Times New Roman",17))
chaddress= Entry(info,textvariable=adrespass,width=17,font=("Calibri",15))

#telephone
telpass=StringVar()
tel=Label(info, text="N° téléphone :",font=("Times New Roman",17))
chtel= Entry(info,textvariable=telpass,width=17,font=("Calibri",15))

#correspondant
correspass=StringVar()
corresp=Label(info, text="Correspondant :",font=("Times New Roman",17))
chcorresp= Entry(info,textvariable=correspass,width=17,font=("Calibri",15))

#cnam
cnampass=StringVar()
cnam=Label(info, text="CNAM :",font=("Times New Roman",17))
chcnam= Entry(info,textvariable=cnampass,width=17,font=("Calibri",15))

#numero client
nclientpass=StringVar()
nclient=Label(info, text="N° Dossier :",font=("Times New Roman",17))
chnclient= Entry(info,textvariable=nclientpass,width=17,font=("Calibri",15))

def remove():
    x=tree.selection()
    response =messagebox.askokcancel("Supprimer client","Voulez vous vraiment supprimez ce client de la liste ?")
    if response ==1 :
        conn = sqlite3.connect('clients.db')
        c = conn.cursor()
        print(x)
        for item in x:
            y = tree.item(item, "text")[0]
            tree.delete(item)
            c.execute("DELETE from customers WHERE oid = "+str(y))
            conn.commit()
            conn.close()
    else:
        tree.selection_remove(tree.focus())


#delete items button
deletebutton=Button(buttonsframe,text="Supprimer client", font=("Calibri",15),command=remove)
deletebutton.grid(row=0,column=2,pady=10,padx=10)

#exit button
exitb= Button(buttonsframe,text="Fermer le programme",font=("Calibri",15),command= fen.destroy)
exitb.grid(row=0,column=3,pady=10,padx=10)
#Entry and button grids
nom.grid(row=0,column=0)
chnom.grid(row=1,column=0)
prenom.grid(row=0,column=1)
chprenom.grid(row=1,column=1)
date.grid(row=0,column=2)
chdate.grid(row=1,column=2)
adresse.grid(row=0,column=3)
chaddress.grid(row=1,column=3)
tel.grid(row=2,column=0)
chtel.grid(row=3,column=0)
corresp.grid(row=2,column=1)
chcorresp.grid(row=3,column=1)
cnam.grid(row=2,column=2)
chcnam.grid(row=3,column=2)
nclient.grid(row=2,column=3)
chnclient.grid(row=3,column=3)

for widget in info.winfo_children():
    widget.grid_configure(padx=10,pady=5)
def deselect(event):
    tree.selection_remove(tree.focus())
tree.bind("<Button-1>",deselect)
tree.bind("<Button-3>",deselect)

fen.mainloop()

