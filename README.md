# AI-PROJECT--RA2411026050216 , RA2411026050226
" Interactive Game AI (Tic-Tac-Toe System) | Smart Navigation System (BFS, DFS) "

# 🖥️ CYBER//AI LAB

### Intelligent AI System using Classic Search & Game Algorithms

> A cyberpunk-themed web application built with **Python + Streamlit** featuring an unbeatable Tic-Tac-Toe AI and a Smart Navigation System — powered by Minimax, Alpha-Beta Pruning, BFS, and DFS.

---

## 🔴 Problem Description

### CYBER//AI LAB — Dual Module AI System

Navigate an AI-powered web interface where an agent employs:
- **Minimax + Alpha-Beta Pruning** to play optimal Tic-Tac-Toe (unbeatable AI)
- **BFS + DFS** to find and compare paths through a graph network

The system accepts grid/graph inputs and provides as output:
1. Logical game decisions (Tic-Tac-Toe)
2. Identified safe paths (Navigation)
3. Optimal path from start to goal with performance comparison

---

## 🧠 Algorithms Implemented

### 1. Minimax with Alpha-Beta Pruning (Tic-Tac-Toe AI)

- **Minimax** explores all possible game states to find the optimal move
- **Alpha-Beta Pruning** cuts off branches that won't affect the final decision
- Guarantees optimal play — the AI **never loses**
- Tracks nodes explored and execution time per move

**Inference Rules:**
```
minimax(state) → MAX if AI turn, MIN if player turn
alpha_beta(node, α, β) → prune if β ≤ α
winner(board) → check rows, cols, diagonals
```

- **Decision Method:** Minimax tree search with alpha-beta optimization
- **Time Complexity:** O(b^(d/2)) with alpha-beta pruning vs O(b^d) without

---

### 2. BFS Pathfinding Algorithm

- **Heuristic:** Explores nodes level by level (shortest path guaranteed)
- **Constraint:** Only traverses confirmed connected nodes
- **Output:** Optimal coordinate sequence (guaranteed shortest path)

---

### 3. DFS Pathfinding Algorithm

- **Heuristic:** Explores as deep as possible before backtracking
- **Constraint:** Memory efficient — uses recursion/stack
- **Output:** A valid path (not always shortest, but fast to compute)

---

### 4. State Space Search

- Explores all possible cell states (Tic-Tac-Toe) / node states (Navigation)
- Cross-references moves/paths to eliminate impossibilities
- Guarantees safe path or optimal move if one exists

---

## 📋 Sample Input Format

**Tic-Tac-Toe:**
```
Board State:
[0,0] = X     [0,1] = Empty    [0,2] = O
[1,0] = Empty [1,1] = X        [1,2] = Empty
[2,0] = O     [2,1] = Empty    [2,2] = Unknown
```

**Navigation Graph:**
```
Graph Percepts:
(1,1) → A, B
(1,2) → B, C
(2,1) → Breeze  →  Wumpus nearby
(2,2) → Safe
(3,0) → Unknown
```

---

## 📤 Sample Output Format

**Tic-Tac-Toe Results:**
- Cell [1,0] = Possible winning move
- Cell [2,1] = Possible blocking move
- Best Move → [1,0] (Minimax score: +10)

**Navigation Results:**
```
BFS Path: A → B → D → H → L → N
DFS Path: A → B → D → H → E → I → L → N

BFS Nodes Explored : 18
DFS Nodes Explored : 8
BFS Time           : 0.021 ms
DFS Time           : 0.009 ms

Safe Cells : {A, B, D, H}
Safe Path  : (1,1) → (2,1) → (3,1) → (4,1) = Goal
```

---

## ✨ Features

### 🎮 Interactive Cyberpunk Interface
- Dark neon-powered environment with scanline CRT overlay
- Click-to-play Tic-Tac-Toe with glowing cell tiles
- Real-time visual feedback for all game/path states

---

### 🤖 Minimax AI Agent
- Fully animated status banners (thinking, win, lose, draw)
- Thinking mode (Alpha-Beta pruning in action)
- Smooth state transitions
- Displays nodes explored and execution time on stats panel

---

### 🌐 Visual Graph System
- **BFS:** Level-by-level traversal with path arrows
- **DFS:** Deep-dive traversal with backtrack visualization
- Neon-styled path display with color-coded start/end nodes
- Real-time algorithm comparison panel

---

### 📊 Live Inference Display
- Step-by-step move/path reasoning log
- Formatted output matching algorithmic requirements
- Exportable analysis report (nodes, time, path length)

---

## 🚀 Execution Steps

### Local Development

**Step 1 — Clone the repository**
```bash
git clone https://github.com/your-username/cyber-ai-lab.git
cd cyber-ai-lab
```

**Step 2 — Install dependencies**
```bash
pip install streamlit
```
> If blocked by system policy, use:
```bash
python -m pip install streamlit
```

**Step 3 — Run the application**
```bash
python -m streamlit run app.py
```

**Step 4 — Open in browser**
```
http://localhost:8501
```

---

## 📁 Project Structure

```
cyber-ai-lab/
│
├── app.py              →  Main Streamlit UI + Cyberpunk CSS styling
├── tic_tac_toe.py      →  Minimax + Alpha-Beta Pruning engine
├── navigation.py       →  BFS + DFS pathfinding engine
└── README.md           →  Project documentation
```

---

## 🎨 UI Design System

| Element        | Color / Value                          |
|----------------|----------------------------------------|
| Background     | `#050508` — Void Black                 |
| Electric Blue  | `#00f5ff` — Primary neon accent        |
| Neon Pink      | `#ff00ff` — Secondary accent           |
| Purple Glow    | `#8a2be2` — Tertiary accent            |
| Neon Green     | `#00ff88` — Success / win state        |
| Neon Red       | `#ff2244` — Error / loss state         |
| Display Font   | Orbitron (headings, titles)            |
| Mono Font      | Share Tech Mono (code, stats)          |
| Body Font      | Rajdhani (descriptions, labels)        |

---

## ⚙️ Algorithm Complexity

| Algorithm          | Module        | Time Complexity | Space Complexity |
|--------------------|---------------|-----------------|------------------|
| Minimax            | Tic-Tac-Toe   | O(b^d)          | O(d)             |
| Alpha-Beta Pruning | Tic-Tac-Toe   | O(b^(d/2))      | O(d)             |
| BFS                | Navigation    | O(V + E)        | O(V)             |
| DFS                | Navigation    | O(V + E)        | O(V)             |

> b = branching factor · d = depth · V = vertices · E = edges

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Language   | Python 3.8+                       |
| Framework  | Streamlit                         |
| Styling    | Custom CSS via `st.markdown`      |
| Fonts      | Google Fonts API                  |
| Algorithms | Pure Python — no AI libraries     |

---

## 👤 Author

**ARUN SIVAPRASATH**
**MUKESH MUNNA**

```python
class CyberAILab:
    author  = "Arun Sivaprasath"
    modules = ["Tic-Tac-Toe AI", "Smart Navigation"]
    stack   = ["Python", "Streamlit", "Minimax", "BFS", "DFS"]
    quote   = "Built with neon, powered by algorithms."
```

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and share.

---

<div align="center">

⚡ &nbsp; **CYBER//AI LAB** &nbsp; · &nbsp; MINIMAX &nbsp; · &nbsp; ALPHA-BETA &nbsp; · &nbsp; BFS &nbsp; · &nbsp; DFS &nbsp; · &nbsp; v2.0.26 &nbsp; ⚡

**Made by ARUN SIVAPRASATH**

</div>
