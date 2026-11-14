# Crude 1H NMR peak assignment report

> No unexplained signal above 0.5H.

| Item | Value |
| --- | --- |
| Expected product | benzil (`O=C(C(=O)c1ccccc1)c1ccccc1`) |
| Reactants | benzoin (`OC(C(=O)c1ccccc1)c1ccccc1`) |
| Deuterated solvent | CDCl3 |
| Integral normalisation | 1H = 8.644 raw integral units (fitted to the product signals) |
| Measured peaks | 6: product 3, reactant 0, solvent/impurity 3, unknown 0, ambiguous 0, minor unassigned 0 |

## 1. Product Assigned

| Observed (ppm) | Mult. | Integral (H) | Assignment | Predicted (ppm) | Predicted H | Deviation | Confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8.01 | m | 3.95 | ArH (C6,10,12,16) | 7.97 | 4 | 0.04 | High | also inside the predicted window of benzoin ArH (C6,10) (predicted 7.90 ppm); the integral leaves no area unaccounted for |
| 7.69 | m | 2.00 | ArH (C8,14) | 7.56 | 2 | 0.13 | Medium | also inside the predicted window of benzoin ArH (C8) (predicted 7.56 ppm); the integral leaves no area unaccounted for |
| 7.54 | m | 4.05 | ArH (C7,9,13,15) | 7.56 | 4 | 0.02 | High | also inside the predicted window of benzoin ArH (C8) (predicted 7.56 ppm), benzoin ArH (C7,9) (predicted 7.38 ppm); the integral leaves no area unaccounted for |

Atom numbering: `[O:1]=[C:2]([C:3](=[O:4])[c:5]1[cH:6][cH:7][cH:8][cH:9][cH:10]1)[c:11]1[cH:12][cH:13][cH:14][cH:15][cH:16]1`

## 2. Reactant Residual

### benzoin (`OC(C(=O)c1ccccc1)c1ccccc1`)

Not detected. No matching peak near CH (C2) at 5.94 ppm.

## 3. Solvent / Water

| Observed (ppm) | Mult. | Integral (H) | Assignment | Reference (ppm) |
| --- | --- | --- | --- | --- |
| 7.28 | s | 0.31 | CHCl3 (residual CDCl3) | 7.26 |
| 2.19 | s | 0.61 | acetone | 2.17 |
| 1.60 | s | 0.66 | H2O (water in CDCl3) | 1.56 |

Declared solvent ethanol was not found in full (all of its signals must be present with integrals in the expected ratio).

Declared solvent acetic acid was not found in full (all of its signals must be present with integrals in the expected ratio).

## 4. Unassigned / Unknowns

None. Every peak with a significant integral is accounted for.

## 5. Ambiguous (conflicts and overlaps)

None.

## Appendix: predicted signals

| Species | Signal | Predicted (ppm) | H | Search window (ppm) | Result |
| --- | --- | --- | --- | --- | --- |
| benzil | ArH (C6,10,12,16) | 7.97 | 4 | +/-0.20 | assigned |
| benzil | ArH (C7,9,13,15) | 7.56 | 4 | +/-0.20 | assigned |
| benzil | ArH (C8,14) | 7.56 | 2 | +/-0.20 | assigned |
| benzoin | ArH (C6,10) | 7.90 | 2 | +/-0.20 | unassigned |
| benzoin | ArH (C8) | 7.56 | 1 | +/-0.20 | unassigned |
| benzoin | ArH (C7,9) | 7.38 | 2 | +/-0.20 | unassigned |
| benzoin | ArH (C12,16) | 7.33 | 2 | +/-0.20 | unassigned |
| benzoin | ArH (C14) | 7.30 | 1 | +/-0.20 | unassigned |
| benzoin | ArH (C13,15) | 7.29 | 2 | +/-0.20 | unassigned |
| benzoin | CH (C2) | 5.94 | 1 | +/-0.20 | unassigned |
| benzoin | OH (O1) | 4.60 | 1 | +/-1.00 | exchangeable, not found |

<sub>peakassign 0.1.0. Predicted shifts are estimates and the assignments are suggestions; they do not replace 2D NMR.</sub>
