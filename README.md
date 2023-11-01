## Prerequisites

- Python 3.1

- MySQL (installation [instructions link](https://dev.mysql.com/doc/refman/8.0/en/windows-installation.html)). **Make sure to set password to mysql123**.

- PySide 6 (install by `pip install pyside6`)

- MySQL Python Connector (install by `pip install mysql-connector-python`)


## INSTALLING AND RUNNING

1. Download/clone this repository (click `Code` > `Download ZIP` and then expand the ZIP).

2. Download data from [this link](https://cricsheet.org/downloads/ipl_json.zip) and save it into a folder and copy its path.

3. Run `data.py` from the code you downloaded.

4. Follow the instructions on-screen (including setting your MySQL database credentials and creating a MySQL database).

5. Choose option A and enter the path to the folder that you downloaded with the cricket data.

6. **To use the application, run gui.py.**

## BUNDLING (not working)

Mac:

```
pyinstaller --add-data fonts:fonts -w gui.py -n Criceval
pyinstaller -c data.py -n Criceval_Data
```

## TEST CRICKET DATA

https://cricsheet.org/downloads/ipl_json.zip

Download into this folder as latest_sample_data.
Run init.py.