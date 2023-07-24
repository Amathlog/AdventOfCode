from pathlib import Path
import os


template = R"""
#include <common/test_case.h>
#include <gtest/gtest.h>

#include <parser.h>
#include <path_utils.h>

namespace Year{0}
{
namespace Day{1}
{
class Solution : public ::AOCSolution
{
public:
    virtual bool SolvePartOne(const AOCResult& result, bool verbose) override;
    virtual bool SolvePartTwo(const AOCResult& result, bool verbose) override;
};

bool Solution::SolvePartOne(const AOCResult& result, bool verbose)
{
    return false;
}

bool Solution::SolvePartTwo(const AOCResult& result, bool verbose)
{
    return false;
}

}
}

TEST(Year{0}, Day{1}_Example)
{
    std::string entry = AOCCommon::ParseFile(AOCCommon::GetRootPath() / "solutions" / "{0}" / "Day{1}" / "example.txt");
    AOCResult result(std::move(entry), "", "");

    Year{0}::Day{1}::Solution solution;
    //ASSERT_TRUE(solution.SolvePartOne(result, false));
    //ASSERT_TRUE(solution.SolvePartTwo(result, false));
}

TEST(Year{0}, Day{1}_Entry)
{
    std::string entry = AOCCommon::ParseFile(AOCCommon::GetRootPath() / "solutions" / "{0}" / "Day{1}" / "entry.txt");
    AOCResult result(std::move(entry), "", "");

    Year{0}::Day{1}::Solution solution;
    //ASSERT_TRUE(solution.SolvePartOne(result, false));
    //ASSERT_TRUE(solution.SolvePartTwo(result, false));
}
"""

def generate_files(year: int, day: int):
    root = Path(os.path.abspath(__file__)).parent.parent

    year_str = str(year)
    day_str = "0" + str(day) if day < 10 else str(day)

    folder = root / "solutions" / year_str / ("Day" + day_str)
    folder.mkdir(parents = True, exist_ok=True)

    entry_file = folder / "entry.txt"
    entry_file.touch(exist_ok=True)
    example_file = folder / "example.txt"
    example_file.touch(exist_ok=True)

    solution_file = folder / "solution.cpp"
    content = template.replace("{0}", year_str).replace("{1}", day_str)
    with solution_file.open("w") as f:
        f.write(content)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        exit(-1)

    generate_files(int(sys.argv[1]), int(sys.argv[2]))
    
