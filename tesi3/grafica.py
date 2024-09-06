import time
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence,ImageFile
import math
from drone import esegui_codice_asp,salva_coordinate,leggi_file_asp,leggi_fatti_da_file,trasforma,crea_dic,leggi_coordinate_da_file
import os

class ApplicazioneGrafica:
    def __init__(self, root):

        self.root = root
        self.root.title("Applicazione Grafica")
        self.tempo = 0

        # Creazione della tabella per visualizzare il tempo
        self.etichetta_tempo = tk.Label(root, text="Tempo: 0")
        self.etichetta_tempo.grid(row=0, column=0)

        # Creazione del bottone
        self.button = tk.Button(root, text="vai al tempo successivo", command=self.onClick)
        self.button.grid(row=0, column=0, sticky="nw")

        # Carica l'immagine di sfondo
        self.sfondo_img = Image.open("sfondoo.png")
        self.sfondo_img = self.sfondo_img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        self.sfondo = ImageTk.PhotoImage(self.sfondo_img)

        # Creazione del canvas con l'immagine di sfondo
        self.mappa = tk.Canvas(root, width=root.winfo_screenwidth() , height=root.winfo_screenheight())
        self.mappa.create_image(0, 0, anchor=tk.NW, image=self.sfondo)
        self.mappa.grid(row=1, column=0)

        # Carica l'immagine del drone
        self.drone_images = self.load_gif_frames("drone1.gif", root.winfo_screenwidth() , root.winfo_screenheight())

        # Creazione del frame per la tabella
        self.frame_tabella = tk.Frame(root, width=root.winfo_screenwidth() // 8, height=root.winfo_screenheight())
        self.frame_tabella.grid(row=1, column=1, padx=1)

        # Aggiungi etichetta nell'angolo alto a destra
        self.etichetta_angolo_alto_destra = tk.Label(root, text=" \n", font=("Helvetica", 16))
        self.etichetta_angolo_alto_destra.place(x=root.winfo_screenwidth()-20, y=0, anchor=tk.NE)

        self.centrale = tk.Label(root, text=" \n", font=("Helvetica", 16))
        self.centrale.place(x=root.winfo_screenwidth()-700, y=50, anchor=tk.NE)

        # Carica le coordinate da un file di testo
        self.coordinate = self.carica_coordinate_da_file("coordinate2.txt")

        # Avvia l'aggiornamento del tempo
        self.avvia_tempo()

    def load_gif_frames(self, filename, target_width=None, target_height=None):
        # Carica e restituisce una lista di frame GIF, ridimensionati
        gif = Image.open(filename)
        frames = [frame.copy().resize((target_width, target_height)) for frame in ImageSequence.Iterator(gif)]
        return [ImageTk.PhotoImage(frame) for frame in frames]

    def carica_coordinate_da_file(self, nome_file):
        coordinate = []
        with open(nome_file, 'r') as file:
            for line in file:
                tempo, x, y = map(int, line.strip().split(','))
                coordinate.append((x, y))
        return coordinate

    def avvia_tempo(self):
        self.mappa.bind("<Button-1>", self.controlla_tempo)  # Collega l'evento di click del mouse alla funzione controlla_tempo

    def controlla_tempo(self, event):
        if self.tempo == 0:
            self.aggiorna_tempo()

    def stampa_file_nome_inizia_con_X(self, cartella, tempo):
        files = os.listdir(cartella)
        trovato = False
        
        # Ciclare attraverso i file
        for file_name in files:
            if file_name.startswith(str(tempo) + "_"):
                trovato = True
                # Costruire il percorso completo del file
                percorso_file = os.path.join(cartella, file_name)
                # Aprire e leggere il contenuto del file
                with open(percorso_file, 'r') as file:
                    contenuto = file.readlines()
                    righe_centrale = []
                    righe_angolo_alto_destra = []
                    for riga in contenuto:
                        if riga.startswith("Ho trovato due incendi,"):
                            righe_centrale.append(riga)
                        elif riga.startswith(" più grave:"):
                            righe_centrale.append(riga)
                        else:
                            righe_angolo_alto_destra.append(riga)
                    
                    if righe_centrale:
                        testo_centrale = "".join("Ho trovato due incendi, \n gestirò prima quello piu grave")
                        self.centrale.config(text=testo_centrale)
                    
                    if righe_angolo_alto_destra:
                        testo_angolo_alto_destra = "".join(righe_angolo_alto_destra)
                        self.etichetta_angolo_alto_destra.config(text=testo_angolo_alto_destra)

        
        # Se nessun file è stato trovato
        if not trovato:
            self.etichetta_angolo_alto_destra.config(text="Sorvolo dell'area")
            self.centrale.config(text="")
        
        # Aggiornamento dell'interfaccia grafica
        self.root.update()  # oppure self.root.update_idletasks() se preferisci

    def individua_valori(self, cartella, tempo):
        files = os.listdir(cartella)
        ambulanzaN = 0
        ambulanzaVetN = 0
        richiestaVentilatori = False
        dueIncendiInsieme = False
        valori1 = 0
        canadair = False
        valori2 = 0
        # Ciclare attraverso i file
        for file_name in files:
            if file_name.startswith(str(tempo) + "_"):

                # Costruire il percorso completo del file
                percorso_file = os.path.join(cartella, file_name)
                # Aprire e leggere il contenuto del file
                with open(percorso_file, 'r') as file:
                    for i in file:
                        if i.startswith("richiesta di ventilatori manuali"):
                            # Trova l'intero successivo nel nome del file
                            try:
                                richiestaVentilatori = True
                            except ValueError:
                                continue  

                        if i.startswith("chiamata soccorso veterinaria: "):
                            # Trova l'intero successivo nel nome del file
                            try:
                                index = i.index(": ") + 2  # Indice dopo ": "
                                ambulanzaVetN = int(i[index:])
                            except ValueError:
                                continue  

                        if i.startswith("stato di allerta"):
                            # Trova l'intero successivo nel nome del file
                            try:
                                canadair = True
                            except ValueError:
                                continue 

                        if i.startswith("chiamata soccorso: "):
                            # Trova l'intero successivo nel nome del file
                            try:
                                index = i.index(": ") + 2  # Indice dopo ": "
                                ambulanzaN = int(i[index:])
                            except ValueError:
                                continue  
                        
                        
                        if i.startswith(" più grave: "):
                            # Trova l'intero successivo nel nome del file
                            try:
                                dueIncendiInsieme = True
                                valori = i[len(" più grave: ("):-1]  # Rimuovi il testo iniziale e la parentesi finale
                                valori_splittati = valori.split(" ")  # Dividi i valori utilizzando la virgola come separatore
                                valori_splittati2 = valori_splittati[3].split(",")
                                valori1 = int(valori_splittati2[0])
                                valori2 = int(valori_splittati2[1])
                            except ValueError:
                                continue
        return ambulanzaN,ambulanzaVetN,richiestaVentilatori,dueIncendiInsieme,valori1,valori2,canadair
        
    def aggiorna_tempo(self):
        self.tempo += 1
        self.etichetta_tempo.config(text=f"Tempo: {self.tempo}")
        t = self.tempo
        self.stampa_file_nome_inizia_con_X("fattiOrdinati", self.tempo)

        # Cerca le coordinate corrispondenti al tempo corrente nel file "coordinate.txt"
        tempo_presente = False
        coordinate_fuoco = None
        for line in open("coordinate2.txt", "r"):
            tempo_linea, x, y = map(int, line.strip().split(','))
            if tempo_linea == self.tempo:
                tempo_presente = True
                coordinate_fuoco = (x, y)
                #print(f"Tempo {self.tempo}, X = {x}, Y = {y}")
                break

        # Se il tempo corrente non è presente come primo valore nel file, mostra il drone
        if self.tempo < 10:
            if self.tempo == 1 or not tempo_presente:
                self.mostra_drone(self.tempo, self.tempo + 1, tempo_presente)
            else:
                self.ripristina_sfondo()
                self.mostra_fuoco(coordinate_fuoco,tempo_presente,self.tempo)
        else:
            self.ripristina_sfondo()
            self.etichetta_angolo_alto_destra.config(text = "Il drone è scarico\n ritorna alla base")
            self.root.update()

    def mostra_fuoco(self, coordinate_fuoco,tempo_presente,tempo):
        # Sostituisci lo sfondo con l'immagine del fuoco
        ambulanzaN,ambulanzaVetN,richiestaVentilatori,dueIncendiInsieme,x,y,canadair = self.individua_valori("fattiOrdinati", tempo)
        
        if coordinate_fuoco:   
            # Carica l'immagine del fuoco
            self.fuoco_frames = self.load_gif_frames("fuoco2.gif", 100, 100)  # Carica i frame della GIF del fuoco
            self.drone_frames = self.load_gif_frames("droneS.gif", 100, 100)  # Carica i frame della GIF del fuoco
            self.camion = self.load_gif_frames("camionPompieri.png", 100, 100)  # Carica i frame della GIF del fuoco
            
            # Rimuovi eventuali immagini del fuoco precedenti
            self.mappa.delete("camionPompieri")
            self.mappa.delete("fuoco")
            self.mappa.delete("droneS")

            if dueIncendiInsieme == True:
                self.fuoco_frames1 = self.load_gif_frames("fuoco2Bis.gif", 100, 100)  # Carica i frame della GIF del fuoco
                self.mappa.delete("fuoco2")
                
            if ambulanzaVetN or ambulanzaN >0:
                self.ambu_frames = self.load_gif_frames("ambu.png", 100, 100)  # Carica i frame della GIF del fuoco
                self.mappa.delete("ambu")
                
            if richiestaVentilatori == True:
                self.soccorso_frames = self.load_gif_frames("droneSoccorso.png", 100, 100)  # Carica i frame della GIF del fuoco
                self.mappa.delete("droneSoccorso")
            
            if canadair == True:
                self.canadair_frames = self.load_gif_frames("canadair3.gif", 100, 100)  # Carica i frame della GIF del fuoco
                self.mappa.delete("canadair")
            
            
            # Mostra l'immagine animata del fuoco alle coordinate specificate
            self.mostra_frame_fuoco(0, coordinate_fuoco,tempo_presente,ambulanzaN,ambulanzaVetN,richiestaVentilatori,dueIncendiInsieme,x,y,canadair)

    def mostra_frame_fuoco(self, index, coordinate_fuoco,tempo_presente,ambulanzaN,ambulanzaVetN,richiestaVentilatori,dueIncendiInsieme,x,y,canadair):
        #if index == len(self.fuoco_frames) and tempo_presente:
        #        self.mostra_fuoco(coordinate_fuoco,tempo_presente,0)  # Riparte la GIF del fuoco
        coordinate_fuoco2 = (x, y)

        if index < len(self.fuoco_frames):
            frame = self.fuoco_frames[index]
            self.mappa.create_image(coordinate_fuoco[0], coordinate_fuoco[1], anchor=tk.CENTER, image=frame, tags="fuoco")
            self.root.after(100, self.mostra_frame_fuoco, index + 1, coordinate_fuoco,tempo_presente,ambulanzaN,ambulanzaVetN,richiestaVentilatori,dueIncendiInsieme,x,y,canadair)

        if index < len(self.drone_frames):
                frame2 = self.drone_frames[0]
                self.mappa.create_image(coordinate_fuoco[0], coordinate_fuoco[1]-70, anchor=tk.CENTER, image=frame2, tags="droneS")
        
        if index < len(self.camion):
                frameC = self.camion[0]
                self.mappa.create_image(coordinate_fuoco[0], coordinate_fuoco[1]+150, anchor=tk.CENTER, image=frameC, tags="camionPompieri")
        
        if dueIncendiInsieme == True and x>0 and y>0:
            #print ("Sono due incendi insieme ")
            if index < len(self.fuoco_frames1):
                frameFuoco = self.fuoco_frames1[index]
                self.mappa.create_image(x, y, anchor=tk.CENTER, image=frameFuoco, tags="fuoco2")

        if ambulanzaVetN or ambulanzaN >0:
            if index < len(self.ambu_frames):
                frame3 = self.ambu_frames[0]
                self.mappa.create_image(coordinate_fuoco[0], coordinate_fuoco[1]+90, anchor=tk.CENTER, image=frame3, tags="ambu")
        
        if richiestaVentilatori == True:
            frame4 = self.soccorso_frames[0]
            self.mappa.create_image(coordinate_fuoco[0]-60, coordinate_fuoco[1]-70, anchor=tk.CENTER, image=frame4, tags="droneSoccorso")

        if canadair == True:
            if index < len(self.canadair_frames):
                frame5 = self.canadair_frames[index]
                self.mappa.create_image(coordinate_fuoco[0], coordinate_fuoco[1]-220, anchor=tk.CENTER, image=frame5, tags="canadair")
                #self.root.after(20, self.mostra_frame_fuoco, index + 1, coordinate_fuoco,tempo_presente,ambulanzaN,ambulanzaVetN,richiestaVentilatori,dueIncendiInsieme,x,y,canadair)

            
    def load_gif_frames(self, filename, target_width=None, target_height=None):
        
        # Carica e restituisce una lista di frame GIF, ridimensionati
        gif = Image.open(filename)
        frames = [frame.copy().resize((target_width, target_height)) for frame in ImageSequence.Iterator(gif)]
        return [ImageTk.PhotoImage(frame) for frame in frames]
    
    def mostra_drone(self,t,t1,tempo_presente):
        # Sostituisci lo sfondo con la GIF del drone
        self.sostituisci_sfondo_con_gif(t, t1,tempo_presente)

    def sostituisci_sfondo_con_gif(self, start_time, end_time,tempo_presente):
        # Carica le immagini della GIF
        self.gif_frames = self.load_gif_frames("drone.gif", self.root.winfo_screenwidth(), self.root.winfo_screenheight())

        # Funzione per mostrare i frame della GIF per un intervallo di tempo specifico
        def show_gif_frames(index):
            if index < len(self.gif_frames) and start_time <= self.tempo < end_time:
                frame = self.gif_frames[index]
                self.mappa.create_image(0, 0, anchor=tk.NW, image=frame)
                self.root.after(100, show_gif_frames, index + 1)
            elif self.tempo == 1 or not tempo_presente:  
                #Se il tempo è esattamente uguale a 1 o se il tempo corrente non è presente nel file, ricomincia a mostrare la GIF
                self.root.after(100, show_gif_frames, 0)
            else:
                self.ripristina_sfondo()

        # Avvia la visualizzazione dei frame della GIF
        show_gif_frames(0)

    def ripristina_sfondo(self):
        # Ripristina lo sfondo
        self.mappa.create_image(0, 0, anchor=tk.NW, image=self.sfondo)

    def onClick(self):
        self.aggiorna_tempo()  # Chiamata per aggiornare il tempo



def main():
    root = tk.Tk()
    
    
    trasforma("modello.txt")
    codice_asp = leggi_file_asp('codicePerGrafica.lp')
    fatti = leggi_fatti_da_file("fatti.txt")
    esegui_codice_asp(codice_asp, fatti)

    coordinate = crea_dic("coordinate2.txt")
    app = ApplicazioneGrafica(root)
    leggi_coordinate_da_file(coordinate)
    root.mainloop()

if __name__ == "__main__":
    main()
