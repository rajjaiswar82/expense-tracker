import streamlit as st
from database import create_user, authenticate_user

def auth_page():
    st.markdown("""
        <style>
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
            .auth-subtitle {
                text-align: center;
                color: #a29bfe;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            .auth-form {
                padding: 20px;
            }
            .auth-input {
                margin-bottom: 20px;
            }
            .auth-button {
                width: 100%;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                margin-top: 20px;
                transition: all 0.3s ease;
            }
            .auth-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            }
            .auth-message {
                text-align: center;
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                font-weight: 500;
            }
            .success-message {
                background: linear-gradient(145deg, #2d3436 0%, #1a1a1a 100%);
                border: 1px solid #00b894;
                color: #00b894;
            }
            .error-message {
                background: linear-gradient(145deg, #2d3436 0%, #1a1a1a 100%);
                border: 1px solid #e57373;
                color: #e57373;
            }
            .auth-footer {
                text-align: center;
                margin-top: 30px;
                color: #a29bfe;
                font-size: 0.9em;
            }
            .auth-tabs {
                margin-bottom: 30px;
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 50px;
            }
            .stTabs [data-baseweb="tab"] {
                padding: 10px 20px;
                font-size: 1.1em;
                font-weight: 500;
            }
            .password-requirements {
                font-size: 0.85em;
                color: #a29bfe;
                margin-top: 5px;
                padding: 10px;
                background-color: #2d2d2d;
                border-radius: 5px;
                border: 1px solid #404040;
            }
            .password-requirements ul {
                margin: 5px 0;
                padding-left: 20px;
            }
            .password-requirements li {
                margin-bottom: 5px;
            }
            .password-requirements .valid {
                color: #00b894;
            }
            .password-requirements .invalid {
                color: #e57373;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Create tabs for Login and Register
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="auth-title">Welcome Back!</h2>', unsafe_allow_html=True)
        st.markdown('<p class="auth-subtitle">Sign in to manage your expenses</p>', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            submit_button = st.form_submit_button("Login", use_container_width=True, type="primary")
            
            if submit_button:
                if not username or not password:
                    st.error("Please fill in all fields")
                else:
                    user_id = authenticate_user(username, password)
                    if user_id:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="auth-title">Create Account</h2>', unsafe_allow_html=True)
        st.markdown('<p class="auth-subtitle">Start tracking your expenses today</p>', unsafe_allow_html=True)
        
        with st.form("register_form", clear_on_submit=True):
            new_user = st.text_input(
                "Username",
                placeholder="Choose a username",
                key="register_username"
            )
            
            new_pass = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password",
                key="register_password"
            )
            
            confirm_pass = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm your password",
                key="register_confirm_password"
            )
            
            # Password requirements
            st.markdown("""
                <div class="password-requirements">
                    Password must contain:
                    <ul>
                        <li class="valid">At least 8 characters</li>
                        <li class="valid">At least one uppercase letter</li>
                        <li class="valid">At least one number</li>
                        <li class="valid">At least one special character</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
            submit_button = st.form_submit_button("Create Account", use_container_width=True, type="primary")
            
            if submit_button:
                if not new_user or not new_pass or not confirm_pass:
                    st.error("Please fill in all fields")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match")
                elif len(new_pass) < 8:
                    st.error("Password must be at least 8 characters long")
                elif not any(c.isupper() for c in new_pass):
                    st.error("Password must contain at least one uppercase letter")
                elif not any(c.isdigit() for c in new_pass):
                    st.error("Password must contain at least one number")
                elif not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in new_pass):
                    st.error("Password must contain at least one special character")
                else:
                    if create_user(new_user, new_pass):
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Username already exists")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a footer
    st.markdown("""
        <div class="auth-footer">
            <p>© 2025 Expense Tracker | Secure & Private</p>
        </div>
    """, unsafe_allow_html=True) 