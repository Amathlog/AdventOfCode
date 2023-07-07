add_compile_definitions(_SILENCE_CXX17_STRSTREAM_DEPRECATION_WARNING)

include_directories(${AdventOfCode_SOURCE_DIR}/common/include)

file(GLOB_RECURSE COMMON_LIB_SRC
    ${AdventOfCode_SOURCE_DIR}/common/include/*.h
    ${AdventOfCode_SOURCE_DIR}/common/src/*.cpp
)

add_library(AOCCommon STATIC ${COMMON_LIB_SRC})