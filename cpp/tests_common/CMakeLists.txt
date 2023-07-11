# Add GTest
set(BUILD_GMOCK OFF)
enable_testing()
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})

include_directories(${AdventOfCode_SOURCE_DIR}/common/include common)
include_directories(${AdventOfCode_SOURCE_DIR}/tests_common)

file(GLOB_RECURSE TEST_COMMON_SRC
    "${AdventOfCode_SOURCE_DIR}/tests_common/**/*.cpp"
    "${AdventOfCode_SOURCE_DIR}/tests_common/*.cpp"
)

add_executable(TestsCommon ${TEST_COMMON_SRC})
target_link_libraries(TestsCommon AOCCommon gtest_main)
set_target_properties(TestsCommon PROPERTIES FOLDER "cpp")

add_custom_command(TARGET TestsCommon POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory "$<TARGET_FILE_DIR:TestsCommon>/data/"
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        "${AdventOfCode_SOURCE_DIR}/tests_common/data"
        "$<TARGET_FILE_DIR:TestsCommon>/data"
        )

#include(GoogleTest)
#gtest_discover_tests(NesEmulatorUnitTests)