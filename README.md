# Load Balancing Strategies — A Comparison

Discrete simulation comparing three request-distribution strategies across a pool of servers.

## Strategies

- **Round-robin** — assign requests in fixed rotation
- **Random** — assign to a uniformly random server
- **Least-connections** — assign to whichever server currently holds the fewest

## Setup

Five servers, 200 requests per run. Each strategy runs against the same request stream; the notebook plots the resulting load distribution per server.

## Results

Across 2,000 simulated runs:

| Strategy | Mean spread (max - min load) | Mean std. dev. |
|---|---|---|
| Round-robin | 0.00 | 0.00 |
| Random | 14.96 | 5.41 |
| Least-connections | 0.00 | 0.00 |

Round-robin and least-connections both distribute perfectly evenly. Random leaves roughly 15 requests between the busiest and the quietest server, with a standard deviation of about 5.4.

## Limitation of the model

Least-connections is indistinguishable from round-robin here, and that is an artifact of the simulation rather than a property of the strategies. `ServiceInstance.current_load` only ever increments — requests are never completed or released — so all servers hold equal load at each assignment step and least-connections degenerates into a rotation.

Separating the two requires modelling request completion: assigning each request a service duration and decrementing a server's load when it finishes. Under uneven request durations, least-connections would be expected to outperform round-robin, which is the case this simulation cannot currently show.

## Running it

Open `Load_balancing_strategies_comparison.ipynb` and run top to bottom. Requires only `matplotlib`.

---

Coursework notebook — B.Tech CSE (AI & ML), Woxsen University.
