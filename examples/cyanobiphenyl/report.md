# Crude 1H NMR peak assignment report

> No unexplained signal above 0.5H.

| Item | Value |
| --- | --- |
| Expected product | 4-cyanobiphenyl (`N#Cc1ccc(cc1)-c1ccccc1`) |
| Reactants | phenylboronic acid (`OB(O)c1ccccc1`), 4-bromobenzonitrile (`N#Cc1ccc(Br)cc1`) |
| Deuterated solvent | CDCl3 |
| Integral normalisation | 1H = 8.853 raw integral units (fitted to the product signals) |
| Measured peaks | 5: product 2, reactant 1, solvent/impurity 1, unknown 0, ambiguous 1, minor unassigned 0 |

## 1. Product Assigned

| Observed (ppm) | Mult. | Integral (H) | Assignment | Predicted (ppm) | Predicted H | Deviation | Confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7.62 | m | 1.95 | ArH (C10,14) | 7.62 | 2 | 0.00 | High | also inside the predicted window of 4-bromobenzonitrile ArH (C5,8) (predicted 7.62 ppm), 4-bromobenzonitrile ArH (C4,9) (predicted 7.54 ppm); the integral leaves no area unaccounted for |
| 7.49 | m | 3.00 | ArH (C12) + ArH (C11,13) | 7.42 / 7.44 | 3 | 0.07 | High | also inside the predicted window of 4-bromobenzonitrile ArH (C5,8) (predicted 7.62 ppm), 4-bromobenzonitrile ArH (C4,9) (predicted 7.54 ppm); the integral leaves no area unaccounted for |

Atom numbering: `[N:1]#[C:2][c:3]1[cH:4][cH:5][c:6](-[c:9]2[cH:10][cH:11][cH:12][cH:13][cH:14]2)[cH:7][cH:8]1`

## 2. Reactant Residual

### phenylboronic acid (`OB(O)c1ccccc1`)

Detected at about **12 mol%** of the product (3% of the total integral).

| Observed (ppm) | Mult. | Integral (H) | Assignment | Predicted (ppm) | Predicted H | Deviation | Confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7.29 | s | 0.36 | ArH (C7) + ArH (C6,8) | 7.35 / 7.37 | 3 | 0.08 | Medium | - |

Signals hidden under other peaks: ArH (C5,9) at 7.77 ppm; see section 5.

### 4-bromobenzonitrile (`N#Cc1ccc(Br)cc1`)

Not detected. Its predicted signals (ArH (C5,8) at 7.62 ppm, ArH (C4,9) at 7.54 ppm) all coincide with peaks that are already assigned, so it cannot be excluded on shift alone. Those peaks carry no excess integral, so any residual amount is small.

## 3. Solvent / Water

| Observed (ppm) | Mult. | Integral (H) | Assignment | Reference (ppm) |
| --- | --- | --- | --- | --- |
| 2.20 | s | 1.98 | acetone | 2.17 |

Declared solvent ethanol was not found in full (all of its signals must be present with integrals in the expected ratio).

Declared solvent ethyl acetate was not found in full (all of its signals must be present with integrals in the expected ratio).

## 4. Unassigned / Unknowns

None. Every peak with a significant integral is accounted for.

## 5. Ambiguous (conflicts and overlaps)

| Observed (ppm) | Mult. | Integral (H) | Type | Explanation |
| --- | --- | --- | --- | --- |
| 7.74 | m | 4.00 | Overlap | 4-cyanobiphenyl ArH (C5,7) + ArH (C4,8) (predicted 7.65 / 7.69 ppm), about 4.00H; phenylboronic acid was detected elsewhere and its ArH (C5,9) (predicted 7.77 ppm) should add about 0.24H here |

## Appendix: predicted signals

| Species | Signal | Predicted (ppm) | H | Search window (ppm) | Result |
| --- | --- | --- | --- | --- | --- |
| 4-cyanobiphenyl | ArH (C4,8) | 7.69 | 2 | +/-0.20 | assigned |
| 4-cyanobiphenyl | ArH (C5,7) | 7.65 | 2 | +/-0.20 | assigned |
| 4-cyanobiphenyl | ArH (C10,14) | 7.62 | 2 | +/-0.20 | assigned |
| 4-cyanobiphenyl | ArH (C11,13) | 7.44 | 2 | +/-0.20 | assigned |
| 4-cyanobiphenyl | ArH (C12) | 7.42 | 1 | +/-0.20 | assigned |
| phenylboronic acid | ArH (C5,9) | 7.77 | 2 | +/-0.38 | unassigned |
| phenylboronic acid | ArH (C6,8) | 7.37 | 2 | +/-0.38 | assigned |
| phenylboronic acid | ArH (C7) | 7.35 | 1 | +/-0.28 | assigned |
| phenylboronic acid | OH (O1,3) | 7.01 | 2 | +/-1.00 | exchangeable, not found |
| 4-bromobenzonitrile | ArH (C5,8) | 7.62 | 2 | +/-0.20 | unassigned |
| 4-bromobenzonitrile | ArH (C4,9) | 7.54 | 2 | +/-0.20 | unassigned |

<sub>peakassign 0.1.0. Predicted shifts are estimates and the assignments are suggestions; they do not replace 2D NMR.</sub>
