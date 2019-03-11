import time

from narrator import Narrator

def main():
    global narrator

    if not narrator.okay():
        #TODO show error message
        exit()

    while not end:
        delay = narrator.narrate()()
        time.sleep(delay)

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
    global narrator 
    narrator = Narrator()
    narrator.onInputListener = onInputListener
    narrator.onGameLoadedListener = onGameLoadedListener

    narrator.start()

    global end
    end = False

    main()