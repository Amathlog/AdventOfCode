#include <filesystem>
#include <gtest/gtest.h>

#include <path_utils.h>

TEST(PathUtils, FindRootFile)
{
    std::filesystem::path rootPath = AOCCommon::GetRootPath();
    ASSERT_TRUE(std::filesystem::exists(rootPath / ".root_file"));
}