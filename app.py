import streamlit as st
from sympy import latex, symbols, Add, factor
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

# Définir les symboles
x, y, a, b = symbols("x y a b")
transformations = standard_transformations + (implicit_multiplication_application,)

st.title("🧠 Factorisation avec étapes détaillées")
st.write("Entrez une expression (ex : `3x^3 + 12x^2 + 39x`)")

# Entrée utilisateur
user_input = st.text_input("Expression :", "3x^3 + 12x^2 + 39x")
afficher_etapes = st.checkbox("📘 Afficher les étapes")

# Bouton pour lancer la factorisation
if st.button("📤 Factoriser"):
    if user_input.strip():
        try:
            expr = parse_expr(user_input.replace("^", "**"), transformations=transformations)
            grouped = {}

            # Regroupement des termes par degré
            if isinstance(expr, Add):
                for term in expr.args:
                    coeff, var = term.as_coeff_mul()
                    degree = 0
                    for v in var:
                        if v == x:
                            degree += 1
                    grouped.setdefault(degree, []).append(term)
            else:
                coeff, var = expr.as_coeff_mul()
                degree = 0
                for v in var:
                    if v == x:
                        degree += 1
                grouped.setdefault(degree, []).append(expr)

            # Affichage des étapes
            if afficher_etapes:
                st.markdown("### 🔍 Étapes détaillées en langage mathématique")
                for deg in sorted(grouped.keys(), reverse=True):
                    terms = grouped[deg]
                    term_str = " + ".join(
                        [str(t).replace("**", "^").replace("*", "") for t in terms]
                    )
                    label = f"x^{deg}" if deg > 1 else "x" if deg == 1 else "autres"
                    st.latex(rf"\text{{Termes en }} {label} :\ {term_str}")

            # Réécriture + factorisation
            expr_regroupee = sum([sum(terms) for terms in grouped.values()])
            expr_factorisee = factor(expr_regroupee)

            if afficher_etapes:
                st.latex(
                    rf"\text{{Réécriture regroupée : }} {str(expr_regroupee).replace('**', '^').replace('*', '')}"
                )
                st.latex(
                    rf"\text{{Mise en facteur finale : }} {str(expr_factorisee).replace('**', '^').replace('*', '')}"
                )

            # Résultat final au même format que les étapes
            st.markdown("---")
            st.latex(rf"\text{{Résultat final mis en facteur : }} {latex(expr_factorisee)}")
        except Exception as e:
            st.error(f"Erreur lors de l'analyse : {e}")
