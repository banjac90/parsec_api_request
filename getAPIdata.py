import pandas as pd
from PyQt5.QtCore import QThread, QMutex
from worker.pyqtworker import Worker

#get all team machines
#headers are for auth on parsec API and, MUST BE TOP SICRET!
#Headers contains parsec API key

# def getMachinesFromParsecAPI(status_function, handle_results):
#     # url = request_data["url"]
#     # query = request_data.get('query')        
#     # header = {'Authorization': 'Bearer tapi_2MpVKNJBcdp8LX70beGfYCffwWt.NDBmMzVlZDRiMWNhMzkxYzg2OGYzMDkxNTE4NTE0ZGM'}

#     # try:
#     #     response = requests.get(url=url, params=query, headers=header)                        
#     #     response.raise_for_status()
#     #     result = response.json() 
#     # except requests.HTTPError as error:  
#     #     print(f'Error during sending request to {url}: {error}')  
#     # finally:
#     #     return result['data']
    

machine_thread = QThread()
user_thread = QThread()
mutex = QMutex()

def getMachinesFromParsecAPI(status_function, handle_results, second_thread):
    
    request_data = {
        'url': 'https://api.parsec.app/v1/teams/2K8swCWalUnTtYv7VQTnkLy0pL1/machines',
        'query': {
            'offset': '0',
            'limit': '15',
            'teamID': '2K8swCWalUnTtYv7VQTnkLy0pL1'
        }
    }
    
    machine_request_worker = Worker(request_data)
    machine_request_worker.moveToThread(machine_thread)
    
    def machine_finished():
        machine_thread.quit()
        machine_request_worker.deleteLater()
        machine_thread.deleteLater()
        second_thread()
    
    machine_thread.started.connect(machine_request_worker.send_request)
    machine_request_worker.status_message.connect(status_function)
    machine_request_worker.results.connect(handle_results)
    machine_request_worker.finished.connect(machine_finished)
    machine_thread.start()

def getUsersFromParsecAPI(status_function, handle_results, update_data):           
    request_data ={
        'url': "https://api.parsec.app/v1/teams/2K8swCWalUnTtYv7VQTnkLy0pL1/members",
        'query': {
            'offset': '0',
            'limit': '15',
            'teamID': '2K8swCWalUnTtYv7VQTnkLy0pL1'
        }
    }
    
    user_request_worker = Worker(request_data)
    user_request_worker.moveToThread(user_thread)
    
    def user_finished():
        user_thread.quit()
        user_request_worker.deleteLater()
        user_thread.deleteLater()   
        update_data()
             

    user_thread.started.connect(user_request_worker.send_request)
    user_request_worker.status_message.connect(status_function)
    user_request_worker.results.connect(handle_results)
    user_request_worker.finished.connect(user_finished)
    
    user_thread.start()
    
   
# def getUsersFromParsecAPI(status_function, handle_results):

#     # url = request_data["url"]
#     # query = request_data.get('query')        
#     # header = {'Authorization': 'Bearer tapi_2MpVKNJBcdp8LX70beGfYCffwWt.NDBmMzVlZDRiMWNhMzkxYzg2OGYzMDkxNTE4NTE0ZGM'}

#     # try:
#     #     response = requests.get(url=url, params=query, headers=header)                        
#     #     response.raise_for_status()
#     #     result = response.json() 
#     # except requests.HTTPError as error:  
#     #     print(f'Error during sending request to {url}: {error}')  
#     # finally:
#     #     return result['data']


def parse_parsec_data(machine_data, user_data): 
    print("parse_parsec_data started")
    machines = machine_data    
    users = user_data    
    data = None
    #parse machines data dict
    machines = pd.DataFrame.from_dict(machines)
    machines = machines[['peer_id', 'user_id', 'name']]
    print(f"Machines: {machines}")
    #parse users data dict
    users = pd.DataFrame.from_dict(users)
    users = users[['user_id', 'name', 'email']]
    print(f"Users: {users}")
    #merge data on 'user_id' column
    data = pd.merge(machines, users, on='user_id')
    data = data[['name_y', 'name_x', 'peer_id']]
    data.rename(columns={'name_y':'user', 'name_x':'Computer Name'}, inplace=True)
    data.rename(columns={'name_y':'user', 'name_x':'Computer Name'}, inplace=True)    
    data.rename(columns={'name_y':'user', 'name_x':'Computer Name'}, inplace=True)    
    
    return data
    


    
