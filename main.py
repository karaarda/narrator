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
    
def loadGameListener(onInputLoad):

    print('Do you want to load the previously saved game?\n0.No\n1.Yes')

    userInputLoad = int(input())

    onInputLoad(userInputLoad)

if __name__ == "__main__":
    global narrator 
    narrator = Narrator()
    narrator.onInputListener = onInputListener
    narrator.loadGameListener = loadGameListener

    global end
    end = False

    main()