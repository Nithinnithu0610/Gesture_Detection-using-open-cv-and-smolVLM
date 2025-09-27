
import argparse, time, csv, os, subprocess, sys
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', default='sample_videos', help='Input videos or frames dir')
parser.add_argument('--output', default='benchmarks/results_summary.csv', help='CSV output summary')
args = parser.parse_args()

# This script assumes you will run the detectors and they will produce logs in logs/
# For demonstration, if logs are already present, it will summarize them.
def summarize_logs():
    rows = []
    # Summarize mediapipe gesture log
    gm = 'logs/gesture_outputs.log'
    gs = 'logs/gesture_outputs_smolvlm.log'
    if os.path.exists(gm):
        with open(gm,'r') as f:
            lines = f.readlines()[1:]
            cnt = len(lines)
            rows.append(['mediapipe', cnt])
    else:
        rows.append(['mediapipe', 0])
    if os.path.exists(gs):
        with open(gs,'r') as f:
            lines = f.readlines()[1:]
            cnt = len(lines)
            rows.append(['smolvlm', cnt])
    else:
        rows.append(['smolvlm', 0])
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output,'w',newline='') as out:
        import csv
        writer = csv.writer(out)
        writer.writerow(['detector','detections_count'])
        for r in rows:
            writer.writerow(r)
    print('Benchmark summary written to', args.output)

if __name__=='__main__':
    summarize_logs()
