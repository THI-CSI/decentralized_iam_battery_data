#ifndef PROCESS_JSON_H
#define PROCESS_JSON_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

#include "cJSON.h"

#include "process_json.h"

void free_json_string(const char* json_string);
char random_char(int value);
char* random_string(int length);
int random_integer(int min, int max);
float random_float(float min, float max);
char* generate_timestamp();
char* process_json_data();

#endif // PROCESS_JSON_H
