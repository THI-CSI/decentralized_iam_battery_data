#include "cJSON.h"
#include "process_json.h"

int main() {
	// Seed for random number generator
	srand(time(NULL));

	char* json_data = process_json_data();
	if (json_data != NULL) {
		printf("Generated JSON Data:\n%s\n", json_data);
		free(json_data);
	} else {
		fprintf(stderr, "Failed to generate JSON data\n");
	}

	return 0;
}
