#include "process_json.h"

// Used by mockBMS to free json_string. Not used by BMS.
void free_json_string(const char* json_string) {
    free((void*)json_string);
}

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
    // Seed for random number generator
    srand(time(NULL));

    char* string = random_string(47);
    char* timestamp = generate_timestamp(); // timestamp

    //random_float(-10000.0f, 10000.0f)
    //timestamp
    //random_integer(-5000, 5000)
    //string

    // Create JSON object
    cJSON *json = cJSON_CreateObject();

    // Create carbonFootprint object
    cJSON *carbonFootprint = cJSON_CreateObject();
    cJSON_AddItemToObject(json, "carbonFootprint", carbonFootprint);

    // Create carbonFootprintPerLifecycleStage array
    cJSON *carbonFootprintPerLifecycleStage = cJSON_CreateArray();
    cJSON_AddItemToObject(carbonFootprint, "carbonFootprintPerLifecycleStage", carbonFootprintPerLifecycleStage);

    // Create lifecycle stage object
    cJSON *lifecycleStageObject = cJSON_CreateObject();
    cJSON_AddStringToObject(lifecycleStageObject, "lifecycleStage", "RawMaterialExtraction");
    cJSON_AddNumberToObject(lifecycleStageObject, "carbonFootprint", random_float(-10000.0f, 10000.0f));
    cJSON_AddItemToArray(carbonFootprintPerLifecycleStage, lifecycleStageObject);

    cJSON_AddStringToObject(carbonFootprint, "carbonFootprintStudy", "telnet://192.0.2.16:80/");
    cJSON_AddNumberToObject(carbonFootprint, "absoluteCarbonFootprint", random_float(-10000.0f, 10000.0f));
    cJSON_AddNumberToObject(carbonFootprint, "batteryCarbonFootprint", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(carbonFootprint, "carbonFootprintPerformanceClass", string);

    // Create circularity object
    cJSON *circularity = cJSON_CreateObject();
    cJSON_AddItemToObject(json, "circularity", circularity);

    cJSON_AddNumberToObject(circularity, "renewableContent", random_float(-10000.0f, 10000.0f));

    // Create dismantlingAndRemovalInformation array
    cJSON *dismantlingAndRemovalInformation = cJSON_CreateArray();
    cJSON_AddItemToObject(circularity, "dismantlingAndRemovalInformation", dismantlingAndRemovalInformation);

    // Create document object
    cJSON *documentObject = cJSON_CreateObject();
    cJSON_AddStringToObject(documentObject, "documentType", "BillOfMaterial");
    cJSON_AddStringToObject(documentObject, "mimeType", string);
    cJSON_AddStringToObject(documentObject, "documentURL", "telnet://192.0.2.16:80/");
    cJSON_AddItemToArray(dismantlingAndRemovalInformation, documentObject);

    // Create recycledContent array
    cJSON *recycledContent = cJSON_CreateArray();
    cJSON_AddItemToObject(circularity, "recycledContent", recycledContent);

    // Create recycled material object
    cJSON *recycledMaterialObject = cJSON_CreateObject();
    cJSON_AddNumberToObject(recycledMaterialObject, "preConsumerShare", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(recycledMaterialObject, "recycledMaterial", "Cobalt");
    cJSON_AddNumberToObject(recycledMaterialObject, "postConsumerShare", random_float(-10000.0f, 10000.0f));
    cJSON_AddItemToArray(recycledContent, recycledMaterialObject);

    // Create endOfLifeInformation object
    cJSON *endOfLifeInformation = cJSON_CreateObject();
    cJSON_AddItemToObject(circularity, "endOfLifeInformation", endOfLifeInformation);
    cJSON_AddStringToObject(endOfLifeInformation, "separateCollection", "ftp://ftp.is.co.za/rfc/rfc1808.txt");
    cJSON_AddStringToObject(endOfLifeInformation, "wastePrevention", "http://www.wikipedia.org");
    cJSON_AddStringToObject(endOfLifeInformation, "informationOnCollection", "telnet://192.0.2.16:80/");

    // Create safetyMeasures object
    cJSON *safetyMeasures = cJSON_CreateObject();
    cJSON_AddItemToObject(circularity, "safetyMeasures", safetyMeasures);
    cJSON_AddStringToObject(safetyMeasures, "safetyInstructions", "http://www.ietf.org/rfc/rfc2396.txt");

    // Create extinguishingAgent array
    cJSON *extinguishingAgent = cJSON_CreateArray();
    cJSON_AddItemToObject(safetyMeasures, "extinguishingAgent", extinguishingAgent);
    cJSON_AddItemToArray(extinguishingAgent, cJSON_CreateString(string));

    // Create sparePartSources array
    cJSON *sparePartSources = cJSON_CreateArray();
    cJSON_AddItemToObject(circularity, "sparePartSources", sparePartSources);

    // Create spare part source object
    cJSON *sparePartSourceObject = cJSON_CreateObject();
    cJSON_AddStringToObject(sparePartSourceObject, "nameOfSupplier", string);

    // Create components array
    cJSON *components = cJSON_CreateArray();
    cJSON_AddItemToObject(sparePartSourceObject, "components", components);

    // Create component object
    cJSON *componentObject = cJSON_CreateObject();
    cJSON_AddStringToObject(componentObject, "partName", "Cell");
    cJSON_AddStringToObject(componentObject, "partNumber", string);
    cJSON_AddItemToArray(components, componentObject);

    cJSON_AddStringToObject(sparePartSourceObject, "supplierWebAddress", "ftp://ftp.is.co.za/rfc/rfc1808.txt");
    cJSON_AddStringToObject(sparePartSourceObject, "emailAddressOfSupplier", "supplier@example.com");

    // Create addressOfSupplier object
    cJSON *addressOfSupplier = cJSON_CreateObject();
    cJSON_AddItemToObject(sparePartSourceObject, "addressOfSupplier", addressOfSupplier);
    cJSON_AddStringToObject(addressOfSupplier, "addressCountry", "Germany");
    cJSON_AddStringToObject(addressOfSupplier, "streetAddress", "Street 1");
    cJSON_AddStringToObject(addressOfSupplier, "postalCode", "DE-10719");

    cJSON_AddItemToArray(sparePartSources, sparePartSourceObject);

    // Create generalProductInformation object
    cJSON *generalProductInformation = cJSON_CreateObject();
    cJSON_AddItemToObject(json, "generalProductInformation", generalProductInformation);

    cJSON_AddStringToObject(generalProductInformation, "batteryCategory", "lmt");

    // Create operatorInformation object
    cJSON *operatorInformation = cJSON_CreateObject();
    cJSON_AddItemToObject(generalProductInformation, "operatorInformation", operatorInformation);
    cJSON_AddStringToObject(operatorInformation, "identifier", string);
    cJSON_AddStringToObject(operatorInformation, "contactName", string);

    // Create postalAddress object
    cJSON *postalAddress = cJSON_CreateObject();
    cJSON_AddItemToObject(operatorInformation, "postalAddress", postalAddress);
    cJSON_AddStringToObject(postalAddress, "addressCountry", "Germany");
    cJSON_AddStringToObject(postalAddress, "streetAddress", "Hindenburgstr. 10");
    cJSON_AddStringToObject(postalAddress, "postalCode", "10719");

    cJSON_AddStringToObject(generalProductInformation, "productIdentifier", string);
    cJSON_AddStringToObject(generalProductInformation, "batteryStatus", "Original");
    cJSON_AddStringToObject(generalProductInformation, "puttingIntoService", timestamp);
    cJSON_AddNumberToObject(generalProductInformation, "batteryMass", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(generalProductInformation, "manufacturingDate", timestamp);
    cJSON_AddStringToObject(generalProductInformation, "batteryPassportIdentifier", "urn:bmwk:123456687678");
    cJSON_AddStringToObject(generalProductInformation, "warrentyPeriod", "--01");

    // Create manufacturerInformation object
    cJSON *manufacturerInformation = cJSON_CreateObject();
    cJSON_AddItemToObject(generalProductInformation, "manufacturerInformation", manufacturerInformation);
    cJSON_AddStringToObject(manufacturerInformation, "identifier", "JxkyvRnL");
    cJSON_AddStringToObject(manufacturerInformation, "contactName", string);

    // Create postalAddress object for manufacturer
    cJSON *manufacturerPostalAddress = cJSON_CreateObject();
    cJSON_AddItemToObject(manufacturerInformation, "postalAddress", manufacturerPostalAddress);
    cJSON_AddStringToObject(manufacturerPostalAddress, "addressCountry", "Germany");
    cJSON_AddStringToObject(manufacturerPostalAddress, "streetAddress", "Hindenburgstr. 10");
    cJSON_AddStringToObject(manufacturerPostalAddress, "postalCode", "10719");

    // Create manufacturingPlace object
    cJSON *manufacturingPlace = cJSON_CreateObject();
    cJSON_AddItemToObject(generalProductInformation, "manufacturingPlace", manufacturingPlace);
    cJSON_AddStringToObject(manufacturingPlace, "addressCountry", "Germany");
    cJSON_AddStringToObject(manufacturingPlace, "streetAddress", "Hindenburgstr. 10");
    cJSON_AddStringToObject(manufacturingPlace, "postalCode", "10719");

    // Create labels object
    cJSON *labels = cJSON_CreateObject();
    cJSON_AddItemToObject(json, "labels", labels);
    cJSON_AddStringToObject(labels, "resultOfTestReport", "ftp://ftp.is.co.za/rfc/rfc1808.txt");
    cJSON_AddStringToObject(labels, "declarationOfConformity", "telnet://192.0.2.16:80/");

    // Create labels array
    cJSON *labelsArray = cJSON_CreateArray();
    cJSON_AddItemToObject(labels, "labels", labelsArray);

    // Create label object
    cJSON *labelObject = cJSON_CreateObject();
    cJSON_AddStringToObject(labelObject, "labelingSubject", "SeparateCollection");
    cJSON_AddStringToObject(labelObject, "labelingSymbol", "http://www.ietf.org/rfc/rfc2396.txt");

    // Create labelingMeaning object
    cJSON *labelingMeaning = cJSON_CreateObject();
    cJSON_AddItemToObject(labelObject, "labelingMeaning", labelingMeaning);
    cJSON_AddStringToObject(labelingMeaning, "en", "Separate Collection");

    cJSON_AddItemToArray(labelsArray, labelObject);

    // Create materialComposition object
    cJSON *materialComposition = cJSON_CreateObject();
    cJSON_AddItemToObject(json, "materialComposition", materialComposition);

    // Create batteryChemistry object
    cJSON *batteryChemistry = cJSON_CreateObject();
    cJSON_AddItemToObject(materialComposition, "batteryChemistry", batteryChemistry);
    cJSON_AddStringToObject(batteryChemistry, "shortName", "NMC");
    cJSON_AddStringToObject(batteryChemistry, "clearName", "Lithium nickel manganese cobalt oxides");

    // Create hazardousSubstances array
    cJSON *hazardousSubstances = cJSON_CreateArray();
    cJSON_AddItemToObject(materialComposition, "hazardousSubstances", hazardousSubstances);

    // Create hazardous substance object
    cJSON *hazardousSubstanceObject = cJSON_CreateObject();
    cJSON_AddStringToObject(hazardousSubstanceObject, "hazardousSubstanceClass", "AcuteToxicity");
    cJSON_AddNumberToObject(hazardousSubstanceObject, "hazardousSubstanceConcentration", random_float(-10000.0f, 10000.0f));

    // Create hazardousSubstanceImpact array
    cJSON *hazardousSubstanceImpact = cJSON_CreateArray();
    cJSON_AddItemToObject(hazardousSubstanceObject, "hazardousSubstanceImpact", hazardousSubstanceImpact);
    cJSON_AddItemToArray(hazardousSubstanceImpact, cJSON_CreateString("JxkyvRnL"));

    cJSON_AddStringToObject(hazardousSubstanceObject, "hazardousSubstanceIdentifier", "37-70-2");

    // Create hazardousSubstanceLocation object
    cJSON *hazardousSubstanceLocation = cJSON_CreateObject();
    cJSON_AddItemToObject(hazardousSubstanceObject, "hazardousSubstanceLocation", hazardousSubstanceLocation);
    cJSON_AddStringToObject(hazardousSubstanceLocation, "componentName", "Anode");
    cJSON_AddStringToObject(hazardousSubstanceLocation, "componentId", string);

    cJSON_AddStringToObject(hazardousSubstanceObject, "hazardousSubstanceName", string);
    cJSON_AddItemToArray(hazardousSubstances, hazardousSubstanceObject);

    // Create batteryMaterials array
    cJSON *batteryMaterials = cJSON_CreateArray();
    cJSON_AddItemToObject(materialComposition, "batteryMaterials", batteryMaterials);

    // Create battery material object
    cJSON *batteryMaterialObject = cJSON_CreateObject();
    cJSON_AddStringToObject(batteryMaterialObject, "batteryMaterialIdentifier", "7439-93-2");
    cJSON_AddNumberToObject(batteryMaterialObject, "batteryMaterialMass", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(batteryMaterialObject, "batteryMaterialName", "Lithium");

    // Create batteryMaterialLocation object
    cJSON *batteryMaterialLocation = cJSON_CreateObject();
    cJSON_AddItemToObject(batteryMaterialObject, "batteryMaterialLocation", batteryMaterialLocation);
    cJSON_AddStringToObject(batteryMaterialLocation, "componentName", "Anode");
    cJSON_AddStringToObject(batteryMaterialLocation, "componentId", string);

    cJSON_AddBoolToObject(batteryMaterialObject, "isCriticalRawMaterial", true);
    cJSON_AddItemToArray(batteryMaterials, batteryMaterialObject);

    // ###### Content of Previous Datagen Code (Slightly modified) ######

    // Create performance object
    cJSON *performance = cJSON_CreateObject();
    cJSON_AddItemToObject(json, "performance", performance);

    // Create batteryTechnicalProperties object
    cJSON *batteryTechnicalProperties = cJSON_CreateObject();
    cJSON_AddItemToObject(performance, "batteryTechnicalProperties", batteryTechnicalProperties);

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
    cJSON_AddItemToObject(performance, "batteryCondition", batteryCondition);

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

    // ###### End of Content of Previous Datagen Code ######

    // Create supplyChainDueDiligence object
    cJSON *supplyChainDueDiligence = cJSON_CreateObject();
    cJSON_AddItemToObject(json, "supplyChainDueDiligence", supplyChainDueDiligence);

    // Add properties to supplyChainDueDiligence
    cJSON_AddStringToObject(supplyChainDueDiligence, "supplyChainDueDiligenceReport", "telnet://192.0.2.16:80/");
    cJSON_AddNumberToObject(supplyChainDueDiligence, "supplyChainIndicies", random_float(-10000.0f, 10000.0f));
    cJSON_AddStringToObject(supplyChainDueDiligence, "thirdPartyAussurances", "ftp://ftp.is.co.za/rfc/rfc1808.txt");

    // Print JSON object
    char *json_string = cJSON_Print(json);

    if (json_string == NULL) {
        fprintf(stderr, "Failed to print JSON\n");
        cJSON_Delete(json);
        free(timestamp);
        free(string);
        return NULL;
    }
    //printf("Generated JSON Data:\n%s\n", json_string);

    // Clean up
    cJSON_Delete(json);
    //free(json_string);
    free(timestamp);
    free(string);

    return json_string;
}
