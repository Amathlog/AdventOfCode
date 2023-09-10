#pragma once

#include <cmath>
#include <cstdint>
#include <functional>
#include <type_traits>

namespace AOCCommon
{
template <typename T>
concept Numerical = std::is_arithmetic_v<T>;

template <Numerical T = int32_t>
struct Point
{
    T x{};
    T y{};

    Point() = default;
    Point(T _x, T _y)
        : x(_x)
        , y(_y)
    {
    }

    Point(const Point&) = default;
    Point(Point&&) = default;
    Point& operator=(const Point&) = default;
    Point& operator=(Point&&) = default;

    // Initialize both x and y to value
    Point(T value)
        : x(value)
        , y(value)
    {
    }

    Point& operator+=(const Point& other)
    {
        x += other.x;
        y += other.y;
        return *this;
    }

    Point& operator-=(const Point& other)
    {
        x -= other.x;
        y -= other.y;
        return *this;
    }

    template <Numerical U>
    Point& operator*=(U other)
    {
        x *= other;
        y *= other;
        return *this;
    }

    template <Numerical U>
    Point& operator/=(U other)
    {
        assert(other != U{});
        x /= other;
        y /= other;
    }

    Point operator+(const Point& other) const { return Point(x + other.x, y + other.y); }
    Point operator-(const Point& other) const { return Point(x - other.x, y - other.y); }

    template <Numerical U>
    Point operator*(T other) const
    {
        return Point(x * other, y * other);
    }

    template <Numerical U>
    Point operator/(T other) const
    {
        assert(other != U{});
        return Point(x / other, y / other);
    }

    bool operator==(const Point& other) const { return x == other.x && y == other.y; }

    T Dot(const Point& other) const { return x * other.x + y * other.y; }

    T Cross(const Point& other) const { return x * other.y - y * other.x; }

    T SquaredLength() const { return Dot(*this); }

    double Length() const { return std::sqrt<double>(SquaredLength()); }
};

template <Numerical T>
struct PointHash
{
    std::size_t operator()(const Point<T>& p) const { return std::hash<T>{}(p.x) ^ (std::hash<T>{}(p.y) << 1); }
};

using Pointf = Point<float>;
using Pointd = Point<double>;
using Pointl = Point<int32_t>;
using Pointll = Point<int64_t>;

using PointHashf = PointHash<float>;
using PointHashd = PointHash<double>;
using PointHashl = PointHash<int32_t>;
using PointHashll = PointHash<int64_t>;

} // namespace AOCCommon