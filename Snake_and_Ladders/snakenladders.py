from graphics import *
import random
import time


WINDOW_WIDTH, WINDOW_HEIGHT, MaxPos = 800, 600, 125
win = GraphWin("Snake and Ladders", WINDOW_WIDTH, WINDOW_HEIGHT)

SaLdic = {16: 28,
          19: 39,
          30: 50,
          41: 61,
          52: 72,
          63: 83,
          65: 105,
          74: 94,
          79: 117,
          87: 115, 
          17: 6,
          26: 3,
          43: 21,
          47: 25,
          55: 33,
          59: 8,
          75: 10,
          97: 73,
          106: 1,
          111: 89, 
          113: 109, 
          119: 95,  
          121: 99, 
          }

#---------------------------------------------------------------
# Player class
class Player:
	def __init__(self, inPlayerNum,btnx1,btny1,btnx2,btny2):
		self.playerPos = 1
		self.playerNum = inPlayerNum
		self.btn=Rectangle(Point(btnx1,btny1), Point(btnx2, btny2)) 
		self.colorcode=color_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
		#self.btn.setFill("red") )
		self.btn.setFill(self.colorcode) 
		self.btn.draw(win)
		self.text=Text(Point(btnx1+45, btny1+15), "")
		self.text.draw(win)
		PlayerNoDisplay = Text(Point(btnx1-10, btny1+10), str(inPlayerNum))
		PlayerNoDisplay.draw(win)
		self.circle = Circle(Point(1,1), 1)
		self.circle.draw(win)
		self.circle.setFill(self.colorcode)

	def updatePosition(self, inPos):
		self.playerPos = inPos
		#ll = self.btn.getP1()  # assume p1 is ll (lower left)
		#ur = self.btn.getP2()  # assume p2 is ur (upper right)
		#text2 = Text(Point(ll.getX()+45, ll.getY()+15), "  ")
		#text2.draw(win) 
		self.circle.undraw() 
		#print(m[inPos-1][1],m[inPos-1][2])
		self.circle = Circle(Point(m[inPos-1][1],m[inPos-1][2]), 15)
		self.circle.setFill(self.colorcode)
		self.circle.draw(win)
		self.text.setText(str(inPos))

	def getPosition(self):
		return self.playerPos 

	def getPlayerNum(self):
		return self.playerNum

#---------------------------------------------------------------
def button(startx,starty,endx,endy):
	#btn = Rectangle(Point(750, 55), Point(780, 85))  # points are ordered ll, ur 
	btn = Rectangle(Point(startx,starty), Point(endx, endy))
	btn.setFill("red") 
	btn.draw(win)
	return btn
#---------------------------------------------------------------
def clear(win):
	for item in win.items[:]:
		item.undraw()
	win.update()

#---------------------------------------------------------------
def inside_circle(x, y, a, b, r):
    return (x - a)*(x - a) + (y - b)*(y - b) < r*r

#---------------------------------------------------------------
def inside(point, rectangle):
    """ Is point inside rectangle? """
    ll = rectangle.getP1()  # assume p1 is ll (lower left)
    ur = rectangle.getP2()  # assume p2 is ur (upper right) 

    return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()
#---------------------------------------------------------------
def inside2(point,rectangle,circle):
	ll = rectangle.getP1()  # assume p1 is ll (lower left)
	ur = rectangle.getP2()  # assume p2 is ur (upper right)
	#coordinate = [point.getX(),point.getY()]

	#shape = visual.Circle(win, circle.radius, units='pix') #shape to check if coordinates are within it
	#if shape.contains(coordinate):
	if inside_circle(x, y, a, b, circle.radius):
		clickInside=True
	else:
		clickInside=False
	#text2 = Text(Point(700, 300), "")
	#text2.draw(win)
	#text3 = Text(Point(700, 300), str(ll.getX()) + ' ' + str(point.getX()) + ' ' + str(ur.getX()))
	#text3.draw(win)
	#text4 = Text(Point(700, 350), str(ll.getY()) + ' ' + str(point.getY()) + ' ' + str(ur.getY()))
	#text4.draw(win)
	if not clickInside:
		if (ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()):
			clickInside=True

	return clickInside

#--------------------------------------------------
# Function to handle the players turn
def gameMaster(inPlayer):
	global winner
	print("\n----Player %i Click to roll----" % inPlayer.getPlayerNum())
	clickPoint = win.getMouse()
	if inside(clickPoint, inPlayer.btn):
		# check for game winner
		if inPlayer.getPosition() >= MaxPos:
				print("Player %i is the Winner!" % inPlayer.getPlayerNum())
				winner = True 
				text = Text(Point(700, 500), "Winner : " + str(inPlayer.getPlayerNum()))
				text.draw(win)

		# run dice rolls and movements
		if winner == False:
			# Uncomment to require space to be pressed before jumping turns
			# input()
			roll = rollDice()
			print("You rolled: %i" % roll)
			movePlayer(inPlayer, roll)
			checkPosition(inPlayer)
	#clickPoint = win.getMouse()
	#print(clickPoint)

#--------------------------------------------------
def rollDice():
    return random.randint(1,6)

#--------------------------------------------------
# Handle player movements
def movePlayer(inPlayer, roll):
	if inPlayer.getPosition() + roll <= MaxPos:
		inPlayer.updatePosition(inPlayer.getPosition() + roll)
		print("You are at spot %i" % inPlayer.getPosition())
	else:
		print("You rolled too far")

#--------------------------------------------------
# Checks player landing position and adjusts if snake or ladder
def checkPosition(inPlayer):
	#value = D['x'] if 'x' in D else 0 # if/else expression form
	for pos in SaLdic:
		if pos == inPlayer.getPosition():
			if pos < SaLdic[pos]:
				print("You climbed a Ladder to spot %i" % SaLdic[pos])
			else:
				print("You rode a Snake to spot %i" % SaLdic[pos])
			inPlayer.updatePosition(SaLdic[pos])

#--------------------------------------------------


#--------------------------------------------------
#---- MAIN PROGRAM --------------------------------

myImage = Image(Point(350,250),'vikuntapali2.gif')
myImage.draw(win)

global winner
winner = False
#numPlayers = int(input('Enter number of players: '))

numPlayers=2
playerList = [] 

x=730
y=10
w=30
g=40
for i in range(0,numPlayers):
	playerList.append(Player(i + 1,x,y+g,x+w,y+g+w)) 
	g+=40

m=[]
for i in range(1,MaxPos+10):
	r=i%11
	if r==0:		
		if int(i/11)%2==0:
			m.append([i,1,11-int(i/11)+1])
		else:
			m.append([i,11,11-int(i/11)+1])
	else:
		if int(i/11)%2==0:
			m.append([i,r,11-int(i/11)])
		else:
			m.append([i,11-r+1,11-int(i/11)])

for i in range(len(m)):
	m[i][1]=(m[i][1]-0.5)*2*28 + 42
	m[i][2]=(m[i][2]-0.5)*2*24 + 33

#for c in m:
#	print(c)

centerPoint = Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
#text = Text(Point(700, 500), "Exit")
#text.draw(win)
#c = Circle(Point(450,250), 100)
#d = Circle(Point(200,150), 50)
#r = Rectangle(Point(10,10),Point(60,60))
#win.plotPixel(35, 128, "blue")
#win.setBackground("green")
#clickPoint = win.checkMouse()
#keyString = win.getKey()
#keyString = win.checkKey() 
#c.draw(win)
#d.draw(win)
#r.draw(win)
 


while winner == False:
	for i in playerList: 
		if winner == False:
			gameMaster(i)

win.getMouse() # pause for click in window
win.close()