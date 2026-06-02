cmake_minimum_required(VERSION 3.10)
project(OptionsPulse)

set(CMAKE_CXX_STANDARD 17)

add_executable(pricer
    engine/src/pricer.cpp
    app/main.cpp
)
set(pybind11_DIR "C:/Users/darsh/AppData/Roaming/Python/Python314/site-packages/pybind11/share/cmake/pybind11")
set(PYTHON_EXECUTABLE "C:/Python314/python.exe")
find_package(pybind11 REQUIRED)

pybind11_add_module(optionspulse MODULE
    backend/bindings.cpp    
    engine/src/pricer.cpp
    
)

target_include_directories(optionspulse PRIVATE engine/include)
target_include_directories(pricer PRIVATE engine/include)