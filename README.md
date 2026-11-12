# nmr-peak-assign

Hypothesis-driven assignment of crude ¹H NMR spectra using chemical-shift and
integral cross-validation.

## Overview

A crude reaction mixture gives a ¹H NMR spectrum in which product signals sit
next to unreacted starting materials, residual solvent, water and, sometimes,
byproducts nobody planned for. `peakassign` takes what the chemist already
knows (the expected product, the reactants and the NMR solvent) together with
a peak list that includes integrals, and sorts every peak into one of five
classes:

1. signals of the product,
2. signals of unreacted starting material,
3. solvent, water and declared impurities,
4. **signals that none of the above can explain**,
5. peaks where two candidates overlap or where shift and integral disagree.

The tool does not propose structures for unknown compounds. It works by
elimination: every candidate species claims the area it can account for, and
whatever is left over is reported, prominently if the integral is large.

```
$ python -m peakassign examples/ethyl_benzoate/targets.yaml examples/ethyl_benzoate/measured_peaks.csv
   8.05   2.01H  Product            ethyl benzoate ArH (C7,11)
   7.55   0.97H  Product            ethyl benzoate ArH (C9)
   7.44   2.03H  Product            ethyl benzoate ArH (C8,10)
   7.26   0.21H  Solvent/Impurity   CHCl3 (residual CDCl3)
   4.38   1.98H  Product            ethyl benzoate CH2 (C2)
   3.72   0.60H  Reactant Residual  ethanol CH2 (C2)
   3.50   1.98H  UNKNOWN !!
   1.56   0.42H  Solvent/Impurity   H2O (water in CDCl3)
   1.39   3.01H  Product            ethyl benzoate CH3 (C1)
   1.24   0.92H  Reactant Residual  ethanol CH3 (C1)
ethanol: about 30 mol% of the product (substantial unreacted starting material)
WARNING: Unidentified significant peaks detected. Possible unknown byproducts. Check 3.50 ppm (1.98H).
report: examples/ethyl_benzoate/report.md
```

The full report for this run is in
[examples/ethyl_benzoate/report.md](examples/ethyl_benzoate/report.md).

## Features

- **Hypothesis-driven.** All candidate structures come from the user. The
  tool tests those hypotheses against the spectrum; it never invents a
  structure.
- **Shift and integral cross-validation.** A peak is assigned to a predicted
  signal only if the chemical shift lies inside the search window *and* the
  integral agrees with the number of nuclei.
- **Automatic integral normalisation.** No reference peak has to be chosen.
- **Quantified reactant residue.** Each unreacted starting material is
  reported with its molar ratio to the product.
- **Unknown-signal warning.** Unexplained peaks above a configurable
  integral threshold raise a warning at the top of the report.
- **Explicit ambiguity.** Overlaps and shift/integral conflicts are listed
  separately instead of being resolved silently.
- **Built-in solvent data.** Residual solvent and water signals for eight
  deuterated solvents; common laboratory solvents for CDCl₃ and DMSO-d₆.
- **Markdown and JSON output.**

## Method

### Hypothesis-driven assignment using ppm and integral cross-validation

Predicted ¹H shifts carry an error of 0.1–0.3 ppm, and the signals of a
product, its precursors and their homologues often fall inside the same
window. Shift alone therefore cannot separate them. The integral is an
independent observable, and `peakassign` uses it in four places.

**1. Normalisation by product fit.** The scale that converts raw integrals
into proton counts is the one for which the largest number of predicted
product protons are matched by peaks of the right integral. Every ratio
suggested by a peak/signal pair is tried. A product peak with an impurity
underneath does not distort the scale, because the remaining product peaks
fix it. A reference peak can be set by hand if needed.

**2. Nuclei-count check.** A peak can be assigned to a predicted CH₃ only if
it integrates to about 3H (tolerance: 15 % of the expected value plus 0.1H).
A peak that integrates too low is never accepted for that signal; it is
reported as a conflict ("shift fits, integral does not"). A peak that
integrates too high is assigned, and the excess is reported as area that
still needs an explanation.

**3. Internal consistency of each reactant.** A leftover reactant has its own
concentration, so its integrals cannot be compared with proton counts on the
product scale. Instead one molar ratio is fitted per reactant, and its
signals must agree with each other in proportion to their proton counts. In
the example, ethanol shows CH₂ at 0.60H and CH₃ at 0.92H, a 2 : 3 ratio,
which identifies it at about 30 mol % of the product. The 2.0H peak at
3.50 ppm lies inside the predicted window of the ethanol CH₂ as well, but
its integral does not fit that ratio, so it is not absorbed.

**4. Coverage requirement.** A reactant counts as detected only if at least
60 % of its observable signals are found. A single peak that happens to fall
inside one window of a reactant, while the rest of that reactant is absent,
stays unassigned and the report says why.

Each predicted signal is used at most once and the product is fitted first.
The assignment is a global optimisation over all peaks and signals of a
species, not a nearest-neighbour match; one multiplet may hold up to three
neighbouring predicted signals, and one signal reported as two or three
adjacent peaks is recombined.

### Elimination

1. The product claims the area it can explain.
2. Residual solvent and water are removed.
3. Declared laboratory solvents and each reactant claim what is internally
   consistent.
4. The area nobody claimed is reported.

For an unexplained peak the report gives at most one non-committal hint: if
its shift coincides with a tabulated laboratory solvent (for example
methanol at 3.49 ppm in CDCl₃), that is mentioned so the user can decide
whether to declare the solvent and rerun. Solvents with several signals
(ethyl acetate, diethyl ether, ...) are accepted only if all signals are
present with integrals in the expected ratio.

### Overlap between product and reactant windows

A product peak that also lies inside the predicted window of a reactant is
common (the aromatic protons of ethyl benzoate and benzoic acid, for
instance). Three cases are distinguished:

- the reactant has been detected through other signals: its expected
  contribution here follows from its molar ratio, and the peak is listed as
  ambiguous;
- the peak integrates higher than the product requires and the reactant
  accounts for the excess: listed as ambiguous, with the split;
- the reactant is not detected and the integral equals the product's proton
  count: the peak stays with the product and a note names the overlapping
  window. `--strict-overlap` moves these peaks to the ambiguous class too.

### Search windows

Shifts are predicted by the atom-environment look-up of
[nmr-novelty-check](https://github.com/yingjieshanjrh-coder/nmr-novelty-check),
which is more accurate the larger the matched environment. Its hold-out mean
absolute error for ¹H ranges from 0.14 ppm (environment radius of 4 bonds)
to 0.63 ppm (radius 1). The search window is therefore `--tol` plus a
radius-dependent allowance: ±0.20 ppm at radius 4, ±0.28 ppm at radius 3,
and wider below that. The integral checks described above keep the wider
windows from producing false assignments. The window used for every
predicted signal is listed in the appendix of the report.

## Installation

Python 3.10 or newer. Shift prediction and the shift index come from the
`nmrcheck` package of nmr-novelty-check, which must be installed in the same
environment with its index built. The two projects live in separate folders.

```
git clone https://github.com/yingjieshanjrh-coder/nmr-novelty-check
cd nmr-novelty-check
pip install -e .
nmrcheck build              # skip if the index already exists
cd ..

git clone https://github.com/yingjieshanjrh-coder/nmr-peak-assign
cd nmr-peak-assign
pip install -e .            # adds only pyyaml
```

The index is looked for in the `data/` folder of the installed
nmr-novelty-check. If it is kept elsewhere, set the environment variable
`NMRCHECK_DATA` or pass `--data-dir`. Without an index the tool still runs,
but predicted shifts fall back to fixed atom-type values and the report says
so.

## Quick Start

```
python -m peakassign examples/ethyl_benzoate/targets.yaml examples/ethyl_benzoate/measured_peaks.csv
```

This prints the summary shown above and writes `report.md` next to the peak
list.

```
python -m peakassign targets.yaml measured_peaks.csv [-o report.md] [--json report.json]
```

| Option | Default | Meaning |
| --- | --- | --- |
| `--tol` | 0.08 | Shift deviation (ppm) for a confident match; the search window adds the predictor's uncertainty |
| `--unknown-threshold` | 0.5 | Unexplained integral (H) that raises the warning |
| `--residual-alert` | 0.20 | Reactant : product molar ratio reported as substantial |
| `--strict-overlap` | off | List every product peak inside a reactant window as ambiguous |
| `--data-dir` | auto | Folder holding `index.sqlite` |

## Input Format

`targets.yaml` holds the hypotheses.

```yaml
product:
  smiles: CCOC(=O)c1ccccc1
  name: ethyl benzoate          # optional; `product: CCOC(=O)c1ccccc1` also works
reactants:
  - smiles: OC(=O)c1ccccc1
    name: benzoic acid
  - smiles: CCO
    name: ethanol
solvent: CDCl3                  # CDCl3, DMSO-d6, CD3OD, D2O, acetone-d6, CD3CN, C6D6, CD2Cl2

# optional
extra_solvents: [EtOAc, hexane]        # work-up solvents that may remain
extra_peaks:                           # known impurities not in the table
  - {name: BHT, ppm: 5.01}
reference: {ppm: 4.38, protons: 2}     # fix the integral scale by hand
```

`measured_peaks.csv` is the peak list exported from the spectrometer
software. Integrals are raw relative areas; they do not need to be
normalised. The `multiplicity` column is optional.

```csv
ppm,integral,multiplicity
8.05,2.03,d
7.55,0.98,t
...
```

## Output Classification

| Class | Meaning |
| --- | --- |
| 1. Product Assigned | Shift and integral both agree with a predicted product signal. Listed with the suggested atom assignment and a confidence level (High / Medium) |
| 2. Reactant Residual | Peaks matched to a reactant, with its molar ratio to the product; flagged as substantial above 20 mol % |
| 3. Solvent / Water | Residual solvent, water, and solvents declared under `extra_solvents` |
| 4. Unassigned / Unknowns | Peaks of at least 0.5H that no candidate explains. Raises the warning at the top of the report |
| 5. Ambiguous | Two species under one peak, or a shift that fits the product with an integral that does not |

Unassigned peaks below 0.5H (¹³C satellites, trace impurities) are listed on
one line and do not raise the warning.

Confidence is High when the integral fits, the deviation is within the tight
tolerance and the prediction rests on an environment of at least three
bonds; otherwise Medium. Exchangeable protons are never rated above Medium.

The JSON output (`--json`) contains the same information per peak, including
the share of the integral attributed to each species.

## Limitations

- Predicted shifts are estimates and assignments are suggestions. When a
  prediction is off by more than its window, the real product peak is
  reported as unknown and, at the same time, a product signal with the same
  proton count is reported as not found; reading the two together reveals
  the cause.
- Exchangeable protons (OH, NH) move with concentration and water content.
  They are matched loosely.
- Multiplicity is not predicted. The `multiplicity` column is used only to
  require a singlet or broad peak for water and to discard hints that
  clearly do not fit.
- ¹H only.
- The trace-solvent table (after Fulmer et al., *Organometallics* 2010, 29,
  2176) covers CDCl₃ and DMSO-d₆. For the other solvents only the residual
  and water signals are built in; further impurities can be supplied with
  `extra_peaks`.
- Two candidates whose signals coincide and whose integrals are both
  plausible cannot be separated; such peaks are flagged, not resolved.
- The example data set is synthetic. The tool has not been benchmarked on a
  collection of experimental crude spectra.

## Tests

```
pip install pytest
pytest
```

The tests of the assignment logic use hand-written predictions and need
neither RDKit nor the index. `tests/test_end_to_end.py` runs the ethyl
benzoate example through the real predictor and is skipped when no index is
available.

The example peak list is synthetic: the five signals of ethyl benzoate,
0.3 equivalents of residual ethanol, the CHCl₃ and water signals, and one
unrelated peak at 3.50 ppm with 2.0H.

## Relation to nmr-novelty-check

`peakassign` imports the following from `nmrcheck` and treats that project
as read-only:

- `nmrcheck.predict.predict`: predicted ¹H shifts and proton counts per
  signal;
- `nmrcheck.index.Index`: read-only access to `index.sqlite`;
- `nmrcheck.chem.parse_smiles`: SMILES parsing;
- `nmrcheck.solvents`: deuterated-solvent aliases and residual shifts.

Reading the inputs, the water and trace-solvent tables, the integral-aware
assignment and the report are implemented here.

## License

MIT
