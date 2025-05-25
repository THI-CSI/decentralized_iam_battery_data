cmake_minimum_required(VERSION 3.10)
project(data_gen_c)

set(CMAKE_C_STANDARD 11)

# Add the cJSON library
add_subdirectory(lib/cJSON)

# Include the cJSON header files
include_directories(lib/cJSON)

# Include your own headers (if you have any)
include_directories(src)

# Add the executable and include both main.c and process_json.c
add_executable(data_gen_c src/main.c src/process_json.c)

# Link the cJSON library to your executable
target_link_libraries(data_gen_c cJSON)
