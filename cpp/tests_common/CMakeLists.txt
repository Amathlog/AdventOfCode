# Add GTest
set(BUILD_GMOCK OFF)
enable_testing()
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})

include_directories(${AdventOfCode_SOURCE_DIR}/common/include)
include_directories(${AdventOfCode_SOURCE_DIR}/tests_common)

file(GLOB_RECURSE TEST_COMMON_SRC
    "${AdventOfCode_SOURCE_DIR}/tests_common/**/*.cpp"
    "${AdventOfCode_SOURCE_DIR}/tests_common/*.cpp"
)

add_executable(TestsCommon ${TEST_COMMON_SRC})
target_link_libraries(TestsCommon AOCCommon gtest_main)
set_target_properties(TestsCommon PROPERTIES FOLDER "cpp")
if (DEBUG)
add_definitions(-D_GLIBCXX_DEBUG)
endif()

#include(GoogleTest)
#gtest_discover_tests(NesEmulatorUnitTests)