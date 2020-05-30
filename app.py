from tkinter import *
import importlib
import threading
from time import sleep
import os
from tkinter import simpledialog
import jsonifySettings
soundPath = r'C:\\Users\\rpski\\Desktop\\V3'


def startChat():
    os.system('python -i chat.py')


def startBaxter():
    os.system('python -i baxter.py')


# START READING PREFERENCES #
def ytApiKey():
    userin = simpledialog.askstring("Youtube API Key", "Api Key")
    jsonifySettings.writeSpecificSetting('settings.json', 'ytApiKey', userin)


def takeUserInputConfigMenuoAuth():
    menuOauth = simpledialog.askstring("Twitch OAuth", "Oauth")
    jsonifySettings.writeSpecificSetting('settings.json', 'oAuth', menuOauth)
    return menuOauth


def soundsFolderLocation():
    menuSoundFolderLocation = simpledialog.askstring("Sounds Folder Location", "C:\\location\\of\\this\\file\\Sounds") + '\\'
    jsonifySettings.writeSpecificSetting('settings.json', 'soundFolderLocation', menuSoundFolderLocation)
    return menuSoundFolderLocation


def twitchLogin():
    tUser = simpledialog.askstring("Twitch Username", "Username")
    jsonifySettings.writeSpecificSetting('settings.json', 'twitchUser', tUser)
    tPass = simpledialog.askstring("Twitch Password", "Password")
    jsonifySettings.writeSpecificSetting('settings.json', 'twitchPass', tPass)
    return tUser, tPass


def listDir(dir):
    commandList = []
    commands = []
    fileNames = os.listdir(dir)
    for fileName in fileNames:
        fileName = fileName[:-4]
        commandList.append(fileName)
        commands.append('!' + fileName)

    return commandList, commands

# STOP READING PREFERENCES #
# 
# START WRITE PREFERENCES FUNCTIONS #


# TTS
def writePrefTtsTrue():
    jsonifySettings.writeSpecificSetting('settings.json', 'ttsSetting', 1)


def writePrefTtsFalse():
    jsonifySettings.writeSpecificSetting('settings.json', 'ttsSetting', 0)


# SOUND
def writePrefSoundTrue():
    jsonifySettings.writeSpecificSetting('settings.json', 'soundSetting', 1)


def writePrefSoundFalse():
    jsonifySettings.writeSpecificSetting('settings.json', 'soundSetting', 0)


def chatFileIndicatorTrue():
    print('chat indicator true')
    jsonifySettings.writeSpecificSetting('settings.json', 'chatRunning', 1)


def chatFileIndicatorFalse():
    jsonifySettings.writeSpecificSetting('settings.json', 'chatRunning', 0)


def sliderFileIndicatorTts(val):
    jsonifySettings.writeSpecificSetting('settings.json', 'ttsMaxChars', int(val))


def sliderFileIndicatorSoundsCoolDown(val):
    jsonifySettings.writeSpecificSetting('settings.json', 'sliderFileIndicatorSoundsCoolDown', int(val))


def autoPlayTrue():
    jsonifySettings.writeSpecificSetting('settings.json', 'autoPlaySR', 1)


def autoPlayFalse():
    jsonifySettings.writeSpecificSetting('settings.json', 'autoPlaySR', 0)


# STOP WRITE PREFERENCES FUNCTIONS #
# 
# START BUTTON FUNCTIONS #


#  TTS 
def ttsButtonFunction():
    if ttsStatus['bg'] == 'red':
        ttsStatus['bg'] = 'green'
        writePrefTtsTrue()
        print('write true')
    else:
        ttsStatus['bg'] = 'red'
        writePrefTtsFalse()
        print('write false')


# SOUND
def soundsButtonFunction():
    if soundStatus['bg'] == 'red':
        soundStatus['bg'] = 'green'
        writePrefSoundTrue()
        print('write true')
    else:
        writePrefSoundFalse()
        print('write false')
        soundStatus['bg'] = 'red'


# Autoplay Song Requests
def autoPlaySRButtonFunction():
    if autoPlayStatus['bg'] == 'red':
        autoPlayStatus['bg'] = 'green'
        autoPlayTrue()
        print('write auto play! true')
    else:
        autoPlayStatus['bg'] = 'red'
        autoPlayFalse()
        print('write auto play false')


# CONNECT TO CHAT
def chatConnect():
    if chatStatuss['bg'] == 'red':
        chatStatuss['bg'] = 'green'
        chatStatuss['text'] = 'Disconnect to chat!'
        chatConnectButton['text'] = 'Disconnect from Chat'
        try:
            chatFileIndicatorTrue()
            x = threading.Thread(target=startChat, args=())
            # x.daemon = True
            x.start()
            sleep(1)
        except Exception as e:
            print(e)

    elif chatStatuss['bg'] == 'green':
        print('else')
        chatFileIndicatorFalse()
        sleep(1)
        chatConnectButton['text'] = 'Connect to Chat'
        chatStatuss['bg'] = 'red'
        chatStatuss['text'] = 'Connect to chat!'


# Start Baxter
def connectBaxter():
    if baxterStatus['bg'] == 'red':
        baxterStatus['bg'] = 'green'
        baxterStatus['text'] = 'Disconnect Baxter'
        startBaxterButton['text'] = 'Disconnect Baxter'
        jsonifySettings.writeSpecificSetting('settings.json', 'baxterRunning', 1)
        x = threading.Thread(target=startBaxter, args=())
        x.start()
        sleep(1)
    elif baxterStatus['bg'] == 'green':
        jsonifySettings.writeSpecificSetting('settings.json', 'baxterRunning', 0)
        sleep(1)
        startBaxterButton['text'] = 'Connect Baxter'
        baxterStatus['bg'] = 'red'
        baxterStatus['text'] = 'Connect Baxter!'


def getSliderValueTts(val):
    print(val)
    sliderFileIndicatorTts(val)


def getSliderValueSoundsCoolDown(val):
    print(val)
    sliderFileIndicatorSoundsCoolDown(val)


def scanSounds():
    commandList, commands = listDir(soundPath)
    print('Sounds files imported, commands have been generated')
    

# STOP BUTTON FUNCTIONS #



# Mercy on all ye who dare continue beyond this point
window = Tk()

window.title('Test window')

topFrame = Frame(window)
topFrame.pack()
bottomFrame = Frame(window)
bottomFrame.pack(side=BOTTOM)

ttsButton = Button(topFrame, text="TTS", width=12, command=ttsButtonFunction)
soundButton = Button(topFrame, text="Sounds", width=12, command=soundsButtonFunction)
autoPlaySRButton = Button(topFrame, text="Auto Play Song Requests", width=19, command=autoPlaySRButtonFunction)
chatConnectButton = Button(topFrame, text=" Connect To Chat ", command=chatConnect)
startBaxterButton = Button(topFrame, text=" Start Baxter ", command=connectBaxter)
horizSliderTts = Scale(topFrame, from_=0, to=500, orient=HORIZONTAL, command=getSliderValueTts)
horizSliderTts.set(65)
ttsSliderLabel = Label(topFrame, text='TTS Characters Max')
horizSliderSoundCoolDown = Scale(topFrame, from_=0, to=20, orient=HORIZONTAL, command=getSliderValueSoundsCoolDown)
horizSliderSoundCoolDown.set(10)
soundsCoolDownSliderLabel = Label(topFrame, text='Sound Cooldown Length')


menu = Menu(window)
window.config(menu=menu)
fileMenu = Menu(menu)
fileMenu.add_command(label='Scan Sounds', command=scanSounds)
edit = Menu(menu)
edit.add_command(label='Twitch Oauth', command=takeUserInputConfigMenuoAuth)
edit.add_command(label='YT API key', command=ytApiKey)
edit.add_command(label='Twitch Login Information', command=twitchLogin)
edit.add_command(label='Sounds Folder Location', command=soundsFolderLocation)
menu.add_cascade(label='File', menu=fileMenu)
menu.add_cascade(label='Configure', menu=edit)


ttsSliderLabel.pack(side=BOTTOM, pady=(0,10))
horizSliderTts.pack(side=BOTTOM, pady=(0,0))
soundsCoolDownSliderLabel.pack(side=BOTTOM)
horizSliderSoundCoolDown.pack(side=BOTTOM)
ttsButton.pack(pady=(40,13))
soundButton.pack(pady=13)
autoPlaySRButton.pack(pady=13)
startBaxterButton.pack(pady=13)
chatConnectButton.pack(pady=(13,40))



ttsStatus = Label(bottomFrame, text='Text To Speech', bd=1, relief=SUNKEN, anchor=W, bg='red')
ttsStatus.pack(side=LEFT, fill=X)
soundStatus = Label(bottomFrame, text='Sound Commands', bd=1, relief=SUNKEN, anchor=W, bg='red')
soundStatus.pack(side=LEFT, fill=X)
autoPlayStatus = Label(bottomFrame, text='Auto Play Song Requests', bd=1, relief=SUNKEN, anchor=W, bg='red')
autoPlayStatus.pack(side=LEFT, fill=X)
baxterStatus = Label(bottomFrame, text='Baxter Offline', bd=1, relief=SUNKEN, anchor=W, bg='red')
baxterStatus.pack(side=LEFT, fill=X, pady=1)
chatStatuss = Label(bottomFrame, text='Chat Offline', bd=1, relief=SUNKEN, anchor=W, bg='red')
chatStatuss.pack(side=LEFT, fill=X, pady=1)


def check_requests_for_auto_play():
    with open('songRequests.txt', 'r+') as fin:
        data = fin.readlines()
        if data:
            return True
        else:
            return False


def look_for_request():
    nextUp = ''
    with open('songRequests.txt', 'r+') as fin:
        data = fin.readlines()
        if data:
            nextUp = data[0]
    with open('songRequests.txt', 'w') as fin:
        fin.write("".join(data[1:]))

    try:
        print(data)
        print(nextUp)
        print(("".join(data[1:])))
    except Exception as e:
        print('No requests')

    if nextUp:
        return nextUp
    else:
        print('No song requests')
        return ""


def check_song_request_file():
    sr_settings = jsonifySettings.readSpecificSetting('settings.json', 'autoPlaySR')
    requests_present = check_requests_for_auto_play()
    if sr_settings == 1 and requests_present is False:
        autoPlayStatus['bg'] = 'yellow'
    elif sr_settings == 1 and requests_present is True:
        autoPlayStatus['bg'] = 'green'
    elif sr_settings == 0 and requests_present is True:
        autoPlayStatus['bg'] = 'red'

    window.after(1000, check_song_request_file)

window.after(1000, check_song_request_file)
window.mainloop()

