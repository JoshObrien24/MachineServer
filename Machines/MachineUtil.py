class ControlType:
    ...

class Marlin(ControlType):
    def __str__(self):
        return 'Marlin'

class grbl(ControlType):
    def __str__(self):
        return 'GRBL'

class ControllerEnum:
    MARLIN = Marlin()
    GRBL = grbl()

    __types = [MARLIN, GRBL]

    def fromStr(self, controlType: str):
        for item in self.__types:
            if controlType == str(item):
                return item