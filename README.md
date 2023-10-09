# parsec_api_request
This is PyQt5 application for sending request to Parsec API, using threads.
 
## Requirements:
- PyQt5
- openssl = version 1.1.1w
- Pandas
For installation of openssl follow this [link](https://thesecmaster.com/procedure-to-install-openssl-on-the-windows-platform/)

### About Application
This application uses QtNetwork libraries to facilitate the creation of worker processes, with a prerequisite for OpenSSL 1.1.1 to ensure robust network functionality. Additionally, it employs QtCore.QAbstractTableModel to construct a structured data model for QtTableView widget. This model excels in efficiently receiving and processing data, which is parsed later using the Pandas library.
Application is made only for presentation and main goal was to present how to avoid freezing of Qt application with Qthreads. 
For more information and how to get key of Parsec API follow [Parsec API documentation.](https://parsec.app/docs/teams-api)
Main file for running application is parsecapp.py


