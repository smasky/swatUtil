#include<iostream>
#include<fstream>
#include<string>
#include<regex>
#include<vector>

void read_value_swat(const std::string file_path, const std::vector<std::string> &varname_list, const std::vector<double> &value_list)
{
    std::ifstream file(file_path);
    if (!file.is_open()) {
        std::cerr << "The file is not existed" << std::endl;
        // return -1;
    }
    std::string line;
    
    while (std::getline(file, line)){
        
    }

}