import time

from narrator import Narrator

def main():
    global narrator
    narrator = Narrator()
    narrator.eventHandler.subscribe("inputRequest", onInputListener)
    narrator.eventHandler.subscribe("gameLoaded", onGameLoadedListener)
    narrator.eventHandler.subscribe("narratorReady", onReadyListener)
    narrator.eventHandler.subscribe("step", onNarrationStepListener)
    narrator.eventHandler.subscribe("print", onPrintListener)

    narrator.start()

def onReadyListener(data):
    narrator.narrate()

def onNarrationStepListener(data):
    narrator.narrate()

def onPrintListener(data):
    print (data['message'])

def onInputListener(data):

    for i in range(len(data["options"])):
        print( i, ". " , data["options"][i]["message"] , sep='')

    userInput = int(input())

    data["onInput"](userInput)
    
def onGameLoadedListener(data):

    print('Do you want to load the previously saved game?\n0.No\n1.Yes')

    userInputLoad = int(input())

    if userInputLoad == 0:
        narrator.startNewNarrative()
    else:
        narrator.fastForward()

if __name__ == "__main__":
    main()