import time

from narrator import Narrator

def main():
    global narrator
    narrator = Narrator()
    narrator.eventHandler.subscribe("inputRequest", onInputListener)
    narrator.eventHandler.subscribe("gameLoaded", onGameLoadedListener)
    narrator.eventHandler.subscribe("narratorReady", onReadyListener)
    narrator.eventHandler.subscribe("newCommand", onNewCommandListener);

    narrator.start()

def onReadyListener():
    narrator.narrate()

def onNewCommandListener(data):
    data["command"]()
    narrator.narrate()

def onInputListener(options, onInput):

    for i in range(len(options)):
        print( i, ". " , options[i]["message"] , sep='')

    userInput = int(input())

    onInput(userInput)
    
def onGameLoadedListener():

    print('Do you want to load the previously saved game?\n0.No\n1.Yes')

    userInputLoad = int(input())

    if userInputLoad == 0:
        narrator.startNewNarrative()
    else:
        narrator.fastForward()

if __name__ == "__main__":
    main()