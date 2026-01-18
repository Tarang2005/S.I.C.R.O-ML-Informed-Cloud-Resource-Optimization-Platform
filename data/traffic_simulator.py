import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_traffic_data(minutes=1440, start_time=None):
    if start_time is None:
        start_time = datetime(2026, 1, 15, 0, 0)
    
    np.random.seed(42)
    data = []
    base_requests = 100

    for i in range(minutes):
        timestamp = start_time + timedelta(minutes=i)
        hour = timestamp.hour
        traffic_multiplier = 2.5 if 18 <= hour <= 22 else 1.0
        
        #Traffic Anomaly (10 AM)
        noise = np.random.normal(50, 5) if 600 <= i <= 615 else np.random.normal(0, 15)
        request_count = max(int(base_requests * traffic_multiplier + noise), 10)
        
        cpu_usage = request_count / 3 + np.random.normal(0, 5)
        memory_usage = request_count / 2 + np.random.normal(0, 5)

        #Memory Leak (2 PM)
        if 840 <= i <= 860:
            memory_usage += 40

        cpu_usage = max(min(cpu_usage, 100), 0)
        memory_usage = max(min(memory_usage, 100), 0)
        data.append([timestamp, request_count, cpu_usage, memory_usage])

    return pd.DataFrame(data, columns=["timestamp", "request_count", "cpu_usage", "memory_usage"])