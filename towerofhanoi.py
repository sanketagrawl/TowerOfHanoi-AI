import pygame
import time
import random

# Constants
WIDTH, HEIGHT = 600, 500
WHITE, BLACK, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi AI Search")
font = pygame.font.Font(None, 36)

class TowerOfHanoi:
    def __init__(self):
        self.num_disks = random.randint(3, 7)  # Random number between 3 and 7
        self.paused = False
        self.running = False
        self.move_index = 0
        self.reset_game()
    
    def reset_game(self):
        self.towers = [[i for i in range(self.num_disks, 0, -1)], [], []]
        self.moves = []
        hanoi(self.num_disks, 0, 2, 1, self.moves)
        self.running = False
        self.paused = False
        self.move_index = 0
        self.draw_towers()
        pygame.display.flip()
    
    def draw_towers(self):
        screen.fill(WHITE)
        for x in [150, 300, 450]:
            pygame.draw.rect(screen, BLACK, (x - 5, 150, 10, 200))
        
        for peg in range(3):
            for i, disk in enumerate(self.towers[peg]):
                width = disk * 20
                pygame.draw.rect(screen, RED, (150 + peg * 150 - width//2, 350 - i*20, width, 20))
        
        pygame.draw.rect(screen, GREEN, (50, 420, 100, 50))  # Start Button
        pygame.draw.rect(screen, BLUE, (200, 420, 100, 50))  # Reset Button
        pygame.draw.rect(screen, BLACK, (350, 420, 100, 50))  # Pause Button
        
        screen.blit(font.render("Start", True, WHITE), (75, 435))
        screen.blit(font.render("Reset", True, WHITE), (225, 435))
        screen.blit(font.render("Pause", True, WHITE), (375, 435))
        screen.blit(font.render(f"Disks: {self.num_disks}", True, BLACK), (480, 435))
    
    def play_solution(self):
        if self.running and not self.paused and self.move_index < len(self.moves):
            move = self.moves[self.move_index]
            disk = self.towers[move[0]].pop()
            self.towers[move[1]].append(disk)
            self.move_index += 1
            self.draw_towers()
            pygame.display.flip()
            time.sleep(1.0)
        if self.move_index >= len(self.moves):
            self.running = False
    
    def handle_mouse_click(self, pos):
        x, y = pos
        if 50 <= x <= 150 and 420 <= y <= 470:  # Start Button
            if not self.running:
                self.running = True
                self.paused = False
        elif 200 <= x <= 300 and 420 <= y <= 470:  # Reset Button
            self.reset_game()
        elif 350 <= x <= 450 and 420 <= y <= 470:  # Pause Button
            if self.running:
                self.paused = not self.paused  # Toggle pause
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(pygame.mouse.get_pos())
            
            if self.running and not self.paused:
                self.play_solution()
        pygame.quit()

# Recursive function to generate moves
def hanoi(n, source, target, auxiliary, moves):
    if n == 1:
        moves.append((source, target))
        return
    hanoi(n-1, source, auxiliary, target, moves)
    moves.append((source, target))
    hanoi(n-1, auxiliary, target, source, moves)

# Start the Game
game = TowerOfHanoi()
game.run()
