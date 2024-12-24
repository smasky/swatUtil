from my_module import read_value_swat
import os
file_path="D:\SiHuRiver\model\FuTIanSi001\Scenarios\Test\TxtInOut"
file_name="000020001.gw"

varname_list=["GW_DELAY", "GWQMN", "REVAPMN"]
file_path=os.join(file_path, file_name)
read_value_swat()