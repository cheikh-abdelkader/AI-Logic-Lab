import random

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

def shuffle_question(q):
    choices = q["choices"]
    answers = q["answers"]

    indexed = list(enumerate(choices))
    random.shuffle(indexed)

    new_choices = [c for i, c in indexed]

    # recalcul des bonnes réponses
    new_answers = [
        new_choices.index(choices[i]) for i in answers
    ]

    return {
        "question": q["question"],
        "choices": new_choices,
        "answers": new_answers
    }


def get_questions(n=10):
    q = random.sample(QUESTIONS, k=min(n, len(QUESTIONS)))
    return [shuffle_question(x) for x in q]