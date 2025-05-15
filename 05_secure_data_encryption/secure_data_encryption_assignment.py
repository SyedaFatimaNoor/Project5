import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.colored_header import colored_header
import hashlib
import json
import os
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Secure Vault",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Generate or load encryption key
def get_encryption_key():
    key_file = 'secret.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

# Initialize encryption
KEY = get_encryption_key()
cipher_suite = Fernet(KEY)

# Data storage
DATA_FILE = 'secure_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Encrypt data
def encrypt_data(text, password):
    return cipher_suite.encrypt(text.encode()).decode()

# Decrypt data
def decrypt_data(encrypted_text, password):
    try:
        return cipher_suite.decrypt(encrypted_text.encode()).decode()
    except:
        return None

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.failed_attempts = 0
    st.session_state.locked_until = None

def check_lockout():
    if st.session_state.locked_until and datetime.now() < st.session_state.locked_until:
        return True
    st.session_state.locked_until = None
    return False

def handle_failed_attempt():
    st.session_state.failed_attempts += 1
    if st.session_state.failed_attempts >= 3:
        st.session_state.locked_until = datetime.now() + timedelta(minutes=5)
        st.error("Too many failed attempts. Please try again in 5 minutes.")
        return True
    return False

# Login page
def login_page():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #6e48aa;'>🔐 Secure Data System</h1>
        <p style='color: #666;'>Please log in to continue</p>
    </div>
    """, unsafe_allow_html=True)
    
    if check_lockout():
        remaining = (st.session_state.locked_until - datetime.now()).seconds // 60 + 1
        st.error(f"🔒 Account locked. Please try again in {remaining} minutes.")
        return
    
    with stylable_container(
        key="login_form",
        css_styles="""
            {
                background-color: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
        """
    ):
        st.markdown("### Login")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Login", type="primary")
            
            if submitted:
                if username == "admin" and password == "admin123":
                    st.session_state.authenticated = True
                    st.session_state.failed_attempts = 0
                    st.rerun()
                else:
                    if handle_failed_attempt():
                        st.rerun()
                    st.error(f"❌ Invalid credentials. {3 - st.session_state.failed_attempts} attempts remaining.")

def store_data_page():
    colored_header(
        label="🔒 Store Encrypted Data",
        description="Securely store your sensitive information",
        color_name="violet-70",
    )
    
    with st.expander("ℹ️ How to use", expanded=False):
        st.markdown("""
        1. Enter a unique identifier for your data
        2. Type or paste your sensitive information
        3. Set a strong password
        4. Click 'Store Securely' to encrypt and save
        """)
    
    stored_data = load_data()
    
    with stylable_container(
        key="store_form",
        css_styles="""
            {
                background-color: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
        """
    ):
        with st.form("store_form"):
            col1, col2 = st.columns(2)
            with col1:
                identifier = st.text_input("Identifier*", placeholder="e.g., personal_notes")
            with col2:
                password = st.text_input("Password*", type="password", placeholder="Choose a strong password")
            
            data = st.text_area("Data to encrypt*", placeholder="Enter your sensitive data here...")
            
            submitted = st.form_submit_button("🔒 Store Securely", type="primary")
            
            if submitted:
                if not all([identifier, data, password]):
                    st.error("All fields are required!")
                else:
                    encrypted = encrypt_data(data, password)
                    stored_data[identifier] = {
                        'data': encrypted,
                        'created_at': datetime.now().isoformat()
                    }
                    save_data(stored_data)
                    st.success("✅ Data encrypted and stored successfully!")

def retrieve_data_page():
    colored_header(
        label="🔑 Retrieve Your Data",
        description="Access your encrypted information",
        color_name="blue-70",
    )
    
    stored_data = load_data()
    
    if not stored_data:
        st.warning("No encrypted data found. Store some data first!")
        return
    
    with stylable_container(
        key="retrieve_container",
        css_styles="""
            {
                background-color: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 2rem;
            }
        """
    ):
        identifier = st.selectbox("Select data to retrieve", [""] + list(stored_data.keys()))
        
        if identifier:
            data = stored_data[identifier]
            created_time = datetime.fromisoformat(data['created_at']).strftime('%B %d, %Y at %I:%M %p')
            st.caption(f"Created: {created_time}")
            
            with st.form("retrieve_form"):
                password = st.text_input("Enter password", type="password", 
                                       placeholder="Enter the password used to encrypt")
                submitted = st.form_submit_button("🔓 Decrypt Data", type="primary")
                
                if submitted:
                    with st.spinner('Decrypting...'):
                        decrypted = decrypt_data(data['data'], password)
                        if decrypted:
                            st.success("✅ Decryption successful!")
                            st.text_area("Decrypted Data", decrypted, height=200, 
                                       disabled=True, label_visibility="collapsed")
                        else:
                            st.error("❌ Incorrect password or corrupted data!")

def main():
    if not st.session_state.authenticated:
        login_page()
        return
    
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=Secure+Vault", use_column_width=True)
        st.markdown("---")
        page = st.radio(
            "Navigation",
            ["🏠 Home", "📥 Store Data", "📤 Retrieve Data", "🚪 Logout"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.caption("Secure Vault v1.0")
    
    if "Home" in page:
        st.title("🔐 Secure Vault")
        st.markdown("""
        <div style='margin-bottom: 2rem;'>
            <p style='font-size: 1.1rem; color: #666;'>
                Your personal secure data storage solution with military-grade encryption.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            with stylable_container(
                key="home_card1",
                css_styles="""
                    {
                        background: linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%);
                        padding: 1.5rem;
                        border-radius: 15px;
                        color: white;
                    }
                """
            ):
                st.markdown("### 🔒 Store Securely")
                st.markdown("Encrypt and store your sensitive information with a password of your choice.")
                if st.button("Store Data", key="store_btn", type="primary"):
                    st.session_state.page = "Store Data"
                    st.rerun()
        
        with col2:
            with stylable_container(
                key="home_card2",
                css_styles="""
                    {
                        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
                        padding: 1.5rem;
                        border-radius: 15px;
                        color: white;
                    }
                """
            ):
                st.markdown("### 🔑 Retrieve Data")
                st.markdown("Access your encrypted data using your unique identifier and password.")
                if st.button("Retrieve Data", key="retrieve_btn", type="primary"):
                    st.session_state.page = "Retrieve Data"
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Statistics")
        data = load_data()
        col1, col2 = st.columns(2)
        col1.metric("Total Stored Items", len(data))
        col2.metric("Last Updated", datetime.now().strftime("%Y-%m-%d %H:%M"))
        
    elif "Store" in page:
        store_data_page()
    elif "Retrieve" in page:
        retrieve_data_page()
    elif "Logout" in page:
        st.session_state.authenticated = False
        st.success("You have been logged out successfully!")
        st.rerun()

if __name__ == "__main__":
    main()