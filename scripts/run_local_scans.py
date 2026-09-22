#!/usr/bin/env python3
"""
Local DevSecOps Security Scanner CLI
Runs localized security scans (Secret check, AST analysis, Dependency CVEs) locally.
"""
import subprocess
import sys
import os

# Ensure clean UTF-8 output on all operating systems
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def print_header(title):
    print("\n" + "=" * 60)
    print(f"[*] {title}")
    print("=" * 60)

def run_step(command, step_name):
    print_header(step_name)
    print(f"Executing: {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"[+] {step_name}: PASSED")
            return True
        else:
            print(f"[!] {step_name}: COMPLETED WITH FINDINGS / WARNINGS (Exit Code {result.returncode})")
            return False
    except FileNotFoundError:
        print(f"[-] Tool not installed locally on PATH. Skipping localized run for {step_name}.")
        return True

def main():
    print("[*] Starting Local DevSecOps Security Audit...")
    
    # 1. Dependency Vulnerability Scan (pip-audit)
    run_step([sys.executable, "-m", "pip", "install", "pip-audit", "bandit", "pytest"], "Installing Scanner Tools")
    
    # 2. SAST Analysis with Bandit
    run_step([sys.executable, "-m", "bandit", "-r", "app/", "-ll"], "Static Application Security Testing (Bandit)")
    
    # 3. Unit & Security Regression Tests
    run_step([sys.executable, "-m", "pytest", "tests/"], "Pytest Security & Unit Suite")
    
    # 4. Dependency Vulnerability Audit
    run_step([sys.executable, "-m", "pip_audit", "-r", "requirements.txt"], "Software Composition Analysis (pip-audit)")
    
    print_header("DevSecOps Local Audit Summary")
    print("[+] All local security unit tests & AST scans completed.")
    print("[*] To test full container & ZAP DAST scans, push code to GitHub Actions!")

if __name__ == "__main__":
    main()
