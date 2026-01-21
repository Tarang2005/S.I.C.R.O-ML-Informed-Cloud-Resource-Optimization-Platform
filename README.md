# S.I.C.R.O – Self‑Healing Intelligent Cloud Resource Optimizer

## Overview

**S.I.C.R.O (Self‑Healing Intelligent Cloud Resource Optimizer)** is a production‑grade simulation of an **AI‑driven autoscaling system**. It demonstrates how machine‑learning‑based anomaly detection can influence **cloud infrastructure scaling decisions**, and how those decisions map cleanly to **modern DevOps and Kubernetes primitives**.

The project is intentionally designed to go **beyond a toy ML model** and instead showcase **system design, MLOps thinking, and cloud‑native architecture** — the exact skills expected for Cloud / DevOps / SRE / Platform Engineering internships.

---

## Problem Statement

Traditional autoscaling mechanisms (e.g., basic CPU‑based scaling) are *reactive*. They respond **after** a spike or failure begins. This often leads to:

* Temporary outages
* Over‑provisioning and cloud cost waste
* Resource thrashing due to noisy metrics

S.I.C.R.O explores a **proactive and intelligent approach** where:

* System metrics are continuously analyzed
* ML models detect abnormal behavior early
* Scaling decisions are filtered to avoid noise
* Infrastructure reacts in a controlled, stable manner

---

## High‑Level Architecture

```
Traffic Simulator
      ↓
ML Anomaly Detection (Isolation Forest)
      ↓
Decision Engine (Scale / Maintain Logic)
      ↓
Autoscaling Intent
      ↓
Kubernetes HPA (Runtime Scaling)
```

Infrastructure provisioning is intentionally separated from runtime scaling:

* **Terraform** → defines infrastructure boundaries
* **Kubernetes HPA** → handles dynamic pod scaling

---

## Tech Stack

### Core Logic

* Python 3.9
* Pandas, NumPy
* Scikit‑learn (Isolation Forest)
* Matplotlib

### DevOps & Cloud‑Native

* Docker (containerization)
* Kubernetes (local cluster via KIND)
* Kubernetes Deployment, Service, HPA
* Terraform (Infrastructure as Code)

---

## Key Features

### Intelligent Anomaly Detection

* Uses **Isolation Forest** to detect abnormal CPU & memory patterns
* Robust to noise and sudden metric spikes

### Anti‑Flapping Decision Engine

* Rolling windows for anomaly persistence
* Stability windows before scaling down
* Prevents aggressive or oscillating scaling

### Infrastructure‑Aware Scaling Logic

* Enforces minimum and maximum replica bounds
* Logs all scaling actions for auditability

### Cloud‑Native Autoscaling

* Scaling logic translated into **Kubernetes HPA**
* Stabilization windows mirror ML decision rules

---

## Infrastructure Design

### Terraform (`infra/main.tf`)

Terraform is used to **define infrastructure boundaries**, not runtime behavior.

Purpose:

* Represent where SICRO would run in a real cloud environment
* Define cluster / node constraints
* Demonstrate Infrastructure‑as‑Code knowledge

> Terraform does **not** perform application scaling. Runtime scaling is delegated to Kubernetes HPA.

---

## Kubernetes Usage

SICRO was deployed to a **real local Kubernetes cluster** using **KIND (Kubernetes‑in‑Docker)**.

Kubernetes resources used:

* `Deployment` – defines the SICRO workload
* `Service` – provides stable networking
* `HorizontalPodAutoscaler` – handles runtime scaling

This validates that the system is **cloud‑ready and production‑aligned**.

---

## How to Run (Local)

### 1. Run core monitoring logic

```bash
python -m app.monitor
```

This generates:

* Scaling audit logs
* Resource usage reports
* Decision visualization

### 2. Kubernetes deployment (optional / advanced)

```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get hpa
```

---

## Outputs

* `logs/infra_actions.log` – scaling audit trail
* `reports/sicro_decision_report.png` – system behavior visualization

---

## System Behavior

### ML-Driven Self-Healing
<img width="1500" height="800" alt="image" src="https://github.com/user-attachments/assets/f6cbfc30-5837-4f1c-b716-44393b95a327" />

### Kubernetes Deployment
<img width="1512" height="532" alt="image" src="https://github.com/user-attachments/assets/37519ab4-7e69-4735-a09e-3a880683940c" />

---

## What This Project Demonstrates

* ML applied to systems engineering (AIOps)
* Clear separation of infra vs runtime concerns
* Kubernetes autoscaling fundamentals
* Production‑style decision filtering & safety guards
* End‑to‑end system thinking

---

## Future Improvements

* Integrate Prometheus Metrics Server
* Use real application traffic
* Deploy to managed Kubernetes (EKS / GKE)
* Add CI/CD pipeline for automated deployments

---

## Author

Tarang Patra

---

