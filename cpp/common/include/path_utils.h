#pragma once

#include <filesystem>

#ifdef WIN32
#include <windows.h>
#endif // WIN32

namespace AOCCommon
{
static inline std::filesystem::path GetRootPath()
{
    static std::filesystem::path cachedValue;
    static constexpr const char* rootFile = ".root_file";

    if (!cachedValue.empty())
    {
        return cachedValue;
    }

    std::filesystem::path current;
#ifdef WIN32
    // TODO
#else
    current = std::filesystem::canonical("/proc/self/exe");
#endif // WIN32
    current = current.parent_path();

    while (current.has_parent_path())
    {
        if (std::filesystem::exists(current / rootFile))
        {
            cachedValue = current;
            break;
        }

        current = current.parent_path();
    }

    return cachedValue;
}
} // namespace AOCCommon