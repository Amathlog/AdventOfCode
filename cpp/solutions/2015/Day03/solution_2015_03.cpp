
#include <algorithm>
#include <common/test_case.h>
#include <cstdint>
#include <gtest/gtest.h>

#include <iterator>
#include <maths/point.h>

#include <array>
#include <iostream>
#include <parser.h>
#include <path_utils.h>
#include <split.h>
#include <unordered_map>
#include <unordered_set>

using AOCCommon::PointHashl;
using AOCCommon::Pointl;

constexpr bool s_verbose = true;

namespace Year2015
{
namespace Day03
{
class Solution : public ::AOCSolution
{
public:
    virtual bool SolvePartOne(const AOCResult& result, bool verbose) override;
    virtual bool SolvePartTwo(const AOCResult& result, bool verbose) override;
};

int32_t Transform(char c)
{
    switch (c)
    {
    case '^':
        return 0;
    case 'v':
        return 1;
    case '>':
        return 2;
    case '<':
        return 3;
    default:
        assert(false);
        return -1;
    }
}

bool Solution::SolvePartOne(const AOCResult& result, bool verbose)
{
    // ^ ; v ; > ; <.
    std::array<Pointl, 4> incrs{Pointl(0, 1), Pointl(0, -1), Pointl(1, 0), Pointl(-1, 0)};
    std::vector<int32_t> instructions;
    std::transform(result.input.begin(), result.input.end(), std::back_inserter(instructions), &Transform);

    Pointl current;
    std::unordered_set<Pointl, PointHashl> visited{current};

    for (int32_t i : instructions)
    {
        current += incrs[i];
        visited.emplace(current);
    }

    if (verbose)
    {
        std::cout << "Houses visited:" << visited.size() << std::endl;
    }

    return std::to_string(visited.size()) == result.expected1;

    return false;
}

bool Solution::SolvePartTwo(const AOCResult& result, bool verbose)
{
    // ^ ; v ; > ; <.
    std::array<Pointl, 4> incrs{Pointl(0, 1), Pointl(0, -1), Pointl(1, 0), Pointl(-1, 0)};
    std::vector<int32_t> instructions;
    std::transform(result.input.begin(), result.input.end(), std::back_inserter(instructions), &Transform);

    Pointl currentSanta;
    Pointl currentRoboSanta;
    Pointl* current = &currentRoboSanta;
    std::unordered_set<Pointl, PointHashl> visited{*current};

    for (int32_t i : instructions)
    {
        *current += incrs[i];
        visited.emplace(*current);
        current = (current == &currentSanta) ? &currentRoboSanta : &currentSanta;
    }

    if (verbose)
    {
        std::cout << "Houses visited:" << visited.size() << std::endl;
    }

    return std::to_string(visited.size()) == result.expected2;

    return false;
}

} // namespace Day03
} // namespace Year2015

TEST(Year2015, Day03_Example)
{
    std::string entry = AOCCommon::ParseFile(AOCCommon::GetRootPath() / "solutions" / "2015" / "Day03" / "example.txt");
    AOCResult result(std::move(entry), "4", "3");

    Year2015::Day03::Solution solution;
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

TEST(Year2015, Day03_Entry)
{
    std::string entry = AOCCommon::ParseFile(AOCCommon::GetRootPath() / "solutions" / "2015" / "Day03" / "entry.txt");
    AOCResult result(std::move(entry), "2592", "2360");

    Year2015::Day03::Solution solution;
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
