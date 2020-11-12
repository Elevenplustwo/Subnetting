import random

def rndIp(arg=None): #generiert eine zufällige IPv4 Adresse
    cl = arg #cl steht für class/Klasse der zu generierenden IP Adresse
             #Akzeptable Eingaben sind A,B,C,D,E oder keine Eingabe

    ip1 = random.random()*256 #bei ungültigen Eingaben wird ip1 einfach zufällig generiert 
    if(cl==None): ip1 = random.random()*256
    if(cl=='A'): ip1 = random.random()*128
    if(cl=='B'): ip1 = 128+random.random()*64
    if(cl=='C'): ip1 = 192+random.random()*32
    if(cl=='D'): ip1 = 224+random.random()*16
    if(cl=='E'): ip1 = 240+random.random()*16     
      
    ip2, ip3, ip4 = random.random()*256,random.random()*256,random.random()*256
    res = str(int(ip1)) + '.' + str(int(ip2)) + '.' + str(int(ip3)) + '.' + str(int(ip4))
    return res

#Die Argumente min bzw. max legen die minimale bzw. maximale Länge der zufällig generierten Subnetzmaske fest
def rndSM(minimum=0, maximum=32, cidr=None): #generiert eine zufällige Subnetzmaske
    #seed als zufallszahl zwischen 1 und 31 für die anzahl der 1 in der subnetzmaske
    if cidr!=None: minimum=max(minimum,cidr)
    if maximum==32 or maximum==31: seed= minimum+int(random.random()*(31-minimum)) 
    else: seed = minimum+int(random.random()*(33-minimum-(32-maximum)))
    #generieren der Einsen
    res = '1'*seed
    #generieren der Nullen
    while int(len(res))<32:
        res = res + '0'
    #einfügen der trennenden Punkte  
    res = res[:8] + '.' + res[8:16] + '.' + res[16:24] + '.' + res[24:]   
    #umrechnen in Dezimal und ausgabe
    res = ip2dec(res)
    #subnetzmaske 0.0.0.0 cidr 1 schmeißt nen fehler, also gibts das nicht mehr, keine lust den fehler zu suchen
    if res == "0.0.0.0": 
        res = rndSM()
    return res

def rndcidr(subnetzmaske, minlength=0): #generieren einer beliebiegen cidr nummer kleiner oder gleich der subnetzmaske
    subnetzlänge = len(''.join((filter(lambda i: i != '0' and i != '.', ip2bin(subnetzmaske)))))
    cidr = minlength+int(random.random()*(subnetzlänge+1-minlength))
    return cidr

def dec2bin(arg): #erweiterung der nativen bin() methode
    x = bin(arg)[2:] #bin gibt standardmäßig ein 0b vor den Zahlenwert, das entfernen wir hier
    while len(x)<8:
        x = '0'+ x #fügt führende nullen hinzu bis wir 8 stellen haben
    return x

def bin2dec(arg): #ausm internet geklaut, macht aus binär dezimal 
    decimal, i, n = 0, 0, 0
    while(arg != 0): 
        dec = arg % 10
        decimal = decimal + dec * pow(2, i)
        arg = arg//10
        i += 1
    return decimal

def ip2bin(arg):#ip von binär zu dezimal
    res = arg.split(".") #trennt die ip in eine liste von 4 elementen 
    res = [dec2bin(int(x)) for x in res] #jedes element der liste wird von einer dezimalzahl in eine binärzahl umgewandelt
    res = res[0] + '.' + res[1] + '.' + res[2] + '.' + res[3] #aus der liste wird wieder eine ip
    return res

def ip2dec(arg):#ip von binär zu dezimal
    res = arg.split(".") #trennt die ip in eine liste von 4 elementen 
    res = [bin2dec(int(x)) for x in res] #jedes element der liste wird von einer binärzahl in eine dezimalzahl umgewandelt
    res = str(res[0]) + '.' + str(res[1]) + '.' + str(res[2]) + '.' + str(res[3]) #aus der liste wird wieder eine ip
    return res

def analyze(ip, subnetzmaske, cidr):
    #ip wird in binär umgerechnet
    ip = ip2bin(ip)


    #netzwerkteil
    #cidr betrachtet nur die oktette, nicht die trennenden punkte. die if abfragen passen die länge dementsprechend an
    if(cidr>24):
        cidr +=3
    else:
        if(cidr>16):
            cidr +=2   
        else:
            if(cidr>8):
                cidr +=1
    #Netzwerkteil wird bestimmt, alles über dem wert von cidr hinaus fällt weg.  
    Netzwerkteil = ip [:cidr]


    #Subnetzteil
    #länge des subnetzteils ermitteln
    #um den subnetzteil zu finden filtern wir erst alle Nullen aus der Subnetzmaske (nachdem diese in binärzahlen übersetzt wurde)
    #filtern alle Punkte raus
    subnetzlänge = ''.join((filter(lambda i: i != '0' and i != '.', ip2bin(subnetzmaske))))
    subnetzlänge = len(subnetzlänge)
    #addieren die jetzt fehlenden Punkte zurück auf die länge des Subnetzanteils 1111111111
    if(subnetzlänge>24):
        subnetzlänge +=3
    else:
        if(subnetzlänge>16):
            subnetzlänge +=2   
        else:
            if(subnetzlänge>8):
                subnetzlänge +=1

    #und nehmen uns dann den Bereich nach dem Netzanteil und vor dem Ende der Subnetzmaske  
    Subnetzteil = ip[cidr:subnetzlänge]


    #Hostteil
    #alles hinter dem subnetz
    Hostteil =  ip[subnetzlänge:]

    #Ausgabe der IP in Anteilen
    print("Netzwerkteil | Subnetzteil | Hostteil")
    print(Netzwerkteil, '|' , Subnetzteil, '|' , Hostteil)


    #im wievielten Subnetz bin ich?
    #Filtern der Punkte aus dem Subnetz 
    Subnetz = ''.join((filter(lambda i : i != '.',Subnetzteil)))
    #wenns kein subnetz gibt weil cidr=länge des subnetzteils dann brauchen wir den boolean um nicht in einen fehler zu laufen
    noSubnet = False
    if(Subnetz==''):
        noSubnet = True
    #Subnetz wird erst zu einem Integer, dann von einer Binärzahl zu einer Dezimalzahl umgewandelt.
    #Wir addieren 1 da wir bei den Subnetzen bei 1 zu zählen beginnen und nicht wie bei Binärzahlen bei 0.
    if noSubnet==False: print (bin2dec(int(Subnetz)) + 1, "-tes Subnetz")
    if noSubnet==True: print ("Gibt keine Subnetze.")

    #was ist meine net-id?
    #Jede 1 im Hostteil wird mit einer 0 ersetzt
    Hostteil_NetID = Hostteil.replace("1","0")
    #Der neue Hostteil wird mit dem Netzwerk- und Subnetzteil zusammengeführt und ausgegeben                                                                                                                       
    print("Netzwerk-ID:", ip2dec(Netzwerkteil + Subnetzteil + Hostteil_NetID))


    #was ist meine broadcast-id?
    #Jede 0 im Hostteil wird mit einer 1 ersetzt
    Hostteil_BCID = Hostteil.replace("0","1")
    #Der neue Hostteil wird mit dem Netzwerk- und Subnetzteil zusammengeführt und ausgegeben
    print("Broadcast-ID:", ip2dec(Netzwerkteil + Subnetzteil + Hostteil_BCID))


    #Wieviele Subnetze gibt es? 
    #Anzahl der Subnetze ist 2 zur Potenz der Länge des Subnetzanteils (ohne Punkte) 
    if noSubnet==False: print("Anzahl Subnetze:", 2**len(Subnetz))
    if noSubnet==True: print("Anzahl Subnetze: 0")

    #Wieviele Hosts gibt es?
    #Anzahl der Hosts ist 2 zur Potenz der Länge des Hostteils (ohne Punkte) -2 wegen BC-ID und Net-ID
    Hostteil_filtered = ''.join((filter(lambda i : i != '.',Hostteil)))
    print("Anzahl Hosts:", 2**len(Hostteil_filtered)-2)


    #Wieviele Hosts insgesamt?
    #Anzahl Hosts insgesamt ist Anzahl Hosts in einem Subnetz mal die Anzahl der Subnetze
    if noSubnet==False: print("Anzahl Hosts insgesamt:", 2**len(Subnetz)*(2**len(Hostteil_filtered)-2))
    if noSubnet==True: print("Anzahl Hosts insgesamt:", 2**len(Hostteil_filtered)-2)

def analyzeGUI(ip, subnetzmaske, cidr):

    returnlist = []

    #ip wird in binär umgerechnet
    ip = ip2bin(ip)


    #netzwerkteil
    #cidr betrachtet nur die oktette, nicht die trennenden punkte. die if abfragen passen die länge dementsprechend an
    if(cidr>24):
        cidr +=3
    else:
        if(cidr>16):
            cidr +=2   
        else:
            if(cidr>8):
                cidr +=1
    #Netzwerkteil wird bestimmt, alles über dem wert von cidr hinaus fällt weg.  
    Netzwerkteil = ip [:cidr]


    #Subnetzteil
    #länge des subnetzteils ermitteln
    #um den subnetzteil zu finden filtern wir erst alle Nullen aus der Subnetzmaske (nachdem diese in binärzahlen übersetzt wurde)
    #filtern alle Punkte raus
    subnetzlänge = ''.join((filter(lambda i: i != '0' and i != '.', ip2bin(subnetzmaske))))
    subnetzlänge = len(subnetzlänge)
    #addieren die jetzt fehlenden Punkte zurück auf die länge des Subnetzanteils 1111111111
    if(subnetzlänge>24):
        subnetzlänge +=3
    else:
        if(subnetzlänge>16):
            subnetzlänge +=2   
        else:
            if(subnetzlänge>8):
                subnetzlänge +=1

    #und nehmen uns dann den Bereich nach dem Netzanteil und vor dem Ende der Subnetzmaske  
    Subnetzteil = ip[cidr:subnetzlänge]


    #Hostteil
    #alles hinter dem subnetz
    Hostteil =  ip[subnetzlänge:]

    #Ausgabe der IP in Anteilen
    returnlist.append("Netzwerkteil ")
    returnlist.append(Netzwerkteil)
    returnlist.append("Subnetzteil ")
    returnlist.append(Subnetzteil)
    returnlist.append("Hostteil ")
    returnlist.append(Hostteil)


    #was ist meine net-id?
    #Jede 1 im Hostteil wird mit einer 0 ersetzt
    Hostteil_NetID = Hostteil.replace("1","0")
    #Der neue Hostteil wird mit dem Netzwerk- und Subnetzteil zusammengeführt und ausgegeben                                                                                                                       
    returnlist.append("Netzwerk-ID: ")
    returnlist.append(str(ip2dec(Netzwerkteil + Subnetzteil + Hostteil_NetID)))
    


    #was ist meine broadcast-id?
    #Jede 0 im Hostteil wird mit einer 1 ersetzt
    Hostteil_BCID = Hostteil.replace("0","1")
    #Der neue Hostteil wird mit dem Netzwerk- und Subnetzteil zusammengeführt und ausgegeben
    returnlist.append("Broadcast-ID: ")
    returnlist.append(ip2dec(Netzwerkteil + Subnetzteil + Hostteil_BCID))


    #im wievielten Subnetz bin ich? 
    #Filtern der Punkte aus dem Subnetz 
    Subnetz = ''.join((filter(lambda i : i != '.',Subnetzteil)))
    #wenns kein subnetz gibt weil cidr=länge des subnetzteils dann brauchen wir den boolean um nicht in einen fehler zu laufen
    noSubnet = False
    if(Subnetz==''):
        noSubnet = True
    #Subnetz wird erst zu einem Integer, dann von einer Binärzahl zu einer Dezimalzahl umgewandelt.
    #Wir addieren 1 da wir bei den Subnetzen bei 1 zu zählen beginnen und nicht wie bei Binärzahlen bei 0.
    if noSubnet==False: 
        returnlist.append("Nummer des Subnetzes: ")
        returnlist.append(str(bin2dec(int(Subnetz)) + 1))
    if noSubnet==True: 
        returnlist.append("Nummer des Subnetzes ")
        returnlist.append("Gibt keine Subnetze.")

    #Wieviele Subnetze gibt es? 
    #Anzahl der Subnetze ist 2 zur Potenz der Länge des Subnetzanteils (ohne Punkte) 
    if noSubnet==False: 
        returnlist.append("Anzahl Subnetze: ")
        returnlist.append(str(2**len(Subnetz)))
    if noSubnet==True: 
        returnlist.append("Anzahl Subnetze: ")
        returnlist.append('0')

    #Wieviele Hosts gibt es?
    #Anzahl der Hosts ist 2 zur Potenz der Länge des Hostteils (ohne Punkte) -2 wegen BC-ID und Net-ID
    Hostteil_filtered = ''.join((filter(lambda i : i != '.',Hostteil)))
    returnlist.append("Anzahl Hosts: ")
    returnlist.append(str(2**len(Hostteil_filtered)-2))


    #Wieviele Hosts insgesamt?
    #Anzahl Hosts insgesamt ist Anzahl Hosts in einem Subnetz mal die Anzahl der Subnetze
    if noSubnet==False: 
        returnlist.append("Anzahl Hosts insgesamt: ")
        returnlist.append(str(2**len(Subnetz)*(2**len(Hostteil_filtered)-2)))
    if noSubnet==True: 
        returnlist.append("Anzahl Hosts insgesamt: ")
        returnlist.append(str(2**len(Hostteil_filtered)-2))
        
    
    return returnlist