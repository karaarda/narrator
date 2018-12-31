import time

class Narrator:
    def __init__(self):
        self.narrationLines = []
        self.cursorPos = 0

        self.loadNarration()
        self.loadPreviousState()

    def loadNarration(self):
        global narrator

        with open("data/narration.txt", encoding='utf-16') as narrationFile:
            
            startFound = False

            for line in narrationFile:
                if not startFound and not line.strip().startswith("<start>"):
                    self.cursorPos += 1
                else:
                    startFound = True

                self.narrationLines.append(line) 

    def loadPreviousState(self):
        pass
        #reload previous state of the narrative

    def narrate(self):
        global end
        end = True
        return 0
        #move cursor to the next position and interpret
        #take necessary actions and save the game status

    def okay(self):
        if self.cursorPos >= len(self.narrationLines):
            return False
        
        return True

def main():
    global narrator

    if not narrator.okay():
        exit()

    while not end:
        delay = narrator.narrate()
        time.sleep(delay)

if __name__ == "__main__":
    global narrator 
    narrator = Narrator()
    
    global end
    end = False

    main()