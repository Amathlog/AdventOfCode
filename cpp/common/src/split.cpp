#include <split.h>

std::vector<std::string> AOCCommon::Split(const std::string& inStr, const char* delim, bool discardEmpty)
{
    return SplitAndTransform<std::string>(
        inStr, [](std::string x) { return x; }, delim, discardEmpty);
}
