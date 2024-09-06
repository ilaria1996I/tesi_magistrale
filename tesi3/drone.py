from clingo import Control
import re
import os


def leggi_file_asp(nome_file):
    with open(nome_file, 'r') as file:
        codice_asp = file.read()
    return codice_asp

def leggi_fatti_da_file(nome_file):
    fatti = []
    with open(nome_file, 'r') as file:
        for line in file:
            fatto = line.strip()
            fatti.append(fatto)
    return fatti

def esegui_codice_asp(codice_asp, fatti):
    control = Control()
    control.add("base", [], codice_asp)
    for fatto in fatti:
        control.add("base", [], fatto)
    control.ground([("base", [])])

    num_modelli = 0
    for model in control.solve(yield_=True):
        num_modelli += 1
        ultimo_modello = model

    if num_modelli > 0:
        salva_coordinate(ultimo_modello)
        print_model(ultimo_modello)
    else:
        print("Nessun modello trovato.")

def print_model(model, file_gia_svuotato=False):
    # Cancella il contenuto del file solo se non è già stato svuotato in precedenza
    if not file_gia_svuotato:
        with open("modello.txt", "w") as file:
            file.truncate(0)  # Cancella il contenuto del file
    # Scrivi i simboli nel file
    with open("modello.txt", "a") as file:
        for symbol in model.symbols(shown=True):
            file.write(str(symbol) + '\n')

def salva_coordinate(modello):
    with open("coordinate2.txt", "w") as file:
        for atom in modello.symbols(shown=True):
            if atom.name == "azione" and atom.arguments[0].name == "gestioneIncendio":
                t = atom.arguments[1].number
                x = atom.arguments[2].number
                y = atom.arguments[3].number
                file.write(f"{t},{x},{y}\n")

def trasforma(nome_file):
    cartella = "fattiOrdinati"  # Sostituisci con il percorso della cartella da cui vuoi eliminare i file
    try:
        os.remove("tuo_file.txt")
    except FileNotFoundError:
        print("Non sono riuscita ad eliminare il file")
    
    # Scandisci tutti i file nella cartella
    for nome_file in os.listdir(cartella):
        percorso_file = os.path.join(cartella, nome_file)
        # Verifica se l'elemento è un file
        if os.path.isfile(percorso_file):
            # Elimina il file
            os.remove(percorso_file)

    if os.path.exists(nome_file):
        with open(nome_file, 'r') as file:
            testo = file.read()

        # Rimuovi gli spazi dal testo
        testo_senza_spazi = testo.replace(" ", "")
    
    if os.path.exists(nome_file):
        with open('tuo_file.txt', 'w') as file:
            file.write(testo_senza_spazi)

def crea_stringa_da_file(nome_file, coordinate_dict):
        # Verifica se il nome del file è presente come valore nel dizionario
        for chiave, valore in coordinate_dict.items():
            if valore == nome_file:
                # Crea la stringa con la chiave seguita dal valore corrispondente separato da un underscore
                risultato = f"{chiave}_{valore}"
                return "fattiOrdinati/"+risultato+".txt"

def crea_dic(nome_file):
    coordinate_dict = {}  # Inizializza un dizionario vuoto

    # Apri il file e leggi le righe
    with open(nome_file, "r") as file:
        for line in file:
            # Suddivide la riga in base alle virgole e converte i valori in interi
            valori = line.strip().split(",")
            tempo = valori[0]
            valore = "_".join(valori[1:])

            # Aggiunge la coppia chiave-valore al dizionario
            coordinate_dict[tempo] = valore

    return coordinate_dict
def confronta_coordinate_e_tempo(coordinate, tempo_presente, coordinateDic):
    #print("Ciao")
    for chiave, valori in coordinateDic.items():
        print("Confronto " + valori + " con coordinate " + coordinate)
        if valori == coordinate:
            print("Confronto2 " + str(chiave) + " con coordinate " + str(tempo_presente))
            if chiave == tempo_presente:
                print("Trovato")
                return True
            else:
                return False
            break
    else:
        return False

def leggi_coordinate_da_file(dizionario):
    if os.path.exists('tuo_file.txt'):
        with open('tuo_file.txt', 'r') as file:
            for line in file:
                

                if line.startswith("informazioniPerISoccorritori("):
                    valori = line[len("informazioniPerISoccorritori("):-1]  # Rimuovi il testo iniziale e la parentesi finale
                    valori_splittati = valori.split(",")  # Dividi i valori utilizzando la virgola come separatore
                    nome_file = f'{valori_splittati[0]}_{valori_splittati[1]}'
                    nuovo_nome_file = crea_stringa_da_file(nome_file, dizionario)
                    codice = "ValoriInformazioniPerISoccorritori"
                    scrivi_info_su_file(valori_splittati, str(nuovo_nome_file), codice)
                
                if line.startswith("hoTrovatoDueIncendiViciniSoloUnoHaStatoDiAllertaAlto_X_Y_V_X1_Y1_V1_D("):    
                    valori = line[len("hoTrovatoDueIncendiViciniSoloUnoHaStatoDiAllertaAlto_X_Y_V_X1_Y1_V1_D("):-1]  # Rimuovi il testo iniziale e la parentesi finale
                    valori_splittati = valori.split(",")  # Dividi i valori utilizzando la virgola come separatore
                    nome_file = f'{valori_splittati[0]}_{valori_splittati[1]}'
                    nuovo_nome_file = crea_stringa_da_file(nome_file, dizionario)
                    codice = "hoTrovatoDueIncendiViciniSoloUnoHaStatoDiAllertaAlto_X_Y_V_X1_Y1_V1_D"
                    scrivi_info_su_file(valori_splittati, str(nuovo_nome_file), codice)
                

                if line.startswith("invioVentilatoriManuali("):    
                    valori = line[len("invioVentilatoriManuali("):-1]  # Rimuovi il testo iniziale e la parentesi finale
                    valori_splittati = valori.split(",")  # Dividi i valori utilizzando la virgola come separatore
                    nome_file = f'{valori_splittati[0]}_{valori_splittati[1]}'
                    nuovo_nome_file = crea_stringa_da_file(nome_file, dizionario)
                    codice = "invioVentilatoriManuali"
                    scrivi_info_su_file(valori_splittati, str(nuovo_nome_file), codice)
                
                if line.startswith("chiamataSoccorsoInoltrata("):
                    
                    valori = line[len("chiamataSoccorsoInoltrata("):-1]  # Rimuovi il testo iniziale e la parentesi finale
                    coor = valori.split(",")  # Dividi i valori utilizzando la virgola come separatore
                    nome_file = f'{coor[0]}_{coor[1]}'
                    nuovo_nome_file = crea_stringa_da_file(nome_file, dizionario)
                    codice = "ValoriChiamataSoccorsoInoltrata"
                    scrivi_info_su_file(coor, str(nuovo_nome_file),codice)
            
                if line.startswith("chiamataSoccorsoVeterinarioInoltrata("):
                    
                    valori = line[len("chiamataSoccorsoVeterinarioInoltrata("):-1]  # Rimuovi il testo iniziale e la parentesi finale
                    coor = valori.split(",")  # Dividi i valori utilizzando la virgola come separatore
                    nome_file = f'{coor[0]}_{coor[1]}'
                    nuovo_nome_file = crea_stringa_da_file(nome_file, dizionario)
                    codice = "ValoriChiamataSoccorsoInoltrataVet"
                    scrivi_info_su_file(coor, str(nuovo_nome_file),codice)
                
                if line.startswith("statoDiAllerta("):
                    
                    valori = line[len("statoDiAllerta("):-1]  # Rimuovi il testo iniziale e la parentesi finale
                    coor = valori.split(",")  # Dividi i valori utilizzando la virgola come separatore
                    nome_file = f'{coor[1]}_{coor[2]}'
                    nuovo_nome_file = crea_stringa_da_file(nome_file, dizionario)
                    codice = "ValoreStatoAllerta"
                    scrivi_info_su_file(coor, str(nuovo_nome_file),codice)
                
                if line.startswith("informazioniPerISoccorritoriNelleDueOreSuccessive("):
                    valori = line[len("informazioniPerISoccorritoriNelleDueOreSuccessive("):-1]  # Rimuovi il testo iniziale e la parentesi finale
                    coor = valori.split(",")  # Dividi i valori utilizzando la virgola come separatore
                    nome_file = f'{coor[0]}_{coor[1]}'
                    nuovo_nome_file = crea_stringa_da_file(nome_file, dizionario)
                    codice = "informazioniPerISoccorritoriNelleDueOreSuccessive"
                    scrivi_info_su_file(coor, str(nuovo_nome_file),codice)

def scrivi_info_su_file(coordinate, nome_file,codice):
    with open(nome_file, 'a') as file:
        if (nome_file == "None"):
            print("\n Problema none")
            print(coordinate, nome_file,codice)
        # Scrivi le informazioni nel file
        if codice == "ValoriInformazioniPerISoccorritori":
            file.write(f'direzioneVento: {coordinate[3]}\n')
            file.write(f'condizioneMetereologica: {coordinate[4]}\n')
            file.write(f'gradi: {coordinate[5]}\n')
            file.write(f'umidita: {coordinate[6][:-1]}\n')
        
        if codice == "hoTrovatoDueIncendiViciniSoloUnoHaStatoDiAllertaAlto_X_Y_V_X1_Y1_V1_D":
            file.write(f'Ho trovato due incendi, gestiro prima quello  \n più grave: {coordinate[0]},{coordinate[1]} e al {coordinate[3]},{coordinate[4]}\n')

        if codice == "invioVentilatoriManuali":
            file.write(f'richiesta di ventilatori manuali: {coordinate[2][:-1]}\n')

        if codice == "ValoriChiamataSoccorsoInoltrata":
            file.write(f'chiamata soccorso: {coordinate[3][:-1]}\n')
        
        if codice == "ValoriChiamataSoccorsoInoltrataVet":
            file.write(f'chiamata soccorso veterinaria: {coordinate[3][:-1]}\n')

        if codice == "ValoreStatoAllerta":
            file.write(f'stato di allerta alto\n')
        
        if codice == "informazioniPerISoccorritoriNelleDueOreSuccessive":
            file.write(f'direzione vento fra due ore: {coordinate[3]}\n')
            file.write(f'condizioneMetereologica fra due ore: {coordinate[4]}\n')
            file.write(f'gradi fra due ore: {coordinate[5]}\n')
            file.write(f'umidita fra due ore: {coordinate[6][:-1]}\n')
        file.close()

