#include "parser.h"
#include <cstring>
#include <fstream>
#include <sstream>

std::string AOCCommon::ParseFile(const std::filesystem::path& path)
{
    if (!std::filesystem::exists(path))
    {
        return std::string();
    }

    std::ifstream file;
    file.open(path.c_str());

    std::stringstream buffer;

    if (file.is_open())
    {
        buffer << file.rdbuf();
    }

    file.close();

    return buffer.str();
}

std::vector<std::string> AOCCommon::Split(const std::string& inStr, const char* delim, bool discardEmpty)
{
    return SplitAndTransform<std::string>(
        inStr, [](std::string x) { return x; }, delim, discardEmpty);
}
