# Crude 1H NMR peak assignment report

> **WARNING: Unidentified significant peaks detected. Possible unknown byproducts.** Check 3.50 ppm (1.98H).

| Item | Value |
| --- | --- |
| Expected product | ethyl benzoate (`CCOC(=O)c1ccccc1`) |
| Reactants | benzoic acid (`OC(=O)c1ccccc1`), ethanol (`CCO`) |
| Deuterated solvent | CDCl3 |
| Integral normalisation | 1H = 1.010 raw integral units (fitted to the product signals) |
| Measured peaks | 10: product 5, reactant 2, solvent/impurity 2, unknown 1, ambiguous 0, minor unassigned 0 |

## 1. Product Assigned

| Observed (ppm) | Mult. | Integral (H) | Assignment | Predicted (ppm) | Predicted H | Deviation | Confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8.05 | d | 2.01 | ArH (C7,11) | 8.03 | 2 | 0.02 | High | also inside the predicted window of benzoic acid ArH (C5,9) (predicted 7.86 ppm); the integral leaves no area unaccounted for |
| 7.55 | t | 0.97 | ArH (C9) | 7.56 | 1 | 0.01 | High | also inside the predicted window of benzoic acid ArH (C7) (predicted 7.56 ppm), benzoic acid ArH (C6,8) (predicted 7.47 ppm); the integral leaves no area unaccounted for |
| 7.44 | t | 2.03 | ArH (C8,10) | 7.46 | 2 | 0.02 | High | also inside the predicted window of benzoic acid ArH (C7) (predicted 7.56 ppm), benzoic acid ArH (C6,8) (predicted 7.47 ppm); the integral leaves no area unaccounted for |
| 4.38 | q | 1.98 | CH2 (C2) | 4.38 | 2 | 0.00 | High | - |
| 1.39 | t | 3.01 | CH3 (C1) | 1.38 | 3 | 0.01 | High | - |

Atom numbering: `[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][cH:9][cH:10][cH:11]1`

## 2. Reactant Residual

### benzoic acid (`OC(=O)c1ccccc1`)

Not detected. Its predicted signals (ArH (C5,9) at 7.86 ppm, ArH (C7) at 7.56 ppm, ArH (C6,8) at 7.47 ppm) all coincide with peaks that are already assigned, so it cannot be excluded on shift alone. Those peaks carry no excess integral, so any residual amount is small.

### ethanol (`CCO`)

Detected at about **30 mol%** of the product (11% of the total integral). **Substantial unreacted starting material.**

| Observed (ppm) | Mult. | Integral (H) | Assignment | Predicted (ppm) | Predicted H | Deviation | Confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.72 | q | 0.60 | CH2 (C2) | 3.67 | 2 | 0.05 | High | - |
| 1.24 | t | 0.92 | CH3 (C1) | 1.19 | 3 | 0.05 | High | - |

## 3. Solvent / Water

| Observed (ppm) | Mult. | Integral (H) | Assignment | Reference (ppm) |
| --- | --- | --- | --- | --- |
| 7.26 | s | 0.21 | CHCl3 (residual CDCl3) | 7.26 |
| 1.56 | s | 0.42 | H2O (water in CDCl3) | 1.56 |

## 4. Unassigned / Unknowns

> **WARNING: Unidentified significant peaks detected. Possible unknown byproducts.** The signals below carry a significant integral (>= 0.5H) and are explained by neither the product, the reactants nor the solvent.

| Observed (ppm) | Mult. | Integral (H) | Raw integral | Hints |
| --- | --- | --- | --- | --- |
| **3.50** | s | **1.98** | 2 | shift is close to methanol (3.49, s) in CDCl3; if it was used, declare it under extra_solvents in targets.yaml and rerun |

## 5. Ambiguous (conflicts and overlaps)

None.

## Appendix: predicted signals

| Species | Signal | Predicted (ppm) | H | Search window (ppm) | Result |
| --- | --- | --- | --- | --- | --- |
| ethyl benzoate | ArH (C7,11) | 8.03 | 2 | +/-0.20 | assigned |
| ethyl benzoate | ArH (C9) | 7.56 | 1 | +/-0.20 | assigned |
| ethyl benzoate | ArH (C8,10) | 7.46 | 2 | +/-0.20 | assigned |
| ethyl benzoate | CH2 (C2) | 4.38 | 2 | +/-0.20 | assigned |
| ethyl benzoate | CH3 (C1) | 1.38 | 3 | +/-0.20 | assigned |
| benzoic acid | OH (O1) | 13.00 | 1 | +/-1.00 | exchangeable, not found |
| benzoic acid | ArH (C5,9) | 7.86 | 2 | +/-0.20 | unassigned |
| benzoic acid | ArH (C7) | 7.56 | 1 | +/-0.20 | unassigned |
| benzoic acid | ArH (C6,8) | 7.47 | 2 | +/-0.20 | unassigned |
| ethanol | CH2 (C2) | 3.67 | 2 | +/-0.20 | assigned |
| ethanol | OH (O3) | 3.45 | 1 | +/-1.00 | exchangeable, not found |
| ethanol | CH3 (C1) | 1.19 | 3 | +/-0.20 | assigned |

<sub>peakassign 0.1.0. Predicted shifts are estimates and the assignments are suggestions; they do not replace 2D NMR.</sub>
