#include <catch2/catch_test_macros.hpp>

#include <cstring>
#include <string>

#include <parser.h>
#include <utils/utils.h>

TEST_CASE("Parser")
{
    SECTION("ReadFile")
    {
        std::string res = AOCCommon::ParseFile(Utils::GetDataFolder() / "simple_file.txt");
        REQUIRE_FALSE(res.empty());
    }

    SECTION("ReadLinesWithTrim")
    {
        std::vector<std::string> res = AOCCommon::ParseLines(Utils::GetDataFolder() / "simple_file.txt");
        REQUIRE(res.size() == 3);

        REQUIRE(res[0] == "Hello World!");
        REQUIRE(res[1] == "AdventOfCode");
        REQUIRE(res[2] == "Blablabla");
    }

    SECTION("ReadLinesWithoutTrim")
    {
        std::vector<std::string> res = AOCCommon::ParseLines(Utils::GetDataFolder() / "simple_file.txt", false);
        REQUIRE(res.size() == 4);

        REQUIRE(res[0] == "Hello World!");
        REQUIRE(res[1] == "AdventOfCode");
        REQUIRE(res[2] == "Blablabla");
        REQUIRE(res[3].empty());
    }
}