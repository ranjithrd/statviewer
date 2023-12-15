## NOTE

This branch does not use MySQL; instead it uses SQLite3 and uses inbuilt data. Please use the main branch for mysql or the sqlite branch for sqlite code.

Use this branch only if you want this specific setup of the database. (IPL data as of 12/14/2023).

## INSTALLING AND RUNNING

1. Install SQLite3. [Windows Tutorial](https://www.guru99.com/download-install-sqlite.html)

2. Download/clone this repository (click `Code` > `Download ZIP` and then UNZIP the download).
**Make sure you are on the "easy" branch (the zip will be called `statviewer-easy.zip`).**

3. Install packages with `pip install pyside6 pyqtgraph` or `pip3 install pyside6 pyqtgraph`. Run these commands anywhere from the `cmd` app on Windows or `Terminal` on MacOS.

4. Run `data.py` from the code you downloaded.

5. Choose option `E` and the database will automatically be set up with IPL data as of 12/14/2023.

6. **To use the application, run `gui.py` which is in the folder that you have unzipped.**


## Prerequisites

- Tested with **Python 3.1**

- PIP Packages **(`pyside6`, `mysql-connector-python`, `sqlite3`, `pyqtgraph`)**. `sqlite3` comes in-built with Python in the latest versions.

- **SQLite** [Installing on Windows](https://www.guru99.com/download-install-sqlite.html)