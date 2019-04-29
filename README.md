# Gliding

Generates a weather report of my favorite airports for soaring.

## Requirements

  * python2
  * ```pip2.7 install metar```

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
 1B5: BAD   (DAY, cloud base: 6000 / 7000, wind: 6@0 / 338, KHIE 261252Z AUTO VRB06G17KT 10SM -RA OVC060 09/04 A2984 RMK AO2 SLP113 P0001 T00890044)
KAWO: SO-SO (DAY, cloud base: 10000000 / 5000, wind: 0@0 / 228, KAWO 261316Z AUTO 00000KT 3SM BR CLR 04/03 A3013 RMK AO2 $)
EGPG: BAD   (DAY, cloud base: 2800 / 3000, wind: 13@170 / 163, EGPH 261320Z 17013KT 9999 -RA SCT028 BKN040 13/08 Q1000)
LFLG: BAD   (DAY, cloud base: 4600 / 8000, wind: 10@270 / 126, LFLS 261300Z AUTO 27010KT 9999 FEW046/// BKN088/// BKN120/// ///CB 13/04 Q1017 TEMPO VRB15G25KT 4500 TSRA)
LHHH: SO-SO (DAY, cloud base: 10000000 / 3000, wind: 11@200 / 250, LHBP 261330Z 20011KT 150V230 9999 VCBLDU NSC 28/08 Q1012 NOSIG)
```
  * **OK:** day, clouds are good, wind is perfect for ridge soaring
  * **WEAK:** day, clouds are good, the wind is from the good destiantion but a bit weak
  * **SO-SO:** day, clouds are good, the wind is from a bad direction, nice for pattern or thermaling
  * **BAD:** clouds are low or it's night
