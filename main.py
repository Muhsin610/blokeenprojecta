import tkinter.ttk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import psycopg2
import datetime
import random
import time
import locale
import math
import requests
import atexit

# Hier maken we een connectie met de database
hostname = 'localhost'
database = 'projectA'
username = 'postgres'
pwd = 'Trabzon6161_'
port_id = 5432
conn = psycopg2.connect(
    host=hostname,
    dbname=database,
    user=username,
    password=pwd,
    port=port_id)
cur = conn.cursor()

###############################################
# GUI
###############################################


# We veranderen met locale.setlocale de datumvolgorde van Engels naar het Nederlandse versie.
locale.setlocale(locale.LC_TIME, "nl_NL")

# Variabele voor datum en tijd aanmaken
now = datetime.datetime.now()
current_time= now.strftime("%H:%M:%S")

stations = ["Utrecht", "Amsterdam", "Den Haag"]
# Random choice tussen de stations
rand = random.choice(stations)


# Als er geen naam wordt ingevoerd, wordt er 'anoniem' meegegeven als naam.
def lees_naam():
    if naam.get():
        return naam.get()
    else:
        return "anoniem"


# Functie gemaakt om connectie met SQL in 1x te closen aan het eind
def exit_handler():
    conn.close()
    print('Connection has been closed!')


def verzenden():
    # Je krijgt een aparte bericht met dat je bericht is verzonden en in behandeling is.
    messagebox.showinfo("Hallo " + lees_naam(), "Uw feedback is in behandeling.")
    # Nadat je op verzenden heb geklikt word je bericht en je naam in de database toegevoegd
    cur.execute("""INSERT INTO bericht(naam,  tekst, datum, tijd, stationNaam) VALUES(%s, %s, %s, %s, %s)""",
                (lees_naam(), feedback.get('1.0', 'end-1c'), now, now, rand))
    conn.commit()
    naam.delete(0, END)
    feedback.delete("1.0", "end")


def login():
    # Dit is de inlogapgina van de moderator, hier kan de moderator zijn wachtwoord en gebruikersnaam invoeren
    root = Tk()
    root.title("~~Moderator login~~")
    root.geometry("500x150")
    root.configure(bg="blue")
    label = Label(master=root, text="Welkom, \nlogt u in alstublieft", width=37, bg="blue", fg="white",
                  font=("Helvetica", 14))
    label.grid(row=0, column=0, columnspan=2)
    label0 = Label(master=root, text='gebruikersnaam:', bg="blue", fg="white", font=("Helvetica", 14))
    label0.grid(row=1, column=0)
    gebruikersnaam = Entry(root, width=20, bg="yellow", fg="black", font=("Helvetica", 14))
    gebruikersnaam.grid(row=1, column=1)
    gebruikersnaam.get()
    label1 = Label(master=root, text="   ", bg="blue", font=("Helvetica", 14))
    label1.grid(row=1, column=3)
    label2 = Label(master=root, text='wachtwoord:', bg="blue", fg="white", font=("Helvetica", 14))
    label2.grid(row=2, column=0)
    parola = Entry(master=root, width=20, show="*", bg="yellow", fg="black", font=("Helvetica", 14))
    parola.grid(row=2, column=1)
    parola.get()

    def ingelogd():
        # Als je bent ingelogd controleert het of je gebruikersnaam en wachtwoord met de variabele naam en wachtwoord hieronder overeenkomen en vervolgens krijg je dan de moderatorpagina te zien waar je berichten kunt toelaten of verwijderen
        naam = 'muhsin.kan@student.hu.nl'
        wachtwoord = '0000'
        if gebruikersnaam.get() == naam and parola.get() == wachtwoord:
            # Hier krijg je een nieuwe window, de moderatorspagina, hier kun je berichten goed- of afkeuren
            root = Tk()
            root.state('zoomed')
            root.title("~Moderator pagina~")
            root.geometry("1250x350")
            root.configure(bg="blue")

            style = tkinter.ttk.Style(root)
            style.theme_use("clam")
            style.configure("Treeview", background="white",
                            fieldbackground="yellow", foreground="black")

            def update(rows):
                for i in rows:
                    trv.insert('', 'end', values=i)

            cur = conn.cursor()
            # Treeview wordt aangemaakt om de gegevens daarin toe te voegen, je kan het zien als een soort lijst met gegevens erin
            trv = ttk.Treeview(root, selectmode='browse', height=20)
            trv.pack(pady=100)
            trv["columns"] = ("1", "2", "3")
            trv["show"] = 'headings'
            trv.column("1", width=100, anchor='c')
            trv.column("2", width=100, anchor="c")
            trv.column("3", width=1000, anchor="c")
            trv.heading("1", text="ID")
            trv.heading("2", text="naam")
            trv.heading("3", text="bericht")
            query = """SELECT bericht_id, naam, tekst  FROM bericht order by bericht_id """
            cur.execute(query)


            def stationshalscherm():
                # Hier wordt het stationshalscherm getoond, met recente tijd, live weer,datum, faciliteiten en 5 laatste berichten met de namen
                root = Tk()
                root.title("~~Stationshalscherm~~")
                root.state('zoomed')

                root.configure(bg= 'blue')

                def update(rows):
                    for i in rows:
                        trv.insert('', 'end', values=i)

                cityname = "Utrecht,NL"
                api_key = 'e3ab4f9f02395b08dbf8c125f322443f'

                def getweather(api_key, city):
                    #Je krijgt de live weer met behulp van te verbonden zijn met het api key van het weerapplicatie
                    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

                    response = requests.get(url).json()

                    temp = response['main']['temp']
                    temp = math.floor((temp) - 273.15)

                    return temp

                weather = getweather(api_key, cityname)

                def display_city_name(city):
                    city_label = Label(root, text=f"{cityname}", bg= "blue", fg="white")
                    city_label.config(font=("Consolas", 28))
                    city_label.grid(row=1, column=1)

                def display_stats(weather, temp):
                    temp = Label(root, text=f"Temperatuur: {temp} C", bg= "blue", fg="white")
                    temp.config(font=("Consolas", 22))
                    temp.grid(row=2, column=1)

                display_city_name(cityname)
                temp = getweather(api_key, cityname)
                display_stats(weather, temp)

                def klok1():
                    #We maken voor de label een recente tijd aan, zo kan dat getoond worden op het scherm
                    hour = time.strftime("%H")
                    minute = time.strftime("%M")
                    second = time.strftime("%S")

                    tijd.config(text=hour + ":" + minute + ":" + second)
                    tijd.after(1000, klok1)

                def tarih1():
                    #Zelfde net als hierboven maar dan in datum
                    datum = time.strftime("%A %d %B %Y")

                    myDate.config(text=datum)
                    myDate.after(1000, tarih1)

                tijd = Label(root, text="", font=("Helvetica", 20), bg= "blue", fg="white")
                tijd.grid(row=3, column=1)

                myDate = Label(root, text="", font=("Helvetica", 20), bg= "blue", fg="white")
                myDate.grid(row=4, column=1)

                klok1()
                tarih1()

                style = tkinter.ttk.Style(root)
                style.theme_use("clam")
                style.configure("Treeview", background="white",
                                fieldbackground="yellow", foreground="black")

                trv = ttk.Treeview(root, selectmode='browse', height=8)
                trv.grid(row=5, column=1, pady=40, padx=40)
                trv["columns"] = ("1", "2", "3")
                trv["show"] = 'headings'
                trv.column("1", width=700, anchor='c')
                trv.column("2", width=180, anchor="c")
                trv.column("3", width=180, anchor="c")
                trv.heading("1", text="bericht")
                trv.heading("2", text="naam")
                trv.heading("3", text="Station")
                # Hier wordt laatste 5 berichten geselecteerd
                query0 = """select tekst, naam, stationNaam from alleBericht where goedOfAfgekeurd='goed gekeurd' order by bericht_id desc limit 5"""
                cur.execute(query0)
                rows = cur.fetchall()
                update(rows)
                conn.commit()

                def faciliteiten():

                    ### Utrecht faciliteiten ###

                    #Hier selecteren we gegevens van onze database zodat we informatie kunnen laten zien over de facilitieiten op het stationshalscherm.

                    cur.execute("""select naam from station where id = 1""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script0_label = Label(root, text=f"{r}:", bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script0_label.grid(row=6, column=0)

                    cur.execute("""select aantal from voorziening where id = 1""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script1_label = Label(root, text=f'Er zijn zoveel liften: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script1_label.grid(row=7, column=0)

                    cur.execute("""select aantal from voorziening where id = 2""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script2_label = Label(root, text=f'Er zijn zoveel OV-fietsen: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script2_label.grid(row=8, column=0)

                    cur.execute("""select aantal from voorziening where id = 3""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script3_label = Label(root, text=f'Er zijn zoveel toiletten: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script3_label.grid(row=9, column=0)

                    cur.execute("""select aantal from voorziening where id = 4""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script4_label = Label(root, text=f'Er zijn zoveel Park and Ride: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script4_label.grid(row=10, column=0)

                    ### Amsterdam faciliteiten ###

                    cur.execute("""select naam from station where id = 2""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script5_label = Label(root, text=f"{r}:", bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script5_label.grid(row=6, column=1)

                    cur.execute("""select aantal from voorziening where id = 5""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script6_label = Label(root, text=f'Er zijn zoveel liften: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script6_label.grid(row=7, column=1)

                    cur.execute("""select aantal from voorziening where id = 6""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script7_label = Label(root, text=f'Er zijn zoveel OV-fietsen: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script7_label.grid(row=8, column=1)

                    cur.execute("""select aantal from voorziening where id = 7""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script8_label = Label(root, text=f'Er zijn zoveel toiletten: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script8_label.grid(row=9, column=1)

                    cur.execute("""select aantal from voorziening where id = 8""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script9_label = Label(root, text=f'Er zijn zoveel Park and Ride: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script9_label.grid(row=10, column=1)

                    ### Den Haag faciliteiten ###

                    cur.execute("""select naam from station where id = 3""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script10_label = Label(root, text=f"{r}:", bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script10_label.grid(row=6, column=2)

                    cur.execute("""select aantal from voorziening where id = 9""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script11_label = Label(root, text=f'Er zijn zoveel liften: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script11_label.grid(row=7, column=2)

                    cur.execute("""select aantal from voorziening where id = 10""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script12_label = Label(root, text=f'Er zijn zoveel OV-fietsen: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script12_label.grid(row=8, column=2)

                    cur.execute("""select aantal from voorziening where id = 11""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script13_label = Label(root, text=f'Er zijn zoveel toiletten: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script13_label.grid(row=9, column=2)

                    cur.execute("""select aantal from voorziening where id = 12""")
                    rows = cur.fetchall()
                    for r in rows[0]:
                        select_script14_label = Label(root, text=f'Er zijn zoveel Park and Ride: {r}', bg= "blue", fg="white", font=("Helvetica", 10))
                        select_script14_label.grid(row=10, column=2)

                faciliteiten()
                root.mainloop()

            def doorgeven(trv):
                # Hier wordt doorgegeven dat een bericht is goed gekeurd

                selectedItem = trv.selection()[0]


                uid = trv.item(selectedItem)['values'][0]
                query5 = f"""UPDATE bericht SET goedOfAfgekeurd = 'goed gekeurd', tijdBeoordeling = '{current_time}' WHERE bericht_id=%s"""
                query6 = """select * from bericht;
                                            select * from alleBericht;
                                            insert into alleBericht
                                            select bericht_id, naam, tekst, datum, tijd, goedOfAfgekeurd, tijdBeoordeling, stationNaam
                                            from bericht where bericht.bericht_id=%s"""
                query7 = """DELETE FROM bericht WHERE bericht_id=%s"""

                sel_data = (uid,)
                cur.execute(str(query5), sel_data)
                cur.execute(str(query6), sel_data)
                cur.execute(str(query7), sel_data)

                conn.commit()
                trv.delete(selectedItem)

                conn.commit()
            def delete(trv):

                # Als de moderator op verwijderen klikt dan wordt de bericht_id verwijdert uit de database

                selectedItem = trv.selection()[0]
                uid=trv.item(selectedItem)['values'][0]
                query8 = f"""UPDATE bericht SET goedOfAfgekeurd = 'afgekeurd', tijdBeoordeling = '{current_time}' WHERE bericht_id=%s"""
                query9 = """select * from bericht;
                            select * from alleBericht;
                            insert into alleBericht
                            select bericht_id, naam, tekst, datum, tijd, goedOfAfgekeurd, tijdBeoordeling, stationNaam
                            from bericht where bericht.bericht_id=%s"""
                query10 = """DELETE FROM bericht WHERE bericht_id=%s"""

                sel_data=(uid,)
                cur.execute(str(query8), sel_data)
                cur.execute(str(query9), sel_data)
                cur.execute(str(query10), sel_data)
                conn.commit()
                trv.delete(selectedItem)

            # Hier kan je aangeven met entry's en knoppen welke gegevens je wilt wijzigen, verwijderen, goedkeuren of afkeuren
            buttonAfgekeurd = Button(root, text="Afgekeurd", bg="red", command=lambda: delete(trv))
            buttonAfgekeurd.place(x=700, y=560)
            buttonGoedGekeurd = Button(root, text="Goed keuren", bg="green", command=lambda: doorgeven(trv))
            buttonGoedGekeurd.place(x=800, y=560)
            gui = Button(root, text="Stationshalscherm", command=stationshalscherm, bg="yellow")
            gui.place(x=725, y=600)
            rows = cur.fetchall()
            update(rows)
            conn.commit()

            root.mainloop()
        else:
            # Als het wachtwoord of gebruikersnaam niet correct is dan krijg je een aparte error melding.
            messagebox.showerror(title="Error",
                                 message="U heeft de verkeerde Gebruikersnaam of password ingevoerd, probeer het opnieuw alstublieft.")

    def showPassword():
        # Hier wordt de wachtwoord verborgen met sterren
        if parola.cget("show") == "*":
            parola.config(show="")
        else:
            parola.config(show="*")

    # Je kun het vinkje 'show password' aanvinken en je wachtwoord zien in letters en cijfers
    vinkje = Checkbutton(root, text="show password", command=showPassword, bg="yellow")
    vinkje.place(x=260, y=107)
    inloggen = Button(master=root, text="inloggen", command=ingelogd, bg="yellow")
    inloggen.grid(row=3, column=0, columnspan=2)
    root.mainloop()

def klok():
    # Hier maken we de functie voor recente tijd
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")

    myLabel.config(text=hour + ":" + minute + ":" + second)
    myLabel.after(1000, klok)


def tarih():
    # Hier maken we de functie voor recente datum
    datum = time.strftime("%A %d %B %Y")

    myLabel1.config(text=datum)
    myLabel1.after(1000, tarih)


# Mensen kunnen bij deze applicatie/window hun feedback invoeren.
root = Tk()
root.title(f"~~Geef uw mening over station: {rand}~~")

root.state('zoomed')

bg = PhotoImage(file="img.png")
bg = bg.zoom(2)

my_label = Label(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

myLabel = Label(root, text="", font=("Helvetica", 20), fg="yellow", bg="#0000CE")
myLabel.pack(pady=20)

myLabel1 = Label(root, text="", font=("Helvetica", 20), fg="yellow", bg="#0000CE")
myLabel1.pack(pady=10)

klok()
tarih()

station = Label(master=root, text="Welkom bij station: " + rand, font=("Helvetica", 20), fg="yellow", bg="#0000CE")
station.pack(pady=20)

label = Label(master=root, text='Wat vond u van het station?', font=("Helvetica", 14), fg="yellow", bg="#0000CE")
label.pack(pady=10)

label = Label(master=root, text='Vul hieronder uw bericht in alstublieft: ', font=("Helvetica", 14), fg="yellow",
              bg="#0000CE")
label.pack()

feedback = Text(master=root, bg="yellow", fg="blue", font=("Helvetica", 20), width=40, height=5)
feedback.pack(padx=10, pady=10)
feedback.get('1.0', 'end-1c')
l2 = Label(root, text=0, fg="yellow", bg="#0000CE", font=("Helvetica", 12))
l2.pack()

def root_upd(value):
    # Hier wordt de karakters bijgehouden van het bericht, als het meer dan 140 zijn verwijdert het de overige letters
    root__str = feedback.get('1.0', 'end-1c')
    breaks = root__str.count('\n')
    char_numbers = len(root__str) - breaks
    l2.config(text=str(char_numbers))
    if (char_numbers > 139):
        feedback.delete('end-2c')

feedback.bind('<KeyRelease>', root_upd)

label = Label(master=root, text='Vul hieronder uw naam in alstublieft:', font=("Helvetica", 14), fg="yellow",
              bg="#0000CE", height=1)
label.pack(pady=5)

naam = Entry(master=root, width=20, bg="yellow", justify=CENTER, font=("Helvetica", 14))
naam.pack(padx=10, pady=10)
naam.get()

button = Button(master=root, text='Verzenden', command=verzenden, bg="yellow")
button.pack(pady=10)
#
login()

conn.commit()
root.mainloop()

atexit.register(exit_handler)