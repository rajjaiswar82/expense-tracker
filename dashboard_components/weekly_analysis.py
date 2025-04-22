import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def display_weekly_analysis(all_expenses):
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
    st.subheader("Weekly Analysis")
    
    # Group by week and type
    weekly_data = all_expenses.groupby([
        pd.Grouper(key='date', freq='W'),
        'type'
    ])['amount'].sum().unstack().fillna(0)
    
    # Create weekly chart
    fig_weekly = go.Figure()
    fig_weekly.add_trace(go.Bar(
        x=weekly_data.index,
        y=weekly_data['income'],
        name='Income',
        marker_color='#2ecc71'
    ))
    fig_weekly.add_trace(go.Bar(
        x=weekly_data.index,
        y=weekly_data['expense'],
        name='Expenses',
        marker_color='#e74c3c'
    ))
    fig_weekly.update_layout(
        barmode='group',
        title='Weekly Income vs Expenses',
        xaxis_title='Week',
        yaxis_title='Amount (₹)',
        height=400
    )
    st.plotly_chart(fig_weekly, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True) 