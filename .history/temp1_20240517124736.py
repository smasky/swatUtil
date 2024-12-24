import os
import re
import os
import itertools
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import tempfile
import shutil
from UQPyL.DoE import LHS
from UQPyL.problems import Problem
from UQPyL.utility.metrics import r2_score
from datetime import datetime, timedelta
import subprocess
import multiprocessing
import time
from typing import List, Dict, Any

hru_suffix=["chm", "gw", "hru", "mgt", "sdr", "sep", "sol"]
watershed_suffix=["pnd", "rte", "sub", "swq", "wgn", "wus"]

pattern = r'\s*(\d+\.?\d+)\s*\|\s*([^:]+)\s*:'

work_path="D:\SiHuRiver\model\FuTIanSi001\Scenarios\Test\TxtInOut"
prefix_name="000010001"

database = pd.DataFrame(columns=['para_name', 'type', 'file_name'])
database.set_index('para_name', inplace=True)
for suffix in hru_suffix:
    file_name = prefix_name + "." + suffix
    with open(os.path.join(work_path, file_name), 'r') as f:
        lines=f.readlines()
        for line in lines:
            match=re.search(pattern, line)
            if match:
                para_name=match.group(2)
                value=match.group(1)
                if re.match(".*\..*", value):
                    database.loc[para_name] = ['float', suffix]
                else:
                    database.loc[para_name] = ['int', suffix]

for suffix in ["sol"]:
    file_name = prefix_name + "." + suffix
    pattern1=r'\s+([A-Z]*)\s*\:\s+(\d+\.+\d+)\s+'
    with open(os.path.join(work_path, file_name), 'r') as f:
        lines=f.readlines()
        for line in lines:
            match=re.search(pattern1, line)
            if match:
                para_name=match.group(1)
                value=match.group(2)
                print(para_name, value)
                if re.match(".*\..*", value):
                    database.loc[para_name] = ['float', suffix]
                else:
                    database.loc[para_name] = ['int', suffix]
                    
prefix_name="000010000"                 
for suffix in watershed_suffix:
    file_name = prefix_name + "." + suffix
    with open(os.path.join(work_path, file_name), 'r') as f:
        lines=f.readlines()
        for line in lines:
            match=re.search(pattern, line)
            if match:
                para_name=match.group(2)
                value=match.group(1)
                if re.match(".*\..*", value):
                    database.loc[para_name] = ['float', suffix]
                else:
                    database.loc[para_name] = ['int', suffix]
                    
print(database)
        


