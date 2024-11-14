# LIB
import pygame
import random
import sys

# Init Pygame
pygame.init()

# Color and Size Screen 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Guess the Image Game")

font = pygame.font.Font(None, 32)

# List of images with names
img_list = {
    "animals": "1.jpg",
    "bull fight": "2.jpg",
    "sun watch": "3.jpg",
    "solitaire": "4.jpg",
    "bee": "5.jpg",
    "messi": "6.jpg",
    "qudus": "7.jpg",
}

class GuessTheWord:
    def __init__(self):
        self.score = 0
        self.tries = 3
        self.guessed_letters = set()
        self.used_images = []  # قائمة الصور المستخدمة
        self.next_img()
        self.game_over = False

    def next_img(self):
        # إذا انتهت كل الصور
        if len(self.used_images) == len(img_list):
            self.game_over = True
            return

        # اختيار صورة عشوائية لم يتم استخدامها من قبل
        while True:
            self.img_name, self.img_path = random.choice(list(img_list.items()))
            if self.img_path not in self.used_images:
                self.used_images.append(self.img_path)
                break
        
        # تحميل الصورة وتغيير الحجم
        self.imgs = pygame.image.load(self.img_path)
        self.imgs = pygame.transform.scale(self.imgs, (300, 300))
        self.img_frame = self.imgs.get_rect(center=(400, 230))  # الصورة في المنتصف
        self.guessed_letters.clear()
        self.tries = self.tries

    def show_msg(self, msg, color, pos):
        text = font.render(msg, True, color)
        text_rect = text.get_rect(center=pos)  # ضبط النص في المنتصف
        screen.blit(text, text_rect)

    def display_hint(self):
        hint = ""
        for letter in self.img_name:
            if letter == " " or letter in self.guessed_letters:
                hint += letter + " "  # يظهر المسافة كحرف ظاهر
            else:
                hint += "_ "
        self.show_msg(f"Hint: {hint}", BLACK, (400, 450))  # تحت الصورة

    def check_guess(self, letter):
        # التحقق من أن الحرف ليس مسافة فارغة
        if letter == " ":
            return
        if letter.lower() in self.img_name.lower():
            self.guessed_letters.add(letter.lower())
        else:
            self.tries -= 1
        # إذا كان جميع الحروف مكتملة
        if all(letter == " " or letter in self.guessed_letters for letter in self.img_name):
            self.score += 1
            self.next_img()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.unicode and (event.unicode.isalpha() or event.unicode == " "):
                self.check_guess(event.unicode)

    def draw_screen(self):
        screen.fill(WHITE)
        screen.blit(self.imgs, self.img_frame)  # عرض الصورة في المنتصف
        
        # عرض النقاط فوق الصورة
        self.show_msg(f"Score: {self.score}", BLACK, (400, 50))
        
        # عرض التلميح تحت الصورة
        self.display_hint()
        
        # عرض المحاولات تحت التلميح
        self.show_msg(f"Tries Left: {self.tries}", BLACK, (400, 500))

    def game_over_screen(self, status):
        screen.fill(WHITE)
        if status == "win":
            self.show_msg(f"Your Score is: {self.score}", BLACK, (400, 300))
            self.show_msg("""Congratulations! Press R to restart or Q to quit.""", BLACK, (400, 350))
        else:
            self.show_msg("Game Over! Press R to play again or Q to quit.", BLACK, (400, 300))

def main():
    game = GuessTheWord()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game.game_over:
                game.handle_event(event)
                if game.tries <= 0:
                    game.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = GuessTheWord()  # إعادة تشغيل اللعبة
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        
        if game.game_over:
            game.game_over_screen("win" if len(game.used_images) == len(img_list) else "lose")
        else:
            game.draw_screen()

        pygame.display.flip()

if __name__ == "__main__":
    main()
