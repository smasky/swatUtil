#include<iostream>
#include<fstream>
#include<string>
#include<regex>
#include<vector>
#include<format>

void read_value_swat(const std::string file_path, const std::vector<std::string> &varname_list)
{
    std::ifstream file(file_path);
    if (!file.is_open()) {
        std::cerr << "The file is not existed" << std::endl;
        // return -1;
    }
    std::vector<double> values;

    std::string line;
    std::vector<std::string> lines;

    std::vector<std::regex> patterns;

    for(size_t i=0; i<varname_list.size(); ++i){
        std::string p=std::format(R"(\s*(\d+\.\d+)\s*\|\s*{})", varname_list[i]);
        std::regex pattern(p);
        patterns.push_back(pattern);
    }

    std::vector<int> sign(varname_list.size(), 1);

    while (std::getline(file, line)){
        for (size_t i=0; i<patterns.size(); ++i){
            std::smatch match;
            if (sign[i]&&std::regex_search(line, match, patterns[i])){
                values.push_back(std::stod(match[1].str()));
                sign[i] = 0;
            }
        }

    }

}