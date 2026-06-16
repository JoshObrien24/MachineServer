import json
import os

def addFileToQueue(id: int, filename: str):
    id = f"{id}"

    with open('Server/Uploads/queue.json', 'r') as file:
        content = json.load(file)
    
    try:
        t = content[id]
    except KeyError:
        content[id] = []
    
    content[id].append(filename)

    with open('Server/Uploads/queue.json', 'w') as file:
        json.dump(content, file, indent=2)

def verifyQueue(id: int, filename: str) -> bool:
    id = f"{id}"

    with open('Server/Uploads/queue.json', 'r') as file:
        content = json.load(file)
    
    try:
        t = content[id]
    except KeyError:
        content[id] = []
    
    print(content[id], filename)
    return not filename in content[id]

def getQueue():
    with open('Server/Uploads/queue.json', 'r') as file:
        return json.load(file)

def createQueueFile():
    try:
        with open('Server/Uploads/queue.json', 'r'):
            ...
    except FileNotFoundError:
        try:
            with open('Server/Uploads/queue.json', 'w') as file:
                json.dump({}, file)
        except FileNotFoundError:
            os.mkdir("Server/Uploads")
            with open('Server/Uploads/queue.json', 'w') as file:
                json.dump({}, file)
