import copy
import time
"""Debug arvo kaksi tulostaa kaikki pelitilanteet
   Debug arvo kolme tulostaa myös haun sen hetkisen rekursion syvyyden
   Debug arvo neljä käyttää lisäksi debug_syöte aliohjelman arvoja"""
DEBUG = 2
# Määritellään sudokun leveys / pituus
LAUDAN_KOKO = 9
# Määritellään sudokun neliöiden koko
NELION_KOKO = 3

def debug_syote():
    # Joitakin sudokuja, tarkoitettu debug tarkoitukseen
    # https://kjell.haxx.se/sudoku/
    # 912946083-v3-75-L1
    # return ["7 5 6 x 3 9 4 1 2",\
    #         "1 2 3 4 7 x 9 8 6",\
    #         "9 8 4 1 2 6 5 7 3",\
    #         "3 4 2 7 5 8 1 6 9",\
    #         "5 9 7 6 1 3 8 2 4",\
    #         "8 6 1 2 x 4 3 5 7",\
    #         "x x 8 3 4 7 2 9 5",\
    #         "2 3 9 x 6 1 7 4 8",\
    #         "4 7 5 9 8 2 6 3 1"]
    # 637680085-v3-50-L1
    # return ["2 1 x 3 x x x 7 x",\
    #         "3 x 6 7 5 x x 9 2",\
    #         "x 9 5 8 x 2 6 3 x",\
    #         "x 8 7 x x x x 2 x",\
    #         "x 5 2 x 7 8 4 x 3",\
    #         "1 x 3 2 9 4 7 8 5",\
    #         "x 2 9 4 x x x 1 7",\
    #         "8 7 4 9 x 3 x 5 6",\
    #         "6 x x 5 x 7 9 x 8"]
    # 648377839-v3-33-L1
    # return ["x x x x 2 x 1 x 6",\
    #         "5 x x x x x x x x",\
    #         "1 9 6 x 8 x 4 2 x",\
    #         "6 x 7 x 3 9 x 5 x",\
    #         "x 1 3 x 5 x x 8 x",\
    #         "x x 4 x 1 x x 6 7",\
    #         "3 x x x x 2 x 7 x",\
    #         "4 7 5 3 x 6 x x x",\
    #         "x x x 1 x x x 4 x"]
    # 985188514-v3-17-L5
    return ["x x x x x x 5 x x",\
            "6 x x x x 4 x x x",\
            "x x x x x 2 x x 1",\
            "x x x 6 8 x x x x",\
            "x x x x x x x 1 4",\
            "9 x x x x 5 x x x",\
            "x 2 x x x x x x x",\
            "x x x x x x 8 9 x",\
            "x 4 1 3 x x x x x"]
    

class tuntematon_c:
    """Datatyyppi, jonka tarkoituksena on säilyttää kaikki tuntemattomille tärkeä tieto"""
    # Tuntemattomien koordinaatit taulukossa alkaen nollasta
    x = 0
    y = 0
    # Tuntemattomien sijainti neliöissä
    # Neliöt jaettu seuraavasti, kun x on ensimmäinen luku ja y toinen:
    # 00 10 20
    # 01 11 21
    # 02 12 22
    neliox = 0
    nelioy = 0
    # Tämä muuttuja sisältää kaikki mahdolliset numerot, mitä tuntematon voi olla
    vaihtoehdot = []

class pelitilanne_c:
    """Datatyyppi, joka säilöö koko pelitilanteen sisälleen.
    Hyödyllinen dynaamisesti ohjelmoitavaa hakupuuta käytettäessä"""
    # Pelilauta säilötään kaksiuloitteisena listana lauta muuttujaan
    # Pelilaudassa x on korvattu 0, koska lautaa käsitellään kokonaisluku arvoina
    # Laudan koordinaatteja haetaan typerästi muodossa lauta[y][x]
    # Tämä on valitettava Pythonin listojen ominaisuus
    lauta = []
    # Tuntemattomat listaan tallennetaan kaikki tuntemattomat tuntematon_c olioina
    tuntemattomat = []
    # Tähän tallennetaan se tuntematon, johon sijoitetaan arvattavia arvoja
    arvattava_tuntematon = tuntematon_c()
    # Muuttujaan tallennetaan se haara indeksinä, jota on viimeksi lähdetty seuraamaan
    viimeisin_haara = 0
    # Muuttuja on True, mikäli vastausvaihtoehtoja on ja False, jos ei ole
    ratkaisuja_on = True

def tulosta_ohje(ohje):
    """Tulostaa käyttäjälle ohjeita ohjelman käytöstä"""
    if ohje == 0:
        print("\nVaihtoehdot:\n\
1) Syötä sudoku ja ratkaise se\n\
2) Lataa sudoku tiedostosta ja ratkaise se\n\
3) Vaihda sudokun koko\n\
4) Muuta tulostettavan tiedon määrää\n\
5) Vaihda algoritmia\n\
0) Lopeta ohjelma")
    elif ohje == 1:
        print("Peruuta kirjoittamalla 0 tai\n\
anna sudoku rivikerrallaan seuraavankaltaisessa muodossa:\n\n\
7 5 6 x 3 9 4 1 2\n\
1 2 3 4 7 x 9 8 6\n\
9 8 4 1 2 6 5 7 3\n\
3 4 2 7 5 8 1 6 9\n\
5 9 7 6 1 3 8 2 4\n\
8 6 1 2 x 4 3 5 7\n\
x x 8 3 4 7 2 9 5\n\
2 3 9 x 6 1 7 4 8\n\
4 7 5 9 8 2 6 3 1\n")
    elif ohje == 2:
        print("Poistu kirjoittamalla 0 tai anna tiedeoston nimi.\n\
Tiedoston tulee sisältää välein ja rivinvaihdoin eroteltu sudoku.")
    elif ohje == 3:
        print("Valitse seuraavista:\n\
1) Vaihda ratkaistavan sudokun koko 4 x 4 sudokuksi\n\
2) Vaihda ratkaistavan sudokun koko 9 x 9 sudokuksi (oletus)\n\
0) Peruuta\n")
    elif ohje == 4:
        print("Valitse seuraavista vaihtoehdoista tulostettavan tiedon määrä:\n\
1) Tulosta ainoastaan ratkaisu\n\
2) Tulosta ratkaisun lisäksi välivaiheita (oletus)\n\
3) Tulosta ratkaisun ja välivaiheiden lisäksi rekursion syvyys\n\
0) Peruuta\n")
    elif ohje == 5:
        print("Valitse käytettävä algoritmi:\n\
1) Aloita arvailu ahneesti ensimmäisestä tuntemattomasta (oletus)\n\
2) Aloita arvailu tuntemattomasta, joka sisältää vähiten vaihtoehtoja\n\
3) Aloita arvailu viimeisestä tuntemattomasta\n\
4) Aloita arvailu keskimmäisestä tuntemattomasta\n\
0) Peruuta\n")

def tulosta_pelitilanne(pelitilanne):
    """Tulostaa pelitilanteen käymällä taulukon rivikerrallaan läpi"""
    lauta = pelitilanne.lauta
    lanka = "Pelitilanne:\n"
    for y in range(LAUDAN_KOKO):
        # Käydään läpi rivikerrallaan ja tulostetaan siistitty lista
        lanka = lanka + str(lauta[y]).replace("0","x").replace(",","")[1:2*LAUDAN_KOKO] + "\n"
    print(lanka, end="")

def syote_taulukoksi(syote):
    """Muuntaa yksiuloitteisen string listan kaksi uloitteiseksi integer listaksi"""
    lauta = []
    # Muutetaan kaikki "x":t "0", jotta taulukkoa olisi helpompi käsitellä
    for i in range(LAUDAN_KOKO):
        # Muutetaan kaikki "x":t "0", jotta taulukkoa olisi helpompi käsitellä
        syote[i] = syote[i].replace("x","0")
        # Muunnetaan merkkijono merkki listaksi
        merkki_lista = syote[i].split()
        # Muunnetaan merkki lista kokonaisluku listaksi
        kokonaisluku_lista = list(map(int,merkki_lista))
        # Listäään lista lauta listan jäseneksi
        lauta.append(kokonaisluku_lista)
    return lauta   

def maarittele_tuntemattomat(pelitilanne):
    for x in range(LAUDAN_KOKO):
        for y in range(LAUDAN_KOKO):
            numero = pelitilanne.lauta[y][x]
            if numero == 0:
                # Määritellään uuden löydetyn tuntemattoman tiedot
                tuntematon = tuntematon_c()
                tuntematon.x = x
                tuntematon.y = y
                # Määritellään tuntemattoman neliö datatyypin määritelmän mukaisesti
                tuntematon.neliox = int(x / NELION_KOKO)
                tuntematon.nelioy = int(y / NELION_KOKO)
                tuntematon.vaihtoehdot = list(range(1,LAUDAN_KOKO + 1))
                # Lisätään uusi tuntematon tuntemattomat listaan
                pelitilanne.tuntemattomat.append(tuntematon)
    return pelitilanne            

def poista(lista, arvo):
    """Funktio poistaa kohteen listalta, mikäli se on listalla
    Käytännössä siis Pythonin normi listalta poisto, mutta ilman pelkoa virheestä"""
    if arvo in lista:
        lista.remove(arvo)
    return lista

def poista_tuntematon(pelitilanne, tuntematon):
    """Poistaa tuntemattoman listalta, mikäli sen x ja y arvot vastaavat toisiaan"""
    # Piste notaation välttäminen loopin sisällä nopeuttaa koodin suorittamista.
    x = tuntematon.x
    y = tuntematon.y
    tuntemattomat = pelitilanne.tuntemattomat
    # Käydään läpi kaikki tuntemattomat
    maara = range(len(pelitilanne.tuntemattomat))
    for i in maara:
        #if pelitilanne.tuntemattomat[i].x == tuntematon.x and pelitilanne.tuntemattomat[i].y == tuntematon.y:
        if tuntemattomat[i].x == x and tuntemattomat[i].y == y:
            del pelitilanne.tuntemattomat[i]
            return pelitilanne
    else:
        print("")

def resetoi_tuntemattomat(pelitilanne):
    """Palauttaa kaikkien tuntemattomien vaihtoehdot oletusarvoihinsa"""
    maara = range(len(pelitilanne.tuntemattomat))
    for i in maara:
        pelitilanne.tuntemattomat[i].vaihtoehdot = list(range(1,LAUDAN_KOKO + 1))
    return pelitilanne

def paivita_tuntemattomat(pelitilanne):
    """Funktio päivittää tuntemattomien vaihtoehdot"""
    maara = range(len(pelitilanne.tuntemattomat))
    for i in maara:
        lista = pelitilanne.tuntemattomat[i].vaihtoehdot
        # Poistetaan tuntemattomien vaihtoehdoista kaikki samalla rivillä olevat
        for x in range(LAUDAN_KOKO):
            lista = poista(lista, pelitilanne.lauta[pelitilanne.tuntemattomat[i].y][x])
        # Poistetaan tuntemattomien vaihtoehdoista kaikki samalla sarakkeella olevat
        for y in range(LAUDAN_KOKO):
            lista = poista(lista, pelitilanne.lauta[y][pelitilanne.tuntemattomat[i].x])
        # Poistetaan tuntemattomien vaihtoehdoista kaikki samassa neliössä olevat
        neliox = pelitilanne.tuntemattomat[i].neliox
        nelioy = pelitilanne.tuntemattomat[i].nelioy
        # Käydään siis kolme 3 x 3 neliö alkio kerrallaan läpi
        aloitus_x = NELION_KOKO*neliox
        aloitus_y = NELION_KOKO*nelioy
        for x in range(aloitus_x,aloitus_x + NELION_KOKO):
            for y in range(aloitus_y,aloitus_y + NELION_KOKO):
                lista = poista(lista, pelitilanne.lauta[y][x])
        pelitilanne.tuntemattomat[i].vaihtoehdot = list(lista)
    return pelitilanne

def ratkaise_varmat(pelitilanne):
    """Ratkaisee sellaiset tuntemattomat, jotka ovat yksikäsitteisesti ratkaistavissa"""
    # Resetoidaan tuntemattomien vaihtoehdot, jotka puoli bugisesti periytyvät
    # Peli tilanteesta toiseen
    pelitilanne = resetoi_tuntemattomat(pelitilanne)
    # Päivitetään vaihtoehdot alustavasti
    pelitilanne = paivita_tuntemattomat(pelitilanne)
    # Lasketaan tuntemattomien määrä
    maara = len(pelitilanne.tuntemattomat)
    i = 0
    # Käydään jokainen tuntematon yksitellen läpi
    while i < maara:
        vaihtoehtojen_maara = len(pelitilanne.tuntemattomat[i].vaihtoehdot)
        # Mikäli tuntemattomalla on tasan yksi vaihtoehto, voidaan vaihtoehto sijoittaa laudalle
        if vaihtoehtojen_maara == 1:
            # Asetetaan ainut vaihtoehto pelilaudalle
            pelitilanne.lauta[pelitilanne.tuntemattomat[i].y][pelitilanne.tuntemattomat[i].x] = pelitilanne.tuntemattomat[i].vaihtoehdot[0]
            # Poistetaan kyseinen tuntematon tuntemattomat listalta
            del pelitilanne.tuntemattomat[i]
            pelitilanne = paivita_tuntemattomat(pelitilanne)
            maara = maara - 1
            i = 0
        # Mikäli tuntemattomalla on nolla vaihtoehtoa, voimme todeta, että jotain on pahasti pielessä
        # Tämä käytännössä tarkoittaa sitä, että pitää palata edelliseen pelitilanteeseen
        elif vaihtoehtojen_maara == 0:
            pelitilanne.ratkaisuja_on = False
            break
        else:
            i = i + 1
    return pelitilanne

def kopioi(lahde):
    """Palauttaa kunnollisen kopion lähteestä, jossa arvot eivät ole
    linkitettyjä lukuunottamatta tuntemattomien vaihtoehtoja"""
    # Alustava kopio deepcopy funktiolla
    kohde = copy.deepcopy(lahde)
    kohde.tuntemattomat = []
    # Käydään läpi kaikki tuntemattomat
    maara = range(len(lahde.tuntemattomat))
    for i in maara:
        # Tuntemattomat olioista on pakko ottaa erikseen yksittäiset kopiot, sillä
        # Deepcopy funktio ei valitettavasti osaa kopioida olioita automaattisesti
        kohde.tuntemattomat.append(lahde.tuntemattomat[i])
    return kohde

def resetoi_dynaaminen(pelitilanteet):
    """Nollaa kaikki dynaamiseen ratkaisuun liittyvät muuttujat"""
    for i in range(len(pelitilanteet)):
        maara = len(pelitilanteet[i].tuntemattomat)
        for ii in range(maara):
            del pelitilanteet[i].tuntemattomat[maara - ii - 1]
    del pelitilanteet

def ratkaise_dynaamisesti(pelitilanne, algoritmi):
    """Funktio ratkaisee Sudokun dynaamisia algoritmin suunnitteluperiaatteita käyttäen.
    Funktio hakee vastausta syvyyshakuna niin, että se järjestelmällisesti sijoittelee arvoja
    tuntemattomiin alkaen sellaisesta tuntemattomasta, joka sijaitsee mahdollisimman lähellä
    vasenta laitaa. mikäli parametri (algoritmi) on 0. Mikäli kaikki vaihtoehdot on käyty
    läpi palaa funktio edelliseen haaraan listattuja pelitilanteita hyväksi käyttäen"""
    pelitilanteet = []
    pelitilanne = ratkaise_varmat(pelitilanne)
    pelitilanteet.append(pelitilanne)
    i = 0
    arvauksia = 0
    syvin_haara = 0
    # Otetaan aloitus aika ylös
    aloitus = time.time()
    while True:
        # Lähdetään käsittelemään uutta kopiota pelitilanteesta
        uusipelitilanne = ratkaise_varmat(kopioi(pelitilanteet[i]))
        # Mikäli tuntemattomien lista on tyhjä voidaan sudoku todeta ratkaistuksi
        if not uusipelitilanne.tuntemattomat:
            break
        # Jos ratkaisuja ei ole ollenkaan palataan edelliseen haaraan ja jatketaan seuraavaan haaraan
        elif uusipelitilanne.ratkaisuja_on == False:
            # Tarkistetaan, onko tämän solmun kaikki vaihtoehdot käyty läpi
            while True:
                if pelitilanteet[i].viimeisin_haara == len(pelitilanteet[i].arvattava_tuntematon.vaihtoehdot) - 1:
                    # Mikäli on palataan edelliseen solmuun
                    del pelitilanteet[i]
                    i = i - 1
                else:
                    # Mikäli ei jatketaan seuraavaan solmuun
                    pelitilanteet[i].viimeisin_haara = pelitilanteet[i].viimeisin_haara + 1
                    # Vaihdetaan taulukon arvoa vaihtoehtojen mukaisesti
                    x = pelitilanteet[i].arvattava_tuntematon.x
                    y = pelitilanteet[i].arvattava_tuntematon.y
                    if i != 0:
                        pelitilanteet[i].lauta[y][x] = pelitilanteet[i].arvattava_tuntematon.vaihtoehdot[pelitilanteet[i].viimeisin_haara]
                    else:
                        # Sudoku ei ole ratkaisukelpoinen, jos päädytään tähän haaraan
                        print("Virhe! Tämä ei ole sudoku, koska sille ei ole ratkaisuja")
                        resetoi_dynaaminen(pelitilanteet)
                        return uusipelitilanne
                    break
        # Päädytään tilanteeseen, että tuntemattomia on vielä jäljellä, mutta ratkaisua ei
        # yksikäsitteisesti löydy. Mennään siis yksi solmu alaspäin
        else:
            if algoritmi == 1:
                # Valitaan listan ensimmäinen tuntematon ja edetään
                uusipelitilanne.arvattava_tuntematon = uusipelitilanne.tuntemattomat[0]
            elif algoritmi == 2:
                # Valitaan vähiten tuntemattomia sisältävä tuntematon
                maara = range(len(uusipelitilanne.tuntemattomat))
                uusipelitilanne.arvattava_tuntematon = uusipelitilanne.tuntemattomat[0]
                for index in maara:
                    if len(uusipelitilanne.arvattava_tuntematon.vaihtoehdot) > len(uusipelitilanne.tuntemattomat[index].vaihtoehdot):
                        uusipelitilanne.arvattava_tuntematon = uusipelitilanne.tuntemattomat[index]
            elif algoritmi == 3:
                # Valitaan listan viimeinen tuntematon
                uusipelitilanne.arvattava_tuntematon = uusipelitilanne.tuntemattomat[len(uusipelitilanne.tuntemattomat)-1]
            elif algoritmi == 4:
                # Valitaan keskimmäinen tuntematon
                uusipelitilanne.arvattava_tuntematon = uusipelitilanne.tuntemattomat[int(len(uusipelitilanne.tuntemattomat) / 2)]
            # Asetetaan viimeisin_haara nollaksi, koska lähdetään kokeilemaan ensimmäistä lukua
            uusipelitilanne.viimeisin_haara = 0
            x = uusipelitilanne.arvattava_tuntematon.x
            y = uusipelitilanne.arvattava_tuntematon.y
            # Sijoitetaan arvattava_tuntematon eli kokeilavan tuntemattoman arvo laudalle
            uusipelitilanne.lauta[y][x] = uusipelitilanne.arvattava_tuntematon.vaihtoehdot[0]
            # Poistetaan kyseinen tuntematon tuntemattomien joukosta
            uusipelitilanne = poista_tuntematon(uusipelitilanne,uusipelitilanne.arvattava_tuntematon)
            # Lisätään uusi solmu pelitilanteet listaan
            pelitilanteet.append(kopioi(uusipelitilanne))
            i = i + 1
            if syvin_haara < i:
                syvin_haara = i
        if DEBUG > 1:
            tulosta_pelitilanne(uusipelitilanne)
        if DEBUG > 2:
            print("Solmu:", str(i) + "\n")
        arvauksia = arvauksia + 1
    
    lopetus = time.time()
    print("Arvauksia oli:", str(arvauksia))
    print("Syvin haara mikä tutkittiin oli:", str(syvin_haara))
    print("Aikaa kului:", str(round(lopetus-aloitus,2)), "sekuntia")
    resetoi_dynaaminen(pelitilanteet)
    return uusipelitilanne

def ratkaise(syote, algoritmi):
    """Ratkaistaan sudoku syötteestä"""
    # Luodaan uusi pelitilanne
    pelitilanne = pelitilanne_c()
    # Muutetaan käyttäjän antamat tiedot taulukko muotoon
    pelitilanne.lauta = syote_taulukoksi(syote)
    # Etsitään tuntemattomat ja määritellään niiden sijainti
    pelitilanne = maarittele_tuntemattomat(pelitilanne)
    # Aloitetaan dynaaminen ratkaiseminen
    pelitilanne = ratkaise_dynaamisesti(pelitilanne, algoritmi)
    # Tulostetaan ratkaisu
    tulosta_pelitilanne(pelitilanne)

def onko_virheellinen(merkkijono):
    """Tarkistetaan onko merkkijono kelpaava syötteeksi palauttaa True jos on ja False jos ei ole"""
    testattava = merkkijono.replace("x","0").replace(" ", "")
    # Alustavan syötteen tulee olla 9 kokoisella laudalla 17 merkkiä pitkä ja välit poistettuna 9 merkkiä pitkä
    # Lopputulos voi sisältää vain numeroita
    # Lukujen ja välien tulee vuorotella
    maara = merkkijono.split()
    if len(testattava) != LAUDAN_KOKO or len(maara) != LAUDAN_KOKO or len(merkkijono) != LAUDAN_KOKO*2-1 or testattava.isdigit() != True:
        return False
    else:
        return True

def pyyda_luvut():
    tulosta_ohje(1)
    # Pyydetään käyttäjältä luvut rivi kerrallaan
    lista = []
    i = 0
    while i < LAUDAN_KOKO:
        syote = input("Anna rivi {0}: ".format(i + 1))
        if syote == "0":
            # Tarkoittaa, että käyttäjä haluaa keskeyttää lukujen antamisen
            return [0]
        # Tarkistetaan ettei käyttäjä syötä puutaheinää
        if onko_virheellinen(syote) == False:
            print("Virheellinen syöte, syötä rivi uudelleen")
        else:
            # Jos syöte on kunnossa lisätään se listaan
            lista.append(syote)
            i = i + 1
    print("")
    return lista

def lue_tiedostosta():
    """Hakee syötteen käyttäjän antaman tiedostonimen perusteella"""
    tulosta_ohje(2)
    lista = []
    while True:
        nimi = input("Anna tiedoston nimi: ")
        if nimi == "0":
            # Tarkoittaa, että käyttäjä haluaa peruuttaa tiedoston lukemisen
            return [0]
        # Kokeillaan onko tiedosto olemassa
        try:
            tiedosto = open(nimi, "r")
        except:
            print("Tiedostoa ei ole olemassa, anna olemassa olevan tiedoston nimi.")
        else:
            for i in range(LAUDAN_KOKO):
                # Luetaan tiedosto rivi kerrallaan
                syote = tiedosto.readline()[:-1]
                # Tarkistetaan, että tiedosto on asianmukainen
                if onko_virheellinen(syote) == False:
                    print("Tiedosto on viallinen!")
                    tiedosto.close()
                    lista = []
                    break
                else:
                # Jos syöte on kunnossa lisätään se listaan
                    lista.append(syote)
            else:
                # Tiedosto on onnistuneesti luettu, joten poistutaan loopista
                break
    tiedosto.close()
    return lista

def vaihda_koko():
    """Proseduuri vaihtaa ohjelman tilaa 9 x 9 sudokujen ja 4 x 4 sudokujen välillä"""
    tulosta_ohje(3)
    global LAUDAN_KOKO
    global NELION_KOKO
    while True:
        valinta = input("Valinta: ")
        if valinta == "1":
            # Muutetaan ohjelman tila 2 x 2 sudokuja ratkaisevaksi
            LAUDAN_KOKO = 4
            NELION_KOKO = 2
            break
        elif valinta == "2":
            # Muutetaan ohjelman tila 9 x 9 sudokuja ratkaisevaksi
            LAUDAN_KOKO = 9
            NELION_KOKO = 3
            break
        elif valinta == "0":
            break
        else:
            print("Virheellinen syöte.")
def vaihda_tulostuksen_maaraa():
    """Vaihtaa tulostettavan tiedon määrän käyttäjän toiveiden mukaan"""
    tulosta_ohje(4)
    global DEBUG
    while True:
        valinta = input("Valinta: ")
        if valinta == "1":
            DEBUG = 1
            break
        elif valinta == "2":
            DEBUG = 2
            break
        elif valinta == "3":
            DEBUG = 3
            break
        elif valinta == "0":
            break
        else:
            print("Virheellinen syöte.")

def vaihda_algoritmia(algoritmi):
    tulosta_ohje(5)
    while True:
        valinta = input("Valinta: ")
        if valinta == "1":
            return 1
        elif valinta == "2":
            return 2
        elif valinta == "3":
            return 3
        elif valinta == "4":
            return 4
        elif valinta == "0":
            return algoritmi
        else:
            print("Virheellinen syöte.")

def sudoku():
    algoritmi = 1
    if DEBUG < 4:
        # Suoritetaan ohjelma normaalisti käyttämällä hyväksi valikkorakennetta
        while True:
            tulosta_ohje(0)
            valinta = input("Valintasi: ")
            print("")
            if valinta == "1":
                # Pyydetään käyttäjältä luvut ja ratkaistaan sudoku
                syote = pyyda_luvut()
                if syote[0] != 0:
                    ratkaise(syote,algoritmi)
            elif valinta == "2":
                # Pyydetään käyttäjältä tiedostonimi ja ratkaistaan sudoku
                syote = lue_tiedostosta()
                if syote[0] != 0:
                    ratkaise(syote,algoritmi)
            elif valinta == "3":
                # Kysytään käyttäjältä uusi koko
                vaihda_koko()
            elif valinta == "4":
                # Kysytään käyttäjältä, paljonko hän haluaa tietoa
                vaihda_tulostuksen_maaraa()
            elif valinta == "5":
                # Kysytään käyttäjältä, mitä algoritmia hän haluaa käyttää
                algoritmi = vaihda_algoritmia(algoritmi)
            elif valinta == "0":
                break
            elif valinta != "":
                print("Virheellinen syöte.")
    else:
        # Suoritetaan ohjelma käyttämällä debug aliohjelman arvoja
        ratkaise(debug_syote(),1)

sudoku()