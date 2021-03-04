#include <stdlib.h>
#include <vector>
#include <iostream>
#include <string>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fstream>


std::vector<std::string> split(const std::string& str, const std::string& delim)
{
    std::vector<std::string> tokens;
    size_t prev = 0, pos = 0;
    do
    {
        pos = str.find(delim, prev);
        if (pos == std::string::npos) pos = str.length();
        std::string token = str.substr(prev, pos-prev);
        if (!token.empty()) tokens.push_back(token);
        prev = pos + delim.length();
    }
    while (pos < str.length() && prev < str.length());
    return tokens;
}

int main() {
    int count = 0;
    int num;
    int proc_num;
    std::vector<std::string> lines;
    std::vector<std::string> list_proc_str;
    std::vector<int> list_proc_int;
    std::ifstream file(FILENAME);
    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line)) {
            if (count == 0) {
                lines = split(line, " ");
                num = atoi(lines[0].c_str());
                proc_num = atoi(lines[1].c_str());
            } else {
                list_proc_str = split(line, " ");
            }
            count++;
        }
        file.close();
    }
    for (int i=0; i <= proc_num; i++) {
     int num = atoi(list_proc_str.at(i).c_str());
     list_proc_int.push_back(num);
    }
     for (int k=0; k <= proc_num; k++) {
        for (int m=0; m < num; m++) {
            std::string need = "sleep " + list_proc_str[k];
            int m = list_proc_int[k] / 2;
            std::cout << m << " " + m;
            if (fork() == 0) {
                execv(need.c_str(), NULL);
            }
        }
    }
}