#subnetzmaske, ip adresse und cidr 
# -> nr subnetz, netid, bcid, anzahl hosts, anzahl subnetze, anzahl hosts insgesamt
import random

#mit arg=None können wir _rndIp auch ohne Argument benutzen, 
#in dem Fall wird arg automatisch auf None gesetzt
#Falls ein argument gegeben wird wird dieses stattdessen benutzt
def _rndIp(arg=None): #generiert eine zufällige IPv4 Adresse
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
def _rndSM(min=0, max=32): #generiert eine zufällige Subnetzmaske
    #seed als zufallszahl zwischen 1 und 31 für die anzahl der 1 in der subnetzmaske
    if max==32 or max==31: seed= min+int(random.random()*(31-min)) 
    else: seed = min+int(random.random()*(33-min-(32-max)))
    #generieren der Einsen
    res = '1'*seed
    #generieren der Nullen
    while int(len(res))<32:
        res = res + '0'
    #einfügen der trennenden Punkte  
    res = res[:8] + '.' + res[8:16] + '.' + res[16:24] + '.' + res[24:]   
    #umrechnen in Dezimal und ausgabe
    res = _ip2dec(res)
    #subnetzmaske 0.0.0.0 cidr 1 schmeißt nen fehler, also gibts das nicht mehr, keine lust den fehler zu suchen
    if res == "0.0.0.0": 
        res = _rndSM()
    return res

def _rndcidr(subnetzmaske, minlength=0): #generieren einer beliebiegen cidr nummer kleiner oder gleich der subnetzmaske
    subnetzlänge = len(''.join((filter(lambda i: i != '0' and i != '.', _ip2bin(subnetzmaske)))))
    cidr = minlength+int(random.random()*(subnetzlänge+1-minlength))
    return cidr

def _bin(arg): #erweiterung der nativen bin() methode
    x = bin(arg)[2:] #bin gibt standardmäßig ein 0b vor den Zahlenwert, das entfernen wir hier
    while len(x)<8:
        x = '0'+ x #fügt führende nullen hinzu bis wir 8 stellen haben
    return x

def _dec(arg): #ausm internet geklaut, macht aus binär dezimal 
    decimal, i, n = 0, 0, 0
    while(arg != 0): 
        dec = arg % 10
        decimal = decimal + dec * pow(2, i)
        arg = arg//10
        i += 1
    return decimal

def _ip2bin(arg):#ip von binär zu dezimal
    res = arg.split(".") #trennt die ip in eine liste von 4 elementen 
    res = [_bin(int(x)) for x in res] #jedes element der liste wird von einer dezimalzahl in eine binärzahl umgewandelt
    res = res[0] + '.' + res[1] + '.' + res[2] + '.' + res[3] #aus der liste wird wieder eine ip
    return res

def _ip2dec(arg):#ip von binär zu dezimal
    res = arg.split(".") #trennt die ip in eine liste von 4 elementen 
    res = [_dec(int(x)) for x in res] #jedes element der liste wird von einer binärzahl in eine dezimalzahl umgewandelt
    res = str(res[0]) + '.' + str(res[1]) + '.' + str(res[2]) + '.' + str(res[3]) #aus der liste wird wieder eine ip
    return res

def _analyze(ip, subnetzmaske, cidr):
    #ip wird in binär umgerechnet
    ip = _ip2bin(ip)


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
    subnetzlänge = ''.join((filter(lambda i: i != '0' and i != '.', _ip2bin(subnetzmaske))))
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
    if noSubnet==False: print (_dec(int(Subnetz)) + 1, "-tes Subnetz")
    if noSubnet==True: print ("Gibt keine Subnetze.")

    #was ist meine net-id?
    #Jede 1 im Hostteil wird mit einer 0 ersetzt
    Hostteil_NetID = Hostteil.replace("1","0")
    #Der neue Hostteil wird mit dem Netzwerk- und Subnetzteil zusammengeführt und ausgegeben                                                                                                                       
    print("Netzwerk-ID:", _ip2dec(Netzwerkteil + Subnetzteil + Hostteil_NetID))


    #was ist meine broadcast-id?
    #Jede 0 im Hostteil wird mit einer 1 ersetzt
    Hostteil_BCID = Hostteil.replace("0","1")
    #Der neue Hostteil wird mit dem Netzwerk- und Subnetzteil zusammengeführt und ausgegeben
    print("Broadcast-ID:", _ip2dec(Netzwerkteil + Subnetzteil + Hostteil_BCID))


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


def main():
    
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

    #Zufällige Eingabe
    
    # #_rndIp kann ohne Argument oder mit den Argumenten 'A','B',..,'E' aufgerufen werden. Andere Argumente werden behandelt wie kein Argument. 
    ip = _rndIp()

    # #_rndSM() erzeugt eine zufällige Subnetzmaske zwischen 128.0.0.0 und 255.255.255.252
    # #_rndSM(x) erzeugt eine zufällige Subnetzmaske wobei mindestens x bits 1 sind (von links an) x darf nur im Intervall [0,30] liegen
    # #_rndSM(x,y) erzeugt eine zufällige Subnetzmaske mit mindestens x einsen (von links) und höchstens y einsen insgesamt
    subnetzmaske = _rndSM(9,24)

    # #_rndcidr(subnetzmaske) erzeugt eine zufällige Zahl zwischen 1 und der länge der Subnetzmaske
    # #_rndcidr(subnetzmaske,x) erzeugt eine zufällige Zahl zwischen x und der länge der Subnetzmaske
    cidr = _rndcidr(subnetzmaske,8)
    
    print("------------------")
    print(ip, "/" , cidr )
    print(subnetzmaske)
    print()
    _analyze(ip,subnetzmaske,cidr)
    print()
    print("------------------")

    #-------------------
    
    #Testeingabe

    # print("----------------------")
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print(_rndcidr(_rndSM(9,16),8))
    # print("----------------------")

if __name__ == "__main__":
     main()

