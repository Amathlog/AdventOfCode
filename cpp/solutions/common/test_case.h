#pragma once

#include <gtest/gtest.h>

#include <filesystem>
#include <iostream>
#include <string>

struct AOCResult
{
    AOCResult(std::string _input, std::string _expected1 = "", std::string _expected2 = "");
    static AOCResult FromPath(const std::filesystem::path& _filePath, std::string _expected1 = "",
                              std::string _expected2 = "");

    std::string input;
    std::string expected1;
    std::string expected2;
};

class AOCSolution
{
public:
    AOCSolution() = default;
    virtual ~AOCSolution() = default;

    virtual bool SolvePartOne(const AOCResult& result, bool verbose) { return false; }
    virtual bool SolvePartTwo(const AOCResult& result, bool verbose) { return false; }
};