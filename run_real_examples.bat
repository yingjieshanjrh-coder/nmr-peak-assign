@echo off
rem Runs the three experimental examples and writes report.md / report.json next to each peak list.
for %%d in (acetylthiophene cyanobiphenyl benzil) do (
  echo ==== %%d ====
  python -m peakassign examples\%%d\targets.yaml examples\%%d\measured_peaks.csv -o examples\%%d\report.md --json examples\%%d\report.json
)
pause
