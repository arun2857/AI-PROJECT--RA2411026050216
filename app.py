import streamlit as st
import time
from tic_tac_toe import (create_board, get_best_move, check_winner,
                          is_draw, get_available_moves)
from navigation import bfs, dfs, get_all_nodes, DEFAULT_GRAPH, parse_graph

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CYBER//AI LAB",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Master CSS ────────────────────────────────────────────────────────────────
CYBER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

/* ── Root vars ── */
:root {
  --bg:        #050508;
  --bg2:       #0d0d14;
  --blue:      #00f5ff;
  --pink:      #ff00ff;
  --purple:    #8a2be2;
  --green:     #00ff88;
  --red:       #ff2244;
  --text:      #c8d8e8;
  --dim:       #5a6a7a;
  --glass:     rgba(0,245,255,0.04);
  --glass2:    rgba(138,43,226,0.08);
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Rajdhani', sans-serif !important;
}

/* Scanline overlay */
[data-testid="stAppViewContainer"]::before {
  content: "";
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,245,255,0.015) 2px,
    rgba(0,245,255,0.015) 4px
  );
  pointer-events: none;
  z-index: 9999;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #080810 0%, #0d0d1a 100%) !important;
  border-right: 1px solid rgba(0,245,255,0.2) !important;
  box-shadow: 4px 0 30px rgba(0,245,255,0.05) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Headings ── */
h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; }
h1 { font-size: 2rem !important; letter-spacing: 3px !important; }

/* ── Radio (sidebar nav) ── */
[data-testid="stRadio"] label {
  font-family: 'Orbitron', sans-serif !important;
  font-size: 0.75rem !important;
  letter-spacing: 2px !important;
  color: var(--dim) !important;
  padding: 10px 16px !important;
  border-left: 2px solid transparent !important;
  transition: all 0.2s !important;
  display: block !important;
}
[data-testid="stRadio"] label:hover {
  color: var(--blue) !important;
  border-left-color: var(--blue) !important;
  text-shadow: 0 0 8px var(--blue) !important;
}
[data-testid="stRadio"] [aria-checked="true"] + div label,
[data-testid="stRadio"] input:checked ~ label {
  color: var(--blue) !important;
}

/* ── Buttons ── */
.stButton > button {
  background: transparent !important;
  border: 1px solid var(--blue) !important;
  color: var(--blue) !important;
  font-family: 'Orbitron', sans-serif !important;
  font-size: 0.7rem !important;
  letter-spacing: 2px !important;
  padding: 10px 24px !important;
  border-radius: 2px !important;
  text-transform: uppercase !important;
  transition: all 0.25s !important;
  box-shadow: 0 0 10px rgba(0,245,255,0.2), inset 0 0 10px rgba(0,245,255,0.05) !important;
  position: relative !important;
  overflow: hidden !important;
}
.stButton > button:hover {
  background: rgba(0,245,255,0.1) !important;
  box-shadow: 0 0 25px rgba(0,245,255,0.5), 0 0 50px rgba(0,245,255,0.2),
              inset 0 0 20px rgba(0,245,255,0.1) !important;
  color: #fff !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active {
  transform: translateY(0) !important;
  box-shadow: 0 0 8px rgba(0,245,255,0.3) !important;
}

/* Pink variant for AI button */
.pink-btn .stButton > button {
  border-color: var(--pink) !important;
  color: var(--pink) !important;
  box-shadow: 0 0 10px rgba(255,0,255,0.2), inset 0 0 10px rgba(255,0,255,0.05) !important;
}
.pink-btn .stButton > button:hover {
  background: rgba(255,0,255,0.1) !important;
  box-shadow: 0 0 25px rgba(255,0,255,0.5), 0 0 50px rgba(255,0,255,0.2) !important;
  color: #fff !important;
}

/* ── Text inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
  background: rgba(0,245,255,0.03) !important;
  border: 1px solid rgba(0,245,255,0.25) !important;
  border-radius: 2px !important;
  color: var(--blue) !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.9rem !important;
  box-shadow: 0 0 8px rgba(0,245,255,0.1) !important;
  transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--blue) !important;
  box-shadow: 0 0 15px rgba(0,245,255,0.3) !important;
  outline: none !important;
}
input::placeholder { color: var(--dim) !important; }

/* ── Text area ── */
.stTextArea textarea {
  background: rgba(0,245,255,0.03) !important;
  border: 1px solid rgba(0,245,255,0.2) !important;
  color: var(--blue) !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.8rem !important;
  border-radius: 2px !important;
}

/* ── Select / dropdown ── */
.stSelectbox > div > div {
  cursor: pointer;
}
.stSelectbox svg { fill: var(--blue) !important; }

/* ── Markdown labels ── */
label, .stTextInput label, .stSelectbox label, .stTextArea label {
  font-family: 'Orbitron', sans-serif !important;
  font-size: 0.65rem !important;
  letter-spacing: 2px !important;
  color: var(--dim) !important;
  text-transform: uppercase !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stDeployButton"] { display: none !important; }
.block-container { padding-top: 1.5rem !important; }

/* ── Divider ── */
hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent, var(--blue), var(--pink), var(--purple), transparent) !important;
  margin: 1.5rem 0 !important;
  opacity: 0.5 !important;
}
</style>
"""

# ── Reusable component CSS (injected inline) ──────────────────────────────────
CARD_CSS = """
<style>
.cyber-card {
  background: linear-gradient(135deg, rgba(0,245,255,0.04), rgba(138,43,226,0.06));
  border: 1px solid rgba(0,245,255,0.2);
  border-radius: 4px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 0 20px rgba(0,245,255,0.05), inset 0 0 30px rgba(138,43,226,0.03);
  position: relative;
  overflow: hidden;
}
.cyber-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--blue), transparent);
  opacity: 0.6;
}
.cyber-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.4rem;
  font-weight: 900;
  letter-spacing: 4px;
  text-transform: uppercase;
  background: linear-gradient(90deg, #00f5ff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.25rem;
}
.cyber-subtitle {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.75rem;
  color: rgba(0,245,255,0.5);
  letter-spacing: 2px;
  margin-bottom: 1rem;
}
.stat-box {
  background: rgba(0,0,0,0.4);
  border: 1px solid rgba(0,245,255,0.15);
  border-radius: 3px;
  padding: 0.8rem 1rem;
  text-align: center;
}
.stat-val {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: #00f5ff;
  text-shadow: 0 0 10px rgba(0,245,255,0.6);
  display: block;
}
.stat-label {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 2px;
  color: rgba(200,216,232,0.4);
  text-transform: uppercase;
}
.stat-val.pink  { color: #ff00ff; text-shadow: 0 0 10px rgba(255,0,255,0.6); }
.stat-val.green { color: #00ff88; text-shadow: 0 0 10px rgba(0,255,136,0.6); }
.stat-val.red   { color: #ff2244; text-shadow: 0 0 10px rgba(255,34,68,0.6); }

.path-display {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.85rem;
  background: rgba(0,0,0,0.5);
  border: 1px solid rgba(0,245,255,0.15);
  border-radius: 3px;
  padding: 0.8rem 1rem;
  color: #00f5ff;
  letter-spacing: 1px;
  word-break: break-word;
}
.path-arrow { color: rgba(255,0,255,0.7); margin: 0 4px; }
.section-tag {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.6rem;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: rgba(0,245,255,0.5);
  border-left: 2px solid #00f5ff;
  padding-left: 8px;
  margin-bottom: 0.5rem;
}
.neon-label {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.7rem;
  letter-spacing: 2px;
  text-transform: uppercase;
}
.neon-label.blue  { color: #00f5ff; text-shadow: 0 0 8px rgba(0,245,255,0.5); }
.neon-label.pink  { color: #ff00ff; text-shadow: 0 0 8px rgba(255,0,255,0.5); }
.neon-label.green { color: #00ff88; text-shadow: 0 0 8px rgba(0,255,136,0.5); }
.neon-label.red   { color: #ff2244; text-shadow: 0 0 8px rgba(255,34,68,0.5); }

/* Tic-Tac-Toe grid */
.ttt-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  max-width: 320px;
  margin: 0 auto;
}
.ttt-cell {
  aspect-ratio: 1;
  background: rgba(0,0,0,0.6);
  border: 1px solid rgba(0,245,255,0.2);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Orbitron', sans-serif;
  font-size: 2.2rem;
  font-weight: 900;
  cursor: pointer;
  transition: all 0.15s;
  min-height: 90px;
  box-shadow: inset 0 0 15px rgba(0,0,0,0.5);
  position: relative;
}
.ttt-cell:hover:not(.filled) {
  border-color: rgba(0,245,255,0.6) !important;
  box-shadow: 0 0 20px rgba(0,245,255,0.2), inset 0 0 10px rgba(0,245,255,0.05) !important;
}
.ttt-cell.X {
  color: #00f5ff;
  text-shadow: 0 0 15px rgba(0,245,255,0.8), 0 0 30px rgba(0,245,255,0.4);
  border-color: rgba(0,245,255,0.4);
  box-shadow: 0 0 10px rgba(0,245,255,0.1), inset 0 0 15px rgba(0,245,255,0.05);
}
.ttt-cell.O {
  color: #ff00ff;
  text-shadow: 0 0 15px rgba(255,0,255,0.8), 0 0 30px rgba(255,0,255,0.4);
  border-color: rgba(255,0,255,0.4);
  box-shadow: 0 0 10px rgba(255,0,255,0.1), inset 0 0 15px rgba(255,0,255,0.05);
}
.ttt-cell.win {
  animation: pulse-win 1s ease-in-out infinite alternate;
  border-width: 2px !important;
}
@keyframes pulse-win {
  from { box-shadow: 0 0 10px currentColor, inset 0 0 10px rgba(255,255,255,0.05); }
  to   { box-shadow: 0 0 30px currentColor, 0 0 60px currentColor, inset 0 0 20px rgba(255,255,255,0.1); }
}

.status-banner {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.9rem;
  letter-spacing: 3px;
  text-align: center;
  padding: 0.6rem;
  border-radius: 3px;
  margin-bottom: 1rem;
  text-transform: uppercase;
}
.status-banner.playing {
  border: 1px solid rgba(0,245,255,0.3);
  color: #00f5ff;
  background: rgba(0,245,255,0.05);
}
.status-banner.X-wins {
  border: 1px solid rgba(0,245,255,0.6);
  color: #00f5ff;
  background: rgba(0,245,255,0.1);
  text-shadow: 0 0 10px rgba(0,245,255,0.8);
  box-shadow: 0 0 20px rgba(0,245,255,0.2);
}
.status-banner.O-wins {
  border: 1px solid rgba(255,0,255,0.6);
  color: #ff00ff;
  background: rgba(255,0,255,0.1);
  text-shadow: 0 0 10px rgba(255,0,255,0.8);
  box-shadow: 0 0 20px rgba(255,0,255,0.2);
}
.status-banner.draw {
  border: 1px solid rgba(138,43,226,0.6);
  color: #8a2be2;
  background: rgba(138,43,226,0.1);
  text-shadow: 0 0 10px rgba(138,43,226,0.8);
}
</style>
"""

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.markdown(CYBER_CSS + CARD_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:1.5rem 0.5rem 1rem;">
      <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;font-weight:900;
                  letter-spacing:4px;background:linear-gradient(90deg,#00f5ff,#ff00ff);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  background-clip:text;">CYBER//AI</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;
                  color:rgba(0,245,255,0.4);letter-spacing:3px;margin-top:2px;">LAB v2.0.26</div>
    </div>
    <hr style="border:none;height:1px;background:linear-gradient(90deg,#00f5ff,#ff00ff);opacity:0.3;margin:0 0 1rem;"/>
    """, unsafe_allow_html=True)

    module = st.radio(
        "SELECT MODULE",
        ["🎮  TIC-TAC-TOE AI", "📡  SMART NAVIGATION"],
        label_visibility="visible"
    )

    st.markdown("""
    <div style="margin-top:2rem;padding:1rem;
                background:rgba(0,245,255,0.03);
                border:1px solid rgba(0,245,255,0.1);border-radius:3px;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;
                  color:rgba(0,245,255,0.4);letter-spacing:2px;margin-bottom:0.6rem;">ALGORITHMS</div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:0.8rem;color:rgba(200,216,232,0.5);line-height:1.8;">
        ⚡ Minimax<br/>
        ⚡ Alpha-Beta Pruning<br/>
        ⚡ BFS<br/>
        ⚡ DFS
      </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MODULE 1 – TIC-TAC-TOE
# ═══════════════════════════════════════════════════════════════════════════════
if "🎮" in module:

    # ── Init state ──
    if 'board' not in st.session_state:
        st.session_state.board = create_board()
    if 'current_player' not in st.session_state:
        st.session_state.current_player = 'X'
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'win_combo' not in st.session_state:
        st.session_state.win_combo = []
    if 'ai_nodes' not in st.session_state:
        st.session_state.ai_nodes = 0
    if 'ai_time' not in st.session_state:
        st.session_state.ai_time = 0.0
    if 'move_count' not in st.session_state:
        st.session_state.move_count = 0

    board = st.session_state.board

    # ── Header ──
    st.markdown("""
    <div class="cyber-card" style="margin-bottom:1.5rem;">
      <div class="cyber-title">🎮 Tic-Tac-Toe AI</div>
      <div class="cyber-subtitle">MINIMAX + ALPHA-BETA PRUNING // UNBEATABLE ENGINE</div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:0.9rem;color:rgba(200,216,232,0.5);">
        You are <span style="color:#00f5ff;font-weight:700;">X</span> &nbsp;·&nbsp;
        AI is <span style="color:#ff00ff;font-weight:700;">O</span> &nbsp;·&nbsp;
        Click any cell to make your move
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_board, col_stats = st.columns([3, 2], gap="large")

    with col_board:
        winner = st.session_state.winner
        game_over = st.session_state.game_over

        if game_over:
            if winner == 'X':
                status_class, status_msg = "X-wins", "⚡ YOU WIN — SYSTEM BREACH"
            elif winner == 'O':
                status_class, status_msg = "O-wins", "🤖 AI WINS — RESISTANCE FUTILE"
            else:
                status_class, status_msg = "draw", "◈ DRAW — QUANTUM STALEMATE"
        else:
            player_label = "YOUR TURN" if st.session_state.current_player == 'X' else "AI COMPUTING..."
            status_class, status_msg = "playing", f"◈ {player_label}"

        st.markdown(f'<div class="status-banner {status_class}">{status_msg}</div>',
                    unsafe_allow_html=True)

        win_combo = st.session_state.win_combo

        def cell_html(idx, val):
            filled = "filled " if val else ""
            player_cls = val if val else ""
            win_cls = "win " if idx in win_combo else ""
            symbol = val if val else ""
            return (f'<div class="ttt-cell {filled}{player_cls} {win_cls}" '
                    f'data-idx="{idx}">{symbol}</div>')

        grid_html = '<div class="ttt-grid">'
        for i in range(9):
            grid_html += cell_html(i, board[i])
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:0.5rem;'>", unsafe_allow_html=True)
        rows = st.columns([1, 1, 1])
        button_cols = [rows[0], rows[1], rows[2],
                       rows[0], rows[1], rows[2],
                       rows[0], rows[1], rows[2]]

        st.markdown("""
        <div style='font-family:"Share Tech Mono",monospace;font-size:0.65rem;
                    color:rgba(0,245,255,0.3);letter-spacing:2px;
                    text-align:center;margin-top:0.5rem;'>
          CLICK A NUMBERED CELL BELOW TO PLAY
        </div>
        """, unsafe_allow_html=True)

        available = get_available_moves(board)
        btn_rows = [st.columns(3) for _ in range(3)]
        for i in range(9):
            row_idx, col_idx = divmod(i, 3)
            with btn_rows[row_idx][col_idx]:
                if not game_over and st.session_state.current_player == 'X' and board[i] == '':
                    if st.button(f"▢ {i+1}", key=f"cell_{i}"):
                        board[i] = 'X'
                        st.session_state.move_count += 1
                        w, combo = check_winner(board)
                        if w:
                            st.session_state.winner = w
                            st.session_state.win_combo = combo
                            st.session_state.game_over = True
                        elif is_draw(board):
                            st.session_state.game_over = True
                        else:
                            st.session_state.current_player = 'O'
                            move, nodes, elapsed = get_best_move(board)
                            if move != -1:
                                board[move] = 'O'
                                st.session_state.move_count += 1
                                st.session_state.ai_nodes += nodes
                                st.session_state.ai_time += elapsed
                                w2, combo2 = check_winner(board)
                                if w2:
                                    st.session_state.winner = w2
                                    st.session_state.win_combo = combo2
                                    st.session_state.game_over = True
                                elif is_draw(board):
                                    st.session_state.game_over = True
                                else:
                                    st.session_state.current_player = 'X'
                        st.rerun()
                else:
                    cell_val = board[i]
                    label = cell_val if cell_val else "·"
                    st.button(label, key=f"cell_{i}_dis", disabled=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1rem;'>", unsafe_allow_html=True)
        if st.button("⟳  RESET GAME", key="reset_ttt"):
            st.session_state.board = create_board()
            st.session_state.current_player = 'X'
            st.session_state.game_over = False
            st.session_state.winner = None
            st.session_state.win_combo = []
            st.session_state.ai_nodes = 0
            st.session_state.ai_time = 0.0
            st.session_state.move_count = 0
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_stats:
        st.markdown("""
        <div class="cyber-card">
          <div class="section-tag">AI Performance Metrics</div>
        """, unsafe_allow_html=True)

        nodes = st.session_state.ai_nodes
        ai_ms = st.session_state.ai_time
        moves = st.session_state.move_count

        s1, s2 = st.columns(2)
        with s1:
            st.markdown(f"""
            <div class="stat-box">
              <span class="stat-val pink">{nodes:,}</span>
              <span class="stat-label">Nodes Explored</span>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="stat-box">
              <span class="stat-val">{ai_ms:.2f}</span>
              <span class="stat-label">Time (ms)</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="stat-box" style="margin-top:8px;">
          <span class="stat-val green">{moves}</span>
          <span class="stat-label">Total Moves</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="cyber-card" style="margin-top:1rem;">
          <div class="section-tag">Algorithm Info</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.75rem;
                      line-height:1.9;color:rgba(200,216,232,0.6);">
            <span style="color:#00f5ff;">ALGORITHM</span><br/>
            Minimax + α-β Pruning<br/><br/>
            <span style="color:#ff00ff;">COMPLEXITY</span><br/>
            O(b<sup>d/2</sup>) with pruning<br/><br/>
            <span style="color:#8a2be2;">STRATEGY</span><br/>
            Optimal play guaranteed<br/>
            AI never loses<br/><br/>
            <span style="color:#00ff88;">PLAYER</span><br/>
            You = X &nbsp;|&nbsp; AI = O
          </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MODULE 2 – SMART NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════
else:
    if 'nav_graph' not in st.session_state:
        st.session_state.nav_graph = DEFAULT_GRAPH
    if 'nav_results' not in st.session_state:
        st.session_state.nav_results = None

    graph = st.session_state.nav_graph
    nodes = get_all_nodes(graph)

    st.markdown("""
    <div class="cyber-card" style="margin-bottom:1.5rem;">
      <div class="cyber-title">📡 Smart Navigation</div>
      <div class="cyber-subtitle">BFS + DFS PATHFINDING // GRAPH TRAVERSAL ENGINE</div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:0.9rem;color:rgba(200,216,232,0.5);">
        Find optimal routes through the network — compare BFS vs DFS performance
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_graph = st.columns([2, 3], gap="large")

    with col_input:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-tag">Navigation Parameters</div>', unsafe_allow_html=True)

        start_node = st.selectbox("START NODE", nodes, key="nav_start")
        goal_node  = st.selectbox("GOAL NODE",  nodes, index=len(nodes)-1, key="nav_goal")

        st.markdown("<div style='height:8px'/>", unsafe_allow_html=True)

        if st.button("⚡  EXECUTE PATHFINDING", key="run_nav"):
            if start_node == goal_node:
                st.markdown("""
                <div style="font-family:'Share Tech Mono',monospace;font-size:0.75rem;
                            color:#ff2244;padding:0.5rem;border:1px solid rgba(255,34,68,0.3);
                            border-radius:2px;background:rgba(255,34,68,0.05);">
                  ⚠ START == GOAL — SELECT DIFFERENT NODES
                </div>""", unsafe_allow_html=True)
            else:
                bfs_path, bfs_nodes, bfs_time = bfs(graph, start_node, goal_node)
                dfs_path, dfs_nodes, dfs_time = dfs(graph, start_node, goal_node)
                st.session_state.nav_results = {
                    'bfs': {'path': bfs_path, 'nodes': bfs_nodes, 'time': bfs_time},
                    'dfs': {'path': dfs_path, 'nodes': dfs_nodes, 'time': dfs_time},
                    'start': start_node, 'goal': goal_node
                }
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cyber-card" style="margin-top:1rem;">', unsafe_allow_html=True)
        st.markdown('<div class="section-tag">Custom Graph (optional)</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;
                    color:rgba(0,245,255,0.35);line-height:1.7;margin-bottom:0.5rem;">
          FORMAT: A-B,C; B-D,E<br/>
          Leave empty for default city graph
        </div>""", unsafe_allow_html=True)

        custom_graph_txt = st.text_area("GRAPH DEFINITION", value="", height=80,
                                         placeholder="A-B,C; B-D,E; C-F ...")
        if st.button("↺  LOAD GRAPH", key="load_graph"):
            st.session_state.nav_graph = parse_graph(custom_graph_txt)
            st.session_state.nav_results = None
            st.rerun()

        if st.button("⊞  RESET DEFAULT", key="reset_graph"):
            st.session_state.nav_graph = DEFAULT_GRAPH
            st.session_state.nav_results = None
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col_graph:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-tag">Network Map</div>', unsafe_allow_html=True)

        adj_lines = []
        for node_name in sorted(graph.keys()):
            neighbors = graph[node_name]
            nb_str = "  ⟶  " + "  ·  ".join(
                f'<span style="color:#ff00ff">{n}</span>' for n in neighbors
            )
            adj_lines.append(
                f'<span style="color:#00f5ff;font-weight:700;">{node_name}</span>{nb_str}'
            )

        adj_html = "<br/>".join(adj_lines)
        st.markdown(f"""
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.75rem;
                    line-height:2;background:rgba(0,0,0,0.4);
                    border:1px solid rgba(0,245,255,0.12);border-radius:3px;
                    padding:1rem;max-height:280px;overflow-y:auto;">
          {adj_html}
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        results = st.session_state.nav_results
        if results:
            bfs_r = results['bfs']
            dfs_r = results['dfs']
            src, dst = results['start'], results['goal']

            st.markdown(f"""
            <div style="font-family:'Orbitron',sans-serif;font-size:0.8rem;
                        letter-spacing:3px;color:rgba(0,245,255,0.6);
                        margin:1rem 0 0.5rem;text-align:center;">
              {src} &nbsp;⟶&nbsp; {dst}
            </div>""", unsafe_allow_html=True)

            def path_to_html(path):
                if not path:
                    return '<span style="color:#ff2244;">NO PATH FOUND</span>'
                parts = []
                for i, n in enumerate(path):
                    color = "#00ff88" if i == 0 or i == len(path)-1 else "#00f5ff"
                    parts.append(f'<span style="color:{color};font-weight:700;">{n}</span>')
                return '<span class="path-arrow"> → </span>'.join(parts)

            rcol1, rcol2 = st.columns(2, gap="medium")

            with rcol1:
                st.markdown(f"""
                <div class="cyber-card">
                  <div class="neon-label blue" style="margin-bottom:0.6rem;">⚡ BFS PATH</div>
                  <div class="path-display">{path_to_html(bfs_r['path'])}</div>
                  <div style="display:flex;gap:8px;margin-top:0.8rem;">
                    <div class="stat-box" style="flex:1;">
                      <span class="stat-val" style="font-size:1rem;">{bfs_r['nodes']}</span>
                      <span class="stat-label">Nodes</span>
                    </div>
                    <div class="stat-box" style="flex:1;">
                      <span class="stat-val" style="font-size:1rem;">{bfs_r['time']:.3f}</span>
                      <span class="stat-label">ms</span>
                    </div>
                    <div class="stat-box" style="flex:1;">
                      <span class="stat-val green" style="font-size:1rem;">{len(bfs_r['path']) if bfs_r['path'] else 0}</span>
                      <span class="stat-label">Length</span>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with rcol2:
                st.markdown(f"""
                <div class="cyber-card">
                  <div class="neon-label pink" style="margin-bottom:0.6rem;">⚡ DFS PATH</div>
                  <div class="path-display">{path_to_html(dfs_r['path'])}</div>
                  <div style="display:flex;gap:8px;margin-top:0.8rem;">
                    <div class="stat-box" style="flex:1;">
                      <span class="stat-val pink" style="font-size:1rem;">{dfs_r['nodes']}</span>
                      <span class="stat-label">Nodes</span>
                    </div>
                    <div class="stat-box" style="flex:1;">
                      <span class="stat-val pink" style="font-size:1rem;">{dfs_r['time']:.3f}</span>
                      <span class="stat-label">ms</span>
                    </div>
                    <div class="stat-box" style="flex:1;">
                      <span class="stat-val pink" style="font-size:1rem;">{len(dfs_r['path']) if dfs_r['path'] else 0}</span>
                      <span class="stat-label">Length</span>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            if bfs_r['path'] and dfs_r['path']:
                bfs_better_path = len(bfs_r['path']) <= len(dfs_r['path'])
                bfs_faster      = bfs_r['time'] <= dfs_r['time']
                bfs_fewer_nodes = bfs_r['nodes'] <= dfs_r['nodes']

                st.markdown("""
                <div class="cyber-card" style="margin-top:0;">
                  <div class="section-tag">Algorithm Comparison</div>
                  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:0.5rem;">
                """, unsafe_allow_html=True)

                def winner_badge(condition, true_label, false_label):
                    if condition:
                        return (f'<div style="text-align:center;">'
                                f'<span class="neon-label green">✓ {true_label}</span><br/>'
                                f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:0.6rem;'
                                f'color:rgba(200,216,232,0.3);">wins</span></div>')
                    else:
                        return (f'<div style="text-align:center;">'
                                f'<span class="neon-label pink">✓ {false_label}</span><br/>'
                                f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:0.6rem;'
                                f'color:rgba(200,216,232,0.3);">wins</span></div>')

                st.markdown(f"""
                  {winner_badge(bfs_better_path, 'BFS', 'DFS')}
                  {winner_badge(bfs_faster, 'BFS', 'DFS')}
                  {winner_badge(bfs_fewer_nodes, 'BFS', 'DFS')}
                  <div style="text-align:center;font-family:'Share Tech Mono',monospace;
                               font-size:0.6rem;color:rgba(200,216,232,0.4);">SHORTER PATH</div>
                  <div style="text-align:center;font-family:'Share Tech Mono',monospace;
                               font-size:0.6rem;color:rgba(200,216,232,0.4);">FASTER</div>
                  <div style="text-align:center;font-family:'Share Tech Mono',monospace;
                               font-size:0.6rem;color:rgba(200,216,232,0.4);">FEWER NODES</div>
                </div></div>
                """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr/>
<div style="text-align:center;font-family:'Share Tech Mono',monospace;
            font-size:0.6rem;color:rgba(0,245,255,0.2);letter-spacing:3px;
            padding-bottom:0.5rem;">
  CYBER//AI LAB &nbsp;·&nbsp; MINIMAX &nbsp;·&nbsp; ALPHA-BETA &nbsp;·&nbsp; BFS &nbsp;·&nbsp; DFS &nbsp;·&nbsp; v2.0.26
</div>
<div style="text-align:center;padding-bottom:2rem;">
  <span style="font-family:'Orbitron',sans-serif;font-size:0.8rem;font-weight:700;
               letter-spacing:4px;
               background:linear-gradient(90deg,#00f5ff,#ff00ff);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;
               filter:drop-shadow(0 0 8px rgba(0,245,255,0.5));">
    ⚡ MADE BY &nbsp; ARUN SIVAPRASATH &nbsp; ⚡
  </span>
</div>
""", unsafe_allow_html=True)
