from Machines.MachineUtil import ControlType, ControllerEnum
import json

class Machine:
    def __init__(self, name: str, id: int, controlType: ControlType, suffix: str, macAddr: str = ""):
        self.name = name
        self.id = id
        self.controlType = controlType
        self.suffix = suffix
        self.macAddr = macAddr

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

def loadFromJsonRaw() -> dict:
    with open('Machines/Machines.json', 'r') as file:
        base = json.load(file)

    return base

def parseJson(item: dict) -> Machine:
    try:
        macAddr = item['mac']
    except KeyError:
        macAddr = ""
    return Machine(
        item['name'],
        item["id"],
        ControllerEnum.fromStr(item['controlType']),
        item['suffix'],
        macAddr
    )