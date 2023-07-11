#pragma once

#include <filesystem>
#include <string>
#include <vector>

namespace AOCCommon
{
std::string ParseFile(const std::filesystem::path& path);
std::vector<std::string> ParseLines(const std::filesystem::path& path, bool trim_empty = true);
} // namespace AOCCommon