# File Directory Monitor

This Python program will pass all input files in one directory to another directory.

Commonly used in data transmission files, such as FTP transport, or database ETL sync jobs.

# How to run
1. Clone repo
2. Ensure Python 3+ is installed
3. Change working directory into repository and execute as follows:

-MacOS
```bash
python3 main.py Source Destination
```
-Windows
```bash
python main.py Source Destination
```

# API Documentation
-The directory monitor uses a custom recursive algorithm like os.walk, except that the directory files are allocated in realtime.

-Each recursive scan will build a hierarchy of nested parents and children and move them to their appropriate destination while enforcing hierarchy structure. Additionally, it notes the moved files by marking their existence in an in-memory data-store.

# TODO
- Cleanup code for 1.0.0 release
- Refactor recursive structure for readability.
- Add logging/maintence features for searching activity history.
- Add automated tests
- Add network volatility sensitivity for file system manipulations
