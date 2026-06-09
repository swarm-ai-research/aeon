import subprocess, os
RUN = 'out/programmatic-eda/compute-futures-2026-06-08'
INP = f'{RUN}/sweep_dedup.csv'
steps = [
    (['python3','skills/programmatic-eda/scripts/null_profiler.py','--input',INP,'--output',f'{RUN}/nulls.csv'], f'{RUN}/nulls.txt'),
    (['python3','skills/programmatic-eda/scripts/outlier_detector.py','--input',INP,'--groupby','mode','--output',f'{RUN}/outliers_by_mode.csv'], f'{RUN}/outliers_by_mode.txt'),
    (['python3','skills/programmatic-eda/scripts/distribution_summary.py','--input',INP,'--bins','8','--groupby','mode','--output',f'{RUN}/distributions_by_mode.csv'], f'{RUN}/distributions_by_mode.txt'),
    (['python3','skills/programmatic-eda/scripts/correlation_explorer.py','--input',INP,'--groupby','mode','--threshold','0.8','--output',f'{RUN}/correlations_by_mode.csv'], f'{RUN}/correlations_by_mode.txt'),
]
for cmd, out_path in steps:
    r = subprocess.run(cmd, capture_output=True, text=True)
    body = r.stdout + (('\n[STDERR]\n'+r.stderr) if r.stderr else '')
    open(out_path,'w').write(body)
    print(f'{cmd[1].split("/")[-1]}: rc={r.returncode}')
