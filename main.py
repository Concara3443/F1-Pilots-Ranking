import random
import tkinter as tk
from PIL import Image, ImageTk
import urllib.request
import io
from glicko import Glicko2

ZOOM = False # Set to True to zoom in on the pilot faces

class Pilot:
    def __init__(self, name, image_url):
        self.name = name
        self.rating = 1500
        self.rd = 350
        self.volatility = 0.06
        self.image_url = image_url

pilots = [
    Pilot("Lewis Hamilton", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/hamilton.jpg"),
    Pilot("Max Verstappen", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/verstappen.jpg"),
    Pilot("Charles Leclerc", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/leclerc.jpg"),
    Pilot("Valtteri Bottas", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/bottas.jpg"),
    Pilot("Sergio Perez", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/perez.jpg"),
    Pilot("Lando Norris", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/norris.jpg"),
    Pilot("Daniel Ricciardo", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/ricciardo.jpg"),
    Pilot("Carlos Sainz", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/sainz.jpg"),
    Pilot("Pierre Gasly", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/gasly.jpg"),
    Pilot("Esteban Ocon", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/ocon.jpg"),
    Pilot("Fernando Alonso", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/alonso.jpg"),
    Pilot("Yuki Tsunoda", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/tsunoda.jpg"),
    Pilot("George Russell", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/russell.jpg"),
    Pilot("Alexander Albon", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/albon.jpg"),
    Pilot("Logan Sargeant", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/sargeant.jpg"),
    Pilot("Oscar Piastri", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/piastri.jpg"),
    Pilot("Kevin Magnussen", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/magnussen.jpg"),
    Pilot("Nico Hülkenberg", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/hulkenberg.jpg"),
    Pilot("Lance Stroll", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/stroll.jpg"),
    Pilot("Zhou Guanyu", "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/2024Drivers/zhou.jpg")
]

def load_image(url):
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    im = Image.open(io.BytesIO(raw_data))
    
    if ZOOM:
        width, height = im.size
        left = width * 0.35
        top = height * 0.05
        right = width * 0.65
        bottom = height * 0.45
        im = im.crop((left, top, right, bottom))
        im.thumbnail((200, 200))
    else:
        im = im.resize((200, 200))
    
    return ImageTk.PhotoImage(im)

pilot_images_urls = {pilot.name: pilot.image_url for pilot in pilots}

def preload_images(root):
    images = {}
    for name, url in pilot_images_urls.items():
        images[name] = load_image(url)
    return images

def update_comparison_frame(pilot1, pilot2, images, comparison_frame, compare_pilots):
    for widget in comparison_frame.winfo_children():
        widget.destroy()

    label_instructions = tk.Label(comparison_frame, text="Elige tu piloto favorito o selecciona 'Empate':", font=("Helvetica", 14))
    label_instructions.pack(pady=10)

    frame_pilots = tk.Frame(comparison_frame)
    frame_pilots.pack()

    def choose_pilot(preferred, not_preferred, drawn):
        compare_pilots.selected = (preferred, not_preferred, drawn)
        comparison_frame.event_generate("<<SelectionMade>>")

    # Pilot 1
    frame1 = tk.Frame(frame_pilots)
    frame1.pack(side="left", padx=20)
    label1 = tk.Label(frame1, text=pilot1.name)
    label1.pack()
    img_label1 = tk.Label(frame1, image=images[pilot1.name])
    img_label1.pack()
    button1 = tk.Button(frame1, text="Elegir", command=lambda: choose_pilot(pilot1, pilot2, False))
    button1.pack(pady=5)

    # Pilot 2
    frame2 = tk.Frame(frame_pilots)
    frame2.pack(side="left", padx=20)
    label2 = tk.Label(frame2, text=pilot2.name)
    label2.pack()
    img_label2 = tk.Label(frame2, image=images[pilot2.name])
    img_label2.pack()
    button2 = tk.Button(frame2, text="Elegir", command=lambda: choose_pilot(pilot2, pilot1, False))
    button2.pack(pady=5)

    # Empate
    draw_button = tk.Button(comparison_frame, text="Empate", command=lambda: choose_pilot(pilot1, pilot2, True))
    draw_button.pack(pady=10)

def update_results_window(results_frame, pilots):
    for widget in results_frame.winfo_children():
        widget.destroy()
    sorted_pilots = sorted(pilots, key=lambda p: p.rating, reverse=True)
    tk.Label(results_frame, text="Clasificación de Pilotos", font=("Helvetica", 16)).pack(pady=10)
    for i, pilot in enumerate(sorted_pilots, start=1):
        tk.Label(results_frame, text=f"{i}. {pilot.name}: {pilot.rating:.2f}", font=("Helvetica", 12)).pack()

def main():
    root = tk.Tk()
    root.title("Comparación y Clasificación de Pilotos")

    images = preload_images(root)

    # Results
    results_frame = tk.Frame(root)
    results_frame.pack(side="left", padx=20)

    # Comp
    comparison_frame = tk.Frame(root)
    comparison_frame.pack(side="right", padx=20)

    update_results_window(results_frame, pilots)

    glicko = Glicko2()
    duels = set()
    total_duels = len(pilots) * 2

    def compare_pilots():
        if len(duels) >= total_duels:
            for widget in comparison_frame.winfo_children():
                widget.destroy()
            tk.Label(comparison_frame, text="¡Comparaciones completadas!", font=("Helvetica", 16)).pack(pady=20)
            return
        while True:
            pilot1, pilot2 = random.sample(pilots, 2)
            duel = tuple(sorted([pilot1.name, pilot2.name]))
            if duel not in duels:
                duels.add(duel)
                break
        update_comparison_frame(pilot1, pilot2, images, comparison_frame, compare_pilots)

        def on_selection_made(event):
            preferred, not_preferred, drawn = compare_pilots.selected
            preferred_rating = glicko.create_rating(preferred.rating, preferred.rd, preferred.volatility)
            not_preferred_rating = glicko.create_rating(not_preferred.rating, not_preferred.rd, not_preferred.volatility)
            new_ratings = glicko.rate_1vs1(preferred_rating, not_preferred_rating, drawn)
            preferred.rating, preferred.rd, preferred.volatility = new_ratings[0].mu, new_ratings[0].phi, new_ratings[0].sigma
            not_preferred.rating, not_preferred.rd, not_preferred.volatility = new_ratings[1].mu, new_ratings[1].phi, new_ratings[1].sigma
            update_results_window(results_frame, pilots)
            compare_pilots()

        comparison_frame.bind("<<SelectionMade>>", on_selection_made)

    compare_pilots()

    root.mainloop()

if __name__ == "__main__":
    main()