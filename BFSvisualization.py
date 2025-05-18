from tkinter import *
import tkinter.font
from collections import deque
import time
import threading
import random


window = Tk()
window.title("BFS 미로탐색 알고리즘 시각화")
window.geometry("1000x800")
window.configure(background="black")

m = 35
n = 35
modes = [True,False,False,False]

localmap = []
font = tkinter.font.Font(family="Arial",size=10,weight="bold")
queue = deque()
mapFrame = Frame(window)
mapFrame.pack(side="left")

speed = 0.001

startPos = (0,0)
endPos = (n-1,m-1)

prepared = True
isProcessing = False

def cellOnclick(event):
    global startPos
    global endPos
    global prepared
    global isProcessing
    if prepared and not isProcessing:
        gridInfo = event.widget.grid_info()
        cellPosX = gridInfo["column"]
        cellPosY = gridInfo["row"]
        if not localmap[cellPosX][cellPosY].cget("bg") in ["red","green"]:
            if modes[0]:#시작지점
                if not startPos == (cellPosX,cellPosY) and not endPos == (cellPosX,cellPosY) and event.widget.cget("bg") != "black":
                    if not endPos == (startPos[1],startPos[0]):
                        localmap[startPos[1]][startPos[0]].configure(bg="white",fg="black",text='0')
                    startPos = (cellPosY,cellPosX)            
                    event.widget.configure(bg="red",fg="white",text='1')
            elif modes[1]:#도착지점
                if not endPos == (cellPosX,cellPosY) and not startPos == (cellPosX,cellPosY) and event.widget.cget("bg") != "black":
                    if not startPos == (endPos[1],endPos[0]):
                        localmap[endPos[1]][endPos[0]].configure(bg="white",fg="black")
                    endPos = (cellPosY,cellPosX)            
                    event.widget.configure(bg="green",fg="white")
            elif modes[2]:#벽 세우기
                if not event.widget.cget("bg") == "black":
                    event.widget.configure(bg="black",fg="white")
            elif modes[3]:#벽 제거                
                if not event.widget.cget("bg") == "white":
                    event.widget.configure(bg="white",fg="black")
    
for i in range(m):
    localmap.append([])
    for j in range(n):
        cell = Button(mapFrame,text="0",width=3,height=1,relief="sunken",bg="white",font=("Courier New", 7, "bold"))        
        cell.name = f"{m}/{n}"
        cell.bind("<Button-1>",cellOnclick)
        cell.grid(row=j,column=i)        
        localmap[i].append(cell)

localmap[endPos[1]][endPos[0]].configure(bg="green",fg="white")
localmap[0][0].configure(bg="red",fg="white",text='1')
 
def getPath(path):
    global prepared
    print(path)        
    kx = startPos[1]
    ky = startPos[0]           
    localmap[kx][ky].configure(bg="green")
    for dir in path:
        dirList = {"D":(ky+1,kx),"U":(ky-1,kx),"R":(ky,kx+1),"L":(ky,kx-1)}
        newPos = dirList[dir]
        newx = newPos[1]
        newy = newPos[0]
        newCell = localmap[newx][newy]
        newCell.configure(bg="blue")        
        kx = newx
        ky = newy
    prepared = False
    
        
        


def mazeBFS(x,y,moveList):
    global queue        
    
    localmap[x][y].configure(bg="red",fg = "white")
    aroundPointList = [(y+1,x,"D"),(y-1,x,"U"),(y,x+1,"R"),(y,x-1,"L")]
    if x==m and y==n:
        return
    time.sleep(speed)
    for aroundPoint in aroundPointList:
        xAround = aroundPoint[1]
        yAround = aroundPoint[0]
        if 0<=xAround<=m-1 and 0<=yAround<=n-1:#좌표가 IndexError를 일으키는가
            cell = localmap[xAround][yAround]                       
            if cell.cget("bg") not in ["red", "black",'orange']:
                if (yAround,xAround) == endPos:
                    cell.configure(text = str(int(localmap[x][y].cget("text"))+1))
                    queue = deque()                                     
                    getPath(moveList)
                    break                    
                else:   
                    cell.configure(bg='orange',text = str(int(localmap[x][y].cget("text"))+1))                    
                    queue.append(((yAround,xAround),moveList+aroundPoint[2]))
    
                
def coloring():     
    global isProcessing         
    if not isProcessing:
        isProcessing = True
        queue.append((startPos,""))           
        while queue:
            p = queue.popleft()            
            mazeBFS(p[0][1],p[0][0],p[1])
        isProcessing = False



def start():
    global prepared    
    if prepared:        
        thread = threading.Thread(target=coloring)
        thread.daemon = True  # 메인 프로그램 종료 시 스레드도 종료
        thread.start()
    
    
def clear():
    global queue   
    global isProcessing
    global prepared
    if not isProcessing:
        isProcessing = True
        queue = deque()                
        localmap[endPos[1]][endPos[0]].configure(text='0')  
        localmap[startPos[1]][startPos[0]].configure(bg="red") 
        for row in localmap:
            for cell in row:
                if not cell in [localmap[startPos[1]][startPos[0]],localmap[endPos[1]][endPos[0]]]:
                    cell.configure(bg="white",text = "0",fg="black")
        isProcessing = False
    prepared = True

def reset():
    global prepared
    global isProcessing    
    if not isProcessing:
        isProcessing = True
        localmap[endPos[1]][endPos[0]].configure(text='0')  
        localmap[startPos[1]][startPos[0]].configure(bg="red") 
        for row in localmap:
                for cell in row:                    
                    cell.configure(fg="white")
                    if not cell in [localmap[startPos[1]][startPos[0]],localmap[endPos[1]][endPos[0]]] and not cell.cget("bg") =="black" :                        
                            cell.configure(bg="white",text = "0",fg = "black")
        isProcessing = False
    prepared = True

currentMode = 0

def changeMode():
    global modes
    global currentMode

    currentMode += 1
    if currentMode == 4:
        currentMode = 0

    if currentMode == 0:
        modes = [True,False,False,False]
        modeChangeButton.configure(bg="red",text="시작점 지정")
    elif currentMode == 1:
        modes = [False,True,False,False]
        modeChangeButton.configure(bg="green",text="도착점 지정")
    elif currentMode == 2:
        modes = [False,False,True,False]
        modeChangeButton.configure(bg="black",text="벽 지정")
    elif currentMode == 3:
        modes = [False,False,False,True]
        modeChangeButton.configure(bg="pink",text="벽 제거")

def makeNoise():    
    global isProcessing
    global prepared

    perList = [False,False,True]
    if not isProcessing:
        isProcessing = True
        localmap[endPos[1]][endPos[0]].configure(text='0')  
        localmap[startPos[1]][startPos[0]].configure(bg="red") 
        for row in localmap:
                for cell in row:
                    blorwh = random.choice(perList)
                    if not cell in [localmap[startPos[1]][startPos[0]],localmap[endPos[1]][endPos[0]]]:
                        if blorwh:
                            cell.configure(bg="black",fg="white",text='0')
                        else:
                            cell.configure(bg="white",fg="black",text='0')
        isProcessing = False
    prepared = True

def getSpeed(self):    
   global speed
   newspeed = scale.get()/1000
   speed = newspeed
   
   

        
buttonsFrame = Frame(window)
buttonsFrame.pack(side="left")
        

startButton = Button(buttonsFrame,text="시작",width=10,height=5,command=start,bg="yellow",font=font)
startButton.pack()

resetButton = Button(buttonsFrame,text="다시",width=10,height=5,command=reset,bg="purple",fg="white",font=font)
resetButton.pack()

clearButton = Button(buttonsFrame,text="클리어",width=10,height=5,command=clear,bg="white",font=font)
clearButton.pack()


modeChangeButton = Button(buttonsFrame,text="시작점 지정",width=10,height=5,command=changeMode,bg="red",fg="white",font=font)
modeChangeButton.pack()

noiseButton = Button(buttonsFrame,text="MakeSome\nNoise",width=10,height=5,command=makeNoise,bg="blue",fg="white",font=font)
noiseButton.pack()

scale=tkinter.Scale(buttonsFrame, variable=speed,command=getSpeed, orient="vertical", showvalue=False, tickinterval=1, to=100, length=200,from_=1)
scale.pack()

speedLabel = Label(buttonsFrame,text="속도 조절",width=10,height=2,bg="violet",font=font)
speedLabel.pack()



window.mainloop()





