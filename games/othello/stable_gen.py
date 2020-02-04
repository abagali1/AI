from collections import deque
import random
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
BONUS = 1<<20
LEFTSHIFTS=[0,0,0,0,1,9,8,7]
RIGHTSHIFTS=[1,9,8,7,0,0,0,0]
MASKS = {0:0x7F7F7F7F7F7F7F7F,1:0x007F7F7F7F7F7F7F,2:0xFFFFFFFFFFFFFFFF,3:0x00FEFEFEFEFEFEFE,4:0xFEFEFEFEFEFEFEFE,5:0xFEFEFEFEFEFEFE00,6:0xFFFFFFFFFFFFFFFF,7:0x7F7F7F7F7F7F7F00}
def make_move( my_disks, opp_disks, move):
	my_new_disks,opp_new_disks=my_disks,opp_disks
	newdisk=1<<move
	captured=0
	my_new_disks|=newdisk
	for direction in range(8):
		if direction<4:
			temp=((newdisk>>RIGHTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			temp |=((temp>>RIGHTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			temp |=((temp>>RIGHTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			temp |=((temp>>RIGHTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			temp |=((temp>>RIGHTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			temp |=((temp>>RIGHTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			bounds=((temp>>RIGHTSHIFTS[direction]) & MASKS[direction]) & my_new_disks
			if bounds:
				captured|=temp
		else:
			temp=((newdisk<<LEFTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			temp |=((temp<<LEFTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			temp |=((temp<<LEFTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			temp |=((temp<<LEFTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			temp |=((temp<<LEFTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			temp |=((temp<<LEFTSHIFTS[direction]) & MASKS[direction]) & opp_new_disks
			bounds=((temp<<LEFTSHIFTS[direction]) & MASKS[direction]) & my_new_disks
			if bounds:
				captured|=temp
	my_new_disks^=captured
	opp_new_disks^=captured
	return (my_new_disks,opp_new_disks)

def parseBoard(my_disks,opp_disks):
	blackStable,whiteStable,full=255,255,255
	fringe=deque([(my_disks,opp_disks)])
	seen=set()
	leafseen=set()
	while len(fringe)>0:
		white,black=fringe.popleft()
		if white|black==full:
			blackStable&=black
			whiteStable&=white
			leafseen.add((white,black))
		else:
			for x in range(8):
				if not (white|black) & 2**x:
					# add white's move
					newWhite,newBlack=make_move(white,black,x)
					if (newWhite,newBlack) not in seen:
						seen.add((newWhite,newBlack))
						fringe.append((newWhite,newBlack))
					# add black's move
					newBlack,newWhite=make_move(black,white,x)
					if (newWhite,newBlack) not in seen:
						seen.add((newWhite,newBlack))
						fringe.append((newWhite,newBlack))
	return (whiteStable,blackStable)
def display(white,black):
	board=''
	for x in range(8):
		if black&2**x:
			board+='@'
		elif white&2**x:
			board+='o'
		else:
			board+='.'
	print(board)

def count(disks):
	num=disks&1
	while disks:
		disks=disks>>1
		num+=disks&1
	return num

def boardgen():
	seen=set()
	fringe=deque([(0,0)])
	while len(fringe)>0:
		me,opp=fringe.popleft()
		seen.add((me,opp))
		if me|opp!=255:
			for x in range(8):
				if not (me&2**x or opp&2**x):
					new=(me+2**x,opp)
					if new not in seen:
						seen.add(new)
						fringe.append(new)
					new=(me,opp+2**x)
					if new not in seen:
						seen.add(new)
						fringe.append(new)
	return seen
import time,pickle
stableEdge=dict()
t0=time.time()
pos=0
for white,black in boardgen():
	stableW,stableB=parseBoard(white,black)
	swcount=count(stableW)
	sbcount=count(stableB)
	if (white,black) not in stableEdge:
		stableEdge[(white,black)]=swcount-sbcount
print(time.time()-t0)
print(len(stableEdge))
print(len(str(stableEdge)))
print(stableEdge)
#pickle.dump(stableEdge,open('dictionaries/stabletable.pickle','wb'))