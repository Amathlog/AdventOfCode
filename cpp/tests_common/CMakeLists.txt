find_package(Catch2 3 REQUIRED)

include_directories(${AdventOfCode_SOURCE_DIR}/common/include)
include_directories(${AdventOfCode_SOURCE_DIR}/tests_common)

file(GLOB_RECURSE SOLUTIONS_SRC
    "${AdventOfCode_SOURCE_DIR}/tests_common/**/**/*.cpp"
    "${AdventOfCode_SOURCE_DIR}/tests_common/*.cpp"
)

add_executable(TestsCommon ${SOLUTIONS_SRC})
target_link_libraries(TestsCommon PRIVATE AOCCommon Catch2::Catch2WithMain)
set_target_properties(TestsCommon PROPERTIES FOLDER "cpp")

include(CTest)
include(Catch)
catch_discover_tests(TestsCommon)