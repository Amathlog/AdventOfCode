
#include "hash/md5.h"
#include <charconv>
#include <common/test_case.h>
#include <cstdint>

#include <format>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <parser.h>
#include <path_utils.h>
#include <string>

constexpr bool s_verbose = false;

namespace Year2015
{
namespace Day04
{
class Solution : public ::AOCSolution
{
public:
    virtual bool SolvePartOne(const AOCResult& result, bool verbose) override;
    virtual bool SolvePartTwo(const AOCResult& result, bool verbose) override;
};

bool Solve(const AOCResult& result, bool verbose, bool part2)
{
    int i = 0;
    std::string temp = result.input;
    char buffer[128] = {};
    unsigned init_len = temp.size();
    while (true)
    {
        std::to_chars(buffer, buffer + 128, i);
        int ptr = 0;
        while (buffer[ptr] != '\0')
        {
            int index = init_len + ptr;
            if (index >= temp.size())
            {
                temp.resize(index + 1);
            }

            temp[index] = buffer[ptr++];
        }

        const auto hash = AOCCommon::md5String(temp);

        if (hash[0] == 0 && hash[1] == 0)
        {
            if ((part2 && hash[2] == 0) || (!part2 && (hash[2] >> 4) == 0))
            {
                break;
            }
        }

        i++;
    }

    std::string final_result = std::to_string(i);

    if (verbose)
    {
        std::cout << final_result << std::endl;
    }

    return final_result == (part2 ? result.expected2 : result.expected1);
}

bool Solution::SolvePartOne(const AOCResult& result, bool verbose) { return Solve(result, verbose, false); }
bool Solution::SolvePartTwo(const AOCResult& result, bool verbose) { return Solve(result, verbose, true); }

} // namespace Day04
} // namespace Year2015

TEST_CASE("2015_Day04", "[2015]")
{
    SECTION("Example")
    {
        std::string entry =
            AOCCommon::ParseFile(AOCCommon::GetRootPath() / "solutions" / "2015" / "Day04" / "example.txt");
        AOCResult result(std::move(entry), "609043", "6742839");

        Year2015::Day04::Solution solution;
        if (s_verbose)
        {
            std::cout << "Part 1:" << std::endl;
        }

        REQUIRE(solution.SolvePartOne(result, s_verbose));

        if (s_verbose)
        {
            std::cout << "Part 2:" << std::endl;
        }

        REQUIRE(solution.SolvePartTwo(result, s_verbose));
    }

    SECTION("Entry")
    {
        std::string entry =
            AOCCommon::ParseFile(AOCCommon::GetRootPath() / "solutions" / "2015" / "Day04" / "entry.txt");
        AOCResult result(std::move(entry), "254575", "1038736");

        Year2015::Day04::Solution solution;
        if (s_verbose)
        {
            std::cout << "Part 1:" << std::endl;
        }

        REQUIRE(solution.SolvePartOne(result, s_verbose));

        if (s_verbose)
        {
            std::cout << "Part 2:" << std::endl;
        }

        REQUIRE(solution.SolvePartTwo(result, s_verbose));
    }
}