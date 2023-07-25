#pragma once

#include <ranges>
namespace AOCCommon
{

template <typename T, typename Func, typename... Args>
T Compare(const T& value, int* outIndex, Func compareOp, Args&&... args)
{
    T result = value;
    int count = 0;
    if (outIndex)
    {
        *outIndex = 0;
    }
    (
        [&result, &compareOp, &args, &count, outIndex]
        {
            count++;
            if (compareOp(result, args))
            {
                result = args;
                *outIndex = count;
            }
        }(),
        ...);

    return result;
}

template <typename T, typename... Args>
T Max(const T& value, Args&&... args)
{
    return Compare(
        value, nullptr, [](T& v1, const T& v2) { return v2 > v1; }, std::forward<Args>(args)...);
}

template <typename T, typename... Args>
T Min(const T& value, Args&&... args)
{
    return Compare(
        value, nullptr, [](const T& v1, const T& v2) { return v2 < v1; }, std::forward<Args>(args)...);
}

template <typename T, typename... Args>
int ArgMax(const T& value, Args&&... args)
{
    int result = 0;
    Compare(
        value, &result, [](T& v1, const T& v2) { return v2 > v1; }, std::forward<Args>(args)...);
    return result;
}

template <typename T, typename... Args>
int ArgMin(const T& value, Args&&... args)
{
    int result = 0;
    Compare(
        value, &result, [](const T& v1, const T& v2) { return v2 < v1; }, std::forward<Args>(args)...);
    return result;
}

} // namespace AOCCommon