from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton, 
    QTableView, 
    QTextEdit,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout    
)
import sys
import os
import pandas as pd
from pandasModel import PandasModel
from getAPIdata import getMachinesFromParsecAPI, getUsersFromParsecAPI, parse_parsec_data

api_user_data = None
api_machine_data = None

class ParsecApp(QMainWindow):
    def __init__(self):
        os.environ['PARSEC_AUTH_HEADER'] = 'Bearer tapi_2MpVKNJBcdp8LX70beGfYCffwWt.NDBmMzVlZDRiMWNhMzkxYzg2OGYzMDkxNTE4NTE0ZGM'
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Parsec data generator")
        self.data = pd.DataFrame()
        self.resize(600, 800)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.setData = QPushButton(self)        
        self.table = QTableView(self)
        self.inofo_text = QTextEdit(self)
        self.inofo_text.setReadOnly(True)
        #self.update_status()
        self.update_status("App Initialized")
        self.setData.clicked.connect(self.set_data_to_table)        
        self.setData.setText("Send API request")         
        self.table.showGrid()

        # Layout for button and TextEdit
        one_third_layout = QHBoxLayout()
        one_third_layout.addWidget(self.inofo_text)
        one_third_layout.addWidget(self.setData)

        # Main app layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(one_third_layout)     
        main_layout.addWidget(self.table)
        self.centralWidget.setLayout(main_layout)       

    def machines_request(self):       
        global api_machine_data 
        thread = getMachinesFromParsecAPI(self.update_status, self.handle_machine_data) 
        thread.wait()
        machines = api_machine_data        
        machines = machines['machines'] 
        print(machines)    
        return machines

    def users_request(self):     
        global api_user_data   
        thread = getUsersFromParsecAPI(self.update_status, self.handle_user_data)
        thread.wait()         
        users = api_user_data       
        users = users['users'] 
        print(users)   
        return users  

    def set_data_to_table(self):        
        machines_data = self.machines_request()        
        users_data = self.users_request()                
        self.data = parse_parsec_data(machines_data, users_data)        
        self.model = PandasModel(self.data)        
        self.table.setModel(self.model)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        #self.inofo_text.setText("Done!")

    def update_status(self, messages):
        self.inofo_text.append(messages)   

    def handle_user_data(result): 
        global api_user_data
        print(result)       
        api_user_data = result

    def handle_machine_data(result): 
        global api_machine_data
        print(result)       
        api_machine_data = result    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ParsecApp()
    main.show()



    sys.exit(app.exec())   
    

