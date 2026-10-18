"""
Corrected Load Balancing Simulation (Round-Robin vs. Random vs. Stateful Least-Connections).
Fixes the modeling flaw where uniform request processing durations rendered Least-Connections
indistinguishable from Round-Robin. Incorporates Pareto-distributed job durations and active-connection tracking.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Server:
    def __init__(self, server_id):
        self.server_id = server_id
        self.active_jobs = []  # list of remaining durations
        self.total_processed = 0
        self.busy_time = 0.0

    def tick(self, time_step=1.0):
        # Decrement duration of active jobs
        finished = []
        for i in range(len(self.active_jobs)):
            self.active_jobs[i] -= time_step
            if self.active_jobs[i] <= 0:
                finished.append(i)
                self.total_processed += 1
        for idx in reversed(finished):
            self.active_jobs.pop(idx)

    @property
    def active_connections(self):
        return len(self.active_jobs)

class LoadBalancerSimulation:
    def __init__(self, num_servers=5, num_requests=200, seed=42):
        self.num_servers = num_servers
        self.num_requests = num_requests
        np.random.seed(seed)
        # Heavy-tailed Pareto job duration distribution
        self.job_durations = (np.random.pareto(a=1.8, size=num_requests) + 1.0) * 2.0

    def run_round_robin(self):
        servers = [Server(i) for i in range(self.num_servers)]
        server_idx = 0
        for duration in self.job_durations:
            servers[server_idx].active_jobs.append(duration)
            server_idx = (server_idx + 1) % self.num_servers
            for s in servers:
                s.tick()
        return [s.total_processed + s.active_connections for s in servers]

    def run_least_connections(self):
        servers = [Server(i) for i in range(self.num_servers)]
        for duration in self.job_durations:
            # Route to server with fewest active connections
            least_server = min(servers, key=lambda s: s.active_connections)
            least_server.active_jobs.append(duration)
            for s in servers:
                s.tick()
        return [s.total_processed + s.active_connections for s in servers]

    def run_random(self):
        servers = [Server(i) for i in range(self.num_servers)]
        for duration in self.job_durations:
            choice = np.random.randint(0, self.num_servers)
            servers[choice].active_jobs.append(duration)
            for s in servers:
                s.tick()
        return [s.total_processed + s.active_connections for s in servers]

if __name__ == "__main__":
    sim = LoadBalancerSimulation(num_servers=5, num_requests=200)
    rr_res = sim.run_round_robin()
    lc_res = sim.run_least_connections()
    rnd_res = sim.run_random()

    print(f"Round-Robin Allocation:       {rr_res} | Std Dev: {np.std(rr_res):.2f}")
    print(f"Least-Connections Allocation: {lc_res} | Std Dev: {np.std(lc_res):.2f}")
    print(f"Random Allocation:            {rnd_res} | Std Dev: {np.std(rnd_res):.2f}")
