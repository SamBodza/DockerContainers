# LiveDirectorySync

---

Docker container to sync a live directory into a working directory

---

### Usage
Can specify time to run to avoid conflicts with live system using scheduler.ini

```
[job-exec "Sorting Images"]
schedule = 0 23 19 * * *
container = curator_worker_1
command = python pngcatchup.py
```
---

how long to run for and the file types to sync using config.ini
```
[Runtime]
Hours=
Mins=
Secs=


```
---

Builds postgres DB to track files & folders
Can be used for infographics

---

