# 🛡️ DevSecOps-Pipeline-Sentinel: Zero-Trust CI/CD Security Gate

> **Automated Shift-Left Security Pipeline**: Production-grade DevSecOps CI/CD automation built on Linux and GitHub Actions enforcing secret detection, SAST, SCA, container image hardening, and dynamic API vulnerability scanning (DAST) with automated quality gate enforcement.

[![CI/CD Security Gate](https://img.shields.io/badge/GitHub_Actions-DevSecOps_Pipeline-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/Riyaenthusiast/devsecops-pipeline-sentinel/actions)
[![SAST Semgrep](https://img.shields.io/badge/SAST-Semgrep_%26_Bandit-00B0FF?style=for-the-badge&logo=semgrep&logoColor=white)](https://semgrep.dev/)
[![SCA Trivy](https://img.shields.io/badge/SCA_%26_SBOM-Aqua_Trivy-0078D4?style=for-the-badge&logo=aqua&logoColor=white)](https://trivy.dev/)
[![DAST OWASP ZAP](https://img.shields.io/badge/DAST-OWASP_ZAP_Scan-FF6C37?style=for-the-badge&logo=owasp&logoColor=white)](https://www.zaproxy.org/)
[![Docker Security](https://img.shields.io/badge/Docker-Non--Root_Hardened-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 📌 Architecture & Automated Security Flow

```
[ Developer Commit / Pull Request ]
               │
               ▼
┌────────────────────────────────────────────────────────────────────────┐
│               AUTOMATED "SHIFT-LEFT" DEVSECOPS PIPELINE                │
├────────────────────────────────────────────────────────────────────────┤
│  Stage 1: Secret Scanning       ──> Gitleaks (Catches leaked tokens)   │
│  Stage 2: Static Analysis (SAST)──> Semgrep & Bandit (AST & OWASP T10) │
│  Stage 3: Dependency Check(SCA) ──> Trivy & pip-audit (CVE Database)   │
│  Stage 4: Container Security    ──> Hadolint & Trivy Image CVE Scan    │
│  Stage 5: Dynamic Testing (DAST)──> OWASP ZAP Baseline API Testing     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │     🚦 ZERO-TRUST SECURITY QUALITY GATE ENFORCEMENT    │
       ├────────────────────────────────────────────────────────┤
       │  • Block Deployment if Critical/High CVE > 0           │
       │  • Post Automated Audit Matrix to PR & Step Summary    │
       │  • Upload SARIF Security Findings to Security Tab      │
       └────────────────────────────────────────────────────────┘
```

---

## 🛠️ Security Tooling Matrix & Standards

| Stage | Security Tool | Purpose & Detection Coverage | Standard / Framework |
| :--- | :--- | :--- | :--- |
| **Secrets** | `Gitleaks v8` | Detects hardcoded API keys, JWT secrets, and AWS credentials in git history. | Zero-Trust Credential Defense |
| **SAST** | `Semgrep` & `Bandit` | Identifies SQL injection, SSRF, insecure deserialization, and dangerous sinks. | OWASP Top 10, CWE Top 25 |
| **SCA & SBOM** | `Aqua Trivy` & `pip-audit` | Audits third-party dependencies against National Vulnerability Database (NVD). | NIST SP 800-161 (Supply Chain) |
| **Container** | `Hadolint` & `Trivy Image` | Enforces non-root user execution, minimal base image, and scans OS packages. | CIS Docker Benchmark v1.6 |
| **DAST** | `OWASP ZAP` | Scans running HTTP API endpoints for missing security headers and exposed metadata. | WASC Threat Classification |

---

## ✨ Engineering Highlights & Design Decisions

- **Multi-Stage Non-Root Docker Image**: Implemented multi-stage build pattern using `python:3.11-slim` with dedicated unprivileged user (`UID 10001`), dropping root privileges to mitigate container escape vectors.
- **Fail-Safe Quality Gate**: Configured automated thresholds where any `CRITICAL` or `HIGH` severity CVE blocks mergeability on Pull Requests.
- **Continuous Compliance Summary**: Automatically publishes an aggregated audit matrix directly into GitHub Actions step summaries on every push.

---

## ⚡ Quick Start & Local Execution

### 1. Clone Repository & Setup
```bash
git clone https://github.com/Riyaenthusiast/devsecops-pipeline-sentinel.git
cd devsecops-pipeline-sentinel

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
# source venv/bin/activate     # Linux / macOS

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Local Security Scans
```bash
# Run local AST security checks & dependency audits
python scripts/run_local_scans.py
```

### 3. Build & Run Hardened Container Locally
```bash
# Build Docker image
docker build -t secured-payment-api:latest .

# Run container with unprivileged user
docker run -d -p 8000:8000 --name payment-api secured-payment-api:latest

# Verify health check
curl http://localhost:8000/health
```

---

## 📂 Project Layout

```
devsecops-pipeline-sentinel/
├── .github/
│   └── workflows/
│       └── devsecops-pipeline.yml   # Multi-stage GitHub Actions CI/CD pipeline
├── .zap/
│   └── rules.tsv                    # OWASP ZAP DAST scan configuration rules
├── app/
│   └── main.py                      # Production FastAPI payment microservice
├── tests/
│   └── test_main.py                 # Unit and API authorization regression tests
├── scripts/
│   └── run_local_scans.py           # CLI runner for localized DevSecOps audits
├── Dockerfile                       # Multi-stage, non-root hardened containerfile
├── .dockerignore                    # Build context optimizer
├── requirements.txt                 # Application dependencies
└── README.md                        # Enterprise documentation & architecture
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
