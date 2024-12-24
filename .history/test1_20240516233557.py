from my_module import read_value_swat, set_value_swat
import os
file_path="D:\SiHuRiver\model\FuTIanSi001\Scenarios\Test\TxtInOut"
file_name="000020001.sol"

varname_list=["REVAPMN", "GWQMN"]
file_path=os.path.join(file_path, file_name)

values=[123.12, 122.1]
set_value_swat(file_path, varname_list, values)