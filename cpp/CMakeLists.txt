cmake_minimum_required(VERSION 3.12)

project(AdventOfCode)

# Enable c++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

if (${CMAKE_BUILD_TYPE} STREQUAL "Debug" OR ${CMAKE_BUILD_TYPE} STREQUAL RelWithDebInfo)
  add_compile_definitions("_GLIBCXX_DEBUG")
endif()

set(EXTERNAL_FOLDER "external")
set(COMMON_FOLDER "common")

if(MSVC)
  add_definitions(/MP)
endif()

# set(CMAKE_CXX_FLAGS "-Wall")
if(WIN32)
set(CMAKE_CXX_FLAGS_DEBUG "/ZI /Od")
set(CMAKE_CXX_FLAGS_RELEASE "/O2")
else(WIN32)
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
endif(WIN32)

option(BUILD_TESTS "Build the tests" ON)

add_subdirectory(${AdventOfCode_SOURCE_DIR}/external/googletest build)

add_subdirectory("common")
add_subdirectory("solutions")
add_subdirectory("tests_common")
