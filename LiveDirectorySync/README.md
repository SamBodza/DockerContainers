# LiveDirectorySync

---

###Docker container to sync a live directory into a working directory

---

## Usage
Can specify time to run to avoid conflicts with live system using the scheduler.ini file

In the example below, you should replace container with your container name and replace command with the command for your container to run
```
[job-exec "Sorting Images"]
schedule = 0 23 19 * * *
container = curator_worker_1
command = python pngcatchup.py
```
---
.db_config holds the variables for your databases username, password and database name
```
DB_USER=someuser
DB_PASSWORD=somepassword
DB_PORT=5432
```
.worker_config holds the source and destination variables for the rsync worker
```
WORKER_SRC=/mnt/src
WORKER_DST=/mnt/dst
```
---

In the config.yml file, you can specify how long you want your sync to run for and the file types for it to move using REGEX
```
Runtime:
  Hours: 3
  Minutes: 30
  Seconds: 0
  
Filetypes:
  - .+\.fda
  - .+\.fda-
  
```
---