from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import os.path
import shutil
from subprocess import call



window = Tk()
window.title("Jumpcutter GUI")
window.geometry('320x330')
window.resizable(False, False)


videoFileGUI = ""
silentSpeedGUI = ""
silentThresholdGUI = ""
frameMarginGUI = ""
stemCommand = "python fast_video.py"

# First group of widgets - select original file and place to save jumpcutted version
group1 = LabelFrame(window, text="Main", padx=1, pady=1)
group1.grid(padx=1, pady=1)

labelLocalFile = Label(group1, text="Video File Location")
labelLocalFile.grid(column=0, row=1)

fileLocation = Entry(group1,width=48)
fileLocation.grid(column=0, row=2)



# Action after pressing ... button to selectfile
def selectFileItem():
    # Open file selecter and making path variable
    global videoFileGUI
    videoFileGUI = filedialog.askopenfilename()
    # Writing path to label
    fileLocation.insert(END, videoFileGUI)
    # Getting table with base filename
    baseFileName = os.path.basename(videoFileGUI)
    # Variable only with extension
    extension = os.path.splitext(baseFileName)[1]
    # Original path to file without file and extension
    originalPath = videoFileGUI.replace(baseFileName, '')
    # Combining original Path with filename (without extension)
    finalname = (originalPath + os.path.splitext(baseFileName)[0])
    # Inserting original Path with filename + _jumpcut suffix + original extension


# Button to open file item selection box
selectFile = Button(group1, text="...", command=selectFileItem)
selectFile.grid(column=2, row=2)


labelLocalFile.grid()
fileLocation.grid()
selectFile.grid()


# Group 2 - it is for general manipulation, FPS, sounded speed, silent threshold, silent speed
group2 = LabelFrame(window, text="General", padx=1, pady=1)
group2.grid(padx=0, pady=0)

label3 = Label(group2, text="Frame Margin (default=1)")
label3.grid(column=0,row=5)
frameMarginGUI = Entry(group2,width=4)
frameMarginGUI.insert(0, '1')
frameMarginGUI.grid(column=4, row=5)

label4 = Label(group2, text="Silent threshold (from 0 to 1) (default=0.04)")
label4.grid(column=0,row=7)
silentThresholdGUI = Entry(group2,width=4)
silentThresholdGUI.insert(0, '0.04')
silentThresholdGUI.grid(column=4, row=7)

label5 = Label(group2, text="Silent speed (default=99)")
label5.grid(column=0,row=9)
silentSpeedGUI = Entry(group2,width=4)
silentSpeedGUI.insert(0, '99')
silentSpeedGUI.grid(column=4, row=9)






# Action after clicking start button
def execute():
    fast_video_function(videoFileGUI, float(silentSpeedGUI.get()), float(silentThresholdGUI.get()), int(frameMarginGUI.get()))

executeButton = Button(window, text="Start", command=execute)
executeButton.grid(column=0,row=8)
window.mainloop()