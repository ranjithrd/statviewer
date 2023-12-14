## NOTE

This branch does not use MySQL; instead it uses SQLite3 and uses inbuilt data. Please use the main branch for mysql or the sqlite branch for sqlite code.

Use this branch only if you want this specific setup of the database. (IPL data as of 12/14/2023).

## INSTALLING AND RUNNING

1. Download/clone this repository (click `Code` > `Download ZIP` and then expand the ZIP).
**Make sure you are on the "easy" branch.**

2. Install packages with `pip install pyside6 mysql-connector-python sqlite3` or `pip3 install pyside6 mysql-connector-python sqlite3`. Run these commands anywhere from the `cmd` app on Windows or `Terminal` on MacOS.

3. Run `data.py` from the code you downloaded.

4. Choose option `E` and the database will automatically be set up with IPL data as of 12/14/2023.

5. **To use the application, run gui.py.**


## Prerequisites

- Tested with **Python 3.1**

- PIP Packages **(`pyside6`, `mysql-connector-python`, `sqlite3`)**
