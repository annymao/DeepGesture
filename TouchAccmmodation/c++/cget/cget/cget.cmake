set(CGET_PREFIX "/nfs/master/06/r06922088/code/c++/cget")
set(CMAKE_PREFIX_PATH "/nfs/master/06/r06922088/code/c++/cget")
include_directories(SYSTEM ${CMAKE_PREFIX_PATH}/include)
if (CMAKE_CROSSCOMPILING)
    list(APPEND CMAKE_FIND_ROOT_PATH "/nfs/master/06/r06922088/code/c++/cget")
endif()
if (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX "/nfs/master/06/r06922088/code/c++/cget")
endif()
if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
    set(CMAKE_CXX_ENABLE_PARALLEL_BUILD_FLAG "/MP")
endif()
if (BUILD_SHARED_LIBS)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS "ON" CACHE BOOL "")
endif()
set(CMAKE_FIND_FRAMEWORK "LAST" CACHE STRING "")
set(CMAKE_INSTALL_RPATH "${CGET_PREFIX}/lib" CACHE STRING "")
