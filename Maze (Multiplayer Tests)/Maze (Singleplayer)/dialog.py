import pygame
import os

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

# Sound initialization
talk = pygame.mixer.Sound('sounds/talk.wav')
open_dialog = pygame.mixer.Sound('sounds/open_dialog.wav')
close_dialog = pygame.mixer.Sound('sounds/close_dialog.wav')
#walk = pygame.mixer.Sound('sounds/walk.wav')

# Main class for dialog boxes
class Dialog:
    window_height = 0
    window_width = 0
    display_window = None
    internal_window = None

    def __init__(self, image_file, speed=2):
        self.img = pygame.image.load(os.path.join(image_file)).convert_alpha()
        self.base_img = self.img.copy()
        self.width = self.img.get_size()[0]
        self.height = self.img.get_size()[1]
        self.x = Dialog.window_width / 2 - self.width / 2 
        self.y = Dialog.window_height + self.height
        self.font = pygame.font.SysFont('Comic Sans MS', 25, True)
        self.texts = []
        self.text_speed = speed

    def display_dialog(self, screenshot, file=None):
        '''Override in subclass'''
        pass

    @classmethod
    def dialog_init(cls, window_size, display_window):
        cls.window_width = window_size[0]
        cls.window_height = window_size[1]
        cls.display_window = display_window


# Subclass for text-only dialog boxes
class TextDialog(Dialog):
    
    def display_dialog(self, text_file=None):
        '''Function to take a dialog file and output a dialog in the text box'''
        screenshot = Dialog.internal_window
        # Load texts into dialog
        self.texts = []
        if text_file != None:
            try:
                with open(os.path.join(text_file), 'r') as rf:
                    for line in rf:
                        if line[len(line) - 1] == "\n":
                            line = line[:len(line) - 1]
                        self.texts.append(line)
            except:
                self.texts.append("If you're reading this message, I messed up :( ")
        else:
            self.texts.append("If you're reading this message, I messed up :( ")

        # Raise dialog box into place
        temp_clock = pygame.time.Clock()
        self.y = Dialog.window_height + 1
        self.img = self.base_img.copy()
        open_dialog.play()
        temp_clock.tick()
        for i in range(round(self.height * 1.2 / 12)):
            screen_copy = screenshot.copy()          
            screen_copy.blit(self.img, (self.x, self.y - i * 12))
            Dialog.display_window.blit(pygame.transform.scale(screen_copy, (Dialog.display_window.get_width(), Dialog.display_window.get_height())), (0, 0))
            pygame.display.flip()
            temp_clock.tick(60)

        # Cycle through list of dialogs
        for quote in self.texts:
            # Scroll through the loaded text
            line = 1
            text_start = 0
            self.y = Dialog.window_height - 1.2 * self.height
            spacebar = False
            screen_copy = screenshot.copy()
            temp_clock.tick()
            for frame in range(len(quote) + 1):
                text = self.font.render(quote[text_start:frame], False, (32, 32, 32))
                self.img.blit(text, (25, 25 * line - 10))
                screen_copy.blit(self.img, (self.x, self.y))
                Dialog.display_window.blit(pygame.transform.scale(screen_copy, (Dialog.display_window.get_width(), Dialog.display_window.get_height())), (0, 0))
                pygame.display.flip()
                if text.get_size()[0] > self.width - 70:
                    line += 1
                    text_start = frame
                if frame % 2:
                    talk.play()
                # Break the text-scroll-loop if the player presses 'space'
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        spacebar = True
                if spacebar:
                    break
                temp_clock.tick(30)

            # If the player pressed 'space' for quick-scroll, render the entire text at once.
            line = 1
            text_start = 0
            screen_copy = screenshot.copy()
            for frame in range(len(quote) + 1):
                text = self.font.render(quote[text_start:frame], False, (32, 32, 32))
                self.img.blit(text, (25, 25 * line - 10))
                if text.get_size()[0] > self.width - 70:
                    line += 1
                    text_start = frame
            screen_copy.blit(self.img, (self.x, self.y))
            Dialog.display_window.blit(pygame.transform.scale(screen_copy, (Dialog.display_window.get_width(), Dialog.display_window.get_height())), (0, 0))
            pygame.display.flip()
            
            # Wait for player to press 'space' to continue
            spacebar = False
            while not spacebar:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        spacebar = True
                pygame.display.flip()
            self.img = self.base_img.copy()
    
        # Lower dialog box
        self.y = Dialog.window_height - 1.2 * self.height
        self.img = self.base_img.copy()
        close_dialog.play()
        temp_clock.tick()
        for i in range(round(self.height * 1.2 / 12)):
            screen_copy = screenshot.copy()
            screen_copy.blit(self.img, (self.x, self.y + i * 12))
            Dialog.display_window.blit(pygame.transform.scale(screen_copy, (Dialog.display_window.get_width(), Dialog.display_window.get_height())), (0, 0))
            pygame.display.flip()
            temp_clock.tick(60)
