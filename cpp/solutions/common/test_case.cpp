#include <common/test_case.h>

#include <parser.h>

AOCResult::AOCResult(std::string _input, std::string _expected1, std::string _expected2)
    : input(std::move(_input))
    , expected1(std::move(_expected1))
    , expected2(std::move(_expected2))
{
}

AOCResult AOCResult::FromPath(const std::filesystem::path& _filepath, std::string _expected1, std::string _expected2)
{
    AOCResult res("", std::move(_expected1), std::move(_expected2));

    res.input = AOCCommon::ParseFile(_filepath);

    return res;
}
