#pragma once

#include <charconv>
#include <cstdint>
#include <cstring>
#include <string>
#include <type_traits>
#include <vector>

namespace AOCCommon
{
std::vector<std::string> Split(const std::string& inStr, const char* delim = " ", bool discardEmpty = false);

template <typename T>
requires std::is_integral_v<T>
std::vector<T> SplitInt(const std::string& inStr, const char* delim = " ", uint8_t base = 10,
                        bool discardEmpty = false);

template <typename T, typename Func>
std::vector<T> SplitAndTransform(const std::string& inStr, Func transform, const char* delim = " ",
                                 bool discardEmpty = false);
} // namespace AOCCommon

template <typename T, typename Func>
std::vector<T> AOCCommon::SplitAndTransform(const std::string& inStr, Func transform, const char* delim,
                                            bool discardEmpty)
{
    std::vector<T> res;
    size_t index = 0;
    const size_t delimSize = strlen(delim);
    while (index <= inStr.size())
    {
        size_t temp = inStr.find(delim, index);
        if (temp == std::string::npos)
        {
            if (index < inStr.size() || !discardEmpty)
            {
                res.emplace_back(transform(inStr.substr(index)));
            }
            break;
        }

        size_t substrLen = temp - index;
        if (substrLen > 0 || !discardEmpty)
        {
            res.emplace_back(transform(inStr.substr(index, substrLen)));
        }

        index = temp + delimSize;
    }

    return res;
}

template <typename T>
requires std::is_integral_v<T>
std::vector<T> AOCCommon::SplitInt(const std::string& inStr, const char* delim, uint8_t base, bool discardEmpty)
{
    auto transform = [base](std::string&& x)
    {
        T res;
        std::from_chars(x.c_str(), x.c_str() + x.size(), res, base);
        return res;
    };

    return SplitAndTransform<T>(inStr, transform, delim, discardEmpty);
}