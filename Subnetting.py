#subnetzmaske, ip adresse und cidr 
# -> nr subnetz, netid, bcid, anzahl hosts, anzahl subnetze, anzahl hosts insgesamt

from IP_v_4 import *
from tkinter import *
from functools import partial

#randomize erhält alle relevanten gui elemente und befüllt bei aufruf bedingt die gui mit neuer ip, cidr und subnetzmasken
def randomize(ipclasses, smmin, smmax, cidrmin, check1, check2, check3, entryip,entrysm,entrycidr):
    #ipclasses ist das gui object, wir holen uns also den darin enthaltenen wert mit .get()
    ipclass = ipclasses.get()
  
    #und passen danach den inhalt an für den später folgenden methodenaufruf rndIp(ipclass)
    #rndIp(arg) bekommt 'A' bis 'E', jedes andere Argument wird verworfen und die Ausgabe zufällig
    if ipclass=='Klasse A': ipclass='A'
    if ipclass=='Klasse B': ipclass='B'
    if ipclass=='Klasse C': ipclass='C'
    if ipclass=='Klasse D': ipclass='D'
    if ipclass=='Klasse E': ipclass='E'
    #wie bei ipclasses holen wir uns auch bei smmin und smmax erst den inhalt
    smin = smmin.get()
    smax = smmax.get()
    #fehlende eingabe wird als 0 bzw 32 gedeutet, die standardwerte von rndSM(min,max) bei fehlenden eingaben
    if smin=='': smin=0
    if smax=='': smax=32
    #die eingabe in die gui erfolgt als string, also machen wir hier erst noch int daraus
    smin=int(smin)
    smax=int(smax)
    #inhalt der 3 checkboxen, checkboxen enthalten 1 falls angekreuzt, 0 falls nicht.
    check1 = check1.get()
    check2 = check2.get()
    check3 = check3.get()
    #inhalt cidirmin, bei leerer eingabe wird cidrmin auf 0 gesetzt, den standardwert der methode rndCidr() 
    cidrmin = cidrmin.get()
    if cidrmin=='': cidrmin=0
    #inhalt entrycidr
    
    #falls die checkboxen nicht angekreuzt sind
    #lösch den inhalt in den gui elementen
    #und fülle sie mit neu generierten ip adressen / subnetzmasken / cidr 
    if check1!=1: 
        entryip.delete(0,END)
        entryip.insert(0,rndIp(ipclass))
    if check2!=1: 
        #falls wir cidr beibehalten wird cidr als mindestlänge für die subnetzmaske verwendet
        cidr = 0
        if check3!=0: 
            cidr = int(entrycidr.get())
        entrysm.delete(0,END)
        entrysm.insert(0,rndSM(smin,smax,cidr))
    if check3!=1: 
        entrycidr.delete(0,END)
        entrycidr.insert(0, rndcidr(entrysm.get(),cidrmin))
    return

#getanalyse erhält die gui elemente in denen der nutzer ip, cidr und subnetzmaske generiert hat
#und ruft mit diesen werten die methode analyzeGUI auf
#analyzeGUI gibt eine liste mit werten zurück die benutzt wird um das gui element frameAnalysis zu befüllen
def getanalyse(entryip,entrysm,entrycidr,frameAnalysis,frameTest):
    for x in frameAnalysis.grid_slaves():
        x.grid_forget()
    #werte aus den guielementen holen
    ip=entryip.get()
    subnetzmaske=entrysm.get()
    cidr =int(entrycidr.get())
    #methodenaufruf duh
    resultlist = analyzeGUI(ip,subnetzmaske,cidr)
    #resultliste enthält:
    #[0] bis [17] in dieser Reihenfolge: 
    #0 Titel "Netzwerkteil"
    #1 Inhalt Netzwerkteil
    #2 Titel "Subnetzteil"
    #3 Inhalt Subnetzteil
    #4 Titel "Hostteil"
    #5 Inhalt Hostteil
    #6 Titel "Netzwerk-ID"
    #7 Inhalt Netzwerk-ID
    #8 Titel "Broadcast-ID"
    #9 Inhalt Broadcast-ID
    #10 Titel "Nummer des Subnetzes:"
    #11 Inhalt Nummer des Subnetz + "-tes Subnetz"
    #12 Titel "Anzahl Subnetze"
    #13 Inhalt Anzahl Subnetze
    #14 Titel "Anzahl Hosts"
    #15 Inhalt Anzahl Hosts
    #16 Titel "Hosts insgesamt"
    #17 Inhalt Hosts insgesamt

    #leeres label als platzhalter
    Label(master=frameAnalysis, text='', anchor='w', width="32").grid(row=0,column=0)

    #durchläuft alle elemente der resultlist, startend bei row=1 column=0, row=1 column=1, row=2 column=0, usw. werden die elemente in labels eingepflegt
    for index, x in enumerate(resultlist, start=0):
            #column=index%2, column ist abwechselnd 0 und 1 
            #row=index-index%2+1
            Label(master=frameAnalysis, text=x, anchor='w', width=str(32+10*index%2)).grid(row=index-index%2+1,column=index%2)
    #und frameanalysis anschließend generiert
    frameTest.pack_forget()
    frameAnalysis.pack(fill=BOTH)
    return  

def gettest(entryip,entrysm,entrycidr,frameTest,frameAnalysis):
    for x in frameTest.grid_slaves():
        x.grid_forget()
    #werte aus den guielementen holen
    ip=entryip.get()
    subnetzmaske=entrysm.get()
    cidr =int(entrycidr.get())
    #methodenaufruf duh
    resultlist = analyzeGUI(ip,subnetzmaske,cidr)
    #resultliste enthält:
    #[0] bis [17] in dieser Reihenfolge: 
    #0 Titel "Netzwerkteil"
    #1 Inhalt Netzwerkteil
    #2 Titel "Subnetzteil"
    #3 Inhalt Subnetzteil
    #4 Titel "Hostteil"
    #5 Inhalt Hostteil
    #6 Titel "Netzwerk-ID"
    #7 Inhalt Netzwerk-ID
    #8 Titel "Broadcast-ID"
    #9 Inhalt Broadcast-ID
    #10 Titel "Nummer des Subnetzes:"
    #11 Inhalt Nummer des Subnetz + "-tes Subnetz"
    #12 Titel "Anzahl Subnetze"
    #13 Inhalt Anzahl Subnetze
    #14 Titel "Anzahl Hosts"
    #15 Inhalt Anzahl Hosts
    #16 Titel "Hosts insgesamt"
    #17 Inhalt Hosts insgesamt

    #leeres label als platzhalter
    Label(master=frameTest, text='', anchor='w', width="32").grid(row=0,column=0)

    #durchläuft alle elemente der resultlist, startend bei row=1 column=0, row=1 column=1, row=2 column=0, usw. werden die elemente in labels eingepflegt
    for index, x in enumerate(resultlist, start=0):
            #column=index%2, column ist abwechselnd 0 und 1 
            #row=index-index%2+1
            if index%2==0:Label(master=frameTest, text=x, anchor='w', width="32").grid(row=index-index%2+1,column=index%2)
            else:
                 temp = Entry(master=frameTest, width="42")
                 temp.grid(row=index-index%2+1,column=index%2)
    #und frameanalysis anschließend generiert
    
    frameAnalysis.pack_forget()
    frameTest.pack(fill=BOTH)
    return 

def getcheck(entryip,entrysm,entrycidr,frameAnalysis,frameTest):
    #werte aus den guielementen holen
    ip=entryip.get()
    subnetzmaske=entrysm.get()
    cidr =int(entrycidr.get())
    #methodenaufruf duh
    resultlist = analyzeGUI(ip,subnetzmaske,cidr)
    #resultliste enthält:
    #[0] bis [17] in dieser Reihenfolge: 
    #0 Titel "Netzwerkteil"
    #1 Inhalt Netzwerkteil
    #2 Titel "Subnetzteil"
    #3 Inhalt Subnetzteil
    #4 Titel "Hostteil"
    #5 Inhalt Hostteil
    #6 Titel "Netzwerk-ID"
    #7 Inhalt Netzwerk-ID
    #8 Titel "Broadcast-ID"
    #9 Inhalt Broadcast-ID
    #10 Titel "Nummer des Subnetzes:"
    #11 Inhalt Nummer des Subnetz + "-tes Subnetz"
    #12 Titel "Anzahl Subnetze"
    #13 Inhalt Anzahl Subnetze
    #14 Titel "Anzahl Hosts"
    #15 Inhalt Anzahl Hosts
    #16 Titel "Hosts insgesamt"
    #17 Inhalt Hosts insgesamt
    entrylist = [x for index, x in enumerate(frameTest.grid_slaves()) if type(x) is Entry]
    entrylist.reverse()
    resultlist = [x for index, x in enumerate(resultlist) if index%2==1]
    #print(entrylist)
    #print(resultlist)
    for index, x in enumerate(entrylist):
        if x.get()==resultlist[index]:
            x.configure(bg="green")
        else:
            x.configure(bg="red")

    return


def main():

    
    #Zufällige Eingabe
    
    # #_rndIp kann ohne Argument oder mit den Argumenten 'A','B',..,'E' aufgerufen werden. Andere Argumente werden behandelt wie kein Argument. 
    # ip = rndIp()

    # # #_rndSM() erzeugt eine zufällige Subnetzmaske zwischen 128.0.0.0 und 255.255.255.252
    # # #_rndSM(x) erzeugt eine zufällige Subnetzmaske wobei mindestens x bits 1 sind (von links an) x darf nur im Intervall [0,30] liegen
    # # #_rndSM(x,y) erzeugt eine zufällige Subnetzmaske mit mindestens x einsen (von links) und höchstens y einsen insgesamt
    # subnetzmaske = rndSM(9,11)

    # # #_rndcidr(subnetzmaske) erzeugt eine zufällige Zahl zwischen 1 und der länge der Subnetzmaske
    # # #_rndcidr(subnetzmaske,x) erzeugt eine zufällige Zahl zwischen x und der länge der Subnetzmaske
    # cidr = rndcidr(subnetzmaske,8)
    
    # print("------------------")
    # print(ip, "/" , cidr )
    # print(subnetzmaske)
    # print()
    # analyze(ip,subnetzmaske,cidr)
    # print()
    # print("------------------")

    #GUI

    window = Tk()
    window.title("Subnetting Tool By Marco Meyer")
    window.resizable(height = False, width = False)
    frameTop = Frame()
    frameMiddle = Frame()
    frameBottom = Frame()
    frameAnalysis = Frame()
    frameTest = Frame()
    #frameTop sind die Anzeigen der IP / Cidr und Subnetzmaske
    
    Label(master=frameTop, text="IP / CIDR:", anchor='w', width="12").grid(row=0, column=0)
    entryip = Entry(fg="black", bg="white", width=14, master=frameTop)
    entryip.insert(0, "192.168.178.187")
    entryip.grid(row=0,column=1)

    Label(master=frameTop, text="/").grid(row=0,column=2)
    entrycidr = Entry(fg="black", bg="white", width=2, master=frameTop)
    entrycidr.insert(0, "24")
    entrycidr.grid(row=0,column=3)

    Label(master=frameTop, text="",anchor='w', width="12").grid(row=0, column=4)
    Label(master=frameTop, text="Subnetzmaske:",anchor='w', width="12").grid(row=0, column=5)
    entrysm = Entry(fg="black", bg="white", width=14, master=frameTop)
    entrysm.insert(0, "255.255.255.255")
    entrysm.grid(row=0,column=6)

    frameTop.pack()

    #frameMiddle sind die Eingabemöglichkeiten

    Label(master=frameMiddle, text="IP-Adressen Klasse:",anchor='w', width="18").grid(row=0,column=0)
    options = ['Zufällig ','Klasse A', 'Klasse B', 'Klasse C', 'Klasse D', 'Klasse E']
    ipclass = StringVar(master=frameMiddle)
    ipclass.set(options[0]) #defaultwert leere Eingabe
    ipclasses = OptionMenu(frameMiddle, ipclass, *options)
    ipclasses.grid(row=0,column=1)

    Label(master=frameMiddle, text="IP-Adresse merken:", anchor='w', width="18").grid(row=1,column=0)
    check1 = IntVar()
    ipcheck = Checkbutton(frameMiddle, text="Ja", variable=check1, anchor='w', width='18')
    ipcheck.grid(row=1, column=1)

    Label(master=frameMiddle, text="Subnetzlänge:",anchor='w', width="18").grid(row=2,column=0)
    Label(master=frameMiddle, text="Min:",anchor='w', width="4").grid(row=2,column=1)
    smmin = Entry(fg="black", bg="white", width=14, master=frameMiddle)
    smmin.grid(row=2,column=2)
    Label(master=frameMiddle, text="Max:",anchor='w', width="4").grid(row=2,column=3)
    smmax = Entry(fg="black", bg="white", width=14, master=frameMiddle)
    smmax.grid(row=2,column=4)

    Label(master=frameMiddle, text="Subnetzmaske merken:", anchor='w', width="18").grid(row=3,column=0)
    check2 = IntVar()
    ipcheck = Checkbutton(frameMiddle, text="Ja", variable=check2, anchor='w', width='18')
    ipcheck.grid(row=3, column=1)

    Label(master=frameMiddle, text="CIDR Mindestlänge:",anchor='w', width="18").grid(row=4,column=0)
    cidrmin = Entry(fg="black", bg="white", width=14, master=frameMiddle)
    cidrmin.grid(row=4,column=1)

    Label(master=frameMiddle, text="CIDR merken:", anchor='w', width="18").grid(row=5,column=0)
    check3 = IntVar()
    cidrcheck = Checkbutton(frameMiddle, text="Ja", variable=check3, anchor='w', width='18')
    cidrcheck.grid(row=5, column=1)
    
    frameMiddle.pack()
    
    #frameBottom sind die 2 Knöpfe
    
    randomize2 = partial(randomize, ipclass, smmin, smmax, cidrmin, check1, check2, check3, entryip, entrysm, entrycidr)
    genButton = Button(frameBottom, command=randomize2, text="Randomize")
    genButton.grid(row=0,column=2)

    gettest2 = partial(gettest,entryip, entrysm, entrycidr,frameTest,frameAnalysis)
    testButton = Button(frameBottom, command=gettest2, text="Test")
    testButton.grid(row=0,column=3)

    getcheck2 = partial(getcheck,entryip,entrysm,entrycidr,frameAnalysis,frameTest)
    checkButton = Button(frameBottom, command=getcheck2, text="Check")
    checkButton.grid(row=0,column=4)

    getanalyse2 = partial(getanalyse,entryip, entrysm, entrycidr,frameAnalysis,frameTest)
    analButton = Button(frameBottom, command=getanalyse2, text="Solve")
    analButton.grid(row=0,column=5)
    
    frameBottom.pack()
    
    window.mainloop()

    #Eingabe in der Konsole

    #ip = input("Bitte IP und CIDR eingeben, z.B. 192.168.178.187 /24   _:")
    #subnetzmaske = input("Bitte Subnetzmaske eingeben, z.B. 255.255.255.128  _:")
    #ip von cidr trennen
    #temp = ip.split('/')
    #ip = temp[0]
    #cidr = int(temp[1])
    #print("------------------")
    #print("")
    #_analyze(ip,subnetzmaske,cidr)
    #print("")
    #print("------------------")

    #----------------

if __name__ == "__main__":
     main()

