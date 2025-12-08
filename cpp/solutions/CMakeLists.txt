find_package(Catch2 3 REQUIRED)

include_directories(${AdventOfCode_SOURCE_DIR}/common/include)
include_directories(${AdventOfCode_SOURCE_DIR}/solutions)

file(GLOB_RECURSE SOLUTIONS_SRC
    "${AdventOfCode_SOURCE_DIR}/solutions/**/**/*.cpp"
    "${AdventOfCode_SOURCE_DIR}/solutions/**/*.cpp"
    "${AdventOfCode_SOURCE_DIR}/solutions/*.cpp"
)

add_executable(AOCSolutions ${SOLUTIONS_SRC})
target_link_libraries(AOCSolutions PRIVATE AOCCommon Catch2::Catch2WithMain)
set_target_properties(AOCSolutions PROPERTIES FOLDER "cpp")

include(CTest)
include(Catch)
catch_discover_tests(AOCSolutions)