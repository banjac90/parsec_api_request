# parsec_api_request
This is PyQt5 application for sending request to Parsec API, using threads.
 
Requirements:
- PyQt5
- openssl = version 1.1.1w
- Pandas

This application leverages QtNetwork libraries to facilitate the creation of worker processes, with a prerequisite for OpenSSL 1.1.1 to ensure robust network functionality. Additionally, it employs QtCore.QAbstractTableModel to construct a structured data model tailored for QtTableView. This model excels in efficiently receiving and processing data, which is subsequently parsed using the Pandas library.
