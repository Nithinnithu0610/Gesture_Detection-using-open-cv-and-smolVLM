
import subprocess, argparse, os, time, threading
from multiprocessing import Process
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='', help='video file path; leave empty for webcam')
parser.add_argument('--duration', type=int, default=20, help='duration to run system monitor in seconds (0=until detector ends)')
args = parser.parse_args()

# Start system monitor in background (simple)
sys_monitor_cmd = [sys.executable, 'system_monitor.py', '--out', 'logs/system_usage.log', '--interval', '0.5', '--duration', str(args.duration)]
detector_cmd = [sys.executable, 'gesture_recognition.py', '--input', args.input, '--out_dir', 'frames']

print('Starting system monitor and detector...')
p1 = subprocess.Popen(sys_monitor_cmd)
p2 = subprocess.Popen(detector_cmd)

try:
    p2.wait()
except KeyboardInterrupt:
    print('Interrupted by user')
finally:
    p1.terminate()
    p2.terminate()
