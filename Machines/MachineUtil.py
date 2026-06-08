import json

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

def getIDs() -> list:
    with open('Machines/Machines.json', 'r') as file:
        content = json.load(file)['Machines']
    
    ids = []
    for item in content:
        ids.append(item['id'])
    
    return ids

def addMachine(name: str, id: int, controlType: ControlType, suffix: str) -> None:
    if id not in getIDs():
        machine = {'name': name, 'id': id, 'controlType': str(controlType), 'suffix': suffix}
        with open('Machines/Machines.json', 'r') as file:
            content = json.load(file)
        content['Machines'].append(machine)
        with open('Machines/Machines.json', 'w') as file:
            json.dump(content, file)

def deleteMachineByID(id: int) -> None:
    if id in getIDs():
        with open('Machines/Machines.json', 'r') as file:
            content = json.load(file)
        
        for item in content['Machines']:
            if id == item['id']:
                itemIndex = content['Machines'].index(item)
                break
        
        content['Machines'].pop(itemIndex)

        with open('Machines/Machines.json', 'w') as file:
            json.dump(content, file)