#include "process_json.h"

char random_char(int index) {
    char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    return charset[index];
}

char* random_string(int length) {
    // Allocate memory for the random string
    char* str = (char*)malloc((length + 1) * sizeof(char));
    if (str == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    for (int i = 0; i < length; i++) {
        int value = rand() % 52;
        str[i] = random_char(value);
    }
    str[length] = '\0';

    return str;
}

int random_integer(int min, int max) {
    return (rand() % (max - min + 1)) + min;
}

float random_float(float min, float max) {
    float scale = rand() / (float) RAND_MAX;

    return min + scale * (max - min);
}

char* generate_timestamp() {
    // Allocate memory for timestamp string
    char* timestamp = malloc(32);
    if (timestamp == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    // Get current time
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    struct tm *tm_info = localtime(&ts.tv_sec);

    // Format timestamp
    strftime(timestamp, 20, "%Y-%m-%dT%H:%M:%S", tm_info);
    snprintf(timestamp + 19, 30 - 19, ".%03ld%+03d:00", ts.tv_nsec / 1000000, 1);

    timestamp[29] = '\0';

    return timestamp;
}

char* process_json_data() {
    char* string = random_string(47);
    char* timestamp = generate_timestamp(); // timestamp

    // Create JSON object
    cJSON *json = cJSON_CreateObject();

    // Create sub-object
    cJSON *batteryTechnicalProperties = cJSON_CreateObject();

    // Add sub-object to JSON object
    cJSON_AddItemToObject(json, "batteryTechnicalProperties", batteryTechnicalProperties);

    // Create array
    cJSON *originalPowerCapability = cJSON_CreateArray();

    // Add object of arrays to sub-object
    cJSON_AddItemToObject(batteryTechnicalProperties, "originalPowerCapability", originalPowerCapability);

    // Create object for array
    cJSON *originalPowerCapabilityObject = cJSON_CreateObject();
    cJSON_AddNumberToObject(originalPowerCapabilityObject, "atSoc", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(originalPowerCapabilityObject, "powerCapabilityAt", random_float(-10000.0f, 10000.0f));
    cJSON_AddItemToArray(originalPowerCapability, originalPowerCapabilityObject);

    cJSON_AddNumberToObject(batteryTechnicalProperties, "ratedEnergy", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "maximumVoltage", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "expectedLifetime", random_integer(-5000, 5000));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "ratedMaximumPower", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "capacityThresholdForExhaustion", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(batteryTechnicalProperties, "lifetimeReferenceTest", "telnet://192.168.2.1/");
    cJSON_AddNumberToObject(batteryTechnicalProperties, "temeperatureRangeIdleState", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "ratedCapacity", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "nominalVoltage", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "minimumVoltage", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "initialSelfDischarge", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "roundtripEfficiency", random_float(-10000.0f, 10000.0f));

    // Create array
    cJSON *initialInternalResistance = cJSON_CreateArray();

    // Add object of arrays to sub-object
    cJSON_AddItemToObject(batteryTechnicalProperties, "initialInternalResistance", initialInternalResistance);

    // Create object for array
    cJSON *initialInternalResistanceObject = cJSON_CreateObject();
    cJSON_AddNumberToObject(initialInternalResistanceObject, "ohmicResistance", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(initialInternalResistanceObject, "batteryComponent", "pack");
    cJSON_AddItemToArray(initialInternalResistance, initialInternalResistanceObject);

    cJSON_AddNumberToObject(batteryTechnicalProperties, "cRate", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "cRateLifeCycleTest", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "powerCapabilityRatio", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(batteryTechnicalProperties, "expectedNumberOfCycles", random_float(-10000.0f, 10000.0f));

    // Create sub-object
    cJSON *batteryCondition = cJSON_CreateObject();

    // Add sub-object to JSON object
    cJSON_AddItemToObject(json, "batteryCondition", batteryCondition);

    // Create sub-sub-object
    cJSON *numberOfFullCycles = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "numberOfFullCycles", numberOfFullCycles);

    cJSON_AddNumberToObject(numberOfFullCycles, "numberOfFullCyclesValue", random_integer(-5000, 5000));
    cJSON_AddStringToObject(numberOfFullCycles, "lastUpdate", timestamp);

    cJSON_AddNumberToObject(batteryCondition, "roundTripEfficiencyatFiftyPerCentCycleLife", random_float(-10000.0f, 10000.0f));

    // Create sub-sub-object
    cJSON *stateOfCharge = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "stateOfCharge", stateOfCharge);

    cJSON_AddNumberToObject(stateOfCharge, "stateOfChargeValue", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(stateOfCharge, "lastUpdate", timestamp);

    // Create sub-sub-object
    cJSON *currentSelfDischargingRate = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "currentSelfDischargingRate", currentSelfDischargingRate);

    cJSON_AddNumberToObject(currentSelfDischargingRate, "currentSelfDischargingRateEntity", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(currentSelfDischargingRate, "lastUpdate", timestamp);

    // Create sub-sub-object
    cJSON *remainingEnergy = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "remainingEnergy", remainingEnergy);

    cJSON_AddNumberToObject(remainingEnergy, "remainingEnergyValue", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(remainingEnergy, "lastUpdate", timestamp);

    // Create sub-sub-object
    cJSON *evolutionOfSelfDischarge = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "evolutionOfSelfDischarge", evolutionOfSelfDischarge);

    cJSON_AddNumberToObject(evolutionOfSelfDischarge, "evolutionOfSelfDischargeEntityValue", random_integer(-5000, 5000));

    // Create sub-sub-object
    cJSON *negativeEvents = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "negativeEvents", negativeEvents);

    cJSON_AddStringToObject(negativeEvents, "negativeEvent", string);
    cJSON_AddStringToObject(negativeEvents, "lastUpdate", timestamp);

    // Create sub-sub-object
    cJSON *temperatureInformation = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "temperatureInformation", temperatureInformation);

    cJSON_AddNumberToObject(temperatureInformation, "timeExtremeHighTemp", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(temperatureInformation, "timeExtremeLowTempCharging", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(temperatureInformation, "timeExtremeHighTempCharging", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(temperatureInformation, "timeExtremeLowTemp", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(temperatureInformation, "lastUpdate", timestamp);

    // Create sub-sub-object
    cJSON *stateOfCertifiedEnergy = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "stateOfCertifiedEnergy", stateOfCertifiedEnergy);

    cJSON_AddNumberToObject(stateOfCertifiedEnergy, "stateOfCertifiedEnergyValue", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(stateOfCertifiedEnergy, "lastUpdate", timestamp);

    cJSON_AddNumberToObject(batteryCondition, "energyThroughput", random_float(-10000.0f, 10000.0f));


    // Create array
    cJSON *internalResistanceIncrease = cJSON_CreateArray();

    // Add object of arrays to sub-object
    cJSON_AddItemToObject(batteryCondition, "internalResistanceIncrease", internalResistanceIncrease);

    // Create object for array
    cJSON *internalResistanceIncreaseObject = cJSON_CreateObject();
    cJSON_AddNumberToObject(internalResistanceIncreaseObject, "internalResistanceIncreaseValue", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(internalResistanceIncreaseObject, "batteryComponent", "pack");
    cJSON_AddStringToObject(internalResistanceIncreaseObject, "lastUpdate", timestamp);
    cJSON_AddItemToArray(internalResistanceIncrease, internalResistanceIncreaseObject);

    // Create array
    cJSON *remainingPowerCapability = cJSON_CreateArray();

    // Add object of arrays to sub-object
    cJSON_AddItemToObject(batteryCondition, "remainingPowerCapability", remainingPowerCapability);

    // Create object for array
    cJSON *remainingPowerCapabilityObject = cJSON_CreateObject();

    cJSON *remainingPowerCapabilityValue = cJSON_CreateObject();
    cJSON_AddItemToObject(remainingPowerCapabilityObject, "remainingPowerCapabilityValue", remainingPowerCapabilityValue);

    cJSON_AddNumberToObject(remainingPowerCapabilityValue, "atSoc", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(remainingPowerCapabilityValue, "powerCapabilityAt", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(remainingPowerCapabilityValue, "rPCLastUpdated", timestamp);

    cJSON_AddStringToObject(remainingPowerCapabilityObject, "lastUpdate", timestamp);
    cJSON_AddItemToArray(remainingPowerCapability, remainingPowerCapabilityObject);

    cJSON_AddNumberToObject(batteryCondition, "roundTripEfficiencyFade", random_float(-10000.0f, 10000.0f));

    cJSON_AddNumberToObject(batteryCondition, "powerFade", random_float(-10000.0f, 10000.0f));

    // Create sub-sub-object
    cJSON *remainingRoundTripEnergyEfficiency = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "remainingRoundTripEnergyEfficiency", remainingRoundTripEnergyEfficiency);

    cJSON_AddNumberToObject(remainingRoundTripEnergyEfficiency, "remainingRoundTripEnergyEfficiencyValue", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(remainingRoundTripEnergyEfficiency, "lastUpdate", timestamp);

    // Create sub-sub-object
    cJSON *capacityThroughput = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "capacityThroughput", capacityThroughput);

    cJSON_AddNumberToObject(capacityThroughput, "capacityThroughputValue", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(capacityThroughput, "lastUpdate", timestamp);

    // Create sub-sub-object
    cJSON *remainingCapacity = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "remainingCapacity", remainingCapacity);

    cJSON_AddNumberToObject(remainingCapacity, "remainingCapacityValue", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(remainingCapacity, "lastUpdate", timestamp);

    // Create sub-sub-object
    cJSON *capacityFade = cJSON_CreateObject();

    // Add sub-sub-object to JSON object
    cJSON_AddItemToObject(batteryCondition, "capacityFade", capacityFade);

    cJSON_AddNumberToObject(capacityFade, "capacityFadeValue", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(capacityFade, "lastUpdate", timestamp);

    // Print JSON object
    char *json_string = cJSON_Print(json);
    //printf("Generated JSON Data:\n%s\n", json_string);

    // Clean up
    cJSON_Delete(json);
    //free(json_string);
    free(timestamp);
    free(string);

    return json_string;
}
