import sys, pygame, json

# No guarantees anything will work if you change these, but I'm not your mama
WIDTH = 400
HEIGHT = 500

gameState = count = shipHeight = 0

# Open the json file containing the level info.
# If you're going to have multiple levels,
# You might consider having 1 per file.
with open('mapdata_wip.json') as json_file:
    mapData = json.load(json_file)
    mapBlocks = list(map(list, zip(*mapData['blocks'])))
    mapBlockTypes = mapData['blocktypes']
    mapWidth = mapData['width']
    mapLength = mapData['length']

# Preloading the block and ship images here so we only have to do it once.
blockTypeList = [None]
for i in mapBlockTypes:
    if i.get('image'):
        blockTypeList.append(pygame.image.load(i['image']+".png"))
shipFrameList = [pygame.image.load("ship0.png"), pygame.image.load("ship1.png"), pygame.image.load("ship2.png")]
shadowFrameList = [pygame.image.load("shadow0.png"), pygame.image.load("shadow1.png"), pygame.image.load("shadow2.png")]

# mapPosX and mapPosY reference the top-left corner of the level, offset by the screen diagonal
# ... it's possible that's gibberish. You figure it out.
mapPosX = 200 + (mapLength*32)
mapPosY = 150 - (mapLength*16)
# shipPos is the screen coordinate where the ship is drawn.
# Initially 50 pixels right, 300 pixels down
shipPos = [50,300]

# After this block you can start updating screen elements.
# NOT BEFORE. Trust me.
pygame.init()
screen = pygame.display.set_mode([WIDTH,HEIGHT])
keys = pygame.key.get_pressed()
clock = pygame.time.Clock()

# Prerendering text here to make refreshes a little faster.
# Dynamic text (altitude, scores) will need to be refreshed real-time
font = pygame.font.SysFont("couriernewms", 30)
textInst_1 = font.render("Pygame Zaxxon", True, (255,255,0))
textAlti_1 = font.render("Altitude : ", True, (255,255,0))
textX = font.render("X", True, (255,255,255))

# Clear the screen, draw the level, draw the text overlay
def draw():
    screen.fill((0,0,0))
    drawMap()
    screen.blit(textInst_1, (10,10))
    screen.blit(textAlti_1, (190, 460))
## DEBUGGERY
    screen.blit(textX, (mapPosX, mapPosY))
##    print([mapPosX,mapPosY])

# The heavy lifting happens in this function. 
def drawMap():
    global gameState, keys
    shipBlock = getShipXY()

    # Makes the ship bank left and right with player input
    if keys[pygame.K_LEFT]:         # Left pressed
        shipFrame = 0
    elif keys[pygame.K_RIGHT]:       # Right pressed
        shipFrame = 2
    else:               # Level flight if neither
        shipFrame = 1

    # From left to right, from the ship's POV
    for x in range(0, mapWidth):
        # From the end of the level to the beginning
        for y in range(0, mapLength):
            # bx and by represent current progress through the level ... somehow
            bx = (x*32) - (y*32) + mapPosX
            by = (y*16) + (x*16) + mapPosY
            # Draw all blocks that include at least one pixel on screen
            if -64 <= bx < WIDTH + 32 and -64 <= by < HEIGHT + 64:        
                if mapBlocks[x][y] > 0:
                    # If the ship occupies the same square as a map block
                    if shipBlock == [x,y]:
                        # If the ship is not higher than the current block height
                        if mapBlockTypes[mapBlocks[shipBlock[0]][shipBlock[1]]]['height'] > shipHeight+32:
                            # GAME OVER, MAN, GAME OVER
                            gameState = 1
                    # Write all the blocks to the screen that are visible
                    screen.blit(blockTypeList[mapBlocks[x][y]], (bx, by-mapBlockTypes[mapBlocks[x][y]]['height']))
                # 
                if shipBlock == [x-1,y-1]:
                    # Solid if playing, Blinking if Game Over
                    if(gameState == 0 or count%4 == 0):
                        screen.blit(shipFrameList[shipFrame],(shipPos[0],shipPos[1]+10))
                        screen.blit(shadowFrameList[shipFrame],(shipPos[0],shipPos[1]-shipHeight))
    # Only draw the ship if it exists in a navigable portion of the current level.                    
    if shipBlock[1] >= mapLength-1 or shipBlock[1] < 0 or shipBlock[0] == mapWidth-1:
        screen.blit(shadowFrameList[shipFrame],(shipPos[0],shipPos[1]+10))
        screen.blit(shipFrameList[shipFrame],(shipPos[0],shipPos[1]-shipHeight))

def getShipXY():
    # Math, man; it hurts.
    x = ((shipPos[0]+82)/32)
    y = mapLength - ((shipPos[1]/16) + (mapPosY/16) + ((mapWidth/2)-x))-2
    return [int(x),int(y)]
   
def main():
    global count, gameState, mapPosX, mapPosY, shipHeight, keys

    while 1:

        keys = pygame.key.get_pressed()

        # Kill the game if escape key is pressed
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        if keys[pygame.K_LEFT] > 0:
            if shipBlock[0] > 0:
                shipPos[0] -=1
                shipPos[1] -=0.5
        if keys[pygame.K_RIGHT] > 0:
            if shipBlock[0] < mapWidth-1:
                shipPos[0] +=1
                shipPos[1] +=0.5
        if keys[pygame.K_UP] > 0:
            shipHeight = max(min(85, shipHeight+1), 0)
        if keys[pygame.K_DOWN] > 0:
            shipHeight = max(min(85, shipHeight-1), 0)

        ## Do these as long as the game is not over
        if gameState == 0:
            # shift the level down one pixel, left one half pixel
            # That seems backward, but don't argue with the blit
            mapPosX -=1
            mapPosY +=0.5

        # update ship position, draw the next frame           
        shipBlock = getShipXY()        
        screen.fill([0,0,0])
        draw()
        pygame.display.flip()
        
        count += 1
        # Sixty FPS? Bigger == Faster, anyway
        clock.tick(60)
        # Pygame will largely ignore your input if you don't do this.
        pygame.event.pump()

# Keep these lines here
if __name__ == "__main__":
    main()
