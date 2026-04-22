import streamlit as st
from pyswip import Prolog
import sqlite3
import networkx as nx
from pyvis.network import Network
import tempfile
import streamlit.components.v1 as components

# =========================
# INIT
# =========================
st.set_page_config(layout="wide", page_title="AI Logic Lab")

prolog = Prolog()

# =========================
# DB
# =========================
conn = sqlite3.connect("history.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS history (
    user TEXT,
    query TEXT,
    result TEXT
)
""")
conn.commit()

# =========================
# SESSION
# =========================
if "results" not in st.session_state:
    st.session_state.results = []
    st.session_state.index = 0
    st.session_state.user = "student"

# =========================
# LOAD FILE
# =========================
def load_file(file):
    with open("temp.pl", "wb") as f:
        f.write(file.getbuffer())

    prolog.consult("temp.pl")
    st.success("✔ Base Prolog chargée")

# =========================
# QUERY
# =========================
def run_query(q):
    try:
        results = list(prolog.query(q))  # 🔥 toujours complet

        if not results:
            return "false."

        if results == [{}]:
            return "true."

        return "\n".join(
            [" ; ".join([f"{k} = {v}" for k,v in r.items()]) + " ;"
             for r in results]
        )

    except Exception as e:
        return f"Erreur: {e}"

# =========================
# NEXT
# =========================
def next_solution():
    idx = st.session_state.index + 1
    results = st.session_state.results

    if idx >= len(results):
        return "false."

    st.session_state.index = idx
    return format_res(results[idx])

# =========================
# FORMAT
# =========================
def format_res(r):
    return " ; ".join([f"{k} = {v}" for k, v in r.items()]) + " ;"

# =========================
# HISTORY
# =========================
def save_history(q, r):
    c.execute("INSERT INTO history VALUES (?,?,?)",
              (st.session_state.user, q, r))
    conn.commit()

def get_history():
    c.execute("SELECT query, result FROM history")
    return c.fetchall()

# =========================
# GRAPH
# =========================
def show_graph():
    G = nx.Graph()

    facts = list(prolog.query("enfant(X,Y)"))

    for f in facts:
        G.add_edge(f["X"], f["Y"])

    net = Network(height="500px", width="100%")
    net.from_nx(G)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(tmp.name)

    html = open(tmp.name, "r").read()
    components.html(html, height=500)

# =========================
# NL → PROLOG
# =========================
def nl_to_prolog(text):
    text = text.lower()

    if "grand père" in text:
        return "grand_pere(X,dudulle)"
    if "mère" in text:
        return "mere(X,Y)"

    return text

# =========================
# TRACE (simple)
# =========================
def trace(q):
    return f"""
1. Analyse de la requête : {q}
2. Recherche des règles associées
3. Application des faits
4. Résultat obtenu
"""

# =========================
# UI
# =========================
st.title("🧠 AI Logic Lab")

# Sidebar
st.sidebar.header("⚙️ Configuration")
file = st.sidebar.file_uploader("Charger fichier Prolog")

if file:
    load_file(file)

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "💻 Terminal",
    "📊 Graphe",
    "🔍 Trace",
    "📜 Historique"
])

# =========================
# TERMINAL
# =========================
with tab1:
    st.subheader("Prolog Terminal")

    query = st.text_input("Requête ou langage naturel")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶ Run"):
            q = nl_to_prolog(query)
            st.code(run_query(q), language="prolog")

    with col2:
        if st.button("➡ Next (;)"):
            st.code(next_solution(), language="prolog")

# =========================
# GRAPH
# =========================
with tab2:
    st.subheader("Arbre généalogique")
    if st.button("Afficher Graphe"):
        show_graph()

# =========================
# TRACE
# =========================
with tab3:
    st.subheader("Trace d'inférence")
    if st.button("Afficher Trace"):
        st.code(trace(query))

# =========================
# HISTORY
# =========================
with tab4:
    st.subheader("Historique")

    for q, r in get_history():
        st.code(f"?- {q}\n{r}", language="prolog")