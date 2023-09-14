from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton, 
    QTableView, 
    QTextEdit,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,     
)
import sys
import os
import pandas as pd
from pandasModel import PandasModel
from getAPIdata import getMachinesFromParsecAPI, getUsersFromParsecAPI, parse_parsec_data
from PyQt5.QtCore import QThread, QMutex

  

class ParsecApp(QMainWindow):
    def __init__(self):        
        super().__init__()
        os.environ['PARSEC_AUTH_HEADER'] = 'Bearer tapi_2MpVKNJBcdp8LX70beGfYCffwWt.NDBmMzVlZDRiMWNhMzkxYzg2OGYzMDkxNTE4NTE0ZGM'
        self.initUI()
        
    
    def initUI(self):
        self.machines_data = None
        self.users_data = None      
        self.machines_data_ready = False
        self.user_data_ready = False


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
        self.inofo_text.append("App Initialized")
        self.setData.clicked.connect(self.run_api_threads)        
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


    def handle_user_data(self, result): 
        try:
            print(result)
            self.users_data = result.get('data', {})
            self.user_data_ready = True
            self.check_and_update_table()
        except Exception as e:
            self.inofo_text.append(f"Error handling user data: {str(e)}")

    def handle_machine_data(self, result): 
        try:
            print(result)        
            self.machines_data = result.get('data', {})
            self.machines_data_ready = True
            self.check_and_update_table()
        except Exception as e:
            self.inofo_text.append(f"Error handling machine data: {str(e)}")

    def check_and_update_table(self):
        if self.machines_data_ready and self.user_data_ready:
            self.set_data_to_table()

    def run_api_threads(self):           
        if not self.machines_data_ready and not self.user_data_ready:
            self.inofo_text.append("Sending API requests...")
            self.setData.setEnabled(False)  # Disable the button during requests
            getMachinesFromParsecAPI(self.inofo_text.append, self.handle_machine_data)              
            getUsersFromParsecAPI(self.inofo_text.append, self.handle_user_data)
        else:
            self.check_and_update_table()
            self.inofo_text.append("Data already retrieved and displayed.")
    
    def set_data_to_table(self): 
        self.data = parse_parsec_data(self.machines_data, self.users_data)        
        self.model = PandasModel(self.data)        
        self.table.setModel(self.model)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents() 
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ParsecApp()
    main.show()
    sys.exit(app.exec())   
    

