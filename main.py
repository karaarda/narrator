import time

class Narrator:
    def __init__(self):
        self.narrationLines = []
        self.cursorPos = 0
        self.ENDpos = 0
        self.narrationValues = {}
        self.nestingDegree = 0

        self.loadNarration()
        self.loadPreviousState()

    def loadNarration(self):
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
        self.cursorPos += 1

        currentLine = self.narrationLines[self.cursorPos]

        currentLine = currentLine.strip()

        if currentLine.startswith("PRINT"):
            currentLine = currentLine[5:]
            currentLine = currentLine.strip()
            print(currentLine)

            return 2
        elif currentLine.startswith("GOTO"):
            currentLine = currentLine[4:]
            currentLine = currentLine.strip()

            self.cursorPos = 0
        
            for line in self.narrationLines:
                if line.strip().startswith("<" + currentLine + ">"):
                    break
                else:
                    pass

            return 0

        elif currentLine.startswith("VAR"):
            currentLine = currentLine[3:]
            currentLine = currentLine.strip()

            equalityPos = currentLine.find("=")

            name = currentLine[0:equalityPos].strip()
            value = currentLine[equalityPos+1:].strip()

            self.narrationValues[name] = value
            print(self.narrationValues)
            return 0

        elif currentLine.startswith("IF"):
            currentLine = currentLine[2:]
            currentLine = currentLine.strip()

            isPos = currentLine.find("IS")

            leftValue = currentLine[0:isPos].strip()
            rightValue = currentLine[isPos + 1:].strip()

            if leftValue in self.narrationValues and self.narrationValues[leftValue] == rightValue:
                self.nestingDegree += 1
                for i in range(self.cursorPos, len(self.narrationLines)):
                    if self.narrationLines[i].startswith("END"):
                        self.ENDpos = i
                        return 0
            else:
                dummy_nd = self.nestingDegree + 1  # dummy nesting degree
                for i in range(self.cursorPos, len(self.narrationLines)):
                    if self.narrationLines[i].startswith("ELSE"):
                        self.cursorPos = i - 1  # narrate will increase cursorPos by 1 next time so it will correspond to the line where ELSE is
                        break
                    elif self.narrationLines[i].startswith("IF"):  # this line and below is for nested if statements
                        dummy_nd += 1
                    elif self.narrationLines[i].startswith("END"):
                        dummy_nd -= 1
                        if dummy_nd == self.nestingDegree:
                            break
                return 0
                # ???
                # try to find ELSE or END
                # if ELSE found, increase nesting degree
                # else do nothing.
        elif currentLine.startswith("ELSE"):

            for i in range(self.cursorPos, len(self.narrationLines)):
                if self.narrationLines[i].startswith("END"):
                    self.ENDpos = i
            #Find corresponding END
            #To do so skip over all lines
            #Find as many ENDs as the number of IF commands found
            return 0
        elif currentLine.startswith("END"):
            self.nestingDegree -= 1
            #decrease nesting degree
            pass

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