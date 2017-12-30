import pygame
from test import *
from pygame.locals import *

askList = [] #Records questions asked

quest = Questions()

global kill
kill = quest.category() #Ensures that quest.category() only loops once
pygame.init()

gameScreen = pygame.display.set_mode((1000,600))

pygame.display.set_caption("Jeopardy")
surface1 = pygame.image.load("logo.jpg")

surface1 = pygame.transform.scale(surface1, (1000, 600))
gameScreen.blit(surface1, (0,0))

pygame.display.update()
clock = pygame.time.Clock() #FPS

Red = (200, 0, 0)
Green = (0,200, 0)
brightRed = (255,0,0)
brightGreen = (0, 255, 0)
blue = (0, 0, 170)
gold = (255, 223, 0)
black = (0,0,0)
White = (255, 255, 255)

print("BAS")



def textObjects(text, font):
    textSurface = font.render(text, True, (0,0,0,))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,command):
    """This function checks if the mouse if over the button an whether it's click. Also splits the inputted message"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameScreen, ac, (x, y, w, h))
        if click[0] == 1 and command != None:
            if command == "go":
                questionBoard(50, 20, 0) #Random Input
                #Removed Pass

            elif command == "quit":
                pygame.quit()
                quit()

    else:
        pygame.draw.rect(gameScreen, ic, (x, y, w, h))

    smallText = pygame.font.Font("gyparody.ttf", 20)
    textSurf, textRect = textObjects(msg, smallText)
    textRect.center = ((x + (w/2)), (y + (h/2)))
    gameScreen.blit(textSurf, textRect)

def questionbutton(score):
    """This function checks which coloumn and row the mouse clicks on. Depending on that it calls their corresponding
    qustionCards."""
    x_axis = [200,400,600,800,1000]
    y_axis = [120,240,360,480,600]
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    oldScore = 0
    score = score
    newScore = score + oldScore
    oldScore = newScore


    for i in range(5):
        for y in range(4):
            if mouse[0] < x_axis[i]:
                if y_axis[y] <= mouse[1] < y_axis[y+1]:
                    carry = str(y) + str(i)
                    if click[0] == 1 and carry in askList : #askList is a global variable recording the asked questions
                        #Doesn't allow a already answered cate/row to be clicked
                        return

                    elif click[0] == 1 and carry not in askList:
                        questionCards(y, i, newScore)

def gameIntro():
    """Creates an intro page/surface for the game. Calls the button to add it. """
    intro = True
    print("WHAT")
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("START", 390, 490, 200, 70, gold, White, "go")
        pygame.display.update()

def questionBoard(cateNum, RowNum, score):
    """This function determines the gameboard. Lines are used to divided a blue surface and text(representing)
     numbers are rendered onto it. """
    blue = (0,0,200)
    black = (0,0,0)

    board = pygame.Surface((1000,600))
    board.fill(blue)
    gameScreen.blit(board,(0,0))
    pygame.display.update()

    if len(askList) == 20: #Calls the endgame function if all the questions have been asked
        finalScreen(score)

    pos = [200, 400, 600, 800, 1000]

    for i in range(len(pos)): #Draws black lines vertically
        pygame.draw.line(gameScreen, black, (pos[i],0), (pos[i],600), 2)
        pygame.display.update()

    width = [120,240,360,480,600]

    for i in range(5): #Draws black lines horizontally
        pygame.draw.line(gameScreen, black, (0,width[i]), (1000, width[i]), 2)
        pygame.display.update()

    jeoFont = pygame.font.Font("gyparody.ttf", 35)

    monies = ["$200", "$400", "$600", "$800"]
    val = str(cateNum) + str(RowNum) #Keeps track of asked questions category index and question index
    askList.append(val)
    #Next lines of code render and blit, the monies onto the board
    for i in range(5):
        for y in range(4):
            carry = str(y) + str(i)
            #print(carry, "CARRY")
            if carry in askList:
                continue
            else:
                widths = (120 + width[y]) - 72 # 64
                height = pos[i] - 100 - 35
                text = jeoFont.render(monies[y], 1, (255, 223, 0))
                gameScreen.blit(text, (height, widths))

                pygame.display.update()
    acc = 0
    for x in kill:
        #Renders and splits the category names onto the screen. Only categories of a certain length are used in the
        #Data Structure
        newFont = pygame.font.Font("gyparody.ttf", 32)
        x_axis, y_axis = newFont.size(x) #Returns width of text
        if pos[acc] == 200:
            xy = ((200-x_axis)/2) #Centers the Text
            y_axis = ((120-y_axis)/2)
        else:
            xy = pos[acc-1] + ((200 - x_axis)/2)
            y_axis = ((120-y_axis)/2)

        text = newFont.render(x, 1, (White))
        gameScreen.blit(text, (xy, y_axis))
        acc += 1
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        questionbutton(score)
        #questionbutton is called to keep track of the mouse clicks.
def questionCards(category, q, score):
    """This function shows the question, allows for user Input and checks whether their question is right or wrong
    If its right the value of the question is added to their current score. Wrong it is subtracted."""
    name = ""
    questionScreen = pygame.display.set_mode((1000, 600))
    qImage = pygame.image.load("jeopardy-blank-1-728.jpg")
    qImage = pygame.transform.scale(qImage,(1000, 600))
    questionScreen.blit(qImage,(0, 0))
    font = pygame.font.Font("itc-korinna-regular-59015b18e6411.otf", 40)
    quest.dataBank()

    pygame.mixer.music.load("song.mp3") #Loads jeopardy theme song
    pygame.mixer.music.play(0, 0) #Plays Jeopardy Theme song
    moneyList = [200, 400, 600, 800, 1000]

    while True:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode #Records user input
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == K_RETURN:
                    ans = str(quest.answer(category,q))
                    money = int(moneyList[category])

                    if name.lower() == ans.lower() or name.lower() in ans.lower() and len(name.lower())> 3:
                        #Checks if the answer is correct
                        score += int(money)
                        pygame.mixer.music.rewind()
                        pygame.mixer.music.stop()
                        while True:
                            for evt in pygame.event.get():
                                if evt.type == KEYDOWN:
                                    if evt.key == K_c:
                                        questionBoard(category, q, score)
                                        #Calls questionBoard gives the category, q, score so that it can add to askList
                                        #and keep track of score

                                elif evt.type == QUIT:
                                    pygame.quit()
                                    quit()

                            #If correct it changes to a new surface that shows your score whether you were correct or not
                            newfont = pygame.font.Font("itc-korinna-regular-59015b18e6411.otf", 60)
                            font2 = pygame.font.Font("itc-korinna-regular-59015b18e6411.otf", 50)

                            newScreen = pygame.display.set_mode((1000, 600))
                            newScreen.fill(gold)
                            string = "YOUR CURRENT SCORE IS:"
                            string2 = "PRESS 'C' TO CONTINUE"
                            string3 = "CORRECT"

                            newScreen.blit(font2.render(string3, True, (255, 255, 255)), (360, 50))
                            newScreen.blit(newfont.render(string2, True, (255, 255, 255)), (125, 450))
                            newScreen.blit(newfont.render(string, True, (255, 255, 255)), (100, 150))
                            newScreen.blit(newfont.render(str("$" + str(score)), True, (255, 255, 255)), (400, 300))


                            pygame.display.update()
                    else:
                        score -= int(money)
                        pygame.mixer.music.rewind()
                        pygame.mixer.music.stop()
                        while True:
                            for evt in pygame.event.get():
                                if evt.type == KEYDOWN:
                                    if evt.key == K_c:
                                        questionBoard(category, q, score)

                                elif evt.type == QUIT:
                                    pygame.quit()
                                    quit()

                            else:
                                pass

                            #If user input was wrong, changes to surface that shows your new score and the correct answer
                            newfont = pygame.font.Font("itc-korinna-regular-59015b18e6411.otf", 60)
                            font2 = pygame.font.Font("itc-korinna-regular-59015b18e6411.otf", 50)

                            newScreen = pygame.display.set_mode((1000, 600))
                            newScreen.fill(gold)
                            string = "YOUR CURRENT SCORE IS:"
                            string2 = "PRESS 'C' TO CONTINUE"
                            string3 = str("Answer was: " + ans)


                            #Renders different strings to main surface
                            newScreen.blit(font2.render(string3, True, (255, 255, 255)), (100, 50))
                            newScreen.blit(newfont.render(string2, True, (255, 255, 255)), (125, 450))
                            newScreen.blit(newfont.render(string, True, (255, 255, 255)), (100, 150))
                            newScreen.blit(newfont.render(str("$" + str(score)), True, (255, 255, 255)), (400, 300))
                            pygame.display.update()

                elif evt.key == K_SPACE :
                    name += " "

            elif evt.type == QUIT:
                pygame.quit()
                quit()


        questionScreen.fill((0, 0, 160))
        block = font.render(name, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = questionScreen.get_rect().center
        questionScreen.blit(block, rect)
        jQuestion = str(quest.questions(category, q))

        flat = font.render(jQuestion, True, (255, 255, 255), (150, 100)) #Renders the question onto the surface
        wide = flat.get_width() #Gets length of the question
        lis = jQuestion.split()
        if wide > 800:
            #If the length of the question is more than 800 pixels, it is divided into two new list, which are then
            #joined and rendered in above/below with each other
            lis1 = lis[:len(lis) // 2]
            lis2 = lis[(len(lis) // 2):]

            lis1 = ' '.join(lis1)
            lis2 = " ".join(lis2)

            flat1 = (font.render(lis1, True, (255, 255, 255), (150, 100))).get_width()
            flat2 = (font.render(lis2, True, (255, 255, 255), (150, 100))).get_width()

            if flat2> 750:
                #If the second list is more than 750 pixels long it creates a third row
                lis1 = lis[:len(lis) // 3]
                lis2 = lis[(len(lis) // 3):(len(lis) // 3) * 2]
                lis3 = lis[(len(lis) // 3) * 2:]
                lis1 = ' '.join(lis1)
                lis2 = " ".join(lis2)
                lis3 = " ".join(lis3)

                flat3 = (font.render(lis3, True, (255, 255, 255), (150, 100))).get_width()
                flat2 = (font.render(lis2, True, (255, 255, 255), (150, 100))).get_width()
                flat1 = (font.render(lis1, True, (255, 255, 255), (150, 100))).get_width()

                x = (1000 - flat1) // 2
                questionScreen.blit(font.render(lis1, True, (255, 255, 255)), (x, 50))
                xy = (1000 - flat2) // 2
                questionScreen.blit(font.render(lis2, True, (255, 255, 255)), (xy, 100))
                xyz = (1000- flat3)//2
                questionScreen.blit(font.render(lis3, True, (255, 255, 255)), (xyz, 150))

            else:
                x = (1000 - flat1) // 2
                xy = (1000- flat2)//2
                questionScreen.blit(font.render(lis1, True, (255, 255, 255)), (x, 50))
                questionScreen.blit(font.render(lis2, True, (255, 255, 255)), (xy, 100))
        else:
            x = (1000 - wide) // 2
            questionScreen.blit(font.render(jQuestion, True, (255, 255, 255)), (x, 50))
        pygame.display.flip()


def finalScreen(score):
    """This function is called when all the questions have been asked. Shows your final score"""
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pygame.quit()
                    quit()

        newfont = pygame.font.Font("itc-korinna-regular-59015b18e6411.otf", 60)
        newScreen = pygame.display.set_mode((1000, 600))
        newScreen.fill(gold)
        string = "YOUR FINAL SCORE IS:"
        string2 = "Press Enter to Quit"
        flat = (newfont.render(string, True, (255, 255, 255), (150, 100))).get_width()
        x = (1000-flat)// 2
        #Centers the text
        flat1 = (newfont.render(string2, True, (255, 255, 255),(150, 450))).get_width()
        xy = (1000-flat1)//2

        #Renders Text onto newScreen
        scorewidth = (newfont.render(str("$" + str(score)), True, (255, 255, 255), (150, 100))).get_width()
        newScreen.blit(newfont.render(string, True, (255, 255, 255)), (x, 150))
        newScreen.blit(newfont.render(str("$" + str(score)), True, (255, 255, 255)), ((1000-scorewidth)//2, 250))
        newScreen.blit(newfont.render(string2, True, (255, 255, 255)), (xy, 450))
        pygame.display.update()

def main():
    print("MAIN")
    what = gameIntro()


main()

