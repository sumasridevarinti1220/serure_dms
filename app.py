import streamlit as st
from pathlib import Path
import json
import hashlib
import uuid
from datetime import datetime



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Secure DMS",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"

ASSETS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)

POLICE_BG = ASSETS_DIR / "police_background.jpg"
LEGAL_BG = ASSETS_DIR / "legal_background.jpg"
FORENSIC_BG = ASSETS_DIR / "forensic_background.jpg"
LOGO = ASSETS_DIR / "logo.png"

USERS_FILE = DATA_DIR / "users.json"
CASES_FILE = DATA_DIR / "cases.json"
DOCUMENTS_FILE = DATA_DIR / "documents.json"
AUDIT_FILE = DATA_DIR / "audit_log.json"
BLOCKCHAIN_FILE = DATA_DIR / "blockchain.json"
ALERTS_FILE = DATA_DIR / "security_alerts.json"
LOGIN_ATTEMPTS_FILE = DATA_DIR / "login_attempts.json"


# ============================================================
# DEFAULT USERS
# ============================================================

DEFAULT_USERS = {
    "admin": {
        "password": "Admin@2026",
        "name": "System Administrator",
        "department": "Administration",
        "role": "ADMIN"
    },

    "police_officer": {
        "password": "Police@2026",
        "name": "Police Officer",
        "department": "Police",
        "role": "OFFICER"
    },

    "forensic_officer": {
        "password": "Forensic@2026",
        "name": "Forensic Officer",
        "department": "Forensic",
        "role": "OFFICER"
    },

    "legal_officer": {
        "password": "Legal@2026",
        "name": "Legal Officer",
        "department": "Legal",
        "role": "OFFICER"
    },

    "investigator": {
        "password": "Invest@2026",
        "name": "Investigator",
        "department": "Investigation",
        "role": "OFFICER"
    },

    "court_officer": {
        "password": "Court@2026",
        "name": "Court Officer",
        "department": "Court",
        "role": "OFFICER"
    },

    "security_admin": {
        "password": "Secure@2026",
        "name": "Security Administrator",
        "department": "Security",
        "role": "OFFICER"
    },

    "police_head": {
        "password": "PoliceHead@2026",
        "name": "Police Department Head",
        "department": "Police",
        "role": "HEAD"
    },

    "forensic_head": {
        "password": "ForensicHead@2026",
        "name": "Forensic Department Head",
        "department": "Forensic",
        "role": "HEAD"
    },

    "legal_head": {
        "password": "LegalHead@2026",
        "name": "Legal Department Head",
        "department": "Legal",
        "role": "HEAD"
    },

    "investigation_head": {
        "password": "InvestHead@2026",
        "name": "Investigation Department Head",
        "department": "Investigation",
        "role": "HEAD"
    },

    "court_head": {
        "password": "CourtHead@2026",
        "name": "Court Department Head",
        "department": "Court",
        "role": "HEAD"
    },

    "security_head": {
        "password": "SecurityHead@2026",
        "name": "Security Department Head",
        "department": "Security",
        "role": "HEAD"
    }
}


# ============================================================
# SAFE HTML RENDERER
# ============================================================

def render_html(content):
    st.html(content)


# ============================================================
# JSON FUNCTIONS
# ============================================================

def load_json(path, default):
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
    except Exception:
        pass

    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():

    users = load_json(
        USERS_FILE,
        {}
    )

    changed = False

    # Add missing accounts automatically
    for username, account in DEFAULT_USERS.items():

        if username not in users:
            users[username] = account
            changed = True

    if changed or not USERS_FILE.exists():
        save_json(
            USERS_FILE,
            users
        )

    if not CASES_FILE.exists():
        save_json(CASES_FILE, [])

    if not DOCUMENTS_FILE.exists():
        save_json(DOCUMENTS_FILE, [])

    if not AUDIT_FILE.exists():
        save_json(AUDIT_FILE, [])

    if not BLOCKCHAIN_FILE.exists():
        save_json(BLOCKCHAIN_FILE, [])

    if not ALERTS_FILE.exists():
        save_json(ALERTS_FILE, [])

    if not LOGIN_ATTEMPTS_FILE.exists():
        save_json(
            LOGIN_ATTEMPTS_FILE,
            {}
        )


initialize_database()


# ============================================================
# HASH FUNCTIONS
# ============================================================

def calculate_hash(data):
    return hashlib.sha256(data).hexdigest()


def hash_text(text):
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


# ============================================================
# BLOCKCHAIN
# ============================================================

def add_blockchain_block(entry):

    chain = load_json(
        BLOCKCHAIN_FILE,
        []
    )

    previous_hash = "GENESIS"

    if chain:
        previous_hash = chain[-1]["current_hash"]

    block = {
        "block_number": len(chain) + 1,
        "timestamp": entry["timestamp"],
        "user": entry["user"],
        "action": entry["action"],
        "details": entry["details"],
        "previous_hash": previous_hash
    }

    block_string = json.dumps(
        block,
        sort_keys=True
    )

    block["current_hash"] = hash_text(
        block_string
    )

    chain.append(block)

    save_json(
        BLOCKCHAIN_FILE,
        chain
    )


# ============================================================
# AUDIT LOG
# ============================================================

def add_audit_log(
    action,
    username,
    details=""
):

    logs = load_json(
        AUDIT_FILE,
        []
    )

    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "user": username,
        "action": action,
        "details": details
    }

    logs.append(entry)

    save_json(
        AUDIT_FILE,
        logs
    )

    add_blockchain_block(entry)


# ============================================================
# SECURITY ALERTS
# ============================================================

DEPARTMENT_HEADS = {
    "Police": "police_head",
    "Forensic": "forensic_head",
    "Legal": "legal_head",
    "Investigation": "investigation_head",
    "Court": "court_head",
    "Security": "security_head"
}


def create_security_alert(
    username,
    department
):

    alerts = load_json(
        ALERTS_FILE,
        []
    )

    assigned_to = DEPARTMENT_HEADS.get(
        department,
        "admin"
    )

    alert = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "username": username,
        "department": department,
        "assigned_to": assigned_to,
        "message": (
            f"More than 3 failed login attempts "
            f"detected for user '{username}'."
        ),
        "status": "UNREAD"
    }

    alerts.append(alert)

    save_json(
        ALERTS_FILE,
        alerts
    )


# ============================================================
# AUTHENTICATION
# ============================================================

def authenticate(username, password):

    users = load_json(
        USERS_FILE,
        {}
    )

    attempts = load_json(
        LOGIN_ATTEMPTS_FILE,
        {}
    )

    if username not in users:
        return False

    user = users[username]

    if password == user["password"]:

        attempts[username] = 0

        save_json(
            LOGIN_ATTEMPTS_FILE,
            attempts
        )

        add_audit_log(
            "LOGIN SUCCESS",
            username,
            "Successful login."
        )

        return True

    attempts[username] = (
        attempts.get(username, 0) + 1
    )

    save_json(
        LOGIN_ATTEMPTS_FILE,
        attempts
    )

    if attempts[username] > 3:

        create_security_alert(
            username,
            user["department"]
        )

        add_audit_log(
            "SECURITY ALERT",
            username,
            "More than 3 failed login attempts."
        )

    else:

        add_audit_log(
            "LOGIN FAILED",
            username,
            f"Failed attempt #{attempts[username]}."
        )

    return False


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "user_info" not in st.session_state:
    st.session_state.user_info = {}


# ============================================================
# CSS
# ============================================================

render_html(
    """
    <style>

    .stApp {
        background-color: #07111F;
        color: #FFFFFF;
    }

    .stApp p,
    .stApp span,
    .stApp label {
        color: #FFFFFF !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #0B1F33 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    input,
    textarea {
        background-color: #102A43 !important;
        color: #FFFFFF !important;
        border: 1px solid #245B78 !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #A9C5D5 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #102A43 !important;
        color: #FFFFFF !important;
    }

    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
    }

    .stButton > button {
        background-color: #176B87 !important;
        color: #FFFFFF !important;
        border: 1px solid #35B9D6 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }

    .stButton > button:hover {
        background-color: #2186A5 !important;
        color: #FFFFFF !important;
    }

    .security-card {
        background-color: #0D263A;
        border: 1px solid #245B78;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .security-title {
        color: #FFFFFF !important;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .security-subtitle {
        color: #D6EAF5 !important;
        font-size: 17px;
        margin-bottom: 20px;
    }

    div[data-testid="stMetric"] {
        background-color: #0D263A !important;
        border: 1px solid #245B78 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }

    div[data-testid="stMetric"] label {
        color: #A9C5D5 !important;
    }

    div[data-testid="stMetric"] div {
        color: #FFFFFF !important;
    }

    details {
        background-color: #0D263A !important;
        border: 1px solid #245B78 !important;
        border-radius: 8px !important;
    }

    details summary {
        color: #FFFFFF !important;
    }

    section[data-testid="stFileUploader"] {
        background-color: #0D263A !important;
        border: 1px solid #245B78 !important;
        border-radius: 10px !important;
    }

    section[data-testid="stFileUploader"] * {
        color: #FFFFFF !important;
    }

    table {
        color: #FFFFFF !important;
    }

    th {
        background-color: #12344A !important;
        color: #FFFFFF !important;
    }

    td {
        background-color: #0D263A !important;
        color: #FFFFFF !important;
    }

    </style>
    """
)


# ============================================================
# BACKGROUND
# ============================================================

def set_background(image_path):

    if image_path.exists():

        image = str(image_path).replace(
            "\\",
            "/"
        )

        render_html(
            f"""
            <style>

            .stApp {{
                background-image:
                    linear-gradient(
                        rgba(7,17,31,0.90),
                        rgba(7,17,31,0.90)
                    ),
                    url("{image}");

                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}

            </style>
            """
        )


# ============================================================
# LOGIN
# ============================================================

def login_page():

    set_background(
        POLICE_BG
    )

    render_html(
        """
        <div style="
            max-width:850px;
            margin:auto;
            text-align:center;
            padding:50px 20px 20px 20px;
        ">

            <div style="
                background:#0B1F33;
                border:1px solid #35B9D6;
                border-radius:20px;
                padding:35px;
            ">

                <div style="
                    font-size:55px;
                ">
                    🔐
                </div>

                <h1 style="
                    color:#FFFFFF !important;
                    font-size:34px;
                ">
                    Secure Digital Document Management System
                </h1>

                <p style="
                    color:#D6EAF5 !important;
                    font-size:18px;
                ">
                    Secure platform for police, legal,
                    forensic and investigation documents
                </p>

            </div>

        </div>
        """
    )

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        render_html(
            """
            <div class="security-card">

                <h2 style="
                    color:#FFFFFF !important;
                ">
                    🔑 Login
                </h2>

                <p style="
                    color:#D6EAF5 !important;
                ">
                    Enter your authorized credentials.
                </p>

            </div>
            """
        )

        username = st.text_input(
            "User ID",
            placeholder="Enter your User ID"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        if st.button(
            "🔐 Login",
            use_container_width=True
        ):

            if not username or not password:

                st.warning(
                    "Please enter both User ID and Password."
                )

            elif authenticate(
                username,
                password
            ):

                users = load_json(
                    USERS_FILE,
                    {}
                )

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_info = users[username]

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )


# ============================================================
# SIDEBAR
# ============================================================

def show_sidebar():

    user = st.session_state.user_info

    with st.sidebar:

        if LOGO.exists():

            st.image(
                str(LOGO),
                width=80
            )

        render_html(
            """
            <h2 style="
                color:#FFFFFF !important;
            ">
                🔐 Secure DMS
            </h2>
            """
        )

        render_html(
            f"""
            <div style="
                background:#12344A;
                border:1px solid #245B78;
                border-radius:10px;
                padding:14px;
            ">

                <p style="color:#FFFFFF !important;">
                    <b>User:</b> {user["name"]}
                </p>

                <p style="color:#FFFFFF !important;">
                    <b>Department:</b> {user["department"]}
                </p>

                <p style="color:#FFFFFF !important;">
                    <b>Role:</b> {user["role"]}
                </p>

            </div>
            """
        )

        st.write("")

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_info = {}

            st.rerun()

        render_html(
            """
            <p style="
                color:#FFFFFF !important;
                font-weight:700;
                font-size:16px;
                margin-top:20px;
            ">
                Navigation
            </p>
            """
        )

        pages = [
            "📊 Dashboard",
            "📁 Cases",
            "📄 Documents",
            "🛡️ Integrity Verification",
            "🔎 Search",
            "⛓️ Blockchain Audit",
            "ℹ️ System Information"
        ]

        if user["role"] in ["ADMIN", "HEAD"]:

            pages.append(
                "🚨 Security Alerts"
            )

            pages.append(
                "📋 Audit Trail"
            )

        if user["role"] == "ADMIN":

            pages.append(
                "👥 User Management"
            )

        return st.radio(
            "Navigation",
            pages,
            label_visibility="collapsed"
        )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_page():

    department = st.session_state.user_info[
        "department"
    ]

    if department == "Police":
        set_background(POLICE_BG)

    elif department == "Legal":
        set_background(LEGAL_BG)

    elif department == "Forensic":
        set_background(FORENSIC_BG)

    else:
        set_background(POLICE_BG)

    cases = load_json(
        CASES_FILE,
        []
    )

    documents = load_json(
        DOCUMENTS_FILE,
        []
    )

    alerts = load_json(
        ALERTS_FILE,
        []
    )

    chain = load_json(
        BLOCKCHAIN_FILE,
        []
    )

    render_html(
        """
        <div class="security-title">
            🏠 Secure DMS Dashboard
        </div>

        <div class="security-subtitle">
            Secure Digital Document Management System
        </div>
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📁 Total Cases",
            len(cases)
        )

    with col2:
        st.metric(
            "📄 Documents",
            len(documents)
        )

    with col3:
        st.metric(
            "🚨 Security Alerts",
            len(alerts)
        )

    with col4:
        st.metric(
            "⛓️ Blockchain Blocks",
            len(chain)
        )

    render_html(
        """
        <div class="security-card">

            <h3 style="color:#FFFFFF !important;">
                🔐 Security Features
            </h3>

            <p style="color:#FFFFFF !important;">
                ✓ Role-based authentication
            </p>

            <p style="color:#FFFFFF !important;">
                ✓ SHA-256 document integrity verification
            </p>

            <p style="color:#FFFFFF !important;">
                ✓ Blockchain-style audit trail
            </p>

            <p style="color:#FFFFFF !important;">
                ✓ Failed-login security alerts
            </p>

            <p style="color:#FFFFFF !important;">
                ✓ Secure case and document management
            </p>

        </div>
        """
    )


# ============================================================
# CASES
# ============================================================

def cases_page():

    st.title("📁 Cases")

    cases = load_json(
        CASES_FILE,
        []
    )

    with st.expander(
        "➕ Create New Case",
        expanded=True
    ):

        case_id = st.text_input(
            "Case ID",
            placeholder="Example: CASE-001"
        )

        title = st.text_input(
            "Case Title"
        )

        department = st.selectbox(
            "Department",
            [
                "Police",
                "Forensic",
                "Legal",
                "Investigation",
                "Court",
                "Security"
            ]
        )

        priority = st.selectbox(
            "Priority",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        )

        description = st.text_area(
            "Case Description"
        )

        if st.button(
            "➕ Create Case",
            use_container_width=True
        ):

            if not case_id or not title:

                st.error(
                    "Please enter Case ID and Case Title."
                )

            elif any(
                case["case_id"] == case_id
                for case in cases
            ):

                st.error(
                    "This Case ID already exists."
                )

            else:

                new_case = {
                    "case_id": case_id,
                    "title": title,
                    "department": department,
                    "priority": priority,
                    "description": description,
                    "created_by": st.session_state.username,
                    "created_at": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "status": "Open"
                }

                cases.append(
                    new_case
                )

                save_json(
                    CASES_FILE,
                    cases
                )

                add_audit_log(
                    "CASE CREATED",
                    st.session_state.username,
                    f"Case {case_id} created."
                )

                st.success(
                    f"Case {case_id} created successfully."
                )

    st.subheader(
        "📂 Existing Cases"
    )

    if not cases:

        st.info(
            "No cases have been created yet."
        )

    for case in reversed(cases):

        with st.expander(
            f'📁 {case["case_id"]} — {case["title"]}'
        ):

            st.write(
                f'**Department:** {case["department"]}'
            )

            st.write(
                f'**Priority:** {case["priority"]}'
            )

            st.write(
                f'**Status:** {case["status"]}'
            )

            st.write(
                f'**Created By:** {case["created_by"]}'
            )

            st.write(
                f'**Created At:** {case["created_at"]}'
            )

            st.write(
                f'**Description:** {case["description"]}'
            )


# ============================================================
# DOCUMENTS
# ============================================================

def documents_page():

    st.title("📄 Documents")

    cases = load_json(
        CASES_FILE,
        []
    )

    documents = load_json(
        DOCUMENTS_FILE,
        []
    )

    if not cases:

        st.warning(
            "Create a case first."
        )

        return

    case_ids = [
        case["case_id"]
        for case in cases
    ]

    selected_case = st.selectbox(
        "Select Case",
        case_ids
    )

    uploaded_file = st.file_uploader(
        "Upload Case Document",
        type=[
            "pdf",
            "docx",
            "txt",
            "jpg",
            "jpeg",
            "png"
        ]
    )

    if uploaded_file:

        file_bytes = uploaded_file.getvalue()

        file_hash = calculate_hash(
            file_bytes
        )

        render_html(
            f"""
            <div class="security-card">

                <h3 style="color:#FFFFFF !important;">
                    📄 Document Information
                </h3>

                <p style="color:#FFFFFF !important;">
                    <b>File:</b> {uploaded_file.name}
                </p>

                <p style="color:#FFFFFF !important;">
                    <b>Size:</b> {len(file_bytes)} bytes
                </p>

                <p style="
                    color:#7DE2A7 !important;
                    word-break:break-all;
                ">
                    <b>SHA-256:</b> {file_hash}
                </p>

            </div>
            """
        )

        if st.button(
            "🔒 Securely Store Document",
            use_container_width=True
        ):

            stored_name = (
                str(uuid.uuid4())
                + "_"
                + uploaded_file.name
            )

            stored_path = (
                UPLOADS_DIR / stored_name
            )

            with open(
                stored_path,
                "wb"
            ) as file:

                file.write(
                    file_bytes
                )

            document = {
                "document_id": str(uuid.uuid4()),
                "case_id": selected_case,
                "file_name": uploaded_file.name,
                "stored_file": stored_name,
                "sha256": file_hash,
                "uploaded_by": st.session_state.username,
                "uploaded_at": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }

            documents.append(
                document
            )

            save_json(
                DOCUMENTS_FILE,
                documents
            )

            add_audit_log(
                "DOCUMENT UPLOADED",
                st.session_state.username,
                f"{uploaded_file.name} uploaded."
            )

            st.success(
                "Document securely stored."
            )

    st.subheader(
        "📚 Stored Documents"
    )

    for document in reversed(documents):

        render_html(
            f"""
            <div class="security-card">

                <h3 style="color:#FFFFFF !important;">
                    📄 {document["file_name"]}
                </h3>

                <p style="color:#FFFFFF !important;">
                    <b>Case:</b> {document["case_id"]}
                </p>

                <p style="color:#FFFFFF !important;">
                    <b>Uploaded By:</b>
                    {document["uploaded_by"]}
                </p>

                <p style="
                    color:#7DE2A7 !important;
                    word-break:break-all;
                ">
                    <b>SHA-256:</b>
                    {document["sha256"]}
                </p>

            </div>
            """
        )


# ============================================================
# INTEGRITY VERIFICATION
# ============================================================

def integrity_page():

    st.title(
        "🛡️ Integrity Verification"
    )

    documents = load_json(
        DOCUMENTS_FILE,
        []
    )

    if not documents:

        st.info(
            "No documents are available."
        )

        return

    choices = [
        f'{doc["file_name"]} — {doc["case_id"]}'
        for doc in documents
    ]

    selected = st.selectbox(
        "Select Document",
        choices
    )

    index = choices.index(
        selected
    )

    document = documents[index]

    file_path = (
        UPLOADS_DIR /
        document["stored_file"]
    )

    render_html(
        f"""
        <div class="security-card">

            <h3 style="color:#FFFFFF !important;">
                🔐 Original Document Hash
            </h3>

            <p style="
                color:#7DE2A7 !important;
                word-break:break-all;
            ">
                {document["sha256"]}
            </p>

        </div>
        """
    )

    if not file_path.exists():

        st.error(
            "Stored document could not be found."
        )

        return

    with open(
        file_path,
        "rb"
    ) as file:

        current_bytes = file.read()

    current_hash = calculate_hash(
        current_bytes
    )

    render_html(
        f"""
        <div class="security-card">

            <h3 style="color:#FFFFFF !important;">
                🔍 Current Document Hash
            </h3>

            <p style="
                color:#FFFFFF !important;
                word-break:break-all;
            ">
                {current_hash}
            </p>

        </div>
        """
    )

    if current_hash == document["sha256"]:

        st.success(
            "🟢 INTEGRITY VERIFIED — Document has not been changed."
        )

    else:

        st.error(
            "🔴 INTEGRITY FAILED — Document has been changed."
        )


# ============================================================
# SEARCH
# ============================================================

def search_page():

    st.title("🔎 Search")

    term = st.text_input(
        "Search cases or documents",
        placeholder="Enter case ID, document name, department..."
    )

    if not term:

        st.info(
            "Enter a search term."
        )

        return

    term = term.lower()

    cases = load_json(
        CASES_FILE,
        []
    )

    documents = load_json(
        DOCUMENTS_FILE,
        []
    )

    matching_cases = [
        case
        for case in cases
        if term in json.dumps(case).lower()
    ]

    matching_documents = [
        document
        for document in documents
        if term in json.dumps(document).lower()
    ]

    st.subheader(
        f"📁 Cases Found: {len(matching_cases)}"
    )

    for case in matching_cases:

        render_html(
            f"""
            <div class="security-card">

                <h3 style="color:#FFFFFF !important;">
                    📁 {case["case_id"]}
                </h3>

                <p style="color:#FFFFFF !important;">
                    <b>Title:</b> {case["title"]}
                </p>

                <p style="color:#FFFFFF !important;">
                    <b>Department:</b>
                    {case["department"]}
                </p>

            </div>
            """
        )

    st.subheader(
        f"📄 Documents Found: {len(matching_documents)}"
    )

    for document in matching_documents:

        render_html(
            f"""
            <div class="security-card">

                <h3 style="color:#FFFFFF !important;">
                    📄 {document["file_name"]}
                </h3>

                <p style="color:#FFFFFF !important;">
                    <b>Case:</b>
                    {document["case_id"]}
                </p>

            </div>
            """
        )


# ============================================================
# BLOCKCHAIN AUDIT
# ============================================================

def blockchain_page():

    st.title(
        "⛓️ Blockchain Audit"
    )

    chain = load_json(
        BLOCKCHAIN_FILE,
        []
    )

    if not chain:

        st.info(
            "No blockchain audit blocks yet."
        )

        return

    render_html(
        """
        <div class="security-card">

            <h3 style="color:#FFFFFF !important;">
                ⛓️ Hash-Linked Audit Chain
            </h3>

            <p style="color:#FFFFFF !important;">
                Every activity creates an audit block.
                Each block contains the hash of the
                previous block, making the audit trail
                tamper-evident.
            </p>

        </div>
        """
    )

    for block in reversed(chain):

        with st.expander(
            f'Block #{block["block_number"]} — {block["action"]}'
        ):

            st.write(
                f'**Time:** {block["timestamp"]}'
            )

            st.write(
                f'**User:** {block["user"]}'
            )

            st.write(
                f'**Action:** {block["action"]}'
            )

            st.write(
                f'**Details:** {block["details"]}'
            )

            st.write(
                "Previous Hash"
            )

            st.code(
                block["previous_hash"]
            )

            st.write(
                "Current Hash"
            )

            st.code(
                block["current_hash"]
            )


# ============================================================
# SECURITY ALERTS
# ============================================================

def security_alerts_page():

    st.title(
        "🚨 Security Alerts"
    )

    alerts = load_json(
        ALERTS_FILE,
        []
    )

    username = st.session_state.username
    role = st.session_state.user_info["role"]

    if role == "ADMIN":

        visible_alerts = alerts

    else:

        visible_alerts = [
            alert
            for alert in alerts
            if alert["assigned_to"] == username
        ]

    if not visible_alerts:

        st.success(
            "No security alerts assigned to you."
        )

        return

    for alert in reversed(
        visible_alerts
    ):

        render_html(
            f"""
            <div style="
                background:#351B22;
                border:1px solid #9B404A;
                border-radius:10px;
                padding:18px;
                margin-bottom:15px;
            ">

                <h3 style="
                    color:#FFB4B4 !important;
                ">
                    🚨 Security Alert
                </h3>

                <p style="color:#FFFFFF !important;">
                    <b>Time:</b>
                    {alert["timestamp"]}
                </p>

                <p style="color:#FFFFFF !important;">
                    <b>User:</b>
                    {alert["username"]}
                </p>

                <p style="color:#FFFFFF !important;">
                    <b>Department:</b>
                    {alert["department"]}
                </p>

                <p style="color:#FFFFFF !important;">
                    <b>Assigned To:</b>
                    {alert["assigned_to"]}
                </p>

                <p style="color:#FFFFFF !important;">
                    <b>Message:</b>
                    {alert["message"]}
                </p>

            </div>
            """
        )


# ============================================================
# AUDIT TRAIL
# ============================================================

def audit_page():

    st.title(
        "📋 Audit Trail"
    )

    logs = load_json(
        AUDIT_FILE,
        []
    )

    if not logs:

        st.info(
            "No audit activity yet."
        )

        return

    for log in reversed(logs):

        with st.expander(
            f'{log["timestamp"]} — {log["action"]}'
        ):

            st.write(
                f'**User:** {log["user"]}'
            )

            st.write(
                f'**Action:** {log["action"]}'
            )

            st.write(
                f'**Details:** {log["details"]}'
            )


# ============================================================
# USER MANAGEMENT
# ============================================================

def user_management_page():

    st.title(
        "👥 User Management"
    )

    users = load_json(
        USERS_FILE,
        {}
    )

    st.write(
        f"Total users: **{len(users)}**"
    )

    for username, user in users.items():

        render_html(
            f"""
            <div class="security-card">

                <h3 style="color:#FFFFFF !important;">
                    👤 {user["name"]}
                </h3>

                <p style="color:#FFFFFF !important;">
                    <b>User ID:</b> {username}
                </p>

                <p style="color:#FFFFFF !important;">
                    <b>Department:</b>
                    {user["department"]}
                </p>

                <p style="color:#FFFFFF !important;">
                    <b>Role:</b> {user["role"]}
                </p>

            </div>
            """
        )


# ============================================================
# SYSTEM INFORMATION
# ============================================================

def system_info_page():

    st.title(
        "ℹ️ System Information"
    )

    render_html(
        """
        <div class="security-card">

            <h2 style="color:#FFFFFF !important;">
                🔐 Secure Digital Document Management System
            </h2>

            <p style="color:#FFFFFF !important;">
                <b>Version:</b> 1.0
            </p>

            <p style="color:#FFFFFF !important;">
                <b>Technology:</b> Python + Streamlit
            </p>

            <p style="color:#FFFFFF !important;">
                <b>Security:</b> SHA-256 + Audit Chain
            </p>

        </div>
        """
    )

    col1, col2 = st.columns(2)

    with col1:

        render_html(
            """
            <div class="security-card">

                <h3 style="color:#FFFFFF !important;">
                    🛡️ Security
                </h3>

                <p style="color:#FFFFFF !important;">
                    ✓ Role-based authentication
                </p>

                <p style="color:#FFFFFF !important;">
                    ✓ SHA-256 document hashing
                </p>

                <p style="color:#FFFFFF !important;">
                    ✓ Integrity verification
                </p>

                <p style="color:#FFFFFF !important;">
                    ✓ Blockchain-style audit
                </p>

                <p style="color:#FFFFFF !important;">
                    ✓ Failed login detection
                </p>

                <p style="color:#FFFFFF !important;">
                    ✓ Department security alerts
                </p>

            </div>
            """
        )

    with col2:

        render_html(
            """
            <div class="security-card">

                <h3 style="color:#FFFFFF !important;">
                    🏢 Departments
                </h3>

                <p style="color:#FFFFFF !important;">
                    ✓ Police
                </p>

                <p style="color:#FFFFFF !important;">
                    ✓ Forensic
                </p>

                <p style="color:#FFFFFF !important;">
                    ✓ Legal
                </p>

                <p style="color:#FFFFFF !important;">
                    ✓ Investigation
                </p>

                <p style="color:#FFFFFF !important;">
                    ✓ Court
                </p>

                <p style="color:#FFFFFF !important;">
                    ✓ Security
                </p>

            </div>
            """
        )


# ============================================================
# MAIN APP
# ============================================================

if not st.session_state.logged_in:

    login_page()

else:

    selected_page = show_sidebar()

    if selected_page == "📊 Dashboard":
        dashboard_page()

    elif selected_page == "📁 Cases":
        cases_page()

    elif selected_page == "📄 Documents":
        documents_page()

    elif selected_page == "🛡️ Integrity Verification":
        integrity_page()

    elif selected_page == "🔎 Search":
        search_page()

    elif selected_page == "⛓️ Blockchain Audit":
        blockchain_page()

    elif selected_page == "🚨 Security Alerts":
        security_alerts_page()

    elif selected_page == "📋 Audit Trail":
        audit_page()

    elif selected_page == "👥 User Management":
        user_management_page()

    elif selected_page == "ℹ️ System Information":
        system_info_page()
