#class Command
#
#    def __init__(self, function):
#        self.function = function
#
#    def execute(self, data):
#        self.function(data)

class Section:
    
    def __init__(self, title):
        self.title = title
        self.lines = []
        self.cursorPos = 0
        self.nestingDegree = 0

    def restart(self):
        self.cursorPos = 0
        self.nestingDegree = 0

    def fastForward(self, narrator, input):
        pass

    def command_print(self, narrator, toPrint):
        print(toPrint)

        self.cursorPos += 1

        return 2

    def command_goto(self, narrator, section):
        narrator.setSection(section)

        return 0

    def command_var(self, narrator, dataString):
        data = dataString.split('=')
        narrator.narrationValues[data[0]] = data[1]

        self.cursorPos += 1

        return 0

    def narrate(self, narrator):

        currentLine = self.lines[self.cursorPos]

        currentLine = currentLine.strip()

        if currentLine.startswith("PRINT"):
            return command_print(narrator, currentLine[5:].strip())

        elif currentLine.startswith("GOTO"):
            return command_goto(narrator, currentLine[4:].strip())

        elif currentLine.startswith("VAR"):
            return command_var(narrator, currentLine[3:].strip())

        elif currentLine.startswith("OPTION"):
            options = []
            
            i = self.cursorPos

            while self.lines[i].strip().startswith("OPTION"):                
                i += 1
                
                spacePos = currentLine.find(" ")
                separatorPos = currentLine.find("::")

                option = {}
                option["name"] = currentLine[separatorPos+2:spacePos]
                option["message"] = currentLine[spacePos+1:]

                options.append(option)

                self.cursorPos += 1

                if self.cursorPos < len(self.lines):
                    currentLine = self.lines[self.cursorPos]
                    currentLine = currentLine.strip()
                else:
                    break

            for i in range(len(options)):
                print( i+1 , ". " , options[i]["message"] , sep='')

            userInput = int(input())

            userInput -= 1

            narrator.decisions += str(userInput)
            narrator.save()

            if narrator.config["debug"] == "True":
                print("<" + options[userInput]["name"].strip() + ">")

            narrator.setSection(options[userInput]["name"].strip())

            return 0

        elif currentLine.startswith("DELAY"):

            if narrator.config["fastForward"] == "True":
                return 0

            currentLine = currentLine[5:]
            currentLine = currentLine.strip()

            hour = re.search("([1-9]{1}[0-9]{0,})h", currentLine)
            minute = re.search("([1-9]{1}[0-9]{0,})m", currentLine)
            second = re.search("([1-9]{1}[0-9]{0,})s", currentLine)

            delay = 0

            if hour != None:
                delay += int(hour.group(1)) * 60 * 60
            if minute != None:
                delay += int(minute.group(1)) * 60
            if second != None:
                delay += int(second.group(1))

            self.cursorPos += 1

            return delay

        elif currentLine.startswith("IF"):
            currentLine = currentLine[2:]
            currentLine = currentLine.strip()

            isPos = currentLine.find("IS")

            leftValue = currentLine[0:isPos].strip()
            rightValue = currentLine[isPos + 2:].strip()

            print("right value: " + rightValue)
            print("left value: " + narrator.narrationValues[leftValue])

            if leftValue in narrator.narrationValues and narrator.narrationValues[leftValue] == rightValue:
                self.nestingDegree += 1
            else:
                dummy_nd = 0

                for i in range(self.cursorPos+1, len(self.lines)):
                    if self.lines[i].strip().startswith("END"):
                        if dummy_nd == 0:
                            self.cursorPos = i
                            break
                        else:
                            dummy_nd = dummy_nd - 1

                    elif self.lines[i].strip().startswith("ELSE"):
                        if dummy_nd == 0:
                            self.cursorPos = i
                            break

                    elif self.lines[i].strip().startswith("IF"):
                        dummy_nd = dummy_nd + 1
                # ???
                # try to find ELSE or END
                # if ELSE found, increase nesting degree
                # else do nothing.

            self.cursorPos += 1

            return self.narrate(narrator)
        elif currentLine.startswith("ELSE"):

            dummy_nd = 0

            for i in range(self.cursorPos+1, len(self.lines)):
                if self.lines[i].strip().startswith("END"):
                    if dummy_nd == 0:
                        self.cursorPos = i
                        break
                    else:
                        dummy_nd = dummy_nd - 1
                if self.lines[i].strip().startswith("IF"):
                    dummy_nd = dummy_nd + 1

            #Find corresponding END
            #To do so skip over all lines
            #Find as many ENDs as the number of IF commands found

            self.cursorPos += 1

            return 0
        elif currentLine.startswith("END"):
            self.nestingDegree -= 1
            #decrease nesting degree
    
            self.cursorPos += 1

            return 0
        #move cursor to the next position and interpret
        #take necessary actions and save the game status