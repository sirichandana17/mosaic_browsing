import tkinter as tk
from tkinter import messagebox
import random
import pygame

class MosaicMotifFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("MOSAIC BROWSING")
        self.root.geometry("800x800")
        self.root.attributes('-fullscreen', True)
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.welcome_frame = tk.Frame(self.main_frame, bg="lightblue")
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.welcome_frame, bg="lightblue")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.create_welcome_page()

        self.rules_frame = tk.Frame(self.main_frame, bg="lightyellow")
        self.app_frame = tk.Frame(self.main_frame)

        self.score = 0  
        self.selected_cells = []  

        pygame.mixer.init()
        self.sound_dict = {
            "start": pygame.mixer.Sound("90s-game-ui-7-185100.mp3"),
            "next": pygame.mixer.Sound("button-pressed-38129.mp3"),
            "find_motif": pygame.mixer.Sound("game-bonus-144751.mp3"),
            "restart": pygame.mixer.Sound("bonussound.mp3.wav"),
            "exit": pygame.mixer.Sound("game-fx-9-40197.mp3"),
            "motif_not_found": pygame.mixer.Sound("080205_life-lost-game-over-89697.mp3"),
            "mosaic": pygame.mixer.Sound("microwave-button-82493.mp3"),
            "background_music": pygame.mixer.Sound("Sakura-Girl-Daisy-chosic.com_.mp3")
        }

        self.sound_dict["background_music"].set_volume(0.2)

        self.play_sound("background_music", loop=True)

        # Initialize squares for animation
        self.squares = self.create_squares(75)
        self.animate_squares()
    
    def play_sound(self, sound_name, loop=False):
        """Play sound effect."""
        sound = self.sound_dict[sound_name]
        sound.play(loops=-1 if loop else 0)

    def create_welcome_page(self):
        """Create the welcome page with a title and start button."""
        title_frame = tk.Frame(self.welcome_frame, bg="lightblue")
        title_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)  

        self.welcome_label = tk.Label(title_frame, text="MOSAIC BROWSING", font=("Helvetica", 50, "bold"),
                                      bg="lightblue")
        self.welcome_label.pack()

        button_frame = tk.Frame(self.welcome_frame, bg="lightblue")
        button_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)  

        self.start_button = tk.Button(button_frame, text="Start", command=self.show_rules, font=("Helvetica", 18),
                                      fg="white", bg="black")
        self.start_button.pack(pady=10)
        self.start_button.bind("<Button-1>", lambda event: self.play_sound("start"))

        self.welcome_frame.pack_propagate(False)

        self.animate_start_button()

    def create_squares(self, count):
        """Create a list of squares with random positions and velocities."""
        squares = []
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        for _ in range(count):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            size = random.randint(20, 50)
            vx = random.choice([-1, 1]) * random.uniform(2, 5)  
            vy = random.choice([-1, 1]) * random.uniform(2, 5)  
            squares.append({"x": x, "y": y, "size": size, "vx": vx, "vy": vy})
        return squares

    def animate_squares(self):
        """Animate the squares by updating their positions and redrawing them."""
        self.canvas.delete("square")
        for square in self.squares:
            square["x"] += square["vx"]
            square["y"] += square["vy"]
            if square["x"] <= 0 or square["x"] + square["size"] >= self.root.winfo_width():
                square["vx"] *= -1
            if square["y"] <= 0 or square["y"] + square["size"] >= self.root.winfo_height():
                square["vy"] *= -1
            self.canvas.create_rectangle(square["x"], square["y"], square["x"] + square["size"],
                                         square["y"] + square["size"], fill="white", tags="square")
        self.root.after(20, self.animate_squares)

    def animate_start_button(self):
        """Animate the start button by changing its color."""
        colors = ["grey", "black"]
        current_color = colors[random.randint(0, len(colors) - 1)]

        def change_color():
            nonlocal current_color
            next_color = random.choice([color for color in colors if color != current_color])
            self.start_button.config(bg=next_color)
            current_color = next_color
            self.root.after(500, change_color)

        change_color()

    def show_rules(self):
        """Show the rules page and hide the welcome page."""
        self.welcome_frame.pack_forget()
        self.rules_frame.pack(fill=tk.BOTH, expand=True)
        self.create_rules_page()

    def create_rules_page(self):

        """Create the rules page with instructions and a next button."""
        instructions_frame = tk.Frame(self.rules_frame, bg="lightyellow")
        instructions_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=(self.root.winfo_screenheight() // 10, 20))

        rules = (
            "INSTRUCTIONS:\n"
            "\n"
            "1. The Mosaic is a 10x10 grid of randomly colored cells.\n"
            "2. The Motif is a 2x2 grid of randomly colored cells.\n"
            "3. Click on a 2x2 region in the mosaic to select it.\n"
            "4. Click 'Find Motif' to check if the selected region matches the motif.\n"
            "5. If the motif is found, it will be highlighted in the mosaic.\n"
            "6. If the selected region does not match the motif, the correct motif will be highlighted.\n"
            "7. Click 'Restart' to generate a new motif.\n"
            "8. Click 'Exit' to close the application."
        )

        rules_label = tk.Label(instructions_frame, text=rules, font=("Helvetica", 18), bg="lightyellow",justify=tk.LEFT)
        rules_label.pack(padx=20)

        button_frame = tk.Frame(self.rules_frame, bg="lightyellow")
        button_frame.pack(side=tk.TOP,pady=(20, 10))

        next_button = tk.Button(button_frame, text="Next", command=self.start_application, font=("Helvetica", 18), bg="white", fg="black")
        next_button.pack()
        next_button.bind("<Button-1>", lambda event: self.play_sound("next"))

        self.rules_frame.pack_propagate(False)

    def start_application(self):
        """Start the main application and hide the rules page."""
        self.rules_frame.pack_forget()
        self.app_frame.pack(fill=tk.BOTH, expand=True)
        self.create_application_page()

    def create_application_page(self):
        self.app_frame.config(bg="black")
        """Create the main application page with mosaic and motif canvases and control buttons."""

        container_frame = tk.Frame(self.app_frame)
        container_frame.pack(expand=True)

        self.mosaic_frame = tk.Frame(container_frame)
        self.mosaic_frame.pack(side=tk.LEFT, padx=50, pady=20)
        self.motif_frame = tk.Frame(container_frame)
        self.motif_frame.pack(side=tk.LEFT, padx=50, pady=20)

        tk.Label(self.mosaic_frame, text="MOSAIC", font=("Helvetica", 24)).pack()
        self.mosaic_canvas = tk.Canvas(self.mosaic_frame, width=500, height=500)
        self.mosaic_canvas.pack()
        self.mosaic_canvas.bind("<Button-1>", self.on_mosaic_click)

        tk.Label(self.motif_frame, text="MOTIF", font=("Helvetica", 24)).pack()
        self.motif_canvas = tk.Canvas(self.motif_frame, width=100, height=100)
        self.motif_canvas.pack()

        self.button_frame = tk.Frame(self.motif_frame)
        self.button_frame.pack(pady=20)

        self.find_button = tk.Button(self.button_frame, text="Find Motif", command=self.find_motif,
                                     font=("Helvetica", 18), bg="black", fg="white")
        self.find_button.pack(pady=10)

        self.restart_button = tk.Button(self.button_frame, text="\u21BB", command=self.restart_application,
                                        font=("Helvetica", 25, "bold"), bg="light blue", fg="black", width=1, height=0)
        self.restart_button.config(width=4, height=1)
        self.restart_button.pack(pady=10)
        self.restart_button.bind("<Button-1>", lambda event: self.play_sound("restart"))

        self.exit_button = tk.Button(self.button_frame, text="\u2716", command=self.exit_application,
                                     font=("Helvetica", 25), bg="brown", fg="white", width=1, height=0)
        self.exit_button.config(width=4, height=1)
        self.exit_button.pack(pady=10)
        self.exit_button.bind("<Button-1>", lambda event: self.play_sound("exit"))

        self.result_label = tk.Label(self.motif_frame, text="", font=("Helvetica", 18), fg="red")
        self.result_label.pack(pady=20)

        self.score_label = tk.Label(self.motif_frame, text=f"Score: {self.score}", font=("Helvetica", 18), fg="black")
        self.score_label.pack(pady=20)

        self.draw_motif()
        self.draw_mosaic()

    def draw_mosaic(self):
        """Generate and draw a new 10x10 mosaic grid."""
        self.mosaic = self.generate_random_grid(10, 10)
        self.insert_motif_into_mosaic()
        self.draw_grid(self.mosaic_canvas, self.mosaic, 50)

    def draw_motif(self):
        """Generate and draw a new 2x2 motif grid."""
        self.motif = self.generate_random_grid(2, 2)
        self.draw_grid(self.motif_canvas, self.motif, 50)

    def generate_random_grid(self, rows, cols):
        """Generate a grid with random colors."""
        colors = ['R', 'G', 'Y']
        return [[random.choice(colors) for _ in range(cols)] for _ in range(rows)]

    def draw_grid(self, canvas, grid, size):
        """Draw the given grid on the specified canvas."""
        colors = {'R': 'red', 'G': 'green', 'Y': 'yellow', '': 'white'}
        canvas.delete("all")
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                color = colors[cell]
                canvas.create_rectangle(j * size, i * size, (j + 1) * size, (i + 1) * size, fill=color, outline='black')

    def insert_motif_into_mosaic(self):
        """Insert the motif into a random position within the mosaic."""
        motif = self.motif
        mosaic = self.mosaic
        mosaic_rows = len(mosaic)
        mosaic_cols = len(mosaic[0])
        motif_rows = len(motif)
        motif_cols = len(motif[0])

        # Choose a random position to insert the motif
        self.motif_position = (random.randint(0, mosaic_rows - motif_rows), random.randint(0, mosaic_cols - motif_cols))
        row, col = self.motif_position

        for i in range(motif_rows):
            for j in range(motif_cols):
                mosaic[row + i][col + j] = motif[i][j]

    def highlight_matches(self, positions, motif, color="black"):
        """Highlight the found motifs in the mosaic."""
        size = 50
        for pos in positions:
            row, col = pos
            x1, y1 = col * size, row * size
            x2, y2 = (col + len(motif[0])) * size, (row + len(motif)) * size
            self.mosaic_canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=8, tags="highlight")

    def find_motif(self):
        """Check if the selected cells match the motif and update the score."""
        if not self.selected_cells:
            self.result_label.config(text="Please select a 2x2 region")
            return

        motif = self.motif
        selected_mosaic = [
            [self.mosaic[row][col] for col in range(self.selected_cells[0][1], self.selected_cells[0][1] + 2)]
            for row in range(self.selected_cells[0][0], self.selected_cells[0][0] + 2)
        ]

        if selected_mosaic == motif:
            self.score += 10
            self.result_label.config(text="Motif found!", fg="green")
            self.highlight_matches([self.selected_cells[0]], motif)
            self.play_sound("find_motif")
        else:
            self.result_label.config(text="Motif didn't match", fg="red")
            self.highlight_matches([self.motif_position], motif, color="blue")
            self.play_sound("motif_not_found")

        self.score_label.config(text=f"Score: {self.score}")

    def clear_highlights(self):
        """Clear any highlights from the mosaic canvas."""
        self.mosaic_canvas.delete("highlight")
        self.mosaic_canvas.delete("selection")

    def on_mosaic_click(self, event):
        """Handle click events on the mosaic canvas."""
        x, y = event.x, event.y
        row, col = y // 50, x // 50
        if row < 9 and col < 9:
            self.selected_cells = [(row, col), (row, col + 1), (row + 1, col), (row + 1, col + 1)]
            self.highlight_selection()

    def highlight_selection(self):
        """Highlight the selected cells on the mosaic canvas."""
        self.mosaic_canvas.delete("selection")
        size = 50
        for cell in self.selected_cells:
            row, col = cell
            x1, y1 = col * size, row * size
            x2, y2 = (col + 1) * size, (row + 1) * size
            self.mosaic_canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=3, tags="selection")
        self.play_sound("mosaic")
    
    def restart_application(self):
        """Restart the application by generating new grids and clearing highlights."""
        self.clear_highlights()
        self.result_label.config(text="")
        self.draw_motif()
        self.draw_mosaic()

    def exit_application(self):
        """Exit the application and show the final score."""
        messagebox.showinfo("Score", f"Your score is {self.score}")
        self.root.destroy()

root = tk.Tk()
app = MosaicMotifFinder(root)
root.mainloop()