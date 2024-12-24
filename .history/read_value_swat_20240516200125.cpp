#include<iostream>
#include<fstream>
#include<string>
#include<regex>
#include<vector>
#include<format>

void read_value_swat(const std::string file_path, const std::vector<std::string> &varname_list, const std::vector<double> &value_list)
{
    std::ifstream file(file_path);
    if (!file.is_open()) {
        std::cerr << "The file is not existed" << std::endl;
        // return -1;
    }

    std::string line;
    std::vector<std::string> lines;

    std::vector<std::regex> patterns;

    for(size_t i=0; i<varname_list.size(); ++i){
        std::string p=std::format(R"(\s*(\d+\.\d+)\s*\|\s*{})", varname_list[i]);
        std::regex pattern();
    }

    while (std::getline(file, line)){
        for (size_t i=0; i<varname_list.size(); ++i){

        }

    }

}