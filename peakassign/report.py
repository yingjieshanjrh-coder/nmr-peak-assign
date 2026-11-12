"""Report rendering: Markdown for reading, JSON for scripts."""
import json

from . import __version__, impurities

ALERT = ("WARNING: Unidentified significant peaks detected. "
         "Possible unknown byproducts.")
STATUS_NOTE = {
    "excess": "integral exceeds the prediction by {left:.2f}H; another "
              "signal may lie underneath",
    "split": "integral only fits when summed with the neighbouring peak(s) "
             "(one signal reported as several peaks)",
    "labile": "exchangeable proton; shift and integral vary with "
              "concentration and water content",
}
SIMPLE = {"s", "d", "t", "q", "sep"}
SCALE_NOTE = {
    "product": "fitted to the product signals",
    "reference": "from the reference peak given in targets.yaml",
    "total": "rough estimate from the total area; no product signal matched",
}


def _signal(part):
    labels = " + ".join(part.labels)
    shifts = " / ".join(f"{s:.2f}" for s in part.predicted)
    return labels, shifts


def _notes(state, part):
    notes = []
    if part.status in STATUS_NOTE:
        notes.append(STATUS_NOTE[part.status].format(left=state.left_h))
    if state.also:
        notes.append("also inside the predicted window of "
                     + ", ".join(state.also)
                     + "; the integral leaves no area unaccounted for")
    return "; ".join(notes)


def _table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join(" --- " for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return out


def _assigned_rows(states, key):
    rows = []
    for state in states:
        for part in state.parts:
            if part.species != key:
                continue
            labels, shifts = _signal(part)
            rows.append([f"{state.ppm:.2f}", state.multiplicity or "-",
                         f"{part.h:.2f}", labels, shifts, f"{part.protons:g}",
                         f"{part.delta:.2f}", part.confidence,
                         _notes(state, part) or "-"])
    return rows


ASSIGNED_HEADER = ["Observed (ppm)", "Mult.", "Integral (H)", "Assignment",
                   "Predicted (ppm)", "Predicted H", "Deviation",
                   "Confidence", "Notes"]


def _unknown_hints(state, solvent):
    hints = list(state.hints)
    seen = state.multiplicity.strip().lower()
    near = []
    for name, shift, mult, lines in impurities.nearby_trace(solvent, state.ppm):
        if seen in SIMPLE and mult in SIMPLE and seen != mult:
            continue
        more = f", {lines} signals in total" if lines > 1 else ""
        near.append(f"{name} ({shift:.2f}, {mult}{more})")
    if near:
        hints.append(f"shift is close to {', '.join(near)} in {solvent}; if "
                     "it was used, declare it under extra_solvents in "
                     "targets.yaml and rerun")
    return "; ".join(hints) or "outside every predicted window"


def _ambiguous_text(state):
    if state.conflict:
        return "Conflict", state.conflict
    bits = []
    for part in state.parts:
        labels, shifts = _signal(part)
        if part.role == "solvent":
            bits.append(f"{part.name} ({shifts} ppm), about {part.h:.2f}H")
        else:
            bits.append(f"{part.name} {labels} (predicted {shifts} ppm), "
                        f"about {part.h:.2f}H")
    for item in state.overlaps:
        bits.append(f"{item['name']} was detected elsewhere and its "
                    f"{item['label']} (predicted {item['shift']:.2f} ppm) "
                    f"should add about {item['h']:.2f}H here")
    if not state.overlaps and len({p.species for p in state.parts}) < 2:
        bits += [f"also inside the window of {text}" for text in state.also]
    text = "; ".join(bits)
    if state.left_h:
        text += f"; a further {state.left_h:.2f}H is unexplained"
    return "Overlap", text


def _species_title(report):
    species = report.species
    code = f" (`{species.smiles}`)" if species.smiles and \
        species.smiles != species.name else ""
    return f"{species.name}{code}"


def _group_list(items):
    return ", ".join(f"{g.label} at {g.shift:.2f} ppm" for g in items)


def _reactant_block(report, result):
    lines = [f"### {_species_title(report)}", ""]
    groups = _group_list
    if report.status == "detected":
        level = f"Detected at about **{report.ratio * 100:.0f} mol%** of " \
                f"the product ({report.share * 100:.0f}% of the total " \
                "integral)."
        if report.alert:
            level += " **Substantial unreacted starting material.**"
        lines += [level, ""]
        lines += _table(ASSIGNED_HEADER,
                        _assigned_rows(result.peaks, report.species.key))
        if report.missing:
            lines += ["", f"Signals not found: {groups(report.missing)}. "
                          "The assignment is less certain for that reason."]
        if report.masked:
            lines += ["", f"Signals hidden under other peaks: "
                          f"{groups(report.masked)}; see section 5."]
    elif report.status == "doubtful":
        lines += ["A peak falls inside one of its predicted windows, but "
                  f"most of its signals ({groups(report.missing)}) are "
                  "absent. **Not assigned to this reactant**; the peak is "
                  "listed in section 4."]
    elif report.status == "masked":
        lines += [f"Not detected. Its predicted signals "
                  f"({groups(report.masked)}) all coincide with peaks that "
                  "are already assigned, so it cannot be excluded on shift "
                  "alone. Those peaks carry no excess integral, so any "
                  "residual amount is small."]
    else:
        text = "Not detected."
        if report.missing:
            text += f" No matching peak near {groups(report.missing)}."
        lines += [text]
    return lines + [""]


def _flagged(result):
    return ", ".join(f"{s.ppm:.2f} ppm ({s.left_h:.2f}H)"
                     for s in result.category("unknown") + result.hidden)


def to_markdown(result, title="Crude 1H NMR peak assignment report"):
    cfg = result.settings
    product = result.product
    unknown = result.category("unknown")
    counts = {name: len(result.category(name)) for name in
              ("product", "reactant", "solvent", "unknown", "ambiguous",
               "minor")}

    out = [f"# {title}", ""]
    if result.unknown_alert:
        out += [f"> **{ALERT}** Check {_flagged(result)}.", ""]
    else:
        out += [f"> No unexplained signal above {cfg.unknown_h:g}H.", ""]
    for text in result.warnings:
        out += [f"> Note: {text}", ""]

    reactants = ", ".join(_species_title(r) for r in result.reactants) \
        or "none"
    out += _table(["Item", "Value"], [
        ["Expected product", _species_title(product)],
        ["Reactants", reactants],
        ["Deuterated solvent", result.solvent or "-"],
        ["Integral normalisation",
         f"1H = {result.unit:.3f} raw integral units "
         f"({SCALE_NOTE[result.scale_source]})"],
        ["Measured peaks",
         f"{len(result.peaks)}: product {counts['product']}, reactant "
         f"{counts['reactant']}, solvent/impurity {counts['solvent']}, "
         f"unknown {counts['unknown']}, ambiguous {counts['ambiguous']}, "
         f"minor unassigned {counts['minor']}"],
    ])

    out += ["", "## 1. Product Assigned", ""]
    rows = _assigned_rows(result.category("product"), product.species.key)
    if rows:
        out += _table(ASSIGNED_HEADER, rows)
    else:
        out += ["No peak could be assigned to the product unambiguously."]
    if product.missing:
        lost = ", ".join(f"{g.label} (predicted {g.shift:.2f} ppm, "
                         f"{g.protons}H)" for g in product.missing)
        out += ["", f"**Product signals not found: {lost}.** Either the "
                    "structure is not what was expected, or the signal is "
                    "buried under another peak (see section 5)."]
    if product.species.atom_map:
        out += ["", f"Atom numbering: `{product.species.atom_map}`"]

    out += ["", "## 2. Reactant Residual", ""]
    if not result.reactants:
        out += ["No reactants were given.", ""]
    for report in result.reactants:
        out += _reactant_block(report, result)

    out += ["## 3. Solvent / Water", ""]
    rows = []
    for state in result.category("solvent"):
        for part in state.parts:
            _, shifts = _signal(part)
            rows.append([f"{state.ppm:.2f}", state.multiplicity or "-",
                         f"{part.h:.2f}", part.name, shifts])
    if rows:
        out += _table(["Observed (ppm)", "Mult.", "Integral (H)",
                       "Assignment", "Reference (ppm)"], rows)
    else:
        out += ["No solvent or water signal recognised."]
    for report in result.impurities:
        if report.status != "detected":
            out += ["", f"Declared solvent {report.species.name} was not "
                        "found in full (all of its signals must be present "
                        "with integrals in the expected ratio)."]

    out += ["", "## 4. Unassigned / Unknowns", ""]
    if result.unknown_alert:
        out += [f"> **{ALERT}** The signals below carry a significant "
                f"integral (>= {cfg.unknown_h:g}H) and are explained by "
                "neither the product, the reactants nor the solvent.", ""]
        if unknown:
            out += _table(
                ["Observed (ppm)", "Mult.", "Integral (H)", "Raw integral",
                 "Hints"],
                [[f"**{s.ppm:.2f}**", s.multiplicity or "-", f"**{s.h:.2f}**",
                  f"{s.integral:g}", _unknown_hints(s, result.solvent)]
                 for s in unknown])
        if result.hidden:
            out += ["", "Excess area under peaks that are otherwise "
                        "assigned:", ""]
            out += _table(
                ["Observed (ppm)", "Total (H)", "Explained (H)",
                 "Excess (H)"],
                [[f"{s.ppm:.2f}", f"{s.h:.2f}", f"{s.h - s.left_h:.2f}",
                  f"**{s.left_h:.2f}**"] for s in result.hidden])
    else:
        out += ["None. Every peak with a significant integral is accounted "
                "for."]
    minor = result.category("minor")
    if minor:
        out += ["", f"Minor unassigned peaks below {cfg.unknown_h:g}H (no "
                    "warning raised): "
                + ", ".join(f"{s.ppm:.2f} ppm ({s.h:.2f}H)" for s in minor)
                + "."]

    out += ["", "## 5. Ambiguous (conflicts and overlaps)", ""]
    ambiguous = result.category("ambiguous")
    if ambiguous:
        rows = []
        for state in ambiguous:
            kind, text = _ambiguous_text(state)
            rows.append([f"{state.ppm:.2f}", state.multiplicity or "-",
                         f"{state.h:.2f}", kind, text])
        out += _table(["Observed (ppm)", "Mult.", "Integral (H)", "Type",
                       "Explanation"], rows)
    else:
        out += ["None."]

    out += ["", "## Appendix: predicted signals", ""]
    rows = []
    for report in [product] + result.reactants:
        hit = {id(g) for g in report.matched}
        for group in report.species.groups:
            state = "assigned" if id(group) in hit else \
                ("exchangeable, not found" if group.labile else "unassigned")
            window = max(group.window, cfg.labile_window) if group.labile \
                else group.window
            rows.append([report.species.name, group.label,
                         f"{group.shift:.2f}", group.protons,
                         f"+/-{window:.2f}", state])
    out += _table(["Species", "Signal", "Predicted (ppm)", "H",
                   "Search window (ppm)", "Result"], rows)
    out += ["", f"<sub>peakassign {__version__}. Predicted shifts are "
                "estimates and the assignments are suggestions; they do not "
                "replace 2D NMR.</sub>", ""]
    return "\n".join(out)


def to_dict(result):
    def group(g):
        return {"label": g.label, "shift": g.shift, "protons": g.protons,
                "window": g.window, "labile": g.labile}

    def species(report):
        return {
            "name": report.species.name, "smiles": report.species.smiles,
            "status": report.status, "molar_ratio": report.ratio,
            "integral_h": round(report.h, 3),
            "integral_share": round(report.share, 4), "alert": report.alert,
            "matched": [group(g) for g in report.matched],
            "missing": [group(g) for g in report.missing],
            "masked": [group(g) for g in report.masked],
        }

    peaks = []
    for s in result.peaks:
        peaks.append({
            "ppm": s.ppm, "integral": s.integral, "h": round(s.h, 3),
            "multiplicity": s.multiplicity, "category": s.category,
            "unexplained_h": round(s.left_h, 3),
            "assignments": [{
                "species": p.name, "role": p.role, "signals": p.labels,
                "predicted_ppm": p.predicted, "predicted_h": p.protons,
                "integral_h": round(p.h, 3), "status": p.status,
                "delta": round(p.delta, 3), "confidence": p.confidence,
            } for p in s.parts],
            "overlaps": s.overlaps, "also_in_window": s.also,
            "hints": s.hints, "conflict": s.conflict,
        })
    return {
        "tool": f"peakassign {__version__}",
        "solvent": result.solvent,
        "normalisation": {"raw_integral_per_h": result.unit,
                          "source": result.scale_source},
        "unknown_alert": result.unknown_alert,
        "unknown": [{"ppm": s.ppm, "h": round(s.left_h, 3)}
                    for s in result.category("unknown") + result.hidden],
        "product": species(result.product),
        "reactants": [species(r) for r in result.reactants],
        "declared_impurities": [species(r) for r in result.impurities],
        "peaks": peaks,
        "warnings": result.warnings,
    }


def to_json(result):
    return json.dumps(to_dict(result), ensure_ascii=False, indent=2) + "\n"


CATEGORY_NAME = {
    "product": "Product", "reactant": "Reactant Residual",
    "solvent": "Solvent/Impurity", "unknown": "UNKNOWN !!",
    "ambiguous": "Ambiguous", "minor": "Minor",
}


def to_text(result):
    """Short summary for the terminal."""
    lines = []
    for state in result.peaks:
        who = "; ".join(p.name if p.role == "solvent"
                        else f"{p.name} {' + '.join(p.labels)}"
                        for p in state.parts)
        lines.append(f"{state.ppm:7.2f}  {state.h:5.2f}H  "
                     f"{CATEGORY_NAME[state.category]:<17}  {who}".rstrip())
    for report in result.reactants:
        if report.status == "detected":
            flag = " (substantial unreacted starting material)" \
                if report.alert else ""
            lines.append(f"{report.species.name}: about "
                         f"{report.ratio * 100:.0f} mol% of the product{flag}")
    if result.unknown_alert:
        lines.append(f"{ALERT} Check {_flagged(result)}.")
    else:
        lines.append("No significant unexplained signal.")
    return "\n".join(lines)
