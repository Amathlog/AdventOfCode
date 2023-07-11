#include <string>

#include <gtest/gtest.h>
#include <split.h>

TEST(Split, SplitInt)
{
    std::string test = "10 54 543";
    auto list = AOCCommon::SplitInt<int>(test);
    ASSERT_EQ(list[0], 10);
    ASSERT_EQ(list[1], 54);
    ASSERT_EQ(list[2], 543);
}