
#include "split.h"
#include <common/test_case.h>
#include <gtest/gtest.h>

#include <comparison.h>
#include <parser.h>
#include <path_utils.h>
#include <split.h>

constexpr bool s_verbose = false;

namespace Year2015
{
namespace Day02
{

struct Dimensions
{
    int length = 0;
    int width = 0;
    int height = 0;
};

class Solution : public ::AOCSolution
{
public:
    virtual bool SolvePartOne(const AOCResult& result, bool verbose) override;
    virtual bool SolvePartTwo(const AOCResult& result, bool verbose) override;

private:
    void Init(const std::string& input);
    std::vector<Dimensions> m_input;
};

void Solution::Init(const std::string& input)
{
    auto transform = [this](std::string x)
    {
        std::vector<int> values = AOCCommon::SplitInt<int>(x, "x");
        return Dimensions{values[0], values[1], values[2]};
    };

    m_input = AOCCommon::SplitAndTransform<Dimensions>(input, transform, "\n", true);
}

bool Solution::SolvePartOne(const AOCResult& result, bool verbose)
{
    Init(result.input);

    int finalValue = 0;
    for (const Dimensions& dimension : m_input)
    {
        int temp = 2 * dimension.height * dimension.length + 2 * dimension.height * dimension.width +
                   2 * dimension.length * dimension.width;
        // Also add the smallest side
        int argMax = AOCCommon::ArgMax(dimension.height, dimension.length, dimension.width);
        switch (argMax)
        {
        case 0:
            temp += dimension.length * dimension.width;
            break;
        case 1:
            temp += dimension.height * dimension.width;
            break;
        default:
            temp += dimension.height * dimension.length;
            break;
        }

        finalValue += temp;
    }

    if (verbose)
    {
        std::cout << finalValue << std::endl;
    }

    return result.expected1 == std::to_string(finalValue);
}

bool Solution::SolvePartTwo(const AOCResult& result, bool verbose)
{
    int finalValue = 0;
    for (const Dimensions& dimension : m_input)
    {
        int temp = dimension.height * dimension.length * dimension.width;
        // Also add the smallest side
        int argMax = AOCCommon::ArgMax(dimension.height, dimension.length, dimension.width);
        switch (argMax)
        {
        case 0:
            temp += 2 * (dimension.length + dimension.width);
            break;
        case 1:
            temp += 2 * (dimension.height + dimension.width);
            break;
        default:
            temp += 2 * (dimension.height + dimension.length);
            break;
        }

        finalValue += temp;
    }

    if (verbose)
    {
        std::cout << finalValue << std::endl;
    }

    return result.expected2 == std::to_string(finalValue);
}

} // namespace Day02
} // namespace Year2015

TEST(Year2015, Day02_Example)
{
    std::string entry = AOCCommon::ParseFile(AOCCommon::GetRootPath() / "solutions" / "2015" / "Day02" / "example.txt");
    AOCResult result(std::move(entry), "101", "48");

    Year2015::Day02::Solution solution;
    if (s_verbose)
    {
        std::cout << "Part 1:" << std::endl;
    }

    ASSERT_TRUE(solution.SolvePartOne(result, s_verbose));

    if (s_verbose)
    {
        std::cout << "Part 2:" << std::endl;
    }

    ASSERT_TRUE(solution.SolvePartTwo(result, s_verbose));
}

TEST(Year2015, Day02_Entry)
{
    std::string entry = AOCCommon::ParseFile(AOCCommon::GetRootPath() / "solutions" / "2015" / "Day02" / "entry.txt");
    AOCResult result(std::move(entry), "1586300", "3737498");

    Year2015::Day02::Solution solution;
    if (s_verbose)
    {
        std::cout << "Part 1:" << std::endl;
    }

    ASSERT_TRUE(solution.SolvePartOne(result, s_verbose));

    if (s_verbose)
    {
        std::cout << "Part 2:" << std::endl;
    }

    ASSERT_TRUE(solution.SolvePartTwo(result, s_verbose));
}
