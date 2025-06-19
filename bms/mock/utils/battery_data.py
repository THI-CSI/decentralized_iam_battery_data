import datetime
import json
import pathlib

def get_battery_data_from_file():
  with open(
          pathlib.Path(__file__).parent.parent.parent.parent / "cloud" / "docs" / "example" / "batterypass.json") as f:
    return f.read()

def get_battery_data():
    data = {
  "carbonFootprint": {
    "carbonFootprintPerLifecycleStage": [
      {
        "lifecycleStage": "RawMaterialExtraction",
        "carbonFootprint": -1.7976931348623157E308
      }
    ],
    "carbonFootprintStudy": "telnet://192.0.2.16:80/",
    "absoluteCarbonFootprint": -1.7976931348623157E308,
    "batteryCarbonFootprint": -1.7976931348623157E308,
    "carbonFootprintPerformanceClass": "eOMtThyhVNLWUZNRcBaQKxI"
  },
  "circularity": {
    "renewableContent" : -2.894541E38,
    "dismantlingAndRemovalInformation" : [ {
      "documentType" : "BillOfMaterial",
      "mimeType" : "eOMtThyhVNLWUZNRcBaQKxI",
      "documentURL" : "telnet://192.0.2.16:80/"
    } ],
    "recycledContent" : [ {
      "preConsumerShare" : 30.780313,
      "recycledMaterial" : "Cobalt",
      "postConsumerShare" : 26.266407
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
      "emailAddressOfSupplier" : ".--ww.-w-w--w--ww-.-w.ww.-..-.w-.www..--w.-w..w---ww-.ww-w-ww-w---w.ww--.w-.w-.ww-..w-.-www.-w..w.--@ww.w.-w..--.-w....-ww..w.www-.w.EinpcjJtYqJLuEKKRGXf",
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
    "batteryMass" : 699.0,
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
      "hazardousSubstanceConcentration" : -1.7976931348623157E308,
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
      "batteryMaterialMass" : 1.6111172E38,
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
        "atSoC" : 2.3393242E38,
        "powerCapabilityAt" : -1.2896817E38
      } ],
      "ratedEnergy" : -1.2185897E38,
      "maximumVoltage" : -2.4890157E38,
      "expectedLifetime" : -3072,
      "ratedMaximumPower" : -1.7976931348623157E308,
      "capacityThresholdForExhaustion" : -1.7976931348623157E308,
      "lifetimeReferenceTest" : "telnet://192.0.2.16:80/",
      "temperatureRangeIdleState" : -19.539389775261977,
      "ratedCapacity" : 2.994716E38,
      "nominalVoltage" : -3.1849857E38,
      "minimumVoltage" : 1.687085E38,
      "initialSelfDischarge" : -1.7976931348623157E308,
      "roundtripEfficiency" : 2.1913484E38,
      "initialInternalResistance" : [ {
        "ohmicResistance" : -1.7976931348623157E308,
        "batteryComponent" : "pack"
      } ],
      "cRate" : 9.081415E37,
      "cRateLifeCycleTest" : -3.265165E38,
      "powerCapabilityRatio" : -1.8147613E38,
      "expectedNumberOfCycles" : -4979411194606956234
    },
    "batteryCondition" : {
      "numberOfFullCycles" : {
        "numberOfFullCyclesValue" : 1212721721,
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      },
      "roundTripEfficiencyat50PerCentCycleLife" : 9.766551E37,
      "stateOfCharge" : {
        "stateOfChargeValue" : 6.009356E36,
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      },
      "currentSelfDischargingRate" : {
        "currentSelfDischargingRateEntity" : 1.2559217E38,
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      },
      "remainingEnergy" : {
        "remainingEnergyalue" : -7.096584E37,
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      },
      "evolutionOfSelfDischarge" : {
        "evolutionOfSelfDischargeEntityValue" : -2.209267E37
      },
      "negativeEvents" : [ {
        "negativeEvent" : "eOMtThyhVNLWUZNRcBaQKxI",
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      } ],
      "temperatureInformation" : {
        "timeExtremeHighTemp" : -1.7976931348623157E308,
        "timeExtremeLowTempCharging" : -1.7976931348623157E308,
        "timeExtremeHighTempCharging" : -1.7976931348623157E308,
        "timeExtremeLowTemp" : -1.7976931348623157E308,
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      },
      "stateOfCertifiedEnergy" : {
        "stateOfCertifiedEnergyValue" : -2.309167E38,
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      },
      "energyThroughput" : -1.7976931348623157E308,
      "internalResistanceIncrease" : [ {
        "internalResistanceIncreaseValue" : -1.985763E38,
        "batteryComponent" : "pack",
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      } ],
      "remainingPowerCapability" : [ {
        "remainingPowerCapabilityValue" : {
          "atSoC" : 3.2114295E38,
          "powerCapabilityAt" : -1.6049327E38,
          "rPCLastUpdated" : "2025-01-31T14:06:29.437+01:00"
        },
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      } ],
      "roundTripEfficiencyFade" : 5.5394977E37,
      "powerFade" : 2.7326235E38,
      "remainingRoundTripEnergyEfficiency" : {
        "remainingRoundTripEnergyEfficiencyValue" : -3.0350486E37,
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      },
      "capacityThroughput" : {
        "capacityThroughputValue" : -1.0970223E38,
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      },
      "remainingCapacity" : {
        "remainingCapacityValue" : -3.7981266E37,
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      },
      "capacityFade" : {
        "capacityFadeValue" : -4.8788013E37,
        "lastUpdate" : "2025-01-31T14:06:29.437+01:00"
      }
    }
  },
  "supplyChainDueDiligence": {
    "supplyChainDueDiligenceReport" : "telnet://192.0.2.16:80/",
    "supplyChainIndicies" : 2.1624482E38,
    "thirdPartyAussurances" : "ftp://ftp.is.co.za/rfc/rfc1808.txt"
  }
}
    return json.dumps(data)