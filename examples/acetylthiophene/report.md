# Crude 1H NMR peak assignment report

> No unexplained signal above 0.5H.

| Item | Value |
| --- | --- |
| Expected product | 2-acetylthiophene (`CC(=O)c1cccs1`) |
| Reactants | thiophene (`c1ccsc1`), acetic anhydride (`CC(=O)OC(C)=O`) |
| Deuterated solvent | CDCl3 |
| Integral normalisation | 1H = 16.400 raw integral units (fitted to the product signals) |
| Measured peaks | 5: product 4, reactant 0, solvent/impurity 0, unknown 0, ambiguous 0, minor unassigned 1 |

## 1. Product Assigned

| Observed (ppm) | Mult. | Integral (H) | Assignment | Predicted (ppm) | Predicted H | Deviation | Confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7.68 | dd | 1.00 | ArH (C7) | 7.79 | 1 | 0.11 | High | - |
| 7.62 | dd | 0.97 | ArH (C5) | 7.78 | 1 | 0.17 | Medium | - |
| 7.11 | dd | 0.98 | ArH (C6) | 7.15 | 1 | 0.04 | High | also inside the predicted window of thiophene ArH (C3,5) (predicted 7.10 ppm); the integral leaves no area unaccounted for |
| 2.54 | s | 3.01 | CH3 (C1) | 2.51 | 3 | 0.03 | High | - |

Atom numbering: `[CH3:1][C:2](=[O:3])[c:4]1[cH:5][cH:6][cH:7][s:8]1`

## 2. Reactant Residual

### thiophene (`c1ccsc1`)

Not detected. No matching peak near ArH (C1,2) at 6.90 ppm.

### acetic anhydride (`CC(=O)OC(C)=O`)

Not detected. No matching peak near CH3 (C1,6) at 3.13 ppm.

## 3. Solvent / Water

No solvent or water signal recognised.

Declared solvent acetic acid was not found in full (all of its signals must be present with integrals in the expected ratio).

Declared solvent ethyl acetate was not found in full (all of its signals must be present with integrals in the expected ratio).

## 4. Unassigned / Unknowns

None. Every peak with a significant integral is accounted for.

Minor unassigned peaks below 0.5H (no warning raised): 2.06 ppm (0.13H).

## 5. Ambiguous (conflicts and overlaps)

None.

## Appendix: predicted signals

| Species | Signal | Predicted (ppm) | H | Search window (ppm) | Result |
| --- | --- | --- | --- | --- | --- |
| 2-acetylthiophene | ArH (C7) | 7.79 | 1 | +/-0.28 | assigned |
| 2-acetylthiophene | ArH (C5) | 7.78 | 1 | +/-0.38 | assigned |
| 2-acetylthiophene | ArH (C6) | 7.15 | 1 | +/-0.28 | assigned |
| 2-acetylthiophene | CH3 (C1) | 2.51 | 3 | +/-0.28 | assigned |
| thiophene | ArH (C3,5) | 7.10 | 2 | +/-0.20 | unassigned |
| thiophene | ArH (C1,2) | 6.90 | 2 | +/-0.20 | unassigned |
| acetic anhydride | CH3 (C1,6) | 3.13 | 6 | +/-0.28 | unassigned |

<sub>peakassign 0.1.0. Predicted shifts are estimates and the assignments are suggestions; they do not replace 2D NMR.</sub>
