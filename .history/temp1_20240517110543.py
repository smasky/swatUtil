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
file_name="000010001.gw"
database=pd.DataFrame()

with open(os.path.join(work_path, file_name), 'r') as f:
    lines=f.readlines()
    for line in lines:
        match=re.search(pattern, line)
        


