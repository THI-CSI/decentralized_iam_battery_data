cmake_minimum_required(VERSION 3.10)
project(data_gen_c_v2)

set(CMAKE_C_STANDARD 11)

# Add the cJSON library
add_subdirectory(lib/cJSON)

# Include the cJSON header files
include_directories(lib/cJSON)

# Include your own headers (if you have any)
include_directories(src)

# Add the shared library target
add_library(data_gen_c_v2 SHARED src/process_json.c)

# Link the cJSON library to your shared library
target_link_libraries(data_gen_c_v2 cJSON)

# Executable for testing
add_executable(data_gen_v2 src/main.c)

# Link the shared library to the test executable
target_link_libraries(data_gen_v2 PRIVATE data_gen_c_v2)
