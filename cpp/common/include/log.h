#pragma once

#include <iostream>

namespace AOCCommon
{
static inline bool s_verbose = false;

static void SetVerbose(bool verbose) { s_verbose = verbose; }

template <typename... Args>
static void LogVerbose(Args&&... args)
{
    if (s_verbose)
    {
        Log(std::forward<Args>(args)...);
    }
}

template <typename... Args>
static void Log(Args&&... args)
{
    ((std::cout << args), ...);
    std::cout << std::endl;
}
} // namespace AOCCommon