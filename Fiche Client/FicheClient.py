from tkinter import*
from tkinter import ttk
import sqlite3
from tkinter import messagebox

fen=Tk()
width, height= fen.winfo_screenwidth(),fen.winfo_screenheight()
fen.title("Fiche Patient")
fen.iconbitmap("icon.ico")
fen.geometry('%dx%d+0+0' % (width,height))

#create database
conn=sqlite3.connect('clients.db')
c=conn.cursor()
c.execute('''CREATE TABLE if not exists customers(id integer primary key AUTOINCREMENT,nom text, prenom text, date text, telephone integer, adresse text, correspondant text, cnam integer, nclient integer)''')
conn.commit()
conn.close()

#fonction rechercher
def rechercher():
    typed=searchentry.get().strip(" ")
    conn = sqlite3.connect('clients.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE nom like '%"+typed+"%' or date like '%"+typed+"%'")
    for record in tree.get_children():
        tree.delete(record)
    data = c.fetchall()
    for dt in data:
        c.execute("select id from customers where id='"+str(dt[0])+"'")
        newid=c.fetchall()[0][0];
        tree.insert(parent='', index="end", iid=newid,
                  values=(dt[0],dt[1], dt[2], dt[3], dt[4], dt[5], dt[6], dt[7],dt[8]))
    conn.close()

#search bar
searchframe =Frame(fen)
searchframe.pack()
searchbutton=Button(searchframe,text="Rechercher",font=("calibri",15),command=rechercher)
searchlabel=Label(searchframe,text="Tapez le nom du Patient :",font=("calibri",16))
searchentry=Entry(searchframe,width=80,font=("calibri",16))
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

tree=ttk.Treeview(treeframe,show='headings',yscrollcommand=scrollbar.set,selectmode="extended")
tree.pack()
ttk.Style().theme_use("clam")
ttk.Style().configure("Treeview.Heading", background="silver",font=(None,16))
ttk.Style().configure("Treeview",font=("Calibri",20),rowheight=40)


#columns configurations
scrollbar.config(command=tree.yview)
tree['columns']=("id","Nom","Prénom","Date de naissance","N° de téléphone","Adresse","Correspondant","CNAM","N° client")
tree.column("id",anchor=CENTER,width=0,minwidth=0)
tree.column("Nom",anchor=CENTER,width=220)
tree.column("Prénom",anchor=CENTER,width=220)
tree.column("Date de naissance",anchor=CENTER,width=220)
tree.column("N° de téléphone",anchor=CENTER,width=220)
tree.column("Adresse",anchor=CENTER,width=220)
tree.column("Correspondant",anchor=CENTER,width=220)
tree.column("CNAM",anchor=CENTER,width=220)
tree.column("N° client",anchor=CENTER,width=240)

#headings
tree.heading("id",text="id",anchor=CENTER)
tree.heading("Nom",text="Nom",anchor=CENTER)
tree.heading("Prénom",text="Prénom",anchor=CENTER)
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

#afficher la table initiale
conn = sqlite3.connect('clients.db')
c = conn.cursor()
c.execute("SELECT * from customers")
data = c.fetchall()
for dt in data:
    c.execute("select id from customers where id='"+str(dt[0])+"'")
    newid=c.fetchall()[0][0];
    tree.insert(parent='', index="end", iid=newid,
              values=(dt[0],dt[1], dt[2], dt[3], dt[4], dt[5], dt[6], dt[7],dt[8]))
conn.commit()
conn.close()

#nclient function
def n_client():
    firstname =chnom.get().strip(" ")
    lastname =chprenom.get().strip(" ")
    naissance =chdate.get().strip(" ")
    address = chaddress.get().strip(" ")
    telephone = chtel.get().strip(" ")
    correspondant = chcorresp.get().strip(" ")
    client =chnclient.get().strip(" ")
    ncnam =chcnam.get().strip(" ")
    if firstname and lastname  :
        conn=sqlite3.connect('clients.db')
        c=conn.cursor()
        c.execute("INSERT INTO customers(nom, prenom, date, telephone, adresse, correspondant, cnam, nclient) VALUES(?,?,?,?,?,?,?,?)",
                  (firstname, lastname,naissance,telephone,address,correspondant,ncnam,client))
        conn.commit()
        c.execute("select seq from sqlite_sequence where name='customers'")
        newid=c.fetchall()[0][0]
        tree.insert(parent='',index='end',iid=newid,values=(newid,firstname,lastname,naissance,telephone,address,correspondant,ncnam,client))
        chnom.delete(0,END)
        chprenom.delete(0,END)
        chtel.delete(0,END)
        chcnam.delete(0,END)
        chdate.delete(0,END)
        chaddress.delete(0,END)
        chcorresp.delete(0,END)
        chnclient.delete(0,END)
        chnom.focus()
        conn.close()
    else:
        messagebox.showerror("Erreur","Il faut entrer le prénom et le nom !")

newclient=Button(buttonsframe, text="Enregistrer la fiche",font=("Calibri",15), command=n_client)
newclient.grid(row=0,column=0,pady=10,padx=10)



def afficher():
    for record in tree.get_children():
        tree.delete(record)
    conn = sqlite3.connect('clients.db')
    c = conn.cursor()
    c.execute("SELECT * from customers")
    data = c.fetchall()
    for dt in data:
        c.execute("select id from customers where id='"+str(dt[0])+"'")
        newid=c.fetchall()[0][0];
        tree.insert(parent='', index="end", iid=newid,
                  values=(dt[0],dt[1], dt[2], dt[3], dt[4], dt[5], dt[6], dt[7],dt[8]))
    conn.commit()
    conn.close()

#modele de recherche client button
listeclients=Button(buttonsframe, text="Afficher la liste des clients",font=("Calibri",15),command=afficher)
listeclients.grid(row=0,column=1,pady=10,padx=10)

#nom
nompass=StringVar()
nom =Label(info, text="Nom :",font=("Times New Roman",20))
chnom= Entry(info,textvariable=nompass,width=17,font=("Calibri",18))
chnom.focus()

#prenom
prenompass=StringVar()
prenom = Label(info, text="Prénom :",font=("Times New Roman",20))
chprenom= Entry(info,textvariable=prenompass,width=17,font=("Calibri",18))

#date de naissance
datepass=StringVar()
date =Label(info, text="Date de naissance :",font=("Times New Roman",20))
chdate= Entry(info,textvariable=datepass,width=17,font=("Calibri",18))

#adresse
adrespass=StringVar()
adresse=Label(info,text="Adresse :",font=("Times New Roman",20))
chaddress= Entry(info,textvariable=adrespass,width=17,font=("Calibri",18))

#telephone
telpass=StringVar()
tel=Label(info, text="N° téléphone :",font=("Times New Roman",20))
chtel= Entry(info,textvariable=telpass,width=17,font=("Calibri",18))

#correspondant
correspass=StringVar()
corresp=Label(info, text="Correspondant :",font=("Times New Roman",20))
chcorresp= Entry(info,textvariable=correspass,width=17,font=("Calibri",18))

#cnam
cnampass=StringVar()
cnam=Label(info, text="CNAM :",font=("Times New Roman",20))
chcnam= Entry(info,textvariable=cnampass,width=17,font=("Calibri",18))

#numero client
nclientpass=StringVar()
nclient=Label(info, text="N° Dossier :",font=("Times New Roman",20))
chnclient= Entry(info,textvariable=nclientpass,width=17,font=("Calibri",18))

def remove():
    x=tree.focus()
    if len(x)==0:
        return
    response = messagebox.askokcancel("Supprimer client","Voulez vous vraiment supprimez ce client de la liste ?")
    if response == 1 :
        conn = sqlite3.connect('clients.db')
        c = conn.cursor()
        c.execute("delete from customers where id='"+str(tree.item(x)['values'][0])+"'")
        tree.delete(tree.item(x)['values'][0])
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


