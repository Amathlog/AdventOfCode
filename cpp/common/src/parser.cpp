#include <parser.h>

#include <cstring>
#include <fstream>
#include <sstream>

#include <split.h>

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

std::vector<std::string> AOCCommon::ParseLines(const std::filesystem::path& path, bool trim_empty)
{
    if (!std::filesystem::exists(path))
    {
        return {};
    }

    std::ifstream file;
    file.open(path.c_str());

    std::vector<std::string> res;

    if (file.is_open())
    {
        for (std::string line; std::getline(file, line);)
        {
            if (line.empty() && trim_empty)
            {
                continue;
            }

            res.push_back(std::move(line));
        }
    }

    file.close();

    return res;
}