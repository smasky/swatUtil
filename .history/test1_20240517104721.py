from my_module import _read_value_swat, _set_value_swat
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

def read_value_swat(file_path: str, varname_list: List[str]) -> Dict[str, List[float]]:
    """
    Read values from a SWAT file based on variable names.

    Parameters:
        file_path (str): The path to the SWAT file.
        varname_list (List[str]): A list of variable names to search for.

    Returns:
        Dict[str, List[float]]: A dictionary mapping variable names to lists of values.
    """
    return _read_value_swat(file_path, varname_list)

def set_value_swat(file_path: str, varname_list: List[str], results: Dict[str, List[float]]) -> None:
    """
    Set values in a SWAT file based on variable names.

    Parameters:
        file_path (str): The path to the SWAT file.
        varname_list (List[str]): A list of variable names to search for.
        results (Dict[str, List[float]]): A dictionary mapping variable names to lists of new values.
    """
    _set_value_swat(file_path, varname_list, results)
    
def _get_default_paras(file_path, name):
    pattern=r"(\s*)(\-?\d+\.?\d*)(\s*.*{}.*)".format(name)
    with open(file_path, "r+") as f:
        lines=f.readlines()
        for line in lines:
            match = re.search(pattern, line)
            if match:
                return float(match.group(2))

def _get_default_paras_for_sol(file_path, name):
    pattern=r".*{}.*".format(name)
    with open(file_path, "r+") as f:
        lines=f.readlines()
        for line in lines:
            match = re.search(pattern, line)
            if match:
                numbers=re.findall(r"\d+\.\d+", line)
                return " ".join(numbers)

def _set_paras_for_sol(file_path, name, value, mode, origin_value=None):
    pattern=r"\s*{}.*".format(name)
    with open(file_path, "r+") as f:
        lines=f.readlines()
        for i, line in enumerate(lines):
            match = re.search(pattern, line)
            if match:
                numbers=re.findall(r"\d+\.\d+", line)
                for j, number in enumerate(numbers):
                    if mode=='r':
                        value=float(origin_value[j])*(1+value)
                    elif mode=='a':
                        value=float(origin_value[j])+value
                    line=line.replace(str(number), "{:.2f}".format(value))
                lines[i]=line
                break
        f.seek(0)
        f.writelines(lines)
        f.truncate()
                
def _set_paras(file_path, name, value, mode, origin_value=None):
    
    pattern=r"(\s*)(\-?\d+\.?\d*)(\s*.*{}.*)".format(name)
    with open(file_path, "r+") as f:
        lines=f.readlines()
        for i, line in enumerate(lines):
            match = re.search(pattern, line)
            
            if match:
                if mode=='r':
                    value=origin_value*(1+value)
                elif mode=='a':
                    value=origin_value+value
                    
                new_text = re.sub(pattern,  match.group(1)+"{}".format(value)+match.group(3), line)
                lines[i]=new_text
                break
        f.seek(0)
        f.writelines(lines)
        f.truncate()
###############################


def sub_process(x, swat_cups_indices, lock, swat_cups, log_queue):
    result=-1
    try:
        with lock:
            if not swat_cups_indices:
                log_queue.put("No more swat_cup")
                return None
            
            index=swat_cups_indices.pop()
        
        swat_cup=swat_cups[index]
        result=swat_cup.evaluate(x.reshape(1,-1))
    finally:
        with lock:
            swat_cups_indices.append(index)
            log_queue.put("swat_cup {} finished".format(index))
        
        return result
    
def main(swat_cups, X):
    
    
    with multiprocessing.Manager() as manager:
        lock=manager.Lock()
        swat_cups_indices=manager.list(range(len(swat_cups)))
        log_queue=manager.Queue()
    
        try:
            with multiprocessing.Pool(processes=12) as pool:
                results=pool.starmap(sub_process, [(row, swat_cups_indices, lock, swat_cups, log_queue) for row in X])
        
        finally:
            pass
        
        while not log_queue.empty():
            print(log_queue.get())
        
    return results

class SWAT_CUP(Problem):
    HRU_suffix=["chm", "gw", "hru", "mgt", "sdr", "sep", "sol"]
    Watershed_suffiex=["pnd", "rte", "sub", "swq", "wgn", "wus"]
    n_output=1
    def __init__(self, work_path, para_file_name, observe_file_name, swat_exe_path, rch_id):
        self.work_path=work_path
        self.para_file_name=para_file_name
        self.observe_file_name=observe_file_name
        self.exe_path=os.path.join(self.work_path, swat_exe_path)
        self.rch_id=rch_id
        
        self._initial()
        self._recond_default_values() #assign self.lb self.ub self.n_input
        self._get_observed_data()
    
    def evaluate(self, X):
        n=X.shape[0]
        Y=np.zeros((n,1))
        for i in range(n):
            self._set_values(X[i])
            try:
                subprocess.run(self.exe_path, cwd=self.work_path,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                simulation_data=self._get_simulation_data()
                rch_flows=simulation_data.query('RCH=={}'.format(self.rch_id))['FLOW_OUTcms'].to_numpy()
                Y[i,0]=-r2_score(self.observed_data, rch_flows[self.begin_calibration-1:self.end_calibration])
            except:
                Y[i,0]=-np.inf
        return Y
    
    def _get_simulation_data(self):
        file_name="output.rch"
        file_path=os.path.join(self.work_path, file_name)
        begin_ind=0
        with open(file_path, "r") as f:
            lines=f.readlines()
            for i, line in enumerate(lines):
                match = re.search(r".*FLOW_OUTcms.*", line)
                if match:
                    begin_ind=i
                    break
        colspecs = [
            (7, 11),  # RCH
            (22, 26), # MON
            (52, 62), # FLOW_OUTcms
        ]
        
        simulation_data = pd.read_fwf(file_path, colspecs=colspecs, header=None, names=['RCH', 'MON', 'FLOW_OUTcms'], skiprows=begin_ind+1)
        
        return simulation_data
    
    def _get_observed_data(self):
        file_path=os.path.join(self.work_path, self.observe_file_name)
        data=[]
        with open(file_path, "r") as f:
            lines=f.readlines()
            pattern = re.compile(r'(\d+)\s+FLOW_OUT_(\d+)_(\d+)\s+(\d+\.?\d*)')
            for line in lines:
                match = pattern.match(line)
                if match:
                    index, day, year = map(int, match.groups()[:-1])
                    value = float(match.groups()[-1])
                    data.append([index, day, year,  value])
        observed_data = pd.DataFrame(data, columns=['index', 'day', 'year', 'value'])
        observed_data = observed_data.astype({'index': int, 'day': int, 'year': int, 'value': float}).set_index('index')
        values_array = observed_data['value'].to_numpy(dtype=float)
        
        first_record = observed_data.iloc[0]
        self.begin_calibration=(datetime(int(first_record['year']), 1, 1) + timedelta(int(first_record['day']) - 1)-self.begin_date).days
        
        last_record = observed_data.iloc[-1]
        self.end_calibration=(datetime(int(last_record['year']), 1, 1) + timedelta(int(last_record['day']) - 1)-self.begin_date).days
        
        self.observed_data=values_array
        
    def _set_values(self, paras_values):
        
        paras_values=paras_values.ravel()
        for i in range(self.n_input):
            para_name=self.paras_list[i]
            mode=self.paras_infos.loc[para_name, 'mode']
            value=paras_values[i]
            file_suffix=self.paras_files.loc[para_name, 'file']
            
            if file_suffix in self.HRU_suffix:
                for sub in self.total_sub_list:
                    file_name=sub+"."+file_suffix
                    file_path=os.path.join(self.work_path, file_name)
                    if file_suffix=='sol':
                        _set_paras_for_sol(file_path, para_name, value, mode, str.split(self.default_values.loc[(self.default_values['para_name'] == para_name) & (self.default_values['file_name'] == file_name), 'value'].values[0]))
                    else:
                        _set_paras(file_path, para_name, value, mode, self.default_values.loc[(self.default_values['para_name'] == para_name) & (self.default_values['file_name'] == file_name), 'value'].values[0])
            elif file_suffix in self.Watershed_suffiex:
                for sub in self.watershed_list:
                    file_name=sub+"."+file_suffix
                    file_path=os.path.join(self.work_path, sub+"."+file_suffix)
                    _set_paras(file_path, para_name, value, mode, self.default_values.loc[(self.default_values['para_name'] == para_name) & (self.default_values['file_name'] == file_name), 'value'].values[0])
            elif file_suffix=="bsn":
                file_name="basins."+file_suffix
                file_path=os.path.join(self.work_path, file_name)
                _set_paras(file_path, para_name, value, mode, self.default_values.loc[(self.default_values['para_name'] == para_name) & (self.default_values['file_name'] == file_name), 'value'].values[0])
            
    def _recond_default_values(self):
        
        para_file_name=os.path.join(self.work_path, self.para_file_name)
        paras_infos=pd.read_csv(para_file_name, sep=' ', names=['Parameter', 'mode', 'low_bound', 'up_bound'],  index_col='Parameter')
        self.lb= paras_infos['low_bound'].values
        self.ub= paras_infos['up_bound'].values
        paras_list=paras_infos.index.tolist()
        self.x_labels=paras_list
        num_paras=paras_infos.shape[0]
        self.n_input=num_paras
        ##generate default_values
        default_values_path=os.path.join(self.work_path, 'default_values.xlsx')
        if not os.path.exists(default_values_path):
            default_values=pd.DataFrame(columns=['para_name', 'file_name', 'value'])

            for i in range(num_paras):
                para_name=paras_list[i]
                file_suffix=self.paras_files.loc[para_name, 'file']
                
                if file_suffix in self.HRU_suffix:
                    for sub in self.total_sub_list:
                        file_name=sub+"."+file_suffix
                        file_path=os.path.join(self.work_path, file_name)
                        if file_suffix=='sol':
                            default_values.loc[len(default_values)]=[para_name, file_name, _get_default_paras_for_sol(file_path, para_name)]
                        else:
                            default_values.loc[len(default_values)]=[para_name, file_name, _get_default_paras(file_path, para_name)]
                elif file_suffix in self.Watershed_suffiex:
                    for sub in self.watershed_list:
                        file_name=sub+"."+file_suffix
                        file_path=os.path.join(self.work_path, file_name)
                        default_values.loc[len(default_values)]=[para_name, file_name, _get_default_paras(file_path, para_name)]
                elif file_suffix=="bsn":
                    file_path=os.path.join(self.work_path, "basins."+file_suffix)
                    default_values.loc[len(default_values)]=[para_name, "basins."+file_suffix, _get_default_paras(file_path, para_name)]

            
            default_values.to_excel(default_values_path, index=True)
        else:
            default_values=pd.read_excel(default_values_path, index_col=0)
        self.default_values=default_values
        self.paras_infos=paras_infos
        self.paras_list=paras_list
    def _initial(self):
        Watershed={}
        
        NYSKIP=0
        #read control file fig.cio
        with open(os.path.join(self.work_path, "file.cio"), "r") as f:
            lines=f.readlines()
            for line in lines:
                match1 = re.search(r"(\s*)(\d+)(\s*.*NBYR.*)", line)
                if match1:
                    num_years=int(match1.group(2))
                
                match2 = re.search(r"(\s*)(\d+)(\s*.*IYR.*)", line)
                if match2:
                    begin_year=int(match2.group(2))
                
                match3 = re.search(r"(\s*)(\d+)(\s*.*IDAF.*)", line)
                if match3:
                    begin_day=int(match3.group(2))
                
                match4 = re.search(r"(\s*)(\d+)(\s*.*IDAL.*)", line)
                if match4:
                    end_day=int(match4.group(2))
                    
                match5 = re.search(r"(\s*)(\d+)(\s*.*NYSKIP.*)", line)
                if match5:
                    NYSKIP=int(match5.group(2))
                    
        self.begin_date=datetime(begin_year+NYSKIP, 1, 1) + timedelta(begin_day - 1)
        self.end_date=datetime(begin_year+num_years-1, 1, 1) + timedelta(end_day - 1)
        self.simulation_days=(self.end_date-self.begin_date).days+1
            
        #read control file fig.fig
        with open(os.path.join(self.work_path, "fig.fig"), "r") as f:
            lines=f.readlines()
            for line in lines:
                match = re.search(r'(\d+)\.sub', line)
                if match:
                    Watershed[match.group(1)]=[]
                    
        #read sub files   
        for sub in Watershed:
            file_name=sub+".sub"
            with open(os.path.join(self.work_path, file_name), "r") as f:
                lines=f.readlines()
                for line in lines:
                    match = re.search(r'(\d+)\.mgt', line)
                    if match:
                        Watershed[sub].append(match.group(1))
        
        self.Watershed=Watershed
        self.total_sub_list = list(itertools.chain.from_iterable(Watershed.values()))
        self.watershed_list=list(Watershed.keys())
        #read para_file
        file_path=os.path.join(self.work_path, 'SWAT_paras_files.txt')
        self.paras_files = pd.read_csv(file_path, sep=' ', names=['parameter', 'file'],  index_col='parameter')

file_path="D:\SiHuRiver\model\FuTIanSi001\Scenarios\Test\TxtInOut"
file_name="000020001.sol"      
swat_cup=SWAT_CUP(work_path=file_path,
                    para_file_name="paras_infos.txt",
                    observe_file_name="observed.txt",
                    swat_exe_path="swat_64rel.exe",
                    rch_id=40)
sub_list=swat_cup.total_sub_list

from concurrent.futures import ThreadPoolExecutor
import threading
var_name_list=["GW_DELAY", "GWQMN", "REVAPMN"]
values={"GW_DELAY":[1.0], "GWQMN":[2.0], "REVAPMN":[3.0]}
def task(n, file_path, var_name_list, values):
    set_value_swat(file_path, var_name_list, values)
    return f"Task result for {n}"


def main():
    # 创建一个线程池，可以自动根据需要创建新线程
    
    with ThreadPoolExecutor(max_workers=18) as executor:
        # 提交任务到线程池
        futures = [executor.submit(task, i, os.path.join(file_path,sub_list[i]+".gw"), var_name_list, values ) for i in range(len(sub_list))]
        
        # 获取每个任务的结果
        # for future in futures:
        #     print(future.result())
    # for i in range(len(sub_list)):
    #     set_value_swat(os.path.join(file_path,sub_list[i]+".gw"), var_name_list, values)
class SWAT_UQ():
    def __init__(self, work_path, paras_file_name, observe_file_name, swat_exe_name):
        self.work_path=work_path
        self.paras_file_name=paras_file_name
        self.observed_file_name=observe_file_name
        self.swat_exe_name=swat_exe_name
        
        self._initial()
        self._recond_default_values()
    
    def _recond_default_values(self):
        """
        
        """
        paras_infos=pd.read_csv(os.path.join(self.work_path, self.paras_file_name), sep=' ', names=['Parameter', 'mode', 'low_bound', 'up_bound'],  index_col='Parameter')
        self.lb= paras_infos['low_bound'].values
        self.ub= paras_infos['up_bound'].values
        self.paras_list=paras_infos.index.tolist()
        self.x_labels=self.paras_list
        
        self.n_input=len(self.paras_list)
        
        ##generate default value database for all parameters
        default_database_path=os.path.join(self.work_path, 'default_values.xlsx')
        if not os.path.exists(default_database_path):
            default_values=pd.DataFrame(columns=['para_name', 'file_name', 'value'])
        
        
    def _initial(self):
        """
        
        """
        
        #read control file fig.cio
        paras=["NBYR", "IYR", "IDAF", "IDAL", "NYSKIP"]
        dict_values=read_value_swat(os.path.join(self.work_path, "file.cio"), paras)
        self.begin_date=datetime(int(dict_values["IYR"]), 1, 1)+timedelta(int(dict_values['IDAF'])-1)
        self.end_date=datetime(int(dict_values["IYR"])+int(dict_values['NBYR'])-1, 1, 1)+timedelta(int(dict_values['IDAL'])-1)
        self.simulation_days=(self.end_date-self.begin_date).days+1
        self.output_skip_years=int(dict_values["NYSKIP"])
        
        #read control file fig.fig
        watershed={}
        with open(os.path.join(self.work_path, "fig.fig"), "r") as f:
            lines=f.readlines()
            for line in lines:
                match = re.search(r'(\d+)\.sub', line)
                if match:
                    watershed[match.group(1)]=[]
        
        #read sub files
        for sub in watershed:
            file_name=sub+".sub"
            with open(os.path.join(self.work_path, file_name), "r") as f:
                lines=f.readlines()
                for line in lines:
                    match = re.search(r'(\d+)\.mgt', line)
                    if match:
                        watershed[sub].append(match.group(1))
        
        self.Watershed=watershed
        self.hru_list = list(itertools.chain.from_iterable(watershed.values()))
        self.watershed_list=list(watershed.keys())
        
        self.paras_files = pd.read_csv(os.path.join(self.work_path, 'SWAT_paras_files.txt'), sep=' ', names=['parameter', 'file'],  index_col='parameter')
    
    
        
        
        
        
a=time.time()
main()
b=time.time()
print(b-a)