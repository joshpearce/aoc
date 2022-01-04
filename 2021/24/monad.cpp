
#include <iostream>
#include <string>
#include <cmath>
#include <iomanip>
#include <string>

int constants[14][7] =   
 {{  0,  26,   1,  14,  25,   1,  12},
  {  0,  26,   1,  10,  25,   1,   9},
  {  0,  26,   1,  13,  25,   1,   8},
  {  0,  26,  26,  -8,  25,   1,   3},
  {  0,  26,   1,  11,  25,   1,   0},
  {  0,  26,   1,  11,  25,   1,  11},
  {  0,  26,   1,  14,  25,   1,  10},
  {  0,  26,  26, -11,  25,   1,  13},
  {  0,  26,   1,  14,  25,   1,   3},
  {  0,  26,  26,  -1,  25,   1,  10},
  {  0,  26,  26,  -8,  25,   1,  10},
  {  0,  26,  26,  -5,  25,   1,  14},
  {  0,  26,  26, -16,  25,   1,   6},
  {  0,  26,  26,  -6,  25,   1,   5}};

int alu_iteration(int w, int z, int constants[7]) {

    int x = z % 26;
    x = ((x + constants[3]) != w);
    int y = 25 * x + 1;
    z = std::floor(z / constants[2]);
    z = z * y;
    y = (w + constants[6]) * x;
    z = z + y;

    return z;
}

long run_alu(std::string model_str) {
    int z = 0;
    for (int i=0; i<14; i++) {
        z = alu_iteration(model_str[i] - '0', z, constants[i]);
    }
    return z;
}

int main(int argc, char* argv[]) {

    std::cout << std::fixed;
    std::cout << std::setprecision(4);

    long start = std::stol(argv[1]);
    long end = std::stol(argv[2]);

    long answer = 0;

    int inc = start > end ? -1 : 1;

    for (long i = start; i != end; i = i + inc) {
        std::string model_str = std::to_string(i);

        if (model_str.find('0') == std::string::npos) {
        
            long z = run_alu(model_str);

            if (z == 0) {
                answer = i;
                std::cout << answer << std::endl;
                return 0;
            }  
        }
        if (i % 10000000 == 0) {
            float pct = (float(start - i) / float(start - end)) * 100.0;
            std::cout << answer << ", " << i << ", pct " << pct << std::endl;
            
        }
    }
}