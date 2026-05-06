import tkinter as tk
import random

# Konstanty
WIDTH = 600
HEIGHT = 400
GRID_SIZE = 20
DELAY = 100  # Rychlost hry v ms

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game - Inverted")
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        
        # Had začíná dlouhý (10 článků)
        self.snake = [(100 + i * GRID_SIZE, 100) for i in range(10)][::-1]
        self.direction = "Right"
        self.food = None
        self.score = len(self.snake)
        
        self.score_label = tk.Label(root, text=f"Délka hada: {self.score}", font=("Arial", 14))
        self.score_label.pack()
        
        self.root.bind("<KeyPress>", self.change_direction)
        
        self.spawn_food()
        self.run()

    def spawn_food(self):
        while True:
            x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            self.food = (x, y)
            if self.food not in self.snake:
                break

    def change_direction(self, event):
        new_dir = event.keysym
        all_dirs = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_dir in all_dirs and new_dir != all_dirs.get(self.direction):
            self.direction = new_dir

    def move(self):
        head_x, head_y = self.snake[0]
        
        if self.direction == "Up":
            head_y -= GRID_SIZE
        elif self.direction == "Down":
            head_y += GRID_SIZE
        elif self.direction == "Left":
            head_x -= GRID_SIZE
        elif self.direction == "Right":
            head_x += GRID_SIZE
            
        new_head = (head_x, head_y)
        
        # Kontrola kolize se zdí nebo sebou samým (kromě ocasu, který se posune)
        if (head_x < 0 or head_x >= WIDTH or 
            head_y < 0 or head_y >= HEIGHT or 
            new_head in self.snake[:-1]):
            self.game_over()
            return False
            
        self.snake.insert(0, new_head)
        
        # Kontrola jídla - zkrácení
        if new_head == self.food:
            # Smazání jídla a zkrácení o jeden článek (poprvé za pohyb, podruhé navíc)
            self.snake.pop() # Normální posun (ocas pryč)
            self.snake.pop() # Zkrácení o další článek
            
            self.score = len(self.snake)
            self.score_label.config(text=f"Délka hada: {self.score}")
            
            if self.score <= 1:
                self.victory()
                return False
                
            self.spawn_food()
        else:
            self.snake.pop() # Normální posun
            
        return True

    def draw(self):
        self.canvas.delete("all")
        
        # Vykreslení jídla
        fx, fy = self.food
        self.canvas.create_oval(fx, fy, fx + GRID_SIZE, fy + GRID_SIZE, fill="red")
        
        # Vykreslení hada
        for i, (sx, sy) in enumerate(self.snake):
            color = "green" if i == 0 else "darkgreen"
            self.canvas.create_rectangle(sx, sy, sx + GRID_SIZE, sy + GRID_SIZE, fill=color, outline="black")

    def run(self):
        if self.move():
            self.draw()
            self.root.after(DELAY, self.run)

    def game_over(self):
        self.canvas.create_text(WIDTH/2, HEIGHT/2, text="KONEC HRY", fill="white", font=("Arial", 30))
        self.root.after(2000, self.root.destroy)

    def victory(self):
        self.draw() # Poslední vykreslení hada s délkou 1
        self.canvas.create_text(WIDTH/2, HEIGHT/2, text="VÍTĚZSTVÍ!", fill="yellow", font=("Arial", 30))
        self.root.after(3000, self.root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
