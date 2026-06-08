from MachineUtil import ControlType, ControllerEnum
import json

class Machine:
    def __init__(self, name: str, id: int, controlType: ControlType, suffix: str):
        self.name = name
        self.id = id
        self.controlType = controlType
        self.suffix = suffix

    def __str__(self):
        return f'{self.name}-{self.suffix}'.replace(' ', '-')

def loadFromJson() -> dict:
    with open('Machines/Machines.json', 'r') as file:
        base =  json.load(file)['Machines']
    
    final = {}
    for item in base:
        machine = parseJson(item)
        final[str(machine)] = machine
    
    return final

def parseJson(item: dict) -> Machine:

    controllerEnum = ControllerEnum()

    return Machine(
        item['name'],
        item["id"],
        controllerEnum.fromStr(item['controlType']),
        item['suffix']
    )

if __name__=='__main__':
    print(loadFromJson())
