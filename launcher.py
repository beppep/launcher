import pygame
import time
import os
import pygame_gui


clock = pygame.time.Clock()
SOUND_PATH = os.path.join("assets", "sounds")
pygame.init()
pygame.display.init()

infoObject = pygame.display.Info()
#SCREENSIZE = (1000, 600)
SCREENSIZE = (infoObject.current_w, infoObject.current_h)
FRAMERATE = 60

gameDisplay = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("Bror's pyhtni game launher!!!!!")
#pygame.display.set_icon(pygame.image.load(os.path.join("assets", "textures", "player", "player.png")))

managers={
    "menu":pygame_gui.UIManager(SCREENSIZE),
}


buttons = []
dagames = ["basinDrifter","houseReview","roguelikeGame","CrushingGame"]
for i in range(len(dagames)):
    lvls_per_row = 4
    pos = (100 + (i%lvls_per_row)*200, 100 + (i//lvls_per_row)*150)
    buttons.append(pygame_gui.elements.UIButton(relative_rect=pygame.Rect(pos, (150, 100)),text=dagames[i], manager=managers["menu"]))

jump_out = False
while jump_out == False:
    time_delta = clock.tick(FRAMERATE)/1000.0

    manager=managers["menu"]
    manager.update(time_delta)
    #pygame.event.get()
    for event in pygame.event.get():
        manager.process_events(event)
        if event.type == pygame.QUIT:
            jump_out = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                jump_out = True

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #buttons
            if event.ui_element == buttons[0]:
                import basinDrifter
                basinDrifter.basinDrifterMain()
            if event.ui_element == buttons[1]:
                import houseReview
                houseReview.houseReviewMain()
            if event.ui_element == buttons[2]:
                import roguelikeGame
                roguelikeGame.roguelikeGameMain()
            if event.ui_element == buttons[3]:
                import fightingGame
                fightingGame.fightingGameMain()
            gameDisplay = pygame.display.set_mode(SCREENSIZE)
            gameDisplay.fill((0,0,0))
            pygame.mixer.music.stop()

    manager.draw_ui(gameDisplay)
    

    pygame.display.flip()
    
    
pygame.quit()



