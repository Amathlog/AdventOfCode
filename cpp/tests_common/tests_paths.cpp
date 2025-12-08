#include <catch2/catch_test_macros.hpp>

#include <filesystem>
#include <gtest/gtest.h>

#include <path_utils.h>

TEST_CASE("PathUtils")
{
    SECTION("FindRootFile")
    {
        std::filesystem::path rootPath = AOCCommon::GetRootPath();
        REQUIRE(std::filesystem::exists(rootPath / ".root_file"));
    }
}