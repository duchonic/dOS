from tkinter import *

class Action:
    hrs = 0
    day = 0
    
    def __init__(self, day, hrs):
        self.day = day
        self.hrs = hrs
    
    def left(self, event):
        print("left", self.day, self.hrs, event) 
        print(blub)
    def right(self, event):                           
        print("right", self.day, self.hrs, event)
    def motion(self, event):
        print('motion pos: %s %s' % (event.x, event.y))    




master = Tk()

day = list()

buttonList = list()
buttonList.append(Button(master, text='blub'))
buttonList[0].place(x=0,y=200)


for hour in range(24):
    for day in range(7):
        action = Action(day,hour)
        btn = Button(master, text=str(hour + day*24), bg='blue', width = 3)
        btn.bind('<Button-1>', action.left)
        btn.bind('<Button-2>', action.right)
        btn.bind('<Motion>', action.motion)
        btn.configure(bg = 'red')
        btn.place(x=hour*40, y=day*20)

#msg = Message(master, text = "blub")
#msg.config(bg='lightgreen')
#msg.bind('<Motion>', motion)
#msg.pack()

 
mainloop()