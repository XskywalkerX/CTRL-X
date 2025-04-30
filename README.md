# 🤖 RoboCup 2025 Robot -  Ctrl X

Welcome to the official codebase of our RoboCup robot, powered by **Python** and driven by a clean **Hierarchical State Machine (HSM)** architecture. This repository was designed for speed, modularity, and strategic domination on the field.


---

## 🧠 Behavior Control

We use a **Hierarchical State Machine** to control our robot's decisions.

### Example Behavior Stack:
- `TopState`
  - `IdleState`
  - `AttackState`
    - `ApproachBallState`
    - `KickState`
  - `DefenseState`
    - `BlockGoalState`
    - `RetreatState`

Each state is its own Python class with `on_enter()`, `update()`, and `on_exit()` hooks, making behaviors cleanly isolated and reusable.

---

## 🚀 Getting Started

### Requirements

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

