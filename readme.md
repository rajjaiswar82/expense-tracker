# 💰 Personal Expense Tracker

A modern web application for tracking personal finances with secure authentication, interactive dashboards, and transaction management.



## ✨ Features
- **🔒 Secure Authentication**: Bcrypt password hashing and user sessions
- **📊 Interactive Dashboards**: 
  - Weekly/Monthly/Yearly financial trends
  - Category-wise spending analysis
  - Income vs Expense metrics
- **💸 Transaction Management**:
  - Add income/expenses with rich categorization
  - Recurring transactions support
  - Bulk edit/delete operations
- **🎨 Custom UI**: Themed interface with dark/light mode support
- **📤 Data Export**: Export transactions to CSV

## 🚀 Installation
1. **Prerequisites**:
   - Python 3.8+
   - pip package manager

2. **Setup**:
```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
pip install -r requirements.txt
Run the application:

bash
streamlit run main_app.py
📖 Usage
🔑 Authentication
New users: Register with a username and strong password

Existing users: Login with credentials

📊 Dashboard
View financial metrics (Income, Expenses, Balance)

Interactive charts for spending analysis

Recent transactions list

💸 Adding Transactions
Navigate to "Add Transaction"

Select transaction type (Income/Expense)

Fill amount, category, date, and optional details

Save to record transaction

✂️ Managing Transactions
Filter transactions by date range, type, or category

Edit existing transactions inline

Bulk delete operations

Export filtered data to CSV

⚙️ Configuration
Modify config.py to:

Customize color schemes

Adjust UI styling

Modify chart configurations

🗃️ Database
SQLite database (expense_tracker.db)

Automatic schema initialization

Encrypted password storage

📦 Dependencies
Streamlit - Web framework

Pandas - Data manipulation

Plotly - Interactive visualizations

Bcrypt - Password hashing

See requirements.txt for full list

📜 License
MIT License - Add proper license file


**Note**: 
1. Replace placeholder text (yourusername, license info, etc.) with actual values
2. Add real screenshots for the demo preview
3. Create a proper LICENSE file matching your chosen license
4. Consider adding contribution guidelines and code examples if making public

