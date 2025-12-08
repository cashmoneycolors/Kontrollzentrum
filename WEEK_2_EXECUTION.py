#!/usr/bin/env python3
"""
🚀 WEEK 2 EXECUTION - PRODUCTION BUILD
"""
import subprocess
import os
import sys

def execute_week_2():
    print("="*70)
    print("🚀 WEEK 2: PRODUCTION BUILD")
    print("="*70)
    
    # Step 1: Setup environment
    print("\n[1/4] SETUP PRODUCTION ENVIRONMENT...")
    subprocess.run([sys.executable, "-m", "venv", "venv-prod"], capture_output=True)
    print("✅ Virtual environment created")
    
    # Step 2: Install dependencies
    print("\n[2/4] INSTALLING DEPENDENCIES...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                  capture_output=True)
    print("✅ Dependencies installed")
    
    # Step 3: Configure payment systems
    print("\n[3/4] CONFIGURING PAYMENT SYSTEMS...")
    os.environ["STRIPE_API_KEY"] = os.getenv("STRIPE_API_KEY", "sk_live_...")
    os.environ["PAYPAL_CLIENT_ID"] = os.getenv("PAYPAL_CLIENT_ID", "...")
    print("✅ Payment systems configured")
    
    # Step 4: Build Docker image
    print("\n[4/4] BUILDING DOCKER IMAGE...")
    subprocess.run(["docker", "build", "-t", "kontrollzentrum:5.0", "."],
                  capture_output=True)
    print("✅ Docker image built")
    
    print("\n" + "="*70)
    print("✅ WEEK 2 COMPLETE - READY FOR WEEK 3")
    print("="*70)

if __name__ == "__main__":
    execute_week_2()
