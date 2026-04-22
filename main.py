import streamlit as st
import random, time
from db import SessionLocal, User, Result
from auth import create_token, verify_token
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timezone

st.set_page_config(layout="wide")

db = SessionLocal()

# =========================
# CONFIG PROF (SECRET)
# =========================
PROF_EMAIL = "Cheikhahmedtelmoud@gmail.com"
PROF_PASSWORD = "SUPNUM2026"

# =========================
# QUESTIONS
# =========================
QUESTIONS = [
    {
        "question": "Qu’est-ce que l’IA ?",
        "choices": [
            "Un langage de programmation",
            "Un programme simulant l’intelligence humaine",
            "Un système réseau",
            "Un OS"
        ],
        "answers": [1]
    },
    {
        "question": "Qui a proposé le test de Turing ?",
        "choices": ["Einstein", "Turing", "Newton", "Boole"],
        "answers": [1]
    },
    {
        "question": "p ⇒ q est équivalent à :",
        "choices": ["p ∧ q", "¬p ∨ q", "p ∨ q", "¬q"],
        "answers": [1]
    },
    {
        "question": "La négation de (p ∧ q) est :",
        "choices": ["¬p ∧ ¬q", "¬p ∨ ¬q", "p ∨ q", "p ∧ q"],
        "answers": [1]
    },
    {
        "question": "Une FNC est :",
        "choices": [
            "Une disjonction de conjonctions",
            "Une conjonction de disjonctions",
            "Une implication",
            "Une équivalence"
        ],
        "answers": [1]
    },
    {
        "question": "Parmi ces propositions, lesquelles sont des connecteurs logiques ?",
        "choices": ["∧", "∨", "⇒", "∀"],
        "answers": [0, 1, 2]
    },
    {
        "question": "∀ signifie :",
        "choices": ["Existe", "Pour tout", "Non", "Ou"],
        "answers": [1]
    },
    {
        "question": "∃ signifie :",
        "choices": ["Pour tout", "Existe", "Et", "Non"],
        "answers": [1]
    },
    {
        "question": "Variables liées :",
        "choices": [
            "Sous quantificateur",
            "Sans quantificateur",
            "Constantes",
            "Fonctions"
        ],
        "answers": [0]
    },
    {
        "question": "Lesquels sont des prédicats ?",
        "choices": [
            "Homme(x)",
            "x",
            "Aime(x,y)",
            "∀x"
        ],
        "answers": [0, 2]
    },
    {
        "question": "Prolog est basé sur :",
        "choices": [
            "Logique",
            "Réseaux",
            "Graphes",
            "Statistiques"
        ],
        "answers": [0]
    },
    {
        "question": "Backtracking signifie :",
        "choices": [
            "Retour arrière",
            "Compilation",
            "Tri",
            "Optimisation"
        ],
        "answers": [0]
    },
    {
        "question": "Dans enfant(X,Y), que signifie X ?",
        "choices": [
            "Parent",
            "Enfant",
            "Variable libre",
            "Fonction"
        ],
        "answers": [1]
    },
    {
        "question": "parent(X,Y) signifie :",
        "choices": [
            "X est enfant de Y",
            "X est parent de Y",
            "Y est parent de X",
            "X = Y"
        ],
        "answers": [1]
    },
    {
        "question": "grand_pere(X,Y) dépend de :",
        "choices": [
            "parent",
            "homme",
            "femme",
            "mange"
        ],
        "answers": [0,1]
    },
    {
        "question": "Une tautologie est :",
        "choices": [
            "Toujours vraie",
            "Toujours fausse",
            "Parfois vraie",
            "Indéterminée"
        ],
        "answers": [0]
    },
    {
        "question": "¬∀x P(x) est équivalent à :",
        "choices": [
            "∃x ¬P(x)",
            "∀x ¬P(x)",
            "¬∃x P(x)",
            "P(x)"
        ],
        "answers": [0]
    },
    {
        "question": "Quels domaines utilisent la logique des prédicats ?",
        "choices": [
            "IA",
            "Systèmes experts",
            "Bases de données",
            "Tous les précédents"
        ],
        "answers": [3]
    },
    {
        "question": "Prolog utilise :",
        "choices": [
            "Backtracking",
            "Machine learning",
            "Compilation C",
            "GPU"
        ],
        "answers": [0]
    },
    {
        "question": "Un moteur d’inférence fait :",
        "choices": [
            "Déduction logique",
            "Stockage",
            "Affichage",
            "Compression"
        ],
        "answers": [0]
    },
]


def shuffle_q(q):
    idx = list(enumerate(q["choices"]))
    random.shuffle(idx)

    new_choices = [c for i,c in idx]
    new_answers = [new_choices.index(q["choices"][i]) for i in q["answers"]]

    return {**q, "choices": new_choices, "answers": new_answers}

def get_q(n):
    q = random.sample(QUESTIONS, min(n,len(QUESTIONS)))
    return [shuffle_q(x) for x in q]

# =========================
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================
# HOME
# =========================
if st.session_state.page == "home":

    st.title("🧠 AI Logic Platform")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎓 Student"):
            st.session_state.page = "student"

    with col2:
        if st.button("👨‍🏫 Teacher"):
            st.session_state.page = "login"

# =========================
# LOGIN PROF
# =========================
elif st.session_state.page == "login":

    st.title("🔐 Teacher Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email == PROF_EMAIL and password == PROF_PASSWORD:
            token = create_token(email)
            st.session_state.token = token
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("❌ Invalid")

# =========================
# DASHBOARD PROF
# =========================
elif st.session_state.page == "dashboard":

    user = verify_token(st.session_state.get("token", ""))

    if not user:
        st.error("Session expired")
        st.session_state.page = "login"
        st.rerun()

    st.title("📊 Teacher Dashboard")

    results = db.query(Result).all()

    if not results:
        st.warning("No data yet")
    else:
        df = pd.DataFrame([{
            "score": r.score,
            "total": r.total
        } for r in results])

        st.dataframe(df)

        # Chart
        fig, ax = plt.subplots()
        ax.hist(df["score"])
        st.pyplot(fig)

# =========================
# STUDENT FORM
# =========================
elif st.session_state.page == "student":

    st.title("🎓 Student Info")

    name = st.text_input("Nom")
    matricule = st.text_input("Matricule")
    specialite = st.selectbox("Spécialité", ["RSS", "DSI", "DWM"])

    if st.button("Start"):
        user = User(name=name, matricule=matricule, specialite=specialite)
        db.add(user)
        db.commit()

        st.session_state.user_id = user.id
        st.session_state.questions = get_q(15)
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()

        st.session_state.page = "quiz"
        st.rerun()

# =========================
# QUIZ
# =========================
elif st.session_state.page == "quiz":

    q = st.session_state.questions[st.session_state.q_index]

    # Timer question
    if "q_time" not in st.session_state:
        st.session_state.q_time = time.time()

    remaining = 15 - (time.time() - st.session_state.q_time)

    if remaining <= 0:
        st.session_state.q_index += 1
        st.session_state.q_time = time.time()
        st.rerun()

    st.progress(remaining/15)
    st.write(q["question"])

    choice = st.multiselect("Answer", q["choices"])
    idx = [q["choices"].index(x) for x in choice]

    if st.button("Validate"):
        if set(idx) == set(q["answers"]):
            st.session_state.score += 1

        st.session_state.q_index += 1
        st.session_state.q_time = time.time()

        if st.session_state.q_index >= len(st.session_state.questions):
            st.session_state.page = "result"

        st.rerun()

# =========================
# RESULT
# =========================
# =========================
# RESULT
# =========================
elif st.session_state.page == "result":

    score = st.session_state.score
    total = len(st.session_state.questions)
    user_id = st.session_state.user_id
    
    # Get user info
    user = db.query(User).filter(User.id == user_id).first()
    
    st.title("🏆 Result")
    st.metric("Score", f"{score}/{total}")
    st.write(f"**Name:** {user.name}")
    st.write(f"**Specialization:** {user.specialite}")
    
    # Save DB
    result = Result(
        user_id=user_id,
        score=score,
        total=total
    )
    db.add(result)
    db.commit()
    
    # Create PDF function that returns bytes
    def create_pdf_bytes():
        from io import BytesIO
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import inch
        from datetime import datetime, timezone
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Create custom style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='darkblue',
            alignment=1  # Center alignment
        )
        
        # Content
        content = []
        
        # Title
        content.append(Paragraph("Certificate of Completion", title_style))
        content.append(Spacer(1, 0.5*inch))
        
        # Body
        content.append(Paragraph(f"This certifies that <b>{user.name}</b>", styles['Normal']))
        content.append(Spacer(1, 0.2*inch))
        content.append(Paragraph(f"has successfully completed the AI Logic Quiz with a score of:", styles['Normal']))
        content.append(Spacer(1, 0.2*inch))
        content.append(Paragraph(f"<b>{score}/{total}</b> ({score/total*100:.1f}%)", styles['Heading1']))
        content.append(Spacer(1, 0.3*inch))
        content.append(Paragraph(f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        content.append(Spacer(1, 0.2*inch))
        content.append(Paragraph(f"Specialization: {user.specialite}", styles['Normal']))
        
        doc.build(content)
        buffer.seek(0)
        return buffer.getvalue()
    
    # Direct download button
    pdf_bytes = create_pdf_bytes()
    st.download_button(
        label="📄 Download Certificate (PDF)",
        data=pdf_bytes,
        file_name=f"certificate_{user.name}_{datetime.now(timezone.utc).strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()