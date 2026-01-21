import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# IMPORTANT: run from project root
from data.traffic_simulator import generate_traffic_data


# -------------------------------
# CONFIGURATION
# -------------------------------
MAX_REPLICAS = 5
MIN_REPLICAS = 1
DECISION_INTERVAL = 10

# -------------------------------
# DECISION ENGINE (Controller)
# -------------------------------

def decision_engine(is_anomaly, is_stable, current_replicas):
    MAX_REPLICAS = 5
    MIN_REPLICAS = 1

def decision_engine(is_anomaly: bool, is_stable: bool, current_replicas: int) -> tuple[int, str]:
    if is_anomaly and current_replicas < MAX_REPLICAS:
        new_replicas = current_replicas + 1
        return new_replicas, f"SCALE UP -> {new_replicas} replicas"

    # Scale down ONLY if stable AND no anomaly
    elif is_stable and not is_anomaly and current_replicas > MIN_REPLICAS:
        new_replicas = current_replicas - 1
        return new_replicas, f"SCALE DOWN -> {new_replicas} replicas"

    return current_replicas, "MAINTAIN"


# -------------------------------
# MAIN MONITOR
# -------------------------------

def run_monitor():
    print("S.I.C.R.O Orchestrator Initializing...")

    df = generate_traffic_data(start_time=datetime.now())

    # -------------------------------
    # ML ANOMALY DETECTION
    # -------------------------------

    scaler = StandardScaler()
    features = scaler.fit_transform(df[['cpu_usage', 'memory_usage']])

    clf = IsolationForest(contamination=0.02, random_state=42)
    df['ml_anomaly'] = clf.fit_predict(features)

    # Persistent anomaly detection
    df['is_alert'] = (df['ml_anomaly'] == -1).rolling(window=5).sum() >= 3
    df['is_alert'] = (df['ml_anomaly'] == -1).rolling(window=5).sum().fillna(0) >= 3

    # Stability window (prevents flapping)
    df['is_stable'] = (df['ml_anomaly'] == 1).rolling(window=10).sum() >= 8
    df['is_stable'] = (df['ml_anomaly'] == 1).rolling(window=10).sum().fillna(0) >= 8

    # -------------------------------
    # INFRASTRUCTURE SIMULATION
    # -------------------------------

    current_replicas = 1
    replica_history = []
    actions_taken = []

    print("Running Decision Engine...")

    for i in range(len(df)):
        # Decision every 10 minutes
        if i % 10 == 0:
        if i % DECISION_INTERVAL == 0:
            current_replicas, action = decision_engine(
                df['is_alert'].iloc[i],
                df['is_stable'].iloc[i],
                current_replicas
            )

            if action != "MAINTAIN":
                actions_taken.append(
                    f"{df['timestamp'].iloc[i]} | {action}"
                )

        replica_history.append(current_replicas)

    df['replica_count'] = replica_history

    # -------------------------------
    # AUDIT LOG (UTF-8 SAFE)
    # -------------------------------

    with open("infra_actions.log", "w", encoding="utf-8") as f:
        f.write("\n".join(actions_taken))

    print(f"Infrastructure optimized. {len(actions_taken)} scaling events logged.")

    # -------------------------------
    # VISUALIZATION
    # -------------------------------

    fig, ax1 = plt.subplots(figsize=(15, 8))

    ax1.plot(df["timestamp"], df["cpu_usage"], label="CPU %", color='tab:red', alpha=0.6)
    ax1.plot(df["timestamp"], df["memory_usage"], label="Memory %", color='tab:green', alpha=0.6)
    ax1.set_ylabel("Resource Usage (%)")

    ax2 = ax1.twinx()
    ax2.step(
        df["timestamp"],
        df["replica_count"],
        where='post',
        label="Replica Count",
        color='black',
        linewidth=2
    )
    ax2.set_ylabel("Server Replicas")
    ax2.set_ylim(0, 6)

    plt.title("S.I.C.R.O – ML-Driven Self-Healing System")
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))

    plt.savefig("sicro_decision_report.png")
    plt.close()


if __name__ == "__main__":
    run_monitor()
