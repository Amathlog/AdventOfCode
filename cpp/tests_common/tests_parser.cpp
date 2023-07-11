#include <string>

#include <cstring>
#include <gtest/gtest.h>
#include <parser.h>
#include <utils/utils.h>

TEST(Parser, ReadFile)
{
    std::string res = AOCCommon::ParseFile(Utils::GetDataFolder() / "simple_file.txt");
    ASSERT_FALSE(res.empty());
}

TEST(Parser, ReadLinesWithTrim)
{
    std::vector<std::string> res = AOCCommon::ParseLines(Utils::GetDataFolder() / "simple_file.txt");
    ASSERT_EQ(res.size(), 3);

    ASSERT_EQ(res[0], "Hello World!");
    ASSERT_EQ(res[1], "AdventOfCode");
    ASSERT_EQ(res[2], "Blablabla");
}

TEST(Parser, ReadLinesWithoutTrim)
{
    std::vector<std::string> res = AOCCommon::ParseLines(Utils::GetDataFolder() / "simple_file.txt", false);
    ASSERT_EQ(res.size(), 4);

    ASSERT_EQ(res[0], "Hello World!");
    ASSERT_EQ(res[1], "AdventOfCode");
    ASSERT_EQ(res[2], "Blablabla");
    ASSERT_TRUE(res[3].empty());
}