from PyQt6.QtCore import QObject, pyqtSignal
import requests
import logging

class Worker(QObject):
    status_message = pyqtSignal(str)   
    finished = pyqtSignal()
    results = pyqtSignal(dict)

    def __init__(self, data) -> None:
        super().__init__()        
        self.result = None
        self._data = data
            
    def send_request(self):        
        url = self._data['url']        
        query = self._data.get('query')        
        header = {'Authorization': 'Bearer tapi_2MpVKNJBcdp8LX70beGfYCffwWt.NDBmMzVlZDRiMWNhMzkxYzg2OGYzMDkxNTE4NTE0ZGM'}

        # if header is None:
        #     self.status_message.emit('API key is not set in enviorment variable')
        #     return
       
        try:
            # Use get method from request
            self.status_message.emit(f'Sending request to {url}' )
            response = requests.get(url=url, params=query, headers=header)                        
            response.raise_for_status()
                       
            self.result = response.json()  
            self.results.emit(self.result) 
            logging.info("done")         
            logging.info(self.result)
        except requests.HTTPError as error:  
            logging.error(f'Error during sending request to {url}: {error}')      
            self.status_message.emit(f'Error during sending request to {url}: {error}')              
        finally:
            logging.info(f'Data from {url} collected!') 
            self.status_message.emit(f'Data from {url} collected!')
            self.finished.emit()
            


