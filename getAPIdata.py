import pandas as pd
from PyQt6.QtCore import QThread
from worker.pyqtworker import Worker
import json

#get all team machines
#headers are for auth on parsec API and, MUST BE TOP SICRET!
#Headers contains parsec API key



machine_thread = QThread()

def getMachinesFromParsecAPI(status_function, handle_results):
    print("getMachinesFromParsecAPI started")
    request_data = {
        'url': 'https://api.parsec.app/v1/teams/2K8swCWalUnTtYv7VQTnkLy0pL1/machines',
        'query': {
            'offset': 0,
            'limit': 15,
            'teamID': '2K8swCWalUnTtYv7VQTnkLy0pL1'
            }        
    }
    machine_request_worker = Worker(request_data)      
    machine_request_worker.moveToThread(machine_thread)    
    machine_thread.started.connect(machine_request_worker.send_request)
    machine_request_worker.status_message.connect(status_function)  
    machine_request_worker.results.connect(handle_results) 
    machine_request_worker.finished.connect(machine_thread.quit)
    machine_request_worker.finished.connect(machine_request_worker.deleteLater)
    machine_thread.finished.connect(machine_thread.deleteLater)
     
    machine_thread.start() 
    return machine_thread
    
user_thread = QThread()

def getUsersFromParsecAPI(status_function, handle_results):
    print("getUsersFromParsecAPI started")
    request_data ={
        'url': "https://api.parsec.app/v1/teams/2K8swCWalUnTtYv7VQTnkLy0pL1/members/",
        'query': {
        'offset': 0,
        'limit': 15,
        'teamID': '2K8swCWalUnTtYv7VQTnkLy0pL1'
        }       
    }

    user_request_worker = Worker(request_data)
    user_request_worker.moveToThread(user_thread)     
    user_thread.started.connect(user_request_worker.send_request)
    user_request_worker.status_message.connect(status_function)
    user_request_worker.results.connect(handle_results)
    user_request_worker.finished.connect(user_thread.quit)
    user_request_worker.finished.connect(user_request_worker.deleteLater)
    user_thread.finished.connect(user_thread.deleteLater)

    user_thread.start()     
    return user_thread

def parse_parsec_data(machine_data, user_data):
    
    print("parse_parsec_data started")
    machines = machine_data
    users = user_data
    #parse machines data dict
    machines = pd.DataFrame.from_dict(machines)
    machines = machines[['peer_id', 'user_id', 'name']]
    #parse users data dict
    users = pd.DataFrame.from_dict(users)
    users = users[['user_id', 'name', 'email']]

    #merge data on 'user_id' column
    data = pd.merge(machines, users, on='user_id')
    data = data[['name_y', 'name_x', 'peer_id']]
    data.rename(columns={'name_y':'user', 'name_x':'Computer Name'}, inplace=True)
    
    return data


    
