import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from database import get_db

def display_dashboard(user_id):
    st.markdown("""
        <style>
            .dashboard-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .metric-card {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .chart-container {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .summary-card {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .trend-indicator {
                font-size: 0.8em;
                margin-left: 5px;
            }
            .positive-trend {
                color: #28a745;
            }
            .negative-trend {
                color: #dc3545;
            }
            .budget-progress {
                height: 20px;
                background-color: #f8f9fa;
                border-radius: 10px;
                margin-bottom: 10px;
            }
            .budget-progress-bar {
                height: 100%;
                border-radius: 10px;
                background-color: #28a745;
                transition: width 0.3s ease;
            }
            .budget-warning {
                background-color: #ffc107;
            }
            .budget-danger {
                background-color: #dc3545;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="dashboard-title">📊 Dashboard</h2>', unsafe_allow_html=True)
    
    try:
        with get_db() as conn:
            # Fetch current month's data
            current_month = datetime.now().strftime('%Y-%m')
            expenses = pd.read_sql('''
                SELECT date, type, category, amount 
                FROM expenses 
                WHERE user_id = ? AND strftime('%Y-%m', date) = ?
                ORDER BY date DESC
            ''', conn, params=(user_id, current_month))
            
            # Fetch last month's data for comparison
            last_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
            last_month_expenses = pd.read_sql('''
                SELECT date, type, category, amount 
                FROM expenses 
                WHERE user_id = ? AND strftime('%Y-%m', date) = ?
                ORDER BY date DESC
            ''', conn, params=(user_id, last_month))
            
            # Fetch all data for trend analysis
            all_expenses = pd.read_sql('''
                SELECT date, type, category, amount 
                FROM expenses 
                WHERE user_id = ?
                ORDER BY date ASC
            ''', conn, params=(user_id,))
            
            # Convert date column to datetime
            expenses['date'] = pd.to_datetime(expenses['date'], format='mixed')
            last_month_expenses['date'] = pd.to_datetime(last_month_expenses['date'], format='mixed')
            all_expenses['date'] = pd.to_datetime(all_expenses['date'], format='mixed')

            
            # Calculate metrics
            current_income = expenses[expenses['type'] == 'income']['amount'].sum()
            current_expenses = expenses[expenses['type'] == 'expense']['amount'].sum()
            current_balance = current_income - current_expenses
            
            last_month_income = last_month_expenses[last_month_expenses['type'] == 'income']['amount'].sum()
            last_month_expenses_total = last_month_expenses[last_month_expenses['type'] == 'expense']['amount'].sum()
            
            # Calculate percentage changes
            income_change = ((current_income - last_month_income) / last_month_income * 100) if last_month_income != 0 else 0
            expenses_change = ((current_expenses - last_month_expenses_total) / last_month_expenses_total * 100) if last_month_expenses_total != 0 else 0
            
            # Display metrics
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
            
            # Weekly Analysis
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
            
            # Monthly Analysis
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
            
            # Yearly Analysis
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("Yearly Analysis")
            
            # Group by year and type
            yearly_data = all_expenses.groupby([
                pd.Grouper(key='date', freq='Y'),
                'type'
            ])['amount'].sum().unstack().fillna(0)
            
            # Create yearly chart
            fig_yearly = go.Figure()
            fig_yearly.add_trace(go.Bar(
                x=yearly_data.index.year,
                y=yearly_data['income'],
                name='Income',
                marker_color='#2ecc71'
            ))
            fig_yearly.add_trace(go.Bar(
                x=yearly_data.index.year,
                y=yearly_data['expense'],
                name='Expenses',
                marker_color='#e74c3c'
            ))
            fig_yearly.update_layout(
                barmode='group',
                title='Yearly Income vs Expenses',
                xaxis_title='Year',
                yaxis_title='Amount (₹)',
                height=400
            )
            st.plotly_chart(fig_yearly, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Category Analysis
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("Category Analysis")
            
            # Group by category and type
            category_data = all_expenses.groupby(['category', 'type'])['amount'].sum().unstack().fillna(0)
            
            # Create category chart
            fig_category = go.Figure()
            fig_category.add_trace(go.Bar(
                x=category_data.index,
                y=category_data['income'],
                name='Income',
                marker_color='#2ecc71'
            ))
            fig_category.add_trace(go.Bar(
                x=category_data.index,
                y=category_data['expense'],
                name='Expenses',
                marker_color='#e74c3c'
            ))
            fig_category.update_layout(
                barmode='group',
                title='Category-wise Income vs Expenses',
                xaxis_title='Category',
                yaxis_title='Amount (₹)',
                height=400
            )
            st.plotly_chart(fig_category, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Recent Transactions
            st.markdown('<div class="summary-card">', unsafe_allow_html=True)
            st.subheader("Recent Transactions")
            recent_transactions = expenses.head(10)
            st.dataframe(
                recent_transactions,
                column_config={
                    "date": st.column_config.DateColumn("Date"),
                    "type": st.column_config.TextColumn("Type"),
                    "category": st.column_config.TextColumn("Category"),
                    "amount": st.column_config.NumberColumn("Amount", format="₹%.2f")
                },
                hide_index=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Failed to load dashboard data: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)