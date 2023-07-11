#include <utils/utils.h>

std::filesystem::path Utils::GetDataFolder() { return std::filesystem::current_path() / "data"; }
