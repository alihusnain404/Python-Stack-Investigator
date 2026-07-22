import time
import sys

print("[+] Application Started in Production Mode...", flush=True)
time.sleep(2)

print("[!] Processing high-volume database queries...", flush=True)
time.sleep(2)

# Simulated Crash Event
try:
    active_users = 0
    calculated_load = 5000 / active_users
except Exception as e:
    print("--- CRITICAL SYSTEM FAILURE ---", flush=True)
    import traceback
    traceback.print_exc(file=sys.stdout)
    print("--- CONTAINER SHUTDOWN ---", flush=True)