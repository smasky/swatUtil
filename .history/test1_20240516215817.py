from my_module import read_value_swat
import os
file_path="D:\SiHuRiver\model\FuTIanSi001\Scenarios\Test\TxtInOut"
file_name="000020001.sol"

varname_list=["Ave", "Ksat", "Albedo"]
file_path=os.path.join(file_path, file_name)
res=read_value_swat(file_path, varname_list)
print(res)