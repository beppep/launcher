import pygame
import time
import os
import pygame_gui
import sys


"""
pyinstaller command:

pyinstaller launcher.py --onefile --noconsole --icon=icon.ico --add-data "launcherFiles;launcherFiles" --name GameLauncher
"""

os.environ['SDL_VIDEO_CENTERED'] = '1' #? dafuq is this

assets_path = None
if hasattr(sys, '_MEIPASS'):
    assets_path = os.path.join(sys._MEIPASS, "launcherFiles")
else:
    assets_path = "launcherFiles"

clock = pygame.time.Clock()
pygame.init()
pygame.display.init()

FRAMERATE = 60

infoObject = pygame.display.Info()
SCREENSIZE = (infoObject.current_w, infoObject.current_h)
#print(SCREENSIZE)
gameDisplay = pygame.display.set_mode(SCREENSIZE)
gameDisplay.blit(pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "loading.png")),SCREENSIZE),(0,0))
pygame.display.update()

pygame.display.set_caption("brors python game launcher")
#pygame.display.set_icon(pygame.image.load(os.path.join("assets", "textures", "player", "player.png")))

mainImage = pygame.image.load(os.path.join(assets_path,"LAUNCHERCOVERART.png"))
mainImage = pygame.transform.scale(mainImage, SCREENSIZE)

managers={
    "menu":pygame_gui.UIManager(SCREENSIZE),
}

pygame.font.init() # you have to call this at the start, 
myfont = pygame.font.SysFont('Calibri', 100)
myfont2 = pygame.font.SysFont('Calibri', 20)
somethingCrashed = 0

dagames = ["Fighting Game","House Review","Roguelike Game","Space Shooter","Jumping Game","Quit"]
dahelptexts = ["1-2 Players.\n\nA classic fighting game with many characters!\n\n(Press number keys to change the controls),\n\n(Controller support)","1 Player.\n\nA relaxing stressful game about building and selling houses.","1 Player.\n\nA classic top-down roguelike.","1 Player.\n\nShoot ships in space and stuff.\n\n(Controller support)","2 Players.\n\nA cool game about jumping over each other.","0 Players.\n\nNot very fun. Not recommended."]
helptext = ""

buttons = []
top_left_buttons = (400,300)
for i in range(len(dagames)):
    lvls_per_row = 2
    pos = (top_left_buttons[0] + (i%lvls_per_row)*200, top_left_buttons[1] + (i//lvls_per_row)*150)
    buttons.append(pygame_gui.elements.UIButton(relative_rect=pygame.Rect(pos, (150, 100)),text=dagames[i], manager=managers["menu"]))
help_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect(top_left_buttons[0] + lvls_per_row*200, top_left_buttons[1], 200, 400),html_text="",manager=managers["menu"])


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

        if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            helptext = dagames[buttons.index(event.ui_element)] + "\n\n" + dahelptexts[buttons.index(event.ui_element)]
            help_textbox.html_text=helptext
            help_textbox.rebuild()
        #if event.type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
         #   helptext = ""
          #  help_textbox.html_text=helptext
           # help_textbox.rebuild()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #buttons
            try:
                if event.ui_element == buttons[0]:
                    import launcherFiles.fightingGame
                    launcherFiles.fightingGame.fightingGameMain()
                elif event.ui_element == buttons[1]:
                    import launcherFiles.houseReview
                    launcherFiles.houseReview.houseReviewMain()
                elif event.ui_element == buttons[2]:
                    import launcherFiles.roguelikeGame
                    launcherFiles.roguelikeGame.roguelikeGameMain()
                elif event.ui_element == buttons[3]:
                    import launcherFiles.blastGame
                    launcherFiles.blastGame.blastGameMain()
                elif event.ui_element == buttons[4]:
                    import launcherFiles.jumpingGame
                    launcherFiles.jumpingGame.jumpingGameMain()
                elif event.ui_element == buttons[5]:
                    jump_out = True
                else:
                    print("watafaaack?!")
                somethingCrashed = False
            except Exception as e:
                somethingCrashed = e
                errortextsurface = myfont2.render("Sorry! It crashed... Please tell me in what situation!   Error: "+str(e), True, (220,220,220))
            gameDisplay = pygame.display.set_mode(SCREENSIZE)
            try:
                pygame.mixer.music.stop()
            except:
                pass

    gameDisplay.blit(mainImage, (0,0))
    manager.draw_ui(gameDisplay)
    maintextsurface = myfont.render("BROR's GAME LAUNCHER", True, (20,20,20))
    gameDisplay.blit(maintextsurface,(SCREENSIZE[0]//4 - 100,50))
    
    if somethingCrashed:
        gameDisplay.blit(errortextsurface,(0,SCREENSIZE[1]-50))

    pygame.display.flip()
    
    
pygame.quit()
#quit() # bad for pyinstalker?


"""

each game must have a function with all the code of the game. this is because all the code is run when you import the game, but only the first time.

things ouside of the main function will not be run the second time you play. importing stuff and pygame init are unnecessary since 



games can be imported at the top of this program or when you want to run their main fcn. doesnt matter that much. mostly about startup times.

afaik the fonts work with pyinstaller. dont know which fonts but whatever


"""