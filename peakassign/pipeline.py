"""From the two input files to a classified peak list."""
from . import impurities
from .assign import Group, Settings, Species, analyse


def trace_species(name, solvent):
    """A declared lab solvent as a species, or as loose lines if it has no
    fixed proton ratio (grease, TMS)."""
    lines = impurities.trace_lines(name, solvent)
    if any(protons is None for _, _, protons in lines):
        return None, [{"name": name, "kind": "trace", "ppm": ppm,
                       "window": impurities.TRACE_WINDOW}
                      for ppm, _, _ in lines]
    groups = [Group(label=f"{mult}, {protons}H", shift=ppm, protons=protons,
                    window=impurities.TRACE_WINDOW,
                    tight=impurities.TRACE_WINDOW)
              for ppm, mult, protons in lines]
    return Species(key=f"trace:{name}", role="impurity", name=name,
                   groups=groups), []


def run(targets, peaks, index=None, cfg=None, tol=0.08, predict=None):
    """Classify `peaks` for the species in `targets`.

    `predict` defaults to the nmrcheck-based predictor; tests pass their own
    so the assignment logic can be checked without RDKit or the index.
    """
    if predict is None:
        from .predictor import build_species as predict
    cfg = cfg or Settings()
    product = predict(targets.product.smiles, "product", "product",
                      targets.product.name, index, tol)
    reactants = [predict(r.smiles, f"reactant{i}", "reactant", r.name,
                         index, tol)
                 for i, r in enumerate(targets.reactants, start=1)]

    lines = impurities.solvent_lines(targets.solvent)
    extra = []
    for name in targets.extra_solvents:
        species, loose = trace_species(name, targets.solvent)
        if species:
            extra.append(species)
        lines += loose
    for item in targets.extra_peaks:
        lines.append({"name": item["name"], "kind": "trace",
                      "ppm": item["ppm"], "window": impurities.TRACE_WINDOW})

    result = analyse(peaks, product, reactants, lines=lines, impurities=extra,
                     cfg=cfg, reference=targets.reference,
                     solvent=targets.solvent)
    if index is None:
        result.warnings.append(
            "The nmrcheck shift index (index.sqlite) was not found, so "
            "predicted shifts fall back to fixed atom-type values with very "
            "wide search windows; treat the assignments as indicative only. "
            "Run `nmrcheck build` in nmr-novelty-check, or point --data-dir "
            "at the folder that holds the index.")
    weak = [g for s in [product] + reactants for g in s.groups
            if g.radius < 2 and not g.labile]
    if weak and index is not None:
        result.warnings.append(
            f"{len(weak)} predicted signal(s) rest on a small atom "
            "environment (radius < 2 bonds). Their search windows were "
            "widened accordingly, so check those assignments with care.")
    return result
