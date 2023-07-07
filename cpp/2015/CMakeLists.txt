# Add GTest
set(BUILD_GMOCK OFF)
add_subdirectory(${AdventOfCode_SOURCE_DIR}/external/googletest build)
enable_testing()
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})

include_directories(${AdventOfCode_SOURCE_DIR}/common/include)
include_directories(${AdventOfCode_SOURCE_DIR}/2015)

file(GLOB_RECURSE YEAR_2015_SRC
    "${AdventOfCode_SOURCE_DIR}/2015/*.cpp"
)

add_executable(AOCYear2015 ${YEAR_2015_SRC})
target_link_libraries(AOCYear2015 AOCCommon gtest_main)
set_target_properties(AOCYear2015 PROPERTIES FOLDER "cpp")

#include(GoogleTest)
#gtest_discover_tests(NesEmulatorUnitTests)