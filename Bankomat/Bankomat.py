import tkinter as tk                
import time
import sqlite3
from tkinter import messagebox
import functools
import os

lozinka=0
broj_pokusaja=2
trenutno_stanje=0

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data={'Stanje':tk.IntVar()}
      
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Meni, Podizanje, Uplata, Stanje):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
                   
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#000066')
     
        self.controller = controller

        #Naslov
        self.controller.title('NLB Komercijalna banka ')
        self.controller.state('zoomed')
        self.controller.iconphoto(False,tk.PhotoImage(file='Slike/index.png'))

        hederLabela=tk.Label(self,text='Dobrodosli',font=('Arial',50, 'italic'), foreground='white',background='#000066')
        hederLabela.pack(pady=25)

        rastojanje= tk.Label(self,height=4,bg='#000066')
        rastojanje.pack()

        sifra=tk.Label(self,text='Unesite vas pin',font=('Arial',15, 'bold'), bg='#000066', fg='white')
        sifra.pack(pady=7)

        moja_sifra=tk.IntVar()
        moja_sifra.set("")
        
        sifra_polje=tk.Entry(self,textvariable=moja_sifra,font=('Arial',13),width=22)
        sifra_polje.focus_set()
        sifra_polje.pack(ipady=9)

        def zvezdice(_):
            sifra_polje.configure(fg='black',show='*')
        sifra_polje.bind('<FocusIn>',zvezdice)
        
       
        
        def provera():
            global broj_pokusaja
            if  broj_pokusaja>0:
                
                if moja_sifra.get()>0 and moja_sifra.get()<10000:
                    conn = sqlite3.connect('baza.db')
                    c=conn.cursor()
                    query="SELECT pin from Banka Where pin ="+str(moja_sifra.get())
                    c.execute(query)
                    provera=c.fetchone()
                    conn.commit()
                    conn.close()
                    
                    if provera:
                        global lozinka
                        lozinka = moja_sifra.get()                    
                        controller.show_frame('Meni')
                        moja_sifra.set("")
                        los_unos['text']=""
                        
                    else:
                        los_unos['text']='Pogresan pin, ostalo vam je '+ str(broj_pokusaja)+ ' pokusaja'
                        moja_sifra.set("")
                        broj_pokusaja-=1
                       
                else:
                    los_unos['text']='Pogresan pin, ostalo vam je '+ str(broj_pokusaja)+ ' pokusaja'
                    moja_sifra.set("")
                    broj_pokusaja-=1
            else:
                messagebox.showwarning('NLB Komercijalna banka', 'Preostalo vam je 0 pokusaja molimo Vas izadjite iz aplikacije')
                sifra_polje.config(state='disabled')
                los_unos['text']='Nemate vise pokusaja'
                moja_sifra.set("")
                
        dugme_unos=tk.Button(self,text='Unesi',command=provera, relief='ridge', borderwidth=4,width=27,height=3)
        dugme_unos.pack(pady=10)

        los_unos=tk.Label(self, text="", font=('Arial',15), fg='white',bg='#9933ff', anchor='n')
        los_unos.pack(fill='both',expand=True)

        donji_f=tk.Frame(self,relief='raised',borderwidth=3)
        donji_f.pack(fill='x', side='bottom')

        visa_s=tk.PhotoImage(file='Slike/visa.png')
        visa_l=tk.Label(donji_f,image=visa_s)
        visa_l.pack(side='left')
        visa_l.image=visa_s

        master_s=tk.PhotoImage(file='Slike/maestro.png')
        master_l=tk.Label(donji_f,image=master_s)
        master_l.pack(side='left')
        master_l.image=master_s
        
        def vreme():
            trenutno_v= time.strftime('%I:%M %p')
            vreme_l.config(text=trenutno_v)
            vreme_l.after(200,vreme)
            
            
        vreme_l=tk.Label(donji_f,font=('Arial',12))
        vreme_l.pack(side='right')
        vreme()


class Meni(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#000066')
        self.controller = controller
        self.frames = {}
       

        hederLabela=tk.Label(self,text='NLB bankomat',font=('Arial',50, 'italic'), foreground='white',background='#000066')
        hederLabela.pack(pady=25)

        meni_l=tk.Label(self,text="Glavni meni",font=('Arial',20,'bold'),fg='white',bg='#000066')
        meni_l.pack()

        opcije_l=tk.Label(self,text="Izaberite opciju", font=("Arial",13,'bold'), fg="white", bg='#000066',anchor='w')
        opcije_l.pack(fill='x')
        
        def prikaz_stanja():
            global lozinka
            conn = sqlite3.connect('baza.db')
            c=conn.cursor()
            Query="SELECT Stanje from Banka WHERE Pin="+str(lozinka)            
            c.execute(Query)  
            trenutno_stanje= str(c.fetchone()[0])
            controller.shared_data['Stanje'].set(trenutno_stanje)
            conn.commit()
            conn.close()

        
        dugmad_f=tk.Frame(self, bg='#9933ff')
        dugmad_f.pack(fill='both',expand=True)
        
        def podizanje():
            controller.show_frame("Podizanje")
        dugme_podizanje=tk.Button(dugmad_f,text="Podizanje", command=podizanje, relief="raised",borderwidth=3,width=50,height=5)
        dugme_podizanje.grid(row=0, column=0,pady=5)

        def uplata():
            controller.show_frame("Uplata")
        dugme_uplata=tk.Button(dugmad_f,text="Uplata", command=uplata, relief="raised"
                               ,borderwidth=3,width=50,height=5)
        dugme_uplata.grid(row=1, column=0,pady=5)

        def stanje():
            controller.show_frame("Stanje")
        dugme_stanje=tk.Button(dugmad_f,text="Prikaz stanja", command=lambda:[stanje(),prikaz_stanja()], relief="raised",borderwidth=3,width=50,height=5)
        dugme_stanje.grid(row=2, column=0,pady=5)

        def izlaz():
            controller.show_frame("StartPage")
        dugme_izlaz=tk.Button(dugmad_f,text="Nazad", command=izlaz, relief="raised",borderwidth=3,width=50,height=5)
        dugme_izlaz.grid(row=3, column=0,pady=5)
        

        donji_f=tk.Frame(self,relief='raised',borderwidth=3)
        donji_f.pack(fill='x', side='bottom')

        visa_s=tk.PhotoImage(file='Slike/visa.png')
        visa_l=tk.Label(donji_f,image=visa_s)
        visa_l.pack(side='left')
        visa_l.image=visa_s

        master_s=tk.PhotoImage(file='Slike/maestro.png')
        master_l=tk.Label(donji_f,image=master_s)
        master_l.pack(side='left')
        master_l.image=master_s
        
        def vreme():
            trenutno_v= time.strftime('%I:%M %p')
            vreme_l.config(text=trenutno_v)
            vreme_l.after(200,vreme)
               
        vreme_l=tk.Label(donji_f,font=('Arial',12))
        vreme_l.pack(side='right')
        vreme()
     


class Podizanje(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#000066')
        self.controller = controller

        hederLabela=tk.Label(self,text='NLB bankomat',font=('Arial',50, 'italic'), foreground='white',background='#000066')
        hederLabela.pack(pady=25)

        iznos_l=tk.Label(self,text="Izaberite iznos koji zelite da podignete",font=('Arial',20,'bold'),fg='white',bg='#000066')
        iznos_l.pack()

        dugmad_f=tk.Frame(self, bg='#9933ff')
        dugmad_f.pack(fill='both',expand=True)

        #baza je potrebna- gotovo
        def podizanje(iznos):
            global lozinka
            global trenutno_stanje
            conn = sqlite3.connect('baza.db')
            c=conn.cursor()
            c.execute("SELECT Stanje FROM Banka where Pin =? ",(lozinka,))
            trenutno_stanje=functools.reduce(lambda sub, ele: sub * 10 + ele, c.fetchone())
            
            
            if iznos> trenutno_stanje:
                messagebox.showwarning('NLB Komercijalna banka', 'Nemate dovoljno novca na racunu')
            else:
                
                trenutno_stanje-=iznos
                controller.shared_data['Stanje'].set(trenutno_stanje)
                controller.show_frame('Meni')
                c.execute('Update Banka SET Stanje=? WHERE Pin=?',(trenutno_stanje,lozinka))
                conn.commit()
                conn.close()
       
        petsto=tk.Button(dugmad_f,text='500',command=lambda:podizanje(500), relief='raised',borderwidth=5,width=70,height=7)
        petsto.grid(row=0,column=0,pady=5)

        hiljadu=tk.Button(dugmad_f,text='1000',command=lambda:podizanje(1000), relief='raised',borderwidth=5,width=70,height=7)
        hiljadu.grid(row=1,column=0,pady=5)

        dve_hiljade=tk.Button(dugmad_f,text='2000',command=lambda:podizanje(2000), relief='raised',borderwidth=5,width=70,height=7)
        dve_hiljade.grid(row=2,column=0,pady=5)

        pet_hiljada=tk.Button(dugmad_f,text='5000',command=lambda:podizanje(5000), relief='raised',borderwidth=5,width=70,height=7)
        pet_hiljada.grid(row=0,column=1,pady=5,padx=350)

        deset_hiljada=tk.Button(dugmad_f,text='10000',command=lambda:podizanje(10000), relief='raised',borderwidth=5,width=70,height=7)
        deset_hiljada.grid(row=1,column=1,pady=5)

        def izlaz():
            controller.show_frame("Meni")
        dugme_stanje=tk.Button(dugmad_f,text="Nazad", command=izlaz, relief="raised",borderwidth=5,width=70,height=7)
        dugme_stanje.grid(row=3, column=0,pady=5)
        
        novac=tk.StringVar()
       
        proizvoljan_unos=tk.Entry(dugmad_f,textvariable=novac,width=85,justify='right')
        proizvoljan_unos.grid(row=2,column=1,pady=5,ipady=50)
        
        def pr_unos(_):
            if int(novac.get())%500 == 0:
                global trenutno_stanje
                conn = sqlite3.connect('baza.db')
                c=conn.cursor()
                c.execute("SELECT Stanje FROM Banka where Pin =? ",(lozinka,))
                trenutno_stanje=functools.reduce(lambda sub, ele: sub * 10 + ele, c.fetchone())
                controller.shared_data['Stanje'].set(trenutno_stanje)
                trenutno_stanje-=int(novac.get())
                c.execute('Update Banka SET Stanje=? WHERE Pin=?',(trenutno_stanje,lozinka))
                conn.commit()
                conn.close()
                controller.show_frame('Meni')
                novac.set('')
            else:
                messagebox.showwarning('NLB Komercijalna banka', 'Molim Vas unesite broj koji je deljiv sa 500')
                novac.set('')
                
        proizvoljan_unos.bind('<Return>',pr_unos)#
        

        donji_f=tk.Frame(self,relief='raised',borderwidth=3)
        donji_f.pack(fill='x', side='bottom')

        visa_s=tk.PhotoImage(file='Slike/visa.png')
        visa_l=tk.Label(donji_f,image=visa_s)
        visa_l.pack(side='left')
        visa_l.image=visa_s

        master_s=tk.PhotoImage(file='Slike/maestro.png')
        master_l=tk.Label(donji_f,image=master_s)
        master_l.pack(side='left')
        master_l.image=master_s
        
        def vreme():
            trenutno_v= time.strftime('%I:%M %p')
            vreme_l.config(text=trenutno_v)
            vreme_l.after(200,vreme)
               
        vreme_l=tk.Label(donji_f,font=('Arial',12))
        vreme_l.pack(side='right')
        vreme()

        
        
class Uplata(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#5900b3')
        self.controller = controller

        hederLabela=tk.Label(self,text='NLB bankomat',font=('Arial',50, 'italic'), foreground='white',background='#5900b3')
        hederLabela.pack(pady=25)

        rastojanje= tk.Label(self,height=4,bg='#5900b3')
        rastojanje.pack()

        iznos_uplate=tk.Label(self,text='Unesite iznos',font=('Arial',15, 'bold'), bg='#5900b3', fg='white')
        iznos_uplate.pack(pady=7)
        
        novac=tk.StringVar()
        iznos=tk.Entry(self,textvariable=novac,font=('Arial',15),width=22)
        iznos.pack(ipady=5)
        
        def uplata_novca():
            
            conn = sqlite3.connect('baza.db')
            c=conn.cursor()
            c.execute("SELECT Stanje FROM Banka where Pin =? ",(lozinka,))
            trenutno_stanje=functools.reduce(lambda sub, ele: sub * 10 + ele, c.fetchone())
            trenutno_stanje+=int(novac.get())
            controller.shared_data['Stanje'].set(trenutno_stanje)
            c.execute('Update Banka SET Stanje=? WHERE Pin=?',(trenutno_stanje,lozinka))
            conn.commit()
            conn.close()
            controller.show_frame('Meni')
            novac.set('')
            
        iznos_d=tk.Button(self,text='Unesite iznos koji zelite da uplatite',command=uplata_novca,
                          relief='raised',borderwidth=3,width=30,height=3)
        iznos_d.pack(pady=5)

        donji_f=tk.Frame(self,relief='raised',borderwidth=3)
        donji_f.pack(fill='x', side='bottom')

        visa_s=tk.PhotoImage(file='Slike/visa.png')
        visa_l=tk.Label(donji_f,image=visa_s)
        visa_l.pack(side='left')
        visa_l.image=visa_s

        master_s=tk.PhotoImage(file='Slike/maestro.png')
        master_l=tk.Label(donji_f,image=master_s)
        master_l.pack(side='left')
        master_l.image=master_s
        
        def vreme():
            trenutno_v= time.strftime('%I:%M %p')
            vreme_l.config(text=trenutno_v)
            vreme_l.after(200,vreme)
               
        vreme_l=tk.Label(donji_f,font=('Arial',12))
        vreme_l.pack(side='right')
        vreme()

        
        
class Stanje(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#000066')
        self.controller = controller
        global trenutno_stanje
        
        
        
        hederLabela=tk.Label(self,text='NLB bankomat',font=('Arial',50, 'italic'), foreground='white',background='#000066')
        hederLabela.pack(pady=25)
        

        stanje_l=tk.Label(self,textvariable=controller.shared_data['Stanje'],font=('Arial',20),fg='white',bg='#000066',anchor='w')
        stanje_l.pack(fill='x')

        def Izlaz():
            controller.show_frame('StartPage')
            global trenutno_stanje
            trenutno_stanje=0
            controller.shared_data['Stanje'].set(trenutno_stanje)

        def meni():
             controller.show_frame('Meni')
             
        dugmad_f=tk.Frame(self, bg='#9933ff')
        dugmad_f.pack(fill='both',expand=True)
        
        dugme1=tk.Button(dugmad_f,command=meni,text='Meni',relief='raised',borderwidth=3,width=50,height=5)
        dugme1.grid(row=0,column=0,pady=5)
    
        dugme2=tk.Button(dugmad_f,command=Izlaz,text='Izlaz',relief='raised',borderwidth=3,width=50,height=5)
        dugme2.grid(row=1,column=0,pady=5)


        

             

        donji_f=tk.Frame(self,relief='raised',borderwidth=3)
        donji_f.pack(fill='x', side='bottom')

        visa_s=tk.PhotoImage(file='Slike/visa.png')
        visa_l=tk.Label(donji_f,image=visa_s)
        visa_l.pack(side='left')
        visa_l.image=visa_s

        master_s=tk.PhotoImage(file='Slike/maestro.png')
        master_l=tk.Label(donji_f,image=master_s)
        master_l.pack(side='left')
        master_l.image=master_s
        
        def vreme():
            trenutno_v= time.strftime('%I:%M %p')
            vreme_l.config(text=trenutno_v)
            vreme_l.after(200,vreme)
               
        vreme_l=tk.Label(donji_f,font=('Arial',12))
        vreme_l.pack(side='right')
        vreme()
          


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()






