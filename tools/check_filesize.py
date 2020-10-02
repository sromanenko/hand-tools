#!/usr/bin/env python

import datetime as dt
import json
import os
import re

now = dt.datetime.now()
ago = now-dt.timedelta(minutes=1450)
ago_resume_features = now-dt.timedelta(minutes=10150) #resume_features
resume_features_pattern = re.compile("^resume_features_slot_\d+\.bkf\.bz2$")
path = "/backup/postgres-backup/"
filelist = os.walk(path)
metrics = []

for root, dirs, files in filelist:
    for file in files:
        if file.endswith(".bz2"):
             fpath = os.path.join(root, file)
             st = os.stat(fpath)
             mtime = dt.datetime.fromtimestamp(st.st_mtime)
             if mtime > (ago_resume_features if resume_features_pattern.match(file) else ago):
                 filesize = os.path.getsize(fpath)
                 metrics.append({"name": "backup.file.size", "labels": {"backup_file": file}, "value": filesize})
print (json.dumps(metrics))

