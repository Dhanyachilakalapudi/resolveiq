# ResolveIQ – AI-Assisted Exception Resolution Workbench

ResolveIQ is an AI-assisted exception resolution workbench built for the **Supervity Forward Deployed Engineer Technical Screening Assessment (Problem Statement 9)**.

The application combines deterministic exception detection with AI-powered explanations and a confidence-gated workflow, ensuring that high-confidence exceptions can be resolved automatically while low-confidence cases remain under human control.

---

## Problem Statement

Build a lightweight web application where flagged transactions appear in a queue, allowing a reviewer to:

- View exception details
- Understand why an exception was flagged
- Receive an AI-generated resolution recommendation
- Enforce confidence-based auto-resolution
- Keep a human reviewer in control when confidence is low

---

## Features

- Exception Queue Dashboard
- AI-generated contextual explanations
- Resolution recommendations
- Confidence Gate (90% threshold)
- Automatic resolution for high-confidence exceptions
- Human Review workflow for low-confidence exceptions
- Real-time queue status updates
- FastAPI backend with Swagger documentation
- SQLite-based mock data storage

---

## Architecture

```text
Exception Queue
      │
      ▼
Deterministic Exception Detection
      │
      ▼
AI Analysis & Recommendation
      │
      ▼
Confidence Gate (90%)
      │
 ┌────┴────┐
 ▼         ▼
Auto       Human
Resolve    Review
 │          │
 ▼          ▼
Queue Status Updated