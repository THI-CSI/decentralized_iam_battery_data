# Data-types and Data-attributes of Battery Passport

NOTE: The following information is worked out of the tables of DIN_DKE_SPEC_99100  
Each element of the following has further information (generally and sometimes format specifications) to be read in DIN_DKE_SPEC_99100, if needed the corresponding clause is mentioned below.  
All information is divided in mandatory and recommendation. This aspect was left out here as we just need examples.

### 1) Battery passport data attributes related to identifiers and to general battery properties

| Clause   | Data attribute                        | Data access                      | Data type [Unit] | Static/Dynamic |
|----------|--------------------------------------|----------------------------------|------------------|---------------------------|
| 6.1.2.1  | Battery passport identifier         | Public                           | ID               | S                         |
| 6.1.2.2  | Persons with a legitimate interest  | Persons with a legitimate interest | ID               | S                         |
| 6.1.2.3  | Digital twin identifier             | Persons with a legitimate interest | ID               | S                         |
| 6.1.2.4  | Manufacturer identifier & info      | Public                           | ID               | S                         |
| 6.1.3.1  | Manufacturing place                 | Public                           | String           | S                         |
| 6.1.3.2  | Manufacturing date                  | Public                           | Date [YYYY-MM]   | S                         |
| 6.1.3.3  | Unique battery model identifier     | Persons with a legitimate interest | ID               | S                         |
| 6.1.3.4  | Warranty period of the battery      | Public                           | Date [YYYY-MM]   | S                         |
| 6.1.3.5  | Battery category                    | Public                           | String           | S                         |
| 6.1.3.6  | Battery mass                        | Public                           | Decimal [kg]     | S                         |
| 6.1.3.7  | Battery status                      | Public                           | String           | D                         |

Mentioned:  
" European standards on unique identifiers are developed and drafted in the framework of the standardisation request on the DPP-system. The work is
conducted in the CEN/CLC/JTC 24 “Digital Product Passport (DPP)”. "


### 2) Overview of battery passport data attributes for symbols, labels and documentation of conformity

| Clause | Data attribute                     | Data access                                           | Data type [Unit] | Static/Dynamic |
|--------|------------------------------------|------------------------------------------------------|------------------|-------------------------|
| 6.2.2  | Separate collection symbol         | Public                                              | Graphic          | S                       |
| 6.2.3  | Symbols for cadmium and lead       | Public                                              | Graphic          | S                       |
| 6.2.4  | Carbon footprint label             | Public                                              | Graphic          | S                       |
| 6.2.5  | Extinguishing agent                | Public                                              | String           | S                       |
| 6.2.6  | Meaning of labels and symbols      | Public                                              | String           | S                       |
| 6.2.7  | EU declaration of conformity       | Public                                              | PDF              | S                       |
| 6.2.8  | Results of test reports proving compliance | Persons with a legitimate interest, market surveillance authorities, the European Commission | PDF | S |

Mentioned:  
" To define the rules and specifications for the labelling and marking requirements, BattReg Article 13(10) states that the European Commission must adopt
implementing acts to establish harmonised specifications by 18 August 2025 "


### 3) Battery passport data attributes related to the battery carbon footprint

| Clause  | Data attribute | Data access                              | Data type [Unit] | Static/Dynamic |
|---------|----------------|------------------------------------------|------------------|-------------------------|
| 6.3.2   | Battery carbon footprint per Functional Unit | Public | [kgCO2e/kWh] | S |
| 6.3.3   | Contribution of raw material acquisition and pre-processing lifecycle stage | Public | [kgCO2e/kWh] | S |
| 6.3.4   | Contribution of main product production/manufacturing lifecycle stage | Public | [kgCO2e/kWh] | S |
| 6.3.5   | Contribution of distribution lifecycle stage | Public | [kgCO2e/kWh] | S |
| 6.3.6   | Contribution of end of life and recycling lifecycle stage | Public | [kgCO2e/kWh] | S |
| 6.3.7   | Carbon footprint performance class | Public | String | S |
| 6.3.8   | Web link to public carbon footprint study | Public | Link to PDF | S |
| 6.3.9   | General battery and manufacturer information | Public | See 6.1 and 6.2 | S |
| 6.3.10  | Absolute battery carbon footprint | Public | [tCO2e] | S |


### 4)  Mandatory and suggested supply chain due diligence information to be made available via the battery passport

| Clause | Data attribute | Data access | Data type [Unit] | Static/Dynamic |
|--------|----------------|-------------|------------------|-------------------------|
| 6.4.2  | Information of due diligence report in the Battery Passport | Public | PDF | S |
| 6.4.3  | Third-party assurances (e.g., certifications) of recognised schemes | Public | - | S |
| 6.4.4  | Supply chain indices | Public | - | S |


### 5)  Battery passport data attributes related to battery materials and composition

| Clause | Data attribute                                       | Data access                           | Data type [Unit] | Static/Dynamic |
|--------|------------------------------------------------------|---------------------------------------|------------------|-------------------------|
| 6.5.2  | Battery chemistry                                    | Public                                | String           | S                       |
| 6.5.3  | Critical raw materials                               | Public                                | String           | S                       |
| 6.5.4  | Materials used in cathode, anode, and electrolyte    | Persons with a legitimate interest and Commission    | String           | S                       |
| 6.5.5  | Hazardous substances                                 | Public                                | String           | S                       |
| 6.5.6  | Impact of substances on environment, human health, safety, persons | Public                                | String           | S                       |


### 6)  Circularity information — data attributes

| Clause  | Data attribute                                              | Data access                           | Data type        | Static/Dynamic |
|---------|-------------------------------------------------------------|---------------------------------------|------------------|---------------------------|
| 6.6.1.2 | Dismantling information: Manuals for the removal and the disassembly of the battery pack | Persons with a legitimate interest, European Commission | Link to PDF       | S                         |
| 6.6.1.3 | Part numbers for components                                  | Persons with a legitimate interest, European Commission | URL              | S                         |
| 6.6.1.4 | Postal address of sources for spare parts                    | Persons with a legitimate interest, European Commission | Text             | S                         |
| 6.6.1.4 | E-mail address of sources for spare parts                    | Persons with a legitimate interest, European Commission | Text             | S                         |
| 6.6.1.4  | Web address of sources for spare parts   | Persons with a legitimate interest, European Commission  | URL           | S                       |
| 6.6.1.5  | Safety measures                         | Persons with a legitimate interest, European Commission  | Link to PDF   | S 

Mentioned:  
" None of the data attributes are intended for the label. "


### 7)  Recycled and renewable content — data attributes

| Clause  | Data attribute                                      | Data access                          | Data type [Unit] | Static/Dynamic |
|---------|-----------------------------------------------------|--------------------------------------|------------------|-------------------------|
| 6.6.2.2 | Pre-consumer and post-consumer recycled cobalt, lithium, nickel, and lead share | Public                               | [%]              | S                       |
| 6.6.2.3 | Pre-consumer recycled nickel share                  | Public                               | [%]              | S                       |
| 6.6.2.4 | Pre-consumer recycled cobalt share                  | Public                               | [%]              | S                       |
| 6.6.2.5 | Pre-consumer recycled lithium share                 | Public                               | [%]              | S                       |
| 6.6.2.6 | Pre-consumer recycled lead share                    | Public                               | [%]              | S                       |
| 6.6.2.7 | Post-consumer recycled nickel share                 | Public                               | [%]              | S                       |
| 6.6.2.8 | Post-consumer recycled cobalt share                 | Public                               | [%]              | S                       |
| 6.6.2.9 | Post-consumer recycled lithium share                | Public                               | [%]              | S                       |
| 6.6.2.10| Post-consumer recycled lead share                   | Public                               | [%]              | S                       |
| 6.6.2.11| Renewable content share                             | Public                               | [%]              | S                       |


### 8)  Role of end-users in waste prevention and collection — data attributes

| Clause  | Data attribute                                                          | Data access                           | Data type [Unit] | Static/Dynamic |
|---------|------------------------------------------------------------------------|---------------------------------------|------------------|---------------------------|
| 6.6.3.2 | Information on the role of end-users in contributing to waste prevention | Public                                | Link to PDF      | S                         |
| 6.6.3.3 | Information on the role of end-users in contributing to the separate collection of waste batteries | Public                                | Link to PDF      | S                         |
| 6.6.3.4 | Information on battery collection, preparation for second life and treatment at end of life | Public                                | Link to PDF      | S                         |


### 9)  Data attributes with regard to battery capacity, energy and voltage

| Clause  | Data attribute                | Data access                       | Data type     | Static/Dynamic |
|---------|-------------------------------|-----------------------------------|---------------|-------------------------|
| 6.7.2.2 | Rated capacity                 | Public                            | Decimal [Ah]  | S                       |
| 6.7.2.3 | Remaining capacity             | Persons with a legitimate interest | Decimal [Ah]  | D                       |
| 6.7.2.4 | Capacity fade                  | Persons with a legitimate interest | Integer [%]   | S                       |
| 6.7.2.5 | Certified usable battery energy| Persons with a legitimate interest | Decimal [kWh] | S                       |
| 6.7.2.6 | Remaining usable battery energy| Persons with a legitimate interest | Decimal [kWh] | D                       |
| 6.7.2.7 | State of certified energy (SOCE)| Persons with a legitimate interest | Integer [%]   | D                       |
| 6.7.2.8 | State of charge (SoC)          | Persons with a legitimate interest | Integer [%]   | D                       |
| 6.7.2.9 | Minimum voltage                | Public                            | Decimal [V]   | S                       |
| 6.7.2.10| Maximum voltage                | Public                            | Decimal [V]   | S                       |
| 6.7.2.11| Nominal voltage                | Public                            | Decimal [V]   | S                       |


### 10)  Data attributes regarding power capability

| Clause   | Data attribute                                    | Data access                          | Data type  | Static/Dynamic |
|----------|--------------------------------------------------|--------------------------------------|------------|-------------------------|
| 6.7.3.2  | Original power capability                        | Public                               | Integer [W] | S                       |
| 6.7.3.3  | Remaining power capability                       | Persons with a legitimate interest   | Integer [W] | D                       |
| 6.7.3.4  | Power fade                                       | Persons with a legitimate interest   | Integer [%] | S                       |
| 6.7.3.5  | Maximum permitted battery power                  | Public                               | Integer [W] | S                       |
| 6.7.3.6  | Ratio between nominal battery power and battery energy | Persons with a legitimate interest | Decimal [W/Wh] | S                       |



### 11)  Data attributes regarding round trip energy efficiency

| Clause  | Data attribute                                      | Data access                          | Data type [Unit] | Static/Dynamic |
|---------|-----------------------------------------------------|--------------------------------------|------------------|-------------------------|
| 6.7.4.2 | Initial round trip energy efficiency                | Public                               | Integer [%]      | S                       |
| 6.7.4.3 | Round trip energy efficiency at 50 % of cycle-life  | Public                               | Integer [%]      | S                       |
| 6.7.4.4 | Remaining round trip energy efficiency              | Persons with a legitimate interest   | Integer [%]      | D                       |
| 6.7.4.5 | Energy round trip efficiency fade                   | Persons with a legitimate interest   | Integer [%]      | S                       |
| 6.7.4.6 | Initial self-discharge rate                         | Persons with a legitimate interest   | Decimal [%/month]| S                       |
| 6.7.4.7 | Current self-discharge rate                         | Persons with a legitimate interest   | Decimal [%/month]| D                       |
| 6.7.4.8 | Evolution of self-discharge rates                   | Persons with a legitimate interest   | Integer [%]      | D                       |

Mentioned:  
" Test methods and reference conditions of mandatory data attributes are subject to the ongoing standardization process at CEN/CENELEC relating to
standardization request M/579. "


### 12)  Data attributes regarding internal resistance and electrochemical impedance

| Clause  | Data attribute                                                | Data access                          | Data type [Unit] | Static/Dynamic (S or D) |
|---------|---------------------------------------------------------------|--------------------------------------|------------------|-------------------------|
| 6.7.5.2 | Initial internal resistance of battery cell and pack (module recommended) | Public                               | Integer [Ω]      | S                       |
| 6.7.5.3 | Internal resistance increase of pack (cell and module recommended) | Persons with a legitimate interest   | Integer [%]      | S                       |

Mentioned:  
" Test methods and reference conditions and specifications are subject to the ongoing standardization process at CEN/CENELEC relating to standardization
request M/579. "


### 13)  Data attributes regarding battery lifetime

| Clause  | Data attribute                                | Data access                           | Data type       | Static/Dynamic |
|---------|-----------------------------------------------|---------------------------------------|-----------------|----------------|
| 6.7.6.2 | Expected lifetime in calendar years           | Persons with a legitimate interest    | Decimal [years] | S              |
| 6.7.6.3 | Expected lifetime: Number of charge-discharge cycles | Public                                | Integer [-]     | S              |
| 6.7.6.4 | Number of full charging and discharging cycles | Persons with a legitimate interest    | Integer [-]     | D              |
| 6.7.6.5 | Cycle-life Reference test                     | Public                                | String [-]      | S              |
| 6.7.6.6 | C-rate of relevant cycle-life test            | Public                                | Decimal [A/Ah]  | S              |
| 6.7.6.7 | Energy throughput                             | Persons with a legitimate interest    | Decimal [kWh/k] | D              |
| 6.7.6.8 | Capacity throughput                           | Persons with a legitimate interest    | Decimal [Ah]    | D              |
| 6.7.6.9 | Capacity threshold for exhaustion             | Public                                | Integer [%]     | S              |

Mentioned:  
" None of the data attributes are intended for the label. "



### 14)  Data attributes regarding temperature conditions

| Clause  | Data attribute                                              | Data access                          | Data type     | Static/Dynamic |
|---------|-------------------------------------------------------------|--------------------------------------|---------------|----------------|
| 6.7.7.2 | Temperature information                                      | Persons with a legitimate interest  | [°C]          | D              |
| 6.7.7.3 | Temperature range idle state, lower boundary                | Public                               | Integer [°C]  | S              |
| 6.7.7.4 | Temperature range idle state, upper boundary                | Public                               | Integer [°C]  | S              |
| 6.7.7.5 | Time spent in extreme temperatures above boundary           | Persons with a legitimate interest   | Decimal [min] | D              |
| 6.7.7.6 | Time spent in extreme temperatures below boundary           | Persons with a legitimate interest   | Decimal [min] | D              |
| 6.7.7.7 | Time spent charging during extreme temperatures above boundary | Persons with a legitimate interest   | Decimal [min] | D              |
| 6.7.7.8 | Time spent charging during extreme temperatures below boundary | Persons with a legitimate interest   | Decimal [min] | D              |

Mentioned:  
" None of the data attributes are intended for the label. "  
" Test methods and reference conditions for all data points here are subject to the ongoing standardization process at CEN/CENELEC relating to
standardization request M/579. "


### 15)  Data attributes regarding negative events

| Clause  | Data attribute                     | Data access                        | Data type     | Static/Dynamic |
|---------|------------------------------------|------------------------------------|---------------|----------------|
| 6.7.8.2 | Number of deep discharge events    | Persons with a legitimate interest | Integer [-]   | D              |
| 6.7.8.3 | Number of overcharge events        | Persons with a legitimate interest | Integer [-]   | D              |
| 6.7.8.4 | Information on accidents           | Persons with a legitimate interest | Link to PDF [-] | D              |
