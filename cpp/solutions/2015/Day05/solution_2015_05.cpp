
#include "split.h"
#include <common/test_case.h>

#include <iostream>
#include <parser.h>
#include <path_utils.h>
#include <unordered_map>

constexpr bool s_verbose = true;

namespace Year2015
{
namespace Day05
{
class Solution : public ::AOCSolution
{
public:
    virtual bool SolvePartOne(const AOCResult& result, bool verbose) override;
    virtual bool SolvePartTwo(const AOCResult& result, bool verbose) override;
};

bool IsVowel(char c) { return c == 'a' || c == 'e' || c == 'i' | c == 'o' || c == 'u'; }

bool IsInvalid(char c1, char c2)
{
    return (c1 == 'a' && c2 == 'b') || (c1 == 'c' && c2 == 'd') || (c1 == 'p' && c2 == 'q') || (c1 == 'x' && c2 == 'y');
}

bool Solution::SolvePartOne(const AOCResult& result, bool verbose)
{
    std::vector<std::string> entries = AOCCommon::Split(result.input, "\n");
    int count = 0;
    for (const std::string& entry : entries)
    {
        if (entries.size() < 3)
            continue;

        int vowel_count = 0;
        bool has_double = false;
        bool is_invalid = false;
        for (int i = 0; i < entry.size(); ++i)
        {
            if (vowel_count < 3 && IsVowel(entry[i]))
                vowel_count++;

            if (i > 0 && IsInvalid(entry[i - 1], entry[i]))
            {
                is_invalid = true;
                break;
            }

            if (i > 0 && !has_double && entry[i - 1] == entry[i])
                has_double = true;
        }

        if (!is_invalid && has_double && vowel_count >= 3)
            count++;
    }

    if (verbose)
    {
        std::cout << "Number of nice words: " << count << std::endl;
    }

    return std::to_string(count) == result.expected1;
}

bool Solution::SolvePartTwo(const AOCResult& result, bool verbose)
{
    std::vector<std::string> entries = AOCCommon::Split(result.input, "\n");
    int count = 0;
    for (const std::string& entry : entries)
    {
        if (entries.size() < 4)
            continue;

        bool has_repeat = false;
        bool has_double = false;
        std::unordered_map<char, int> doubles;

        for (int i = 1; i < entry.size(); ++i)
        {
            if (!has_double && entry[i - 1] == entry[i])
            {
                char curr = entry[i];
                if (doubles.contains(curr))
                {
                    has_double = i > doubles[curr] + 1;
                }
                else
                {
                    doubles.emplace(curr, i);
                }
            }

            if (!has_repeat && i > 2 && entry[i - 2] == entry[i])
            {
                has_repeat = true;
            }

            if (has_double && has_repeat)
            {
                count++;
                break;
            }
        }
    }

    if (verbose)
    {
        std::cout << "Number of nice words: " << count << std::endl;
    }

    return std::to_string(count) == result.expected1;
}

} // namespace Day05
} // namespace Year2015

TEST_CASE("2015_Day05", "[2015]")
{
    SECTION("Example")
    {
        std::string entry =
            AOCCommon::ParseFile(AOCCommon::GetRootPath() / "solutions" / "2015" / "Day05" / "example.txt");
        AOCResult result(std::move(entry), "2", "");

        Year2015::Day05::Solution solution;
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
            AOCCommon::ParseFile(AOCCommon::GetRootPath() / "solutions" / "2015" / "Day05" / "entry.txt");
        AOCResult result(std::move(entry), "255", "");

        Year2015::Day05::Solution solution;
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
