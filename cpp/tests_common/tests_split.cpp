#include <catch2/catch_test_macros.hpp>

#include <string>

#include <gtest/gtest.h>
#include <split.h>

TEST_CASE("Split")
{
    SECTION("SplitInt")
    {
        std::string test = "10 54 543";
        auto list = AOCCommon::SplitInt<int>(test);
        REQUIRE(list[0] == 10);
        REQUIRE(list[1] == 54);
        REQUIRE(list[2] == 543);
    }
}