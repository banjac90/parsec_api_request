from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class PandasModel(QtCore.QAbstractTableModel):
    """
    Model created from QAbstractTableModel.
    Main function is to create model for Pandas data.
    Args:
        data: Pandas DataFrame
    """

    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):        
        return self._data.shape[0]

    def columnCount(self, index):        
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])            
            
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])