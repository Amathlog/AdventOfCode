# Add GTest
set(BUILD_GMOCK OFF)
enable_testing()
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})

include_directories(${AdventOfCode_SOURCE_DIR}/common/include)
include_directories(${AdventOfCode_SOURCE_DIR}/solutions)

file(GLOB_RECURSE SOLUTIONS_SRC
    "${AdventOfCode_SOURCE_DIR}/solutions/**/**/*.cpp"
    "${AdventOfCode_SOURCE_DIR}/solutions/*.cpp"
)

add_executable(AOCSolutions ${SOLUTIONS_SRC})
target_link_libraries(AOCSolutions AOCCommon gtest_main)
set_target_properties(AOCSolutions PROPERTIES FOLDER "cpp")

#include(GoogleTest)
#gtest_discover_tests(NesEmulatorUnitTests)