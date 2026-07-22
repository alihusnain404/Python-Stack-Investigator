import docker
import re

def harvest_live_docker_telemetry():
    client = docker.from_env()
    print("[*] Production Telemetry Harvester Activated...")
    print("[*] Scanning active cluster for crashed containers...")
    
    containers = client.containers.list(all=True)
    
    for container in containers:
        raw_logs = container.logs().decode('utf-8')
        
        if "ZeroDivisionError" in raw_logs or "OperationalError" in raw_logs:
            print(f"\n [CRASH DETECTED] Found critical failure inside Container ID: {container.id[:12]} ({container.name})")
            print("="*65)
            print("--- RAW DOCKER TELEMETRY EXTRACTED ---")
            print(raw_logs.strip())
            print("="*65)
            
            error_match = re.search(r'([a-zA-Z0-9_]+Error): (.*)', raw_logs)
            signature = error_match.group(1) if error_match else "RuntimeAnomaly"
            
            print(f" [PARSED LOG DATA] Signature Isolated: {signature}")
            return raw_logs
            
    print("[-] No anomalous container traces detected in this cycle.")
    return None

if __name__ == "__main__":
    harvest_live_docker_telemetry()
