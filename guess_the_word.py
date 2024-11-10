import pygame
import sys
import os

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
screenWidth = 1280
ScreenHigh = 720
screen = pygame.display.set_mode((screenWidth,ScreenHigh)) 
clock = pygame.time.Clock()
main_font = pygame.font.Font("Fonts/funy_font.ttf",50)
font = pygame.font.Font(None, 70)
textFont = pygame.font.Font(None, 30)
icon = pygame.image.load("icon.png")
pygame.display.set_caption("Guess the Word Game")
pygame.display.set_icon(icon)
class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos - 120, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True,"black")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.clicked = False
        
        

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    def checkForInput(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.text_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        return action
        
      
    def changeColor(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right + 150) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "black")
    
class Level:
    def __init__(self):
        self.textMain = pygame.image.load("background/bacWite.png")
        self.TextMain = pygame.transform.scale(self.textMain,(600,200))
        self.levelBg = pygame.image.load("Background/background_1.png")
        self.LevelBg = pygame.transform.scale(self.levelBg,(1280,720))
        self.levels = [["cow", "Levels/cow.png"],["family","Levels/family.png"],["hot","Levels/hot.png"],
                       ["wine","Levels/wine.png"],["swimming","Levels/swimming.png"],["sad","Levels/sad.png"],
                       ["boy","Levels/boy.png"],["cold","Levels/cold.png"],["cowboy","Levels/cowboy.png"],
                       ["dust","Levels/dust.png"],["love","Levels/love.png"],["party","Levels/party.png"],
                       ["quran","Levels/quran.png"],["yoga","Levels/yoga.jpg"],["travel","Levels/travel.png"],
                       ["draw","Levels/draw.png"],["fastfood","Levels/fastFood.png"],["adventure","Levels/adventure.png"],
                       ["motivation","Levels/motivation.png"],["finish","Levels/finish.png"]
                       ]           
        self.current_level = 0
        self.game_over = False
        self.game_over = False
        self.attempts = 3
    def load_new_word(self):
        global word, image, guessed_letters
        guessed_letters = []
        word = self.levels[self.current_level][0]
        image_path = self.levels[self.current_level][1]
        self.attempts = 3
    
        
        if os.path.exists(image_path):
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image,(600,400))
        else:
            print(f"Error: The image {image_path} does not exist.")
            pygame.quit()
            sys.exit()
            
    
    def get_hint(self,word, guessed_letters):
        hint = ""
        for letter in word:
            if letter in guessed_letters:
                hint += letter + " "
            else:
                hint += "_ "
        return hint.strip()
    
    def drawText(self):
        hint_text = font.render(f"{self.get_hint(word, guessed_letters)}", True, "black")
        screen.blit(hint_text, (530, 420))

        attempts_text = textFont.render(f"Remaining Attempts: {self.attempts}", True, "black")
        screen.blit(attempts_text, (530, 500))
        if self.game_over:
            if self.attempts > 0:
                end_text = textFont.render("Congratulations! You guessed the word!", True, "black")
            else:
                end_text = textFont.render(f"You lost! The word was: {word}", True, "black")
            screen.blit(end_text, (450, 520))

            restart_text = textFont.render("Press 'R' to restart or 'N' for the next level.", True, "black")
            screen.blit(restart_text, (450, 540))
            
    def reset_game(self):       
        self.current_level = 0
        self.game_over = False
        self.load_new_word()
        
    def next_level(self):
        
        if self.current_level < len(self.levels) - 1:
            self.current_level += 1
            self.game_over = False
            self.load_new_word()
        else:
            print("You have completed all levels!")
            self.reset_game()
    
    
    def Run(self):
        self.load_new_word()
        
        while True:
            screen.fill("black")
            screen.blit(self.LevelBg,(0,0))
            screen.blit(image,(340,5))
            screen.blit(self.TextMain,(340,405))
            self.drawText()
            
    
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:  
                            self.reset_game()
                        elif event.key == pygame.K_n:  
                            self.next_level()
                    else:
                        if event.unicode.isalpha() and len(event.unicode) == 1:
                            guess = event.unicode.lower()
                            if guess in guessed_letters:
                                print("You've already guessed that letter.")
                            elif guess in word:
                                guessed_letters.append(guess)
                                print("Correct! The letter is in the word.")
                            else:
                                self.attempts -= 1
                                print("Incorrect! That letter is not in the word.")

                            
                            if all(letter in guessed_letters for letter in word):
                                self.game_over = True
                            elif self.attempts == 0:
                                self.game_over = True
                    
            pygame.display.update()
        
        
level = Level()       
bg = pygame.image.load("Background/background_2.png")
#menuIcon = pygame.image.load("Menu/menu.png")
#menuIconSurface = pygame.transform.scale(menuIcon,(50,50))
#menu = Button(menuIconSurface,640,360, "main menu")

playIcon = pygame.image.load("Menu/play.png")
playIconSurface = pygame.transform.scale(playIcon,(50,50))
play = Button(playIconSurface,640,420, "play")

#infoIcon = pygame.image.load("Menu/info.png")
#infoIconSurface = pygame.transform.scale(infoIcon,(50,50))
#info = Button(infoIconSurface,640,480, "info")

#soundIcon = pygame.image.load("Menu/sound.png")
#soundIconSurface = pygame.transform.scale(soundIcon,(50,50))
#sound = Button(soundIconSurface,640,540, "sound On")

#backgSound = pygame.mixer.Sound("Sounds/backgSound.mp3")

backgSound = pygame.mixer.music.load("Sounds/backgSound.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)




newImage = pygame.transform.scale(bg,(screenWidth,ScreenHigh))
while True:
    screen.blit(newImage,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()
        #if event.type == pygame.MOUSEBUTTONDOWN:
            
    if play.checkForInput():
        level.Run()      
            
   # backgSound.play()
    #sound.checkForInput()
    #menu.update()
    play.update()
    #info.update()
    #sound.update()
    #menu.changeColor()
    play.changeColor()
    #info.changeColor()
    #sound.changeColor()
    
    
    
    pygame.display.update()
    clock.tick(60) 
