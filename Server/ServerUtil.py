import json
import os
import subprocess

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

def pingMachine(id: str) -> bool:
    try:
        with open('Machines/Machines.json', 'r') as file:
            content = json.load(file)
        
        ip_addr = '0.0.0.0'
        for machine in content['Machines']:
            if machine['id'] == int(id):
                ip_addr = machine['ip']
        result = subprocess.run(['ping', '-n', '1', ip_addr], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        print('IP Address not connected')
        return False
    except KeyError:
        print(f'IP Not Found for Machine ID: {id}')
        return False