import time
import re

from section import Section

class Narrator:
    def __init__(self):
        self.sections = []
        self.currentSection = None

        self.narrationValues = {}

        self.loadNarration()
        self.loadPreviousState()
        self.setSection("start")

    def loadNarration(self):
        with open("data/narration.txt") as narrationFile:

            currentSection = None

            for line in narrationFile:
                sectionTitle = re.search("<(\w+)>", line)

                if sectionTitle != None:
                    currentSection = Section(sectionTitle.group(1))

                elif line.strip().startswith("</>"):
                    self.sections.append(currentSection)

                else:
                    currentSection.lines.append(line)

    def setSection(self, sectionTitle):
        for section in self.sections:
            if section.title == sectionTitle:
                self.currentSection = section
                self.currentSection.restart()
                break


    def loadPreviousState(self):
        pass
        #reload previous state of the narrative

    def narrate(self):
        return self.currentSection.narrate(self)

    def okay(self):        
        return True