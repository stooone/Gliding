# Gliding

Generates a weather report of my favorite airports for soaring.

## Requirements

  * python2
  * ```pip2.7 install metar```
  * You have to download https://www.aviationweather.gov/docs/metar/stations.txt before running.

## Input

**airports.csv**
```
 1B5;KHIE;7000;338
KAWO;KAWO;5000;228
EGPG;EGPH;3000;163
LFLG;LFLS;8000;126
LHHH;LHBP;3000;250
```
**Format:** airport name;nearest METAR station;minimum cloud base;prefered wind direction

## Output

```
 1B5: SO-SO (DAY, cloud base: 7500.0 / 7000, wind: 6.0@0 / 338)
KAWO: BAD   (NIGHT, cloud base: 10000000 / 5000, wind: 0.0@0.0 / 228)
EGPG: OK    (DAY, cloud base: 4100.0 / 3000, wind: 14.0@180.0 / 163)
LFLG: BAD   (DAY, cloud base: 4500.0 / 8000, wind: 10.0@250.0 / 126)
LHHH: OK    (DAY, cloud base: 10000000 / 3000, wind: 13.0@220.0 / 250)
```
  * **OK:** day, clouds are good, wind is perfect for ridge soaring
  * **WEAK:** day, clouds are good, the wind is from the good destiantion but a bit weak
  * **SO-SO:** day, clouds are good, the wind is from a bad direction, nice for pattern or thermaling
  * **BAD:** clouds are low or it's night
