
import psutil, time, csv, argparse, os
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--out', default='logs/system_usage.log')
parser.add_argument('--interval', type=float, default=0.5)
parser.add_argument('--duration', type=float, default=0)  # 0 means run until stopped
args = parser.parse_args()

os.makedirs(os.path.dirname(args.out), exist_ok=True)
f = open(args.out, 'w', newline='')
writer = csv.writer(f)
writer.writerow(['timestamp','cpu_percent','mem_percent'])

start = time.time()
try:
    while True:
        now = datetime.utcnow().isoformat()
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        writer.writerow([now, cpu, mem])
        f.flush()
        if args.duration>0 and (time.time()-start)>args.duration:
            break
        time.sleep(args.interval)
except KeyboardInterrupt:
    pass
finally:
    f.close()
