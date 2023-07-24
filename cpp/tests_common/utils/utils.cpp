#include "utils/utils.h"
#include "path_utils.h"

std::filesystem::path Utils::GetDataFolder() { return AOCCommon::GetRootPath() / "tests_common" / "data"; }