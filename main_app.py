import pandas as pd
import streamlit as st
import bcrypt
from database import init_db, get_db, create_user, authenticate_user, add_transaction, get_transactions, delete_transaction, update_transaction
from helper import display_dashboard
from config import custom_css
from datetime import datetime, timedelta
from dashboard_components.metrics import display_metrics
from dashboard_components.weekly_analysis import display_weekly_analysis
from dashboard_components.monthly_analysis import display_monthly_analysis
from login_page import auth_page

# Initialize database
try:
    init_db()
except Exception as e:
    st.error(f"Error initializing database: {str(e)}")
    st.stop()

# Custom CSS for better styling
st.markdown("""
    <style>
        /* Main background and container styles */
        .stApp {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: #ffffff;
        }
        
        .main-container {
            background: linear-gradient(145deg, #2d2d2d 0%, #1a1a1a 100%);
            border-radius: 15px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            border: 1px solid #404040;
        }
        
        /* Auth page styles */
        .auth-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            background: linear-gradient(145deg, #2d2d2d 0%, #1a1a1a 100%);
            border: 1px solid #404040;
        }
        
        .auth-title {
            text-align: center;
            color: #ffffff;
            margin-bottom: 30px;
            font-size: 2em;
            font-weight: bold;
            background: linear-gradient(45deg, #6c5ce7, #a29bfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Transaction form styles */
        .transaction-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            background: linear-gradient(145deg, #2d2d2d 0%, #1a1a1a 100%);
            border: 1px solid #404040;
        }
        
        .transaction-title {
            text-align: center;
            color: #ffffff;
            margin-bottom: 30px;
            background: linear-gradient(45deg, #6c5ce7, #a29bfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Button styles */
        .stButton > button {
            background: linear-gradient(45deg, #6c5ce7, #a29bfe);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(45deg, #a29bfe, #6c5ce7);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        
        /* Input field styles */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div {
            background-color: #2d2d2d;
            border: 1px solid #404040;
            border-radius: 8px;
            padding: 8px 12px;
            transition: all 0.3s ease;
            color: #ffffff;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > div:focus {
            border-color: #6c5ce7;
            box-shadow: 0 0 0 2px rgba(108, 92, 231, 0.3);
        }
        
        /* Card styles */
        .summary-card {
            background: linear-gradient(145deg, #2d2d2d 0%, #1a1a1a 100%);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            border: 1px solid #404040;
            transition: all 0.3s ease;
        }
        
        .summary-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
        }
        
        /* Table styles */
        .stDataFrame {
            background-color: #2d2d2d;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            border: 1px solid #404040;
        }
        
        /* Sidebar styles */
        .css-1d391kg {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: white;
            border-right: 1px solid #404040;
        }
        
        /* Success and error message styles */
        .stAlert {
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
        
        .stAlert.success {
            background: linear-gradient(145deg, #2d3436 0%, #1a1a1a 100%);
            border: 1px solid #00b894;
            color: #00b894;
        }
        
        .stAlert.error {
            background: linear-gradient(145deg, #2d3436 0%, #1a1a1a 100%);
            border: 1px solid #e57373;
            color: #e57373;
        }
        
        /* Password requirements */
        .password-requirements .valid {
            color: #00b894;
        }
        
        .password-requirements .invalid {
            color: #e57373;
        }

        /* Text color for better readability */
        .stMarkdown, .stText, .stNumberInput > label, .stTextInput > label, .stSelectbox > label {
            color: #ffffff !important;
        }

        /* Radio button styles */
        .stRadio > div {
            background-color: #2d2d2d;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #404040;
        }

        /* Checkbox styles */
        .stCheckbox > div {
            background-color: #2d2d2d;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #404040;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("💰 Personal Expense Tracker")
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        auth_page() # type: ignore
    else:
        main_app_page()

def main_app_page():
    user_id = st.session_state.user_id
    st.sidebar.header(f"Welcome, {st.session_state.username}!")
    
    # Navigation
    page = st.sidebar.radio("Menu", ["📊 Dashboard", "💸 Add Transaction", "✂️ Manage Transactions"])
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    try:
        if page == "📊 Dashboard":
            display_dashboard(user_id) # type: ignore
        elif page == "💸 Add Transaction":
            add_transaction_form(user_id)
        elif page == "✂️ Manage Transactions":
            manage_transactions(user_id)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def add_transaction_form(user_id):
    st.markdown("""
        <style>
            .transaction-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                background-color: #ffffff;
            }
            .transaction-title {
                text-align: center;
                color: #2c3e50;
                margin-bottom: 30px;
            }
            .transaction-form {
                padding: 20px;
            }
            .transaction-button {
                width: 100%;
                margin-top: 20px;
            }
            .category-select {
                margin-bottom: 20px;
            }
            .amount-input {
                margin-bottom: 20px;
            }
            .date-picker {
                margin-bottom: 20px;
            }
            .description-box {
                margin-bottom: 20px;
            }
            .tags-input {
                margin-bottom: 20px;
            }
            .recurring-section {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="transaction-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="transaction-title">💸 Add New Transaction</h2>', unsafe_allow_html=True)
    
    # Transaction Type Selection
    trans_type = st.radio(
        "Transaction Type",
        ["income", "expense"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    with st.form("Add Transaction", clear_on_submit=True):
        # Amount and Category
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input(
                "Amount",
                min_value=0.01,
                step=0.01,
                format="%.2f",
                value=0.01,
                help="Enter the transaction amount"
            )
        
        with col2:
            category_options = {
                "income": [
                    "Salary", 
                    "Freelance", 
                    "Investments", 
                    "Dividends",
                    "Rental Income",
                    "Business Income",
                    "Side Hustle",
                    "Gifts",
                    "Refunds",
                    "Interest Income",
                    "Pension",
                    "Social Security",
                    "Other Income"
                ],
                "expense": [
                    "Food & Dining",
                    "Groceries",
                    "Restaurants",
                    "Takeout",
                    "Housing",
                    "Rent",
                    "Mortgage",
                    "Utilities",
                    "Maintenance",
                    "Transport",
                    "Fuel",
                    "Public Transport",
                    "Car Maintenance",
                    "Insurance",
                    "Entertainment",
                    "Movies",
                    "Streaming Services",
                    "Games",
                    "Healthcare",
                    "Medical Bills",
                    "Pharmacy",
                    "Insurance",
                    "Education",
                    "Tuition",
                    "Books",
                    "Courses",
                    "Shopping",
                    "Clothing",
                    "Electronics",
                    "Home Goods",
                    "Personal Care",
                    "Travel",
                    "Flights",
                    "Hotels",
                    "Vacation",
                    "Bills & Utilities",
                    "Internet",
                    "Phone",
                    "Electricity",
                    "Water",
                    "Gas",
                    "Other Expenses"
                ]
            }
            category = st.selectbox(
                "Category",
                category_options[trans_type],
                help="Select the transaction category"
            )
        
        # Date and Recurring Options
        col3, col4 = st.columns(2)
        with col3:
            date = st.date_input(
                "Date",
                value=datetime.now(),
                help="Select the transaction date"
            )
        with col4:
            # Add recurring transaction option with better styling
            st.markdown('<div class="recurring-section">', unsafe_allow_html=True)
            is_recurring = st.checkbox("Recurring Transaction")
            if is_recurring:
                recurrence = st.selectbox(
                    "Recurrence",
                    ["Daily", "Weekly", "Monthly", "Yearly"],
                    help="Select how often this transaction repeats"
                )
                end_date = st.date_input(
                    "End Date",
                    value=date + timedelta(days=365),
                    help="Select when to stop the recurring transaction"
                )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Description with character limit and better styling
        description = st.text_area(
            "Description",
            placeholder="Add a description for this transaction (max 200 characters)",
            max_chars=200,
            help="Add details about this transaction"
        )
        
        # Tags input with better styling
        st.markdown('<div class="tags-input">', unsafe_allow_html=True)
        tags = st.text_input(
            "Tags (optional)",
            placeholder="Enter tags separated by commas",
            help="Add tags to categorize your transaction (e.g., work, personal, urgent)"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        submit_button = st.form_submit_button("💾 Save Transaction", use_container_width=True)
        
        if submit_button:
            if not amount or not category or not date:
                st.error("Please fill in all required fields")
            else:
                if add_transaction(user_id, amount, category, description, date, trans_type, tags):
                    st.success("Transaction saved successfully!")
                else:
                    st.error("Failed to save transaction")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add recent transactions preview with better styling
    st.markdown("### 📝 Recent Transactions")
    try:
        recent_transactions = get_transactions(user_id).head(5)
        if not recent_transactions.empty:
            st.dataframe(
                recent_transactions,
                column_config={
                    "date": st.column_config.DateColumn("Date"),
                    "type": st.column_config.TextColumn("Type"),
                    "category": st.column_config.TextColumn("Category"),
                    "amount": st.column_config.NumberColumn("Amount", format="%.2f"),
                    "description": st.column_config.TextColumn("Description"),
                    "tags": st.column_config.TextColumn("Tags")
                },
                hide_index=True
            )
        else:
            st.info("No recent transactions found")
    except Exception as e:
        st.error(f"Failed to load recent transactions: {str(e)}")

def manage_transactions(user_id):
    st.markdown("""
        <style>
            .manage-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .filter-section {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .transaction-table {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 20px;
            }
            .summary-card {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="manage-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="transaction-title">✂️ Manage Transactions</h2>', unsafe_allow_html=True)
    
    try:
        expenses = get_transactions(user_id)
        
        if not expenses.empty:
            # Convert date column to datetime
            expenses['date'] = pd.to_datetime(expenses['date'],format='mixed')
            
            # Filter section
            st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                date_range = st.selectbox(
                    "Date Range",
                    ["All Time", "Last 7 Days", "Last 30 Days", "Last 3 Months", "Last Year"],
                    index=0
                )
            
            with col2:
                transaction_type = st.selectbox(
                    "Transaction Type",
                    ["All", "Income", "Expense"],
                    index=0
                )
            
            with col3:
                category_filter = st.selectbox(
                    "Category",
                    ["All"] + sorted(expenses['category'].unique().tolist()),
                    index=0
                )
            
            with col4:
                amount_range = st.selectbox(
                    "Amount Range",
                    ["All", "0-100", "100-500", "500-1000", "1000+"],
                    index=0
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Apply filters
            filtered_expenses = expenses.copy()
            
            if date_range != "All Time":
                today = datetime.now()
                if date_range == "Last 7 Days":
                    filtered_expenses = filtered_expenses[filtered_expenses['date'] >= today - timedelta(days=7)]
                elif date_range == "Last 30 Days":
                    filtered_expenses = filtered_expenses[filtered_expenses['date'] >= today - timedelta(days=30)]
                elif date_range == "Last 3 Months":
                    filtered_expenses = filtered_expenses[filtered_expenses['date'] >= today - timedelta(days=90)]
                elif date_range == "Last Year":
                    filtered_expenses = filtered_expenses[filtered_expenses['date'] >= today - timedelta(days=365)]
            
            if transaction_type != "All":
                filtered_expenses = filtered_expenses[filtered_expenses['type'] == transaction_type.lower()]
            
            if category_filter != "All":
                filtered_expenses = filtered_expenses[filtered_expenses['category'] == category_filter]
            
            if amount_range != "All":
                if amount_range == "0-100":
                    filtered_expenses = filtered_expenses[filtered_expenses['amount'] <= 100]
                elif amount_range == "100-500":
                    filtered_expenses = filtered_expenses[(filtered_expenses['amount'] > 100) & (filtered_expenses['amount'] <= 500)]
                elif amount_range == "500-1000":
                    filtered_expenses = filtered_expenses[(filtered_expenses['amount'] > 500) & (filtered_expenses['amount'] <= 1000)]
                elif amount_range == "1000+":
                    filtered_expenses = filtered_expenses[filtered_expenses['amount'] > 1000]
            
            # Summary cards
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                total_amount = filtered_expenses['amount'].sum()
                st.metric("Total Amount", f"₹{total_amount:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                avg_amount = filtered_expenses['amount'].mean()
                st.metric("Average Amount", f"₹{avg_amount:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                transaction_count = len(filtered_expenses)
                st.metric("Number of Transactions", transaction_count)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Transaction table
            st.markdown('<div class="transaction-table">', unsafe_allow_html=True)
            st.subheader("Transactions")
            
            # Add delete column
            filtered_expenses['Delete'] = False
            
            edited_df = st.data_editor(
                filtered_expenses,
                column_config={
                    "id": None,
                    "date": st.column_config.DateColumn("Date"),
                    "type": st.column_config.SelectboxColumn("Type", options=["income", "expense"]),
                    "category": st.column_config.SelectboxColumn("Category", 
                            options=sorted(expenses['category'].unique().tolist())),
                    "amount": st.column_config.NumberColumn("Amount", format="₹%.2f"),
                    "description": st.column_config.TextColumn("Description"),
                    "tags": st.column_config.TextColumn("Tags"),
                    "Delete": st.column_config.CheckboxColumn("Delete", default=False)
                },
                key="expense_editor",
                hide_index=True
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Changes", use_container_width=True):
                    try:
                        for index, row in edited_df.iterrows():
                            if not row['Delete']:  # Only update non-deleted rows
                                if update_transaction(
                                    row['id'],
                                    row['amount'],
                                    row['category'],
                                    row['description'],
                                    row['date'],
                                    row['type'],
                                    row['tags']
                                ):
                                    st.success("Transactions updated successfully!")
                                else:
                                    st.error("Failed to update some transactions")
                    except Exception as e:
                        st.error(f"Failed to update transactions: {str(e)}")
            
            with col2:
                if st.button("🗑️ Delete Selected", use_container_width=True):
                    try:
                        for index, row in edited_df.iterrows():
                            if row['Delete']:  # Delete selected rows
                                if delete_transaction(row['id']):
                                    st.success("Selected transactions deleted successfully!")
                                else:
                                    st.error("Failed to delete some transactions")
                        st.rerun()  # Refresh the page to show updated data
                    except Exception as e:
                        st.error(f"Failed to delete transactions: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export options
            st.markdown("### 📤 Export Data")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Export to CSV", use_container_width=True):
                    csv = filtered_expenses.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="transactions.csv",
                        mime="text/csv"
                    )
            
        else:
            st.info("No transactions found")
    except Exception as e:
        st.error(f"Failed to load transactions: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()