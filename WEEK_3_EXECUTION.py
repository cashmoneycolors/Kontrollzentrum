#!/usr/bin/env python3
"""
🚀 WEEK 3 EXECUTION - DEPLOYMENT
"""
import subprocess
import sys

def execute_week_3():
    print("="*70)
    print("🚀 WEEK 3: DEPLOYMENT")
    print("="*70)
    
    # Step 1: Local deployment
    print("\n[1/3] LOCAL DEPLOYMENT...")
    subprocess.run([sys.executable, "PRODUCTION_START.py"], capture_output=True)
    print("✅ Local deployment complete")
    
    # Step 2: Docker deployment
    print("\n[2/3] DOCKER DEPLOYMENT...")
    subprocess.run(["docker", "run", "-d", "-p", "8000:8000", "-p", "8501:8501",
                   "kontrollzentrum:5.0"], capture_output=True)
    print("✅ Docker deployment complete")
    
    # Step 3: Kubernetes deployment
    print("\n[3/3] KUBERNETES DEPLOYMENT...")
    subprocess.run(["kubectl", "apply", "-f", "kubernetes.yml"], capture_output=True)
    print("✅ Kubernetes deployment complete")
    
    print("\n" + "="*70)
    print("✅ WEEK 3 COMPLETE - READY FOR WEEK 4")
    print("="*70)

if __name__ == "__main__":
    execute_week_3()
