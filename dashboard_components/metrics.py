import streamlit as st
import pandas as pd

def display_metrics(current_income, current_expenses, current_balance, income_change, expenses_change):
    st.markdown("""
        <style>
            .metric-card {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Income", f"₹{current_income:.2f}", f"{income_change:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Expenses", f"₹{current_expenses:.2f}", f"{expenses_change:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Balance", f"₹{current_balance:.2f}")
        st.markdown('</div>', unsafe_allow_html=True) 