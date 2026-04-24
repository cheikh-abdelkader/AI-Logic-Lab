# import streamlit as st
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.datasets import make_blobs

# st.title("🧠 Perceptron Interactive")

# lr = st.slider("Learning Rate", 0.001, 1.0, 0.1)
# epochs = st.slider("Epochs", 10, 500, 100)

# X, y = make_blobs(n_samples=100, centers=2, random_state=0)
# y = y.reshape(-1,1)

# W = np.random.randn(2,1)
# b = np.random.randn(1)

# def sigmoid(z):
#     return 1/(1+np.exp(-z))

# losses = []

# for i in range(epochs):
#     Z = X.dot(W) + b
#     A = sigmoid(Z)

#     loss = -np.mean(y*np.log(A+1e-8) + (1-y)*np.log(1-A+1e-8))
#     losses.append(loss)

#     dW = X.T.dot(A - y)/len(y)
#     db = np.mean(A - y)

#     W -= lr*dW
#     b -= lr*db

# # Plot
# fig, ax = plt.subplots()
# ax.plot(losses)
# ax.set_title("Training Loss")
# st.pyplot(fig)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.datasets import make_blobs

st.set_page_config(layout="wide")

st.title("🧠 Perceptron Interactif Avancé")

# =========================
# SIDEBAR CONTROLS
# =========================
st.sidebar.header("⚙️ Paramètres")

lr = st.sidebar.slider("Learning Rate", 0.001, 1.0, 0.1)
epochs = st.sidebar.slider("Epochs", 10, 300, 100)

# poids manuels
st.sidebar.subheader("🎛️ Poids manuels")
w1 = st.sidebar.slider("w1", -5.0, 5.0, 0.0)
w2 = st.sidebar.slider("w2", -5.0, 5.0, 0.0)
b = st.sidebar.slider("bias (b)", -5.0, 5.0, 0.0)

manual_mode = st.sidebar.checkbox("Utiliser poids manuels", value=False)

# =========================
# DATA
# =========================
X, y = make_blobs(n_samples=100, centers=2, random_state=0)
y = y.reshape(-1, 1)

# =========================
# INIT
# =========================
if manual_mode:
    W = np.array([[w1], [w2]])
    b = np.array([b])
else:
    W = np.random.randn(2, 1)
    b = np.random.randn(1)

# =========================
# SIGMOID
# =========================
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# =========================
# UI CONTAINERS
# =========================
plot_placeholder = st.empty()
loss_placeholder = st.empty()

losses = []

# =========================
# TRAINING ANIMATION
# =========================
run = st.button("🚀 Lancer entraînement")

if run:

    for i in range(epochs):

        Z = X.dot(W) + b
        A = sigmoid(Z)

        loss = -np.mean(y*np.log(A+1e-8) + (1-y)*np.log(1-A+1e-8))
        losses.append(loss)

        dW = X.T.dot(A - y) / len(y)
        db = np.mean(A - y)

        if not manual_mode:
            W -= lr * dW
            b -= lr * db

        # =========================
        # PLOT FRONTIÈRE
        # =========================
        fig, ax = plt.subplots()

        ax.scatter(X[:, 0], X[:, 1], c=y.reshape(-1))

        x1 = np.linspace(X[:, 0].min(), X[:, 0].max(), 100)

        if W[1] != 0:
            x2 = -(W[0]*x1 + b)/W[1]
            ax.plot(x1, x2)

        ax.set_title(f"Iteration {i+1}")

        plot_placeholder.pyplot(fig)
        plt.close(fig)

        # =========================
        # PLOT LOSS
        # =========================
        fig2, ax2 = plt.subplots()
        ax2.plot(losses)
        ax2.set_title("Loss")
        loss_placeholder.pyplot(fig2)
        plt.close(fig2)

        time.sleep(0.05)

# =========================
# EXPLANATION
# =========================
st.markdown("""
### 🎯 Comment utiliser :

- Active mode manuel pour tester tes propres poids
- Lance l'entraînement pour voir :
  - 📉 la loss diminuer
  - 📈 la frontière bouger
- Comprends comment le modèle apprend visuellement
""")