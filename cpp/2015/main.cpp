#include <iostream>
#include <string>

#include "parser.h"

int main()
{
    std::string test = "10 54 543";
    auto list = AOCCommon::SplitInt<int>(test);
    for (auto& x : list)
    {
        std::cout << "* " << x << std::endl;
    }

    return 0;
}