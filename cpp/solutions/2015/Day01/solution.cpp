#include <common/test_case.h>
#include <gtest/gtest.h>

#include "parser.h"
#include "path_utils.h"

namespace Year2015
{
namespace Day01
{
class Solution : public ::AOCSolution
{
public:
    virtual bool SolvePartOne(const AOCResult& result, bool verbose) override;
    virtual bool SolvePartTwo(const AOCResult& result, bool verbose) override;
};

bool Solution::SolvePartOne(const AOCResult& result, bool verbose)
{
    int count = 0;
    for (char c : result.input)
    {
        if (c == '(')
        {
            count++;
        }
        else if (c == ')')
        {
            count--;
        }
    }

    if (verbose)
    {
        std::cout << "Part 01: " << count << std::endl;
    }

    return result.expected1 == std::to_string(count);
}

bool Solution::SolvePartTwo(const AOCResult& result, bool verbose)
{
    int count = 0;
    int index = 0;
    for (char c : result.input)
    {
        if (c == '(')
        {
            count++;
        }
        else if (c == ')')
        {
            count--;
        }

        if (count < 0)
        {
            break;
        }

        index++;
    }

    std::string ourRes = (count >= 0 ? std::string("never") : std::to_string(index + 1));

    if (verbose)
    {
        std::cout << "Part 02: " << ourRes << std::endl;
    }

    return result.expected2 == ourRes;
}

} // namespace Day01
} // namespace Year2015

TEST(Year2015, Day01_Example)
{
    std::vector<AOCResult> allExamples = {
        {"(())", "0", "never"},    {"()()", "0", "never"}, {"(((", "3", "never"},
        {"(()(()(", "3", "never"}, {"))(((((", "3", "1"},  {"())", "-1", "3"},
        {"))(", "-1", "1"},        {")))", "-3", "1"},     {")())())", "-3", "1"},
    };

    for (const AOCResult& result : allExamples)
    {
        Year2015::Day01::Solution solution;
        ASSERT_TRUE(solution.SolvePartOne(result, false));
        ASSERT_TRUE(solution.SolvePartTwo(result, false));
    }
}

TEST(Year2015, Day01_Entry)
{
    std::string entry = AOCCommon::ParseFile(AOCCommon::GetRootPath() / "solutions" / "2015" / "Day01" / "entry.txt");
    AOCResult result(std::move(entry), "232", "1783");
    Year2015::Day01::Solution solution;
    ASSERT_TRUE(solution.SolvePartOne(result, false));
    ASSERT_TRUE(solution.SolvePartTwo(result, false));
}