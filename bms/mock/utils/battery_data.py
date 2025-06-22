import datetime
import random
import re
import string
import sys
from typing import Union, Dict, List, Any

if not  __name__ == "__main__":
  import utils.poc.genJSONexampleFromSchema as genJSONexampleFromSchema
  from utils.logging import log
else:
  from logging import log
import json
import os

NEW_DATA_GEN = os.getenv("NEW_DATA_GEN", "false") == "true"

def get_battery_data():
  # TODO
  if NEW_DATA_GEN:
    try:
      genData = genJSONexampleFromSchema.generate_fake_battery_data("../../cloud/BatteryPassDataModel/BatteryData-Root-schema.json")
    except:
      print("Error generating fake data")
    print(genData)
    return genData

  data = get_battery_data_dict()
  return json.dumps(data)


def get_battery_data_update():
  # TODO
  if NEW_DATA_GEN:
    return get_battery_data()

  data = [
    { "performance.batteryCondition.numberOfFullCycles": generate_random_value(int, min_value=10, max_value=10000) },
    { "performance.batteryCondition.remainingCapacity": generate_random_value(int, min_value=10, max_value=100) },
    { "performance.batteryCondition.roundTripEfficiencyat50PerCentCycleLife": generate_random_value(float, min_value=1) },
  ]
  return json.dumps(data)


def get_battery_data_dict():
  data = {
    "carbonFootprint": {
      "carbonFootprintPerLifecycleStage": [
        {
          "lifecycleStage": "RawMaterialExtraction",
          "carbonFootprint": generate_random_value(float)
        }
      ],
      "carbonFootprintStudy": "telnet://192.0.2.16:80/",
      "absoluteCarbonFootprint": generate_random_value(float),
      "batteryCarbonFootprint": generate_random_value(float),
      "carbonFootprintPerformanceClass": "eOMtThyhVNLWUZNRcBaQKxI"
    },
    "circularity": {
      "renewableContent": generate_random_value(float),
      "dismantlingAndRemovalInformation" : [ {
        "documentType" : "BillOfMaterial",
        "mimeType" : "eOMtThyhVNLWUZNRcBaQKxI",
        "documentURL" : "telnet://192.0.2.16:80/"
      } ],
      "recycledContent" : [ {
        "preConsumerShare" : generate_random_value(float, min_value=0.0, max_value=100.0),
        "recycledMaterial" : "Cobalt",
        "postConsumerShare" : generate_random_value(float, min_value=0.0, max_value=100.0)
      } ],
      "endOfLifeInformation" : {
        "separateCollection" : "ftp://ftp.is.co.za/rfc/rfc1808.txt",
        "wastePrevention" : "http://www.wikipedia.org",
        "informationOnCollection" : "telnet://192.0.2.16:80/"
      },
      "safetyMeasures" : {
        "safetyInstructions" : "http://www.ietf.org/rfc/rfc2396.txt",
        "extinguishingAgent" : [ "RYtGKbgicZaHCBRQDSx" ]
      },
      "sparePartSources" : [ {
        "nameOfSupplier" : "yedUsFwdkelQbxeTeQOvaScfqIOOmaa",
        "components" : [ {
          "partName" : "Cell",
          "partNumber" : "JxkyvRnL"
        } ],
        "supplierWebAddress" : "ftp://ftp.is.co.za/rfc/rfc1808.txt",
        "emailAddressOfSupplier" : "info@supplier.com",
        "addressOfSupplier" : {
          "addressCountry" : "Germany",
          "streetAddress" : "Street 1",
          "postalCode" : "DE-10719"
        }
      } ]
    },
    "generalProductInformation": {
      "batteryCategory" : "lmt",
      "operatorInformation" : {
        "identifier" : "VLhpfQGTMDYpsBZxvfBoeygjb",
        "contactName" : "RYtGKbgicZaHCBRQDSx",
        "postalAddress" : {
          "addressCountry" : "Germany",
          "streetAddress" : "Hindenburgstr. 10",
          "postalCode" : "10719"
        }
      },
      "productIdentifier" : "eOMtThyhVNLWUZNRcBaQKxI",
      "batteryStatus" : "Original",
      "puttingIntoService" : "2025-01-10T15:09:02.858+01:00",
      "batteryMass" : generate_random_value(float, min_value=100.0, max_value=1500.0),
      "manufacturingDate" : "2025-01-10T15:09:02.852+01:00",
      "batteryPassportIdentifier" : "urn:bmwk:123456687678",
      "warrentyPeriod" : "--01",
      "manufacturerInformation" : {
        "identifier" : "JxkyvRnL",
        "contactName" : "yedUsFwdkelQbxeTeQOvaScfqIOOmaa",
        "postalAddress" : {
          "addressCountry" : "Germany",
          "streetAddress" : "Hindenburgstr. 10",
          "postalCode" : "10719"
        }
      },
      "manufacturingPlace" : {
        "addressCountry" : "Germany",
        "streetAddress" : "Hindenburgstr. 10",
        "postalCode" : "10719"
      }
    },
    "labels": {
      "resultOfTestReport" : "ftp://ftp.is.co.za/rfc/rfc1808.txt",
      "declarationOfConformity" : "telnet://192.0.2.16:80/",
      "labels" : [ {
        "labelingSubject" : "SeparateCollection",
        "labelingSymbol" : "http://www.ietf.org/rfc/rfc2396.txt",
        "labelingMeaning" : {
          "en" : "Separate Collection"
        }
      } ]
    },
    "materialComposition": {
      "batteryChemistry" : {
        "shortName" : "NMC",
        "clearName" : "Lithium nickel manganese cobalt oxides"
      },
      "hazardousSubstances" : [ {
        "hazardousSubstanceClass" : "AcuteToxicity",
        "hazardousSubstanceConcentration" : generate_random_value(float),
        "hazardousSubstanceImpact" : [ "JxkyvRnL" ],
        "hazardousSubstanceIdentifier" : "37-70-2",
        "hazardousSubstanceLocation" : {
          "componentName" : "Anode",
          "componentId" : "RYtGKbgicZaHCBRQDSx"
        },
        "hazardousSubstanceName" : "yedUsFwdkelQbxeTeQOvaScfqIOOmaa"
      } ],
      "batteryMaterials" : [ {
        "batteryMaterialIdentifier" : "7439-93-2",
        "batteryMaterialMass" : generate_random_value(float, min_value=150.0, max_value=2000.0),
        "batteryMaterialName" : "Lithium",
        "batteryMaterialLocation" : {
          "componentName" : "Anode",
          "componentId" : "eOMtThyhVNLWUZNRcBaQKxI"
        },
        "isCriticalRawMaterial" : True
      } ]
    },
    "performance": {
      "batteryTechicalProperties" : {
        "originalPowerCapability" : [ {
          "atSoC" : generate_random_value(float),
          "powerCapabilityAt" : generate_random_value(float)
        } ],
        "ratedEnergy" : generate_random_value(float),
        "maximumVoltage" : generate_random_value(float),
        "expectedLifetime" : generate_random_value(int, min_value=-32768, max_value=32767),
        "ratedMaximumPower" : generate_random_value(float),
        "capacityThresholdForExhaustion" : generate_random_value(float),
        "lifetimeReferenceTest" : "telnet://192.0.2.16:80/",
        "temperatureRangeIdleState" : generate_random_value(float, min_value=-20.0, max_value=60.0),
        "ratedCapacity" : generate_random_value(float),
        "nominalVoltage" : generate_random_value(float),
        "minimumVoltage" : generate_random_value(float),
        "initialSelfDischarge" : generate_random_value(float),
        "roundtripEfficiency" : generate_random_value(float),
        "initialInternalResistance" : [ {
          "ohmicResistance" : generate_random_value(float),
          "batteryComponent" : "pack"
        } ],
        "cRate" : generate_random_value(float),
        "cRateLifeCycleTest" : generate_random_value(float),
        "powerCapabilityRatio" : generate_random_value(float),
        "expectedNumberOfCycles" : generate_random_value(int, min_value=-9223372036854775808, max_value=9223372036854775807),
      },
      "batteryCondition" : {
        "numberOfFullCycles" : {
          "numberOfFullCyclesValue" : generate_random_value(int),
          "lastUpdate" : get_current_datetime_formatted()
        },
        "roundTripEfficiencyat50PerCentCycleLife" : generate_random_value(float),
        "stateOfCharge" : {
          "stateOfChargeValue" : generate_random_value(float),
          "lastUpdate" : get_current_datetime_formatted()
        },
        "currentSelfDischargingRate" : {
          "currentSelfDischargingRateEntity" : generate_random_value(float),
          "lastUpdate" : get_current_datetime_formatted()
        },
        "remainingEnergy" : {
          "remainingEnergyalue" : generate_random_value(float),
          "lastUpdate" : get_current_datetime_formatted()
        },
        "evolutionOfSelfDischarge" : {
          "evolutionOfSelfDischargeEntityValue" : generate_random_value(float)
        },
        "negativeEvents" : [ {
          "negativeEvent" : "eOMtThyhVNLWUZNRcBaQKxI",
          "lastUpdate" : get_current_datetime_formatted()
        } ],
        "temperatureInformation" : {
          "timeExtremeHighTemp" : generate_random_value(float),
          "timeExtremeLowTempCharging" : generate_random_value(float),
          "timeExtremeHighTempCharging" : generate_random_value(float),
          "timeExtremeLowTemp" : generate_random_value(float),
          "lastUpdate" : get_current_datetime_formatted()
        },
        "stateOfCertifiedEnergy" : {
          "stateOfCertifiedEnergyValue" : generate_random_value(float),
          "lastUpdate" : get_current_datetime_formatted()
        },
        "energyThroughput" : generate_random_value(float),
        "internalResistanceIncrease" : [ {
          "internalResistanceIncreaseValue" : generate_random_value(float),
          "batteryComponent" : "pack",
          "lastUpdate" : get_current_datetime_formatted()
        } ],
        "remainingPowerCapability" : [ {
          "remainingPowerCapabilityValue" : {
            "atSoC" : 3.2114295E38,
            "powerCapabilityAt" : -1.6049327E38,
            "rPCLastUpdated" : get_current_datetime_formatted()
          },
          "lastUpdate" : get_current_datetime_formatted()
        } ],
        "roundTripEfficiencyFade" : generate_random_value(float),
        "powerFade" : generate_random_value(float),
        "remainingRoundTripEnergyEfficiency" : {
          "remainingRoundTripEnergyEfficiencyValue" : generate_random_value(float),
          "lastUpdate" : get_current_datetime_formatted()
        },
        "capacityThroughput" : {
          "capacityThroughputValue" : generate_random_value(float),
          "lastUpdate" : get_current_datetime_formatted()
        },
        "remainingCapacity" : {
          "remainingCapacityValue" : generate_random_value(float),
          "lastUpdate" : get_current_datetime_formatted()
        },
        "capacityFade" : {
          "capacityFadeValue" : generate_random_value(float),
          "lastUpdate" : get_current_datetime_formatted()
        }
      }
    },
    "supplyChainDueDiligence": {
      "supplyChainDueDiligenceReport" : "telnet://192.0.2.16:80/",
      "supplyChainIndicies" : generate_random_value(float),
      "thirdPartyAussurances" : "ftp://ftp.is.co.za/rfc/rfc1808.txt"
    }
  }
  return data


def generate_random_value(datatype: type, regex: str = None, sign: bool = False, min_value: Union[int, float, None] = None, max_value: Union[int, float, None] = None):

  if datatype is str:
    if regex:
      # Simplified regex handling for string generation

      generated_chars = []
      length_min = 5
      length_max = 20

      char_class_match = re.match(r"\[([a-zA-Z0-9\-_]+)\](\{([0-9]+)(?:,([0-9]+))?\})?", regex)
      escape_char_match = re.match(r"\\([dws])(\{([0-9]+)(?:,([0-9]+))?\})?", regex)

      char_set_from_regex = []

      if char_class_match:
        # e.g. [a-zA-Z0-9]{5,10}
        char_class_str = char_class_match.group(1)
        if 'a-z' in char_class_str:
          char_set_from_regex.extend(string.ascii_lowercase)
        if 'A-Z' in char_class_str:
          char_set_from_regex.extend(string.ascii_uppercase)
        if '0-9' in char_class_str:
          char_set_from_regex.extend(string.digits)
        # e.g. '-', '_'
        for char in char_class_str:
          if char not in ['a', 'A', '0', '-', 'z', 'Z', '9'] and char not in char_set_from_regex:
            char_set_from_regex.append(char)

        if char_class_match.group(3):  # Quantifier like {min,max} or {exact}
          length_min = int(char_class_match.group(3))
          length_max = int(char_class_match.group(4)) if char_class_match.group(4) else length_min

      elif escape_char_match:
        escape_type = escape_char_match.group(1)
        if escape_type == 'd':  # \d (digits)
          char_set_from_regex = list(string.digits)
        elif escape_type == 'w':  # \w (letters, digits, underscore)
          char_set_from_regex = list(string.ascii_letters + string.digits + '_')
        elif escape_type == 's':  # \s (whitespace)
          char_set_from_regex = list(string.whitespace)

        if escape_char_match.group(3):  # Has quantifier
          length_min = int(escape_char_match.group(3))
          length_max = int(escape_char_match.group(4)) if escape_char_match.group(4) else length_min

      if char_set_from_regex:
        if not char_set_from_regex:
          log.warning(f"Regex '{regex}' resulted in an empty character set. Using general random string.")
          characters = string.ascii_letters + string.digits + string.punctuation
          length = random.randint(5, 20)
          return ''.join(random.choice(characters) for _ in range(length))

        chosen_length = random.randint(length_min, length_max)
        random_string = ''.join(random.choice(char_set_from_regex) for _ in range(chosen_length))
        return random_string
      else:
        log.warning(f"Regex '{regex}' is too complex or not supported. Using general random string.")
        characters = string.ascii_letters + string.digits + string.punctuation
        length = random.randint(5, 20)
        return ''.join(random.choice(characters) for _ in range(length))
    else:
      characters = string.ascii_letters + string.digits + string.punctuation
      length = random.randint(5, 20)
      random_string = ''.join(random.choice(characters) for _ in range(length))
      return random_string

  elif datatype is int:
    _min = -sys.maxsize -1
    _max = sys.maxsize

    if min_value is not None:
      _min = int(min_value)
    if max_value is not None:
      _max = int(max_value)

    if sign:
      _min = max(0, _min)
      if _max < 0 and max_value is not None:
        _max = sys.maxsize

    return random.randint(_min, _max)

  elif datatype is float:
    _min = sys.float_info.min
    _max = sys.float_info.max

    if min_value is not None:
      _min = float(min_value)
    if max_value is not None:
      _max = float(max_value)

    if sign:
      _min = max(0.0, _min)
      if _max < 0.0 and max_value is not None:
        _max = sys.float_info.max
    return random.uniform(_min, _max)

  elif datatype is bool:
    return random.choice([True, False])

  elif datatype is datetime.datetime:
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365 * 10)
    time_between_dates = end_date - start_date
    total_seconds = int(time_between_dates.total_seconds())
    random_seconds = random.randint(0, total_seconds)
    random_datetime = start_date + datetime.timedelta(seconds=random_seconds)
    return random_datetime

  else:
    return None

def get_current_datetime_formatted() -> str:
  now_utc = datetime.datetime.now(datetime.timezone.utc)
  now_local = now_utc.astimezone()
  date_part = now_local.strftime("%Y-%m-%d")
  time_part = now_local.strftime("%H:%M:%S.%f")[:-3]
  offset = now_local.utcoffset()
  if offset is None:
      tz_offset_str = "+00:00"
  else:
      total_seconds = offset.total_seconds()
      sign = '+' if total_seconds >= 0 else '-'
      abs_seconds = abs(total_seconds)
      hours = int(abs_seconds // 3600)
      minutes = int((abs_seconds % 3600) // 60)
      tz_offset_str = f"{sign}{hours:02}:{minutes:02}"
  return f"{date_part}T{time_part}{tz_offset_str}"


if __name__ == "__main__":
  log.info(f"Random String with Regex '[a-zA-Z0-9]{20}': {generate_random_value(str, "[a-zA-Z0-9]{20}")}")
  log.info(f"Random int: {generate_random_value(int)}")
  log.info(f"Random int signed: {generate_random_value(int, sign=True)}")
  log.info(f"Random int with min_value 100: {generate_random_value(int, min_value=100)}")
  log.info(f"Random int with max_value 100: {generate_random_value(int, max_value=100)}")
  log.info(f"Random int in range 0-10: {generate_random_value(int, min_value=0, max_value=10)}")
  log.info(f"Random float: {generate_random_value(float)}")
  log.info(f"Random float signed: {generate_random_value(float, sign=True)}")
  log.info(f"Random float with min_value 100.0: {generate_random_value(float, min_value=100.0)}")
  log.info(f"Random float with max_value 100.0: {generate_random_value(float, max_value=100.0)}")
  log.info(f"Random float in range 0-10: {generate_random_value(float, min_value=0, max_value=10)}")
  log.info(f"Random bool: {generate_random_value(bool)}")
  log.info(f"Random datetime: {generate_random_value(datetime.datetime)}")

  log.info(f"Current Datetime: {get_current_datetime_formatted()}")