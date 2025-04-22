import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def display_monthly_analysis(all_expenses):
    st.markdown("""
        <style>
            .chart-container {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Monthly Analysis")
    
    # Group by month and type
    monthly_data = all_expenses.groupby([
        pd.Grouper(key='date', freq='M'),
        'type'
    ])['amount'].sum().unstack().fillna(0)
    
    # Create monthly chart
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Scatter(
        x=monthly_data.index,
        y=monthly_data['income'],
        name='Income',
        mode='lines+markers',
        line=dict(color='#2ecc71', width=2)
    ))
    fig_monthly.add_trace(go.Scatter(
        x=monthly_data.index,
        y=monthly_data['expense'],
        name='Expenses',
        mode='lines+markers',
        line=dict(color='#e74c3c', width=2)
    ))
    fig_monthly.update_layout(
        title='Monthly Income vs Expenses Trend',
        xaxis_title='Month',
        yaxis_title='Amount (₹)',
        height=400
    )
    st.plotly_chart(fig_monthly, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True) 