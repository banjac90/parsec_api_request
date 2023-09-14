from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QUrlQuery
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import json

class Worker(QObject):
    status_message = pyqtSignal(str)
    finished = pyqtSignal()
    results = pyqtSignal(dict)

    def __init__(self, data) -> None:
        super().__init__()
        self._data = data
        self.network_manager = None
        self.network_reply = None

        self.status_message.connect(self.append_status)

    def send_request(self):
        self.network_manager = QNetworkAccessManager()
        try:
            url = QUrl(self._data['url'])
            query = self._data.get('query')
            headers = {
                'Authorization': 'Bearer tapi_2MpVKNJBcdp8LX70beGfYCffwWt.NDBmMzVlZDRiMWNhMzkxYzg2OGYzMDkxNTE4NTE0ZGM'
            }

            if not headers['Authorization']:
                self.status_message.emit('API key is not set in environment variable')
                return

            query_string = QUrlQuery()
            if query:
                for key, value in query.items():
                    query_string.addQueryItem(key, value)

            url.setQuery(query_string)
            request = QNetworkRequest(url)

            for header, value in headers.items():
                request.setRawHeader(header.encode(), value.encode())

            self.status_message.emit(f'Sending request to {url.toString()}')
            self.network_reply = self.network_manager.get(request)
            self.network_reply.finished.connect(self.handle_response)
        except Exception as ex:
            self.status_message.emit(f'An unexpected error occurred: {str(ex)}')

    def handle_response(self):
        try:
            if self.network_reply.error() == QNetworkReply.NetworkError.NoError:
                data_bytes = self.network_reply.readAll().data()
                data_str = data_bytes.decode('utf-8')
                data = json.loads(data_str)
                self.status_message.emit('Data received')
                self.results.emit(data)
                print(f"Data emitted {data}")
            else:
                error_message = self.network_reply.errorString()
                self.status_message.emit(f'Error during sending request: {error_message}')
        except Exception as ex:
            self.status_message.emit(f'An unexpected error occurred: {str(ex)}')

        self.network_reply.deleteLater()
        self.finished.emit()

    def append_status(self, message):
        self.status_message.emit(message)


