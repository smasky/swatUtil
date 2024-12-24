from my_module import read_value_swat
import os
file_path="D:\SiHuRiver\model\FuTIanSi001\Scenarios\Test\TxtInOut"
file_name="0000200001.gw"

varname_list=["GW_DELAY", "GWQMN", "REVAPMN"]
file_path=os.path.join(file_path, file_name)
res=read_value_swat(file_path, varname_list)
print(res)