#jumpcutterGUI!#

from tkinter import *
from tkinter import filedialog
import os.path
from subprocess import call

root = Tk()
root.title('JumpCutter v3 GUI!')

def openDialog():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("Video Files", ".mp4 .avi .mpg .mkv .webm .mpeg .m4v"),("Other", "*.*")))
    inputFileLocation = root.filename
    print(inputFileLocation)
    
launchDialog = Button(root, text="Select Input File", command=openDialog)
launchDialog.pack()


silentSpeed = 99
silentThreshold = 0.04
frameMargin = 1

root.mainloop()
