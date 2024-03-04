import pygame
import random
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
    
Point = namedtuple('Point', 'x, y')

# directions
up = 1
right = 2
down = 3
left = 4

# colours
blue = (65, 105, 225)
red = (220,20,60)
green1 = (34, 139, 34)
green2 = (0, 100, 0)
black = (0,0,0)

block_size = 20
speed = 20

class SnakeGame:

    def __init__(self, w=640, h=480):
        self.width = w
        self.height = h

        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        

        self.direction = right
        
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head, Point(self.head.x-block_size, self.head.y), Point(self.head.x-(2*block_size), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.width - block_size) // block_size) * block_size 
        y = random.randint(0, (self.height - block_size) // block_size) * block_size
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self):
        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != right:
                    self.direction = left
                elif event.key == pygame.K_RIGHT and self.direction != left:
                    self.direction = right
                elif event.key == pygame.K_UP and self.direction != down:
                    self.direction = up
                elif event.key == pygame.K_DOWN and self.direction != up:
                    self.direction = down
        
        # move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # if food eaten, place new food. if not, move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # update ui and clock
        self._update_ui()
        self.clock.tick(speed)

        # return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # hits boundary
        if self.head.x > self.width - block_size or self.head.x < 0 or self.head.y > self.height - block_size or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(black)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, green1, pygame.Rect(pt.x, pt.y, block_size, block_size))
            pygame.draw.rect(self.display, green2, pygame.Rect(pt.x+2, pt.y+2, 16, 16))
            
        pygame.draw.rect(self.display, red, pygame.Rect(self.food.x, self.food.y, block_size, block_size))
        
        text = font.render("Score: " + str(self.score), True, blue)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == right:
            x += block_size
        elif direction == left:
            x -= block_size
        elif direction == down:
            y += block_size
        elif direction == up:
            y -= block_size
            
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    game_over = False
    while not game_over:
        game_over, score = game.play_step()
        # play step will set game_over = True when its conditions are passed
        
    print('Final Score', score)
        
        
    pygame.quit()