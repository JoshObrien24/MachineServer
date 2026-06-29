import json
try: 
    from Server.ServerUtil import pingMachine, createArpTable
except ImportError:
    pass

types = []

class ControlType:
    def __init_subclass__(cls):
        global types
        types.append(cls.__name__)

class Marlin(ControlType):
    def __str__(self):
        return self.__name__

class GRBL(ControlType):
    def __str__(self):
        return self.__name__
    
class ControllerEnum:
    global types

    @classmethod
    def fromStr(cls, controlType: str):
        for item in types:
            if controlType == str(item):
                return item
    
    def __str__(self):
        return ', '.join(types)

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
            json.dump(content, file, indent=2)

def addMachineJSON(machine: dict) -> None:
    ids = getIDs()
    
    with open('Machines/Machines.json', 'r') as file:
        content = json.load(file)
    try:
        machine['id']
    except KeyError:
        ids.sort()
        if len(ids) != 0:
            machine['id'] = ids[-1] + 1
        else:
            machine['id'] = 0
    content['Machines'].append(machine)
    with open('Machines/Machines.json', 'w') as file:
        json.dump(content, file, indent=2)

def deleteMachineByID(id: int) -> None:
    id = f"{id}"

    if id in getIDs():
        with open('Machines/Machines.json', 'r') as file:
            content = json.load(file)
        
        for item in content['Machines']:
            if id == item['id']:
                itemIndex = content['Machines'].index(item)
                break
        
        content['Machines'].pop(itemIndex)

        with open('Machines/Machines.json', 'w') as file:
            json.dump(content, file, indent=2)

def getStatus(id: int) -> dict:
    id = f"{id}"
    createArpTable()
    connected = pingMachine(id)
    busy = False
    
    with open('Server/Uploads/queue.json', 'r') as file:
        content = json.load(file)

    try:
        if len(content[id]) > 0 and connected:
            busy = True
    except KeyError:
        pass
    
    return {"connected": connected, "busy": busy}

if __name__ == '__main__':
    test = ControllerEnum()
    print(str(test))