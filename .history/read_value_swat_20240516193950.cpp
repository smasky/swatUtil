#include<iostream>
#include<fstream>
#include<string>
#include<regex>
#include<vector>

void read_value_swat(const std::string file_path, const std::vector<std::string> &varname, const std::vector<double> &value)
{
    std::ifstream file(file_path);
    if (!file.is_open()) {
        std::cerr << "Failed to open file." << std::endl;
        return -1;
    }
    std::string line;


}