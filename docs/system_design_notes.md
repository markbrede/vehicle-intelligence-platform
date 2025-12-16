# System Design Notes — Vehicle Intelligence Platform

## Current System (Implemented)

### Components
- **Client**: My CLI scripts execute locally in Python (`python -m src.<module>`)
- **Persistent storage**: MongoDB Atlas (cloud document database)
- **Data model**: `vehicles` (parent), `maintenance_events` + `expenses` (children via ObjectId reference)

### Reads/Writes
- **Writes**: `insert_vehicle`, `insert_maintenance`, `insert_expense`
- **Reads**:
  - Timeline joins: `query_vehicle_history`
  - Aggregated totals: `query_total_cost`
  - Monthly trend: `query_cost_over_time`
  - Predictive interval: `query_maintenance_intervals`
  - MongoDB-native analytics: `query_analytics_pipelines`

---

## Performance & Scaling Characteristics

### Primary query patterns
- Find vehicle by `(user_id, nickname)`
- Fetch events by `vehicle_id` sorted by date/odometer
- Aggregate by month/category for analytics

### Index strategy (implemented)
- `vehicles`: `(user_id, nickname)` for fast vehicle lookup
- `maintenance_events`: `(vehicle_id, date)` for timeline reads
- `expenses`: `(vehicle_id, date)` for timeline reads
- `(vehicle_id, category)` for category rollups

Expected effects:
- Read latency scales mainly with events per vehicle, not total DB size, because queries are selective on `vehicle_id`.

---

## Data Integrity (Implemented)

MongoDB is schemaless by default, so integrity is enforced using **collection validators**:
- Vehicles require: `user_id, year, make, model, created_at`
- Maintenance requires: `user_id, vehicle_id, date, category, description, cost, created_at`
- Expenses require: `user_id, vehicle_id, date, category, amount, created_at`

Invalid writes are rejected with `Document failed validation`.

---

## Concurrency & Consistency

### What can go wrong
- Two clients writing events simultaneously could create ordering issues (e.g., odometer decreasing).
- Duplicate events can occur if ingestion is re-run without idempotency.

### Current mitigation
- Validators prevent missing required fields.
- Sorting is done at query time (`sort(date)` / `sort(odometer)`).

### Next-step mitigation (planned)
- Add idempotency keys or uniqueness constraints (application-enforced) to prevent duplicates.
- Add optional business-rule checks (e.g., odometer monotonic increasing) prior to insert.

---

## Durability, Recovery, and Failure Modes

### Durability
- MongoDB Atlas persists data across restarts and machine failures.
- Writes are acknowledged by the cluster; data is not stored only locally.

### Recoverability
- If the local machine is lost, data remains in Atlas.
- If the cluster is misconfigured or deleted, recovery depends on backups (Atlas backup options).

### Likely failure modes
- Incorrect DB user permissions (already encountered with `collMod`)
- Network failure between client and Atlas
- Free-tier resource limits (storage caps, throughput constraints)

---

## Cost-to-Customer Ratio (Simple framing)
- Current deployment uses MongoDB Atlas free tier.
- Primary “cost” is developer time and operational risk (permissions, quotas).
- If scaled to real customers, costs scale with:
  - storage (documents)
  - read/write throughput
  - backup requirements
