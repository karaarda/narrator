import re

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

    def narrate(self, narrator):

        currentLine = self.lines[self.cursorPos]

        command = None

        if currentLine.startswith("PRINT"):
            command = self.command_print(narrator, currentLine[5:].strip())

        elif currentLine.startswith("GOTO"):
            command = self.command_goto(narrator, currentLine[4:].strip())

        elif currentLine.startswith("VAR"):
            command = self.command_var(narrator, currentLine[3:].strip())

        elif currentLine.startswith("OPTION"):
            command = self.command_option(narrator, currentLine)

        elif currentLine.startswith("DELAY"):

            if narrator.config["fastForward"] == "True":
                pass #return fastForward command

            command = self.command_delay(narrator, currentLine[5:].strip())

        elif currentLine.startswith("IF"):
            command = self.command_if(narrator, currentLine[2:].strip())

        elif currentLine.startswith("ELSE"):
            command = self.command_else(narrator)

        elif currentLine.startswith("END"):
            command = self.command_end(narrator)

        narrator.eventHandler.fireEvent("newCommand", {"command": command})

    def get_action(self, command):
        pass

    def command_print(self, narrator, toPrint):
        def command():
            nonlocal self
            nonlocal narrator
            nonlocal toPrint

            print(toPrint)

            self.cursorPos += 1
            
            return 2

        return command

    def command_goto(self, narrator, section):
        def command():
            nonlocal self
            nonlocal narrator
            nonlocal section
            
            narrator.setSection(section)

            return 0

        return command

    def command_var(self, narrator, dataString):
        def command():
            nonlocal self
            nonlocal narrator
            nonlocal dataString

            data = dataString.split('=')
            narrator.narrationValues[data[0].strip()] = data[1].strip()

            self.cursorPos += 1
            
            return 0

        return command

    def command_option(self, narrator, currentLine):
        def command():
            nonlocal self
            nonlocal narrator
            nonlocal currentLine

            options = []
            
            i = self.cursorPos

            while self.lines[i].startswith("OPTION"):                
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
                else:
                    break

            def onInput(userInput):
                narrator.setSection(options[userInput]["name"].strip())

                narrator.decisions += str(userInput)
                narrator.save()

                if narrator.config["debug"] == "True":
                    print("<" + options[userInput]["name"].strip() + ">")

            narrator.requestInput( options, onInput)

            return 0

        return command

    def command_delay(self, narrator, timeString):
        def command():
            nonlocal self
            nonlocal narrator
            nonlocal timeString

            hour = re.search("([1-9]{1}[0-9]{0,})h", timeString)
            minute = re.search("([1-9]{1}[0-9]{0,})m", timeString)
            second = re.search("([1-9]{1}[0-9]{0,})s", timeString)

            delay = 0

            if hour != None:
                delay += int(hour.group(1)) * 60 * 60
            if minute != None:
                delay += int(minute.group(1)) * 60
            if second != None:
                delay += int(second.group(1))

            self.cursorPos += 1

            return 0

        return command

    def command_if(self, narrator, condition):
        def command():
            nonlocal self
            nonlocal narrator
            nonlocal condition

            conditionTokens = condition.split("IS")

            leftValue = conditionTokens[0]
            rightValue = conditionTokens[1]

            if narrator.config["debug"] == "True":
                print("right value: " + rightValue)
                print("left value: " + narrator.narrationValues[leftValue])

            if leftValue in narrator.narrationValues and narrator.narrationValues[leftValue] == rightValue:
                self.nestingDegree += 1
            else:
                dummy_nd = 0

                for i in range(self.cursorPos+1, len(self.lines)):
                    if self.lines[i].startswith("END"):
                        if dummy_nd == 0:
                            self.cursorPos = i
                            break
                        else:
                            dummy_nd = dummy_nd - 1

                    elif self.lines[i].startswith("ELSE"):
                        if dummy_nd == 0:
                            self.cursorPos = i
                            break

                    elif self.lines[i].startswith("IF"):
                        dummy_nd = dummy_nd + 1
                # ???
                # try to find ELSE or END
                # if ELSE found, increase nesting degree
                # else do nothing.

            self.cursorPos += 1

            return self.narrate(narrator)()

        return command

    def command_else(self, narrator):
        def command():
            nonlocal self
            nonlocal narrator

            dummy_nd = 0

            for i in range(self.cursorPos+1, len(self.lines)):
                if self.lines[i].startswith("END"):
                    if dummy_nd == 0:
                        self.cursorPos = i
                        break
                    else:
                        dummy_nd = dummy_nd - 1
                if self.lines[i].startswith("IF"):
                    dummy_nd = dummy_nd + 1

            #Find corresponding END
            #To do so skip over all lines
            #Find as many ENDs as the number of IF commands found

            self.cursorPos += 1

            return 0
        return command

    def command_end(self, narrator):
        def command():
            nonlocal self
            nonlocal narrator

            self.nestingDegree -= 1
            #decrease nesting degree

            self.cursorPos += 1

            return 0
        return command