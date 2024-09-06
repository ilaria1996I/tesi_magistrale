import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

# Funzione per animare la GIF
def anima_gif(indice):
    global img, timer_value
    frame = frames[indice]
    img = ImageTk.PhotoImage(frame)
    canvas.itemconfig(immagine_gif, image=img)
    indice = (indice + 1) % len(frames)
    finestra.after(100, anima_gif, indice)  # 100 millisecondi di intervallo

# Funzione per gestire il clic del bottone
def incrementa_tempo():
    global timer_value
    timer_value += 1
    tempo_label.config(text="Tempo: " + str(timer_value))

# Crea la finestra
finestra = tk.Tk()

# Carica lo sfondo
sfondo = Image.open('sfondoo.png')
larghezza, altezza = sfondo.size

# Crea un canvas
canvas = tk.Canvas(finestra, width=larghezza, height=altezza)
canvas.pack()

# Carica la GIF e ottieni i frame
gif_fuoco = Image.open('fuoco2.gif')
frames = [frame.copy() for frame in ImageSequence.Iterator(gif_fuoco)]

# Carica il frame iniziale
img = ImageTk.PhotoImage(frames[0])

# Posiziona lo sfondo sul canvas
sfondo = ImageTk.PhotoImage(sfondo)
sfondo_id = canvas.create_image(0, 0, anchor=tk.NW, image=sfondo)

# Posiziona la GIF sul canvas
immagine_gif = canvas.create_image(larghezza//2, altezza//2, image=img)

# Avvia l'animazione della GIF
indice = 0
anima_gif(indice)

# Aggiungi un bottone per incrementare il tempo
bottone = tk.Button(finestra, text="Incrementa Tempo", command=incrementa_tempo)
bottone.pack()

# Variabile per tenere traccia del tempo
timer_value = 0

# Label per mostrare il tempo
tempo_label = tk.Label(finestra, text="Tempo: " + str(timer_value))
tempo_label.pack()

# Avvia la finestra
finestra.mainloop()
