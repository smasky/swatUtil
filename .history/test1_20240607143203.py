from swat_utility import read_value_swat, copy_origin_to_tmp, write_value_to_file
import os
import re
import itertools
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import tempfile
import shutil

from UQPyL.DoE import LHS
from UQPyL.problems import Problem
from UQPyL.utility.metrics import r_square

from datetime import datetime, timedelta
import subprocess
import queue
import time
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import json

class SWAT_UQ():
    hru_suffix=["chm", "gw", "hru", "mgt", "sdr", "sep", "sol", "ops"]
    watershed_suffix=["pnd", "rte", "sub", "swq", "wgn", "wus"]
    n_output=1
    n_hru=0
    n_rch=0
    n_sub=0
    record_days=0
    observe_infos={}
    def __init__(self, work_path: str, paras_file_name: str, observed_file_name: str, 
                 swat_exe_name: str, special_paras_file: str=None,
                 max_workers: int=12, num_parallel: int=5):
        
        self.work_temp_dir=tempfile.mkdtemp()
        self.work_path=work_path
        self.paras_file_name=paras_file_name
        self.observed_file_name=observed_file_name
        self.swat_exe_name=swat_exe_name
        self.special_paras_file=special_paras_file
        
        self.max_workers=max_workers
        self.num_parallel=num_parallel
        
        self._initial()
        self._record_default_values()
        # self._get_observed_data()
        
        self.work_path_queue=queue.Queue()
        self.work_temp_dirs=[]
        
        for i in range(num_parallel):
            path=os.path.join(self.work_temp_dir, "instance{}".format(i))
            self.work_temp_dirs.append(path)
            self.work_path_queue.put(path)
        
        with ThreadPoolExecutor(max_workers=self.num_parallel) as executor:
            futures = [executor.submit(copy_origin_to_tmp, self.work_path, work_temp) for work_temp in self.work_temp_dirs]
        for future in futures:
            future.result()
            
        # self.exe_queue=queue.Queue()
        # for i in range(num_parallel):
        #     simulator_name=os.path.join(self.work_temp_dirs[i], "swat_{}.exe".format(i))
        #     shutil.copyfile("swat_no_output.exe", simulator_name)
        #     self.exe_queue.put(simulator_name)
    #------------------------------------------interface function-------------------------------------------------#
    def evaluate(self, X):
        """
        evaluate the objective within X
        """
        n=X.shape[0]
        Y=np.zeros((n,1))
        
        self._subprocess(X[0, :], 0)
        
        # with ThreadPoolExecutor(max_workers=self.num_parallel) as executor:
        #     futures=[executor.submit(self._subprocess, X[i, :], i) for i in range(n)]

        # begin_days=self.observe_infos["begin_calibration_days"]
        # end_days=self.observe_infos["end_calibration_days"]
        # weights=self.observe_infos["rch_weights"]
        # true_flows=self.observe_infos["rch_flows"]
        
        # for future in futures:
        #     res=future.result()
        #     i, rch_flows, success=res
        #     Obj=0
        #     if success:
        #         for id, flow in rch_flows.items():
        #             int_id=int(id)
        #             begin_day=begin_days[int_id]-self.output_skip_days
        #             end_day=end_days[int_id]-self.output_skip_days
        #             weight=weights[int_id]
        #             true_flow=true_flows[int_id]
        #             obj=r_square(true_flow, np.array(flow[begin_day:end_day+1]))
        #             Obj+=obj*weight
        #     else:
        #         Obj=-np.inf
        #     Y[i,0]=Obj
        return Y
    
    #------------------------------------private function-----------------------------------------------#
    def _subprocess(self, input_x, id):
        """
        subprocess for run swat with each input_X
        """
        work_path=self.work_path_queue.get()
        self._set_values(work_path, input_x)
        
        # background_data={}
        # background_data["work_path"]=work_path.replace("\\", "/")+"/"
        # background_data["n_days"]=self.record_days
        # background_data["n_hru"]=self.n_hru
        # background_data["n_sub"]=self.n_sub
        # background_data["n_rchs"]=self.n_sub
        # background_data["rch_ids"]=self.observe_infos["rch_ids"]
        
        # run_exe=self.exe_queue.get()
        
        # process = subprocess.Popen(
        # run_exe, 
        # cwd=work_path,
        # stdin=subprocess.PIPE, 
        # stdout=subprocess.PIPE, 
        # stderr=subprocess.PIPE, 
        # text=True
        # )
        # input_string=json.dumps(background_data, indent=4).replace("\n", " ")
        # try:
        #     output, _ = process.communicate(input=input_string)
        #     rch_flows=json.loads(output)
        # except:
        #     rch_flows={}
        #     rch_flows["flow_out"]=0
        #     success=0
        # self.exe_queue.put(run_exe)
        # success=1
        # self.work_path_queue.put(work_path)
        # return (id, rch_flows["flow_out"], success)
    
    def _set_values(self, work_path, paras_values):
        """
        set_value
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures=[]
            for file_name, infos in self.file_var_info.items():
                future = executor.submit(write_value_to_file, work_path, file_name, 
                                         infos["name"], infos["default"], 
                                         infos["index"], infos["mode"], 
                                         paras_values.ravel())
                futures.append(future)
            
            for future in futures:
                res=future.result()
              
    # def _get_observed_data(self):
    #     file_path=os.path.join(self.work_path, self.observed_file_name)
    #     rch_ids=[]
    #     rch_weights={}
    #     data=[]
    #     with open(file_path, "r") as f:
    #         lines=f.readlines()
    #         pattern_id=re.compile(r'FLOW_OUT_(\d+)\s+')
    #         pattern_value = re.compile(r'(\d+)\s+FLOW_OUT_(\d+)_(\d+)\s+(\d+\.?\d*)')
    #         for i, line in enumerate(lines):
    #             match1= pattern_id.match(line)
    #             if match1:
    #                 rch_id=int(match1.group(1))
    #                 rch_ids.append(rch_id)
                    
    #                 match2=re.findall(r'\d+\.?\d*', lines[i+1])
    #                 rch_weight=float(match2[0])
    #                 rch_weights[rch_id]=rch_weight
                    
    #             match = pattern_value.match(line)
    #             if match:
    #                 index, day, year = map(int, match.groups()[:-1])
    #                 value = float(match.groups()[-1])
    #                 data.append([rch_id, index, day, year,  value])
                
    #     observed_data = pd.DataFrame(data, columns=['rch_id', 'index', 'day', 'year', 'value'])
    #     begin_calibration={}
    #     end_calibration={}
    #     rch_id_observed_data={}
        
    #     for rch_id in rch_ids:
    #         flow=observed_data.query('rch_id==@rch_id')
    #         begin_day=int(flow.iloc[0]['day'])
    #         begin_year=int(flow.iloc[0]['year'])
    #         end_day=int(flow.iloc[-1]['day'])
    #         end_year=int(flow.iloc[-1]['year'])
            
    #         flow_value=flow['value'].to_numpy(dtype=float)
    #         begin_calibration[rch_id]=(datetime(int(begin_year), 1, 1) + timedelta(int(begin_day) - 1)-self.begin_date).days
    #         end_calibration[rch_id]=(datetime(int(end_year), 1, 1) + timedelta(int(end_day) - 1)-self.begin_date).days
    #         rch_id_observed_data[rch_id]=flow_value
        
    
    #     if sum(list(rch_weights.values()))!=1.0:
    #         raise ValueError("The sum of weights of observed data should be 1.0, please check observed.txt!")
        
    #     self.observe_infos["begin_calibration_days"]=begin_calibration
    #     self.observe_infos["end_calibration_days"]=end_calibration
    #     self.observe_infos["rch_ids"]=rch_ids
    #     self.observe_infos["rch_flows"]=rch_id_observed_data
    #     self.observe_infos["rch_weights"]=rch_weights
        
    def _record_default_values(self):

        var_infos_path=os.path.join(self.work_path, self.paras_file_name)
        low_bound=[]
        up_bound=[]
        var_name=[]
        mode=[]
        range=[]
        with open(var_infos_path, 'r') as f:
            lines=f.readlines()
            for line in lines:
                tmp_list=line.split()
                var_name.append(tmp_list[0])
                mode.append(tmp_list[1])
                low_bound.append(float(tmp_list[2]))
                up_bound.append(float(tmp_list[3]))
                range.append(tmp_list[4:])
                
        self.lb= np.array(low_bound)
        self.ub= np.array(up_bound)
        self.mode= mode
        self.paras_list=var_name
        self.x_labels=self.paras_list
        
        self.n_input=len(self.paras_list)
        self.file_var_info={}
        types=
        for i, element in enumerate(self.paras_list):
            element=element.split('@')[0]
            suffix=self.paras_file.query('para_name==@element')['file_name'].values[0]
            position=self.paras_file.query('para_name==@element')['position'].values[0]
            type_=self.paras_file.query('para_name==@element')['type'].values[0]
            if suffix in self.hru_suffix:
                if range[i][0]=="all":
                    files=[e+".{}".format(suffix) for e in self.hru_list]
                else:
                    files=[]
                    for ele in range[i]:
                        if "_" not in ele:
                            code=f"{'0' * (9 - 4 - len(ele))}{ele}{'0'*4}"
                            for e in self.watershed_hru[code]:
                                files.append(e+"."+suffix)
                        else:
                            bsn_id, hru_id=ele.split('_')
                            code=f"{'0' * (9 - 4 - len(bsn_id))}{bsn_id}{'0'*(4-len(hru_id))}{bsn_id}"
                            files.append(code+"."+suffix)
            elif suffix in self.watershed_suffix:
                if range[i][0]=="all":
                    files=[e+"."+suffix for e in self.watershed_list]
                else:
                    files=[e+"."+suffix for e in range[i]]
            elif suffix=="bsn":
                files=["basins.bsn"]
            
            for file in files:
                self.file_var_info.setdefault(file,{})
                self.file_var_info[file].setdefault("index", [])
                self.file_var_info[file]["index"].append(i)
                
                self.file_var_info[file].setdefault("mode", [])
                if self.mode[i]=="v":
                    self.file_var_info[file]["mode"].append(0)
                elif self.mode[i]=="r":
                    self.file_var_info[file]["mode"].append(1)
                elif self.mode[i]=="a":
                    self.file_var_info[file]["mode"].append(2)
                
                self.file_var_info[file].setdefault("name", [])
                self.file_var_info[file]["name"].append(element)
                self.file_var_info[file].setdefault("position",[])
                self.file_var_info[file]["position"].append(position)
                self.file_var_info[file].setdefault("type", [])
                self.file_var_info[file]["type"].append(type_)
                                
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交任务到线程池
            futures=[]
            for file_name, infos in self.file_var_info.items():
                futures.append(executor.submit(read_value_swat, self.work_path, file_name , infos["name"], infos["position"], 1))

        for future in futures:
            res=future.result()
            for key, items in res.items():
                values=' '.join(str(value) for value in items)
                _, file_name=key.split('|')
                self.file_var_info[file_name].setdefault("default", [])
                self.file_var_info[file_name]["default"].append(values)
                          
    def delete(self):
        shutil.rmtree(self.work_temp_dir)
            
    def _initial(self):
 
        #read control file fig.cio
        paras=["NBYR", "IYR", "IDAF", "IDAL", "NYSKIP"]
        pos=["default"]*5
        dict_values=read_value_swat(self.work_path, "file.cio", paras, pos, 0)
        self.begin_date=datetime(int(dict_values["IYR"][0]), 1, 1)+timedelta(int(dict_values['IDAF'][0])-1)
        self.end_date=datetime(int(dict_values["IYR"][0])+int(dict_values['NBYR'][0])-1, 1, 1)+timedelta(int(dict_values['IDAL'][0])-1)
        self.simulation_days=(self.end_date-self.begin_date).days+1
        output_skip_years=int(dict_values["NYSKIP"][0])
        self.output_skip_days=(datetime(int(dict_values["IYR"][0])+output_skip_years, 1, 1)+timedelta(int(dict_values['IDAF'][0])-1)-self.begin_date).days
        
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
        
        self.watershed_hru=watershed
        self.hru_list = list(itertools.chain.from_iterable(watershed.values()))
        self.watershed_list=list(watershed.keys())
        
        self.n_hru=len(self.hru_list)
        self.n_sub=len(self.watershed_list)
        self.n_rch=self.n_sub
        self.record_days=self.simulation_days-self.output_skip_days
        
        self.paras_file=pd.read_excel(os.path.join(self.work_path, 'SWAT_paras_files.xlsx'), index_col=0)
        if self.special_paras_file is not None:
            with open(os.path.join(self.work_path, self.special_paras_file), 'r') as f:
                lines=f.readlines()
                for line in lines:
                    tmp_list=line.split()
                    self.paras_file.loc[tmp_list[0]]=tmp_list[1:]
        
file_path="D:\SWAT\TxtInOut"
from UQPyL.DoE import LHS    
swat_cup=SWAT_UQ(work_path=file_path,
                    paras_file_name="paras_infos.txt",
                    observed_file_name="observed.txt",
                    swat_exe_name="swat_64rel.exe",
                    special_paras_file="special_paras.txt",
                    max_workers=1, num_parallel=1)
lhs=LHS('classic')
X=lhs.sample(5, swat_cup.n_input)
X=X*(swat_cup.ub-swat_cup.lb)+swat_cup.lb
Y=swat_cup.evaluate(X)