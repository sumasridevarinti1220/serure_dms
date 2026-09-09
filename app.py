import streamlit as st
import os
import json
import hashlib
import uuid
from datetime import datetime
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Secure Digital Document Management System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).parent

ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"

ASSETS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)


# ============================================================
# ASSETS
# ============================================================

POLICE_BG = "assets/police_background.jpg"
LEGAL_BG = "assets/legal_background.jpg"
FORENSIC_BG = "assets/forensic_background.jpg"
LOGO = "assets/logo.png"


# ============================================================
# DATA FILES
# ============================================================

USERS_FILE = DATA_DIR / "users.json"
CASES_FILE = DATA_DIR / "cases.json"
DOCUMENTS_FILE = DATA_DIR / "documents.json"
AUDIT_FILE = DATA_DIR / "audit_log.json"
ALERTS_FILE = DATA_DIR / "security_alerts.json"
BLOCKCHAIN_FILE = DATA_DIR / "blockchain.json"
LOGIN_ATTEMPTS_FILE = DATA_DIR / "login_attempts.json"


# ============================================================
# DEFAULT USERS
# ============================================================

DEFAULT_USERS = {

    # ADMIN
    "admin": {
        "username": "admin",
        "password": "Admin@2026",
        "name": "System Administrator",
        "department": "NCRB Administration",
        "role": "admin",
        "active": True
    },

    # POLICE
    "police_officer": {
        "username": "police_officer",
        "password": "Police@2026",
        "name": "Police Officer",
        "department": "Police",
        "role": "officer",
        "active": True
    },

    "police_head": {
        "username": "police_head",
        "password": "PoliceHead@2026",
        "name": "Police Department Head",
        "department": "Police",
        "role": "head",
        "active": True
    },

    # FORENSIC
    "forensic_officer": {
        "username": "forensic_officer",
        "password": "Forensic@2026",
        "name": "Forensic Officer",
        "department": "Forensic",
        "role": "officer",
        "active": True
    },

    "forensic_head": {
        "username": "forensic_head",
        "password": "ForensicHead@2026",
        "name": "Forensic Department Head",
        "department": "Forensic",
        "role": "head",
        "active": True
    },

    # LEGAL
    "legal_officer": {
        "username": "legal_officer",
        "password": "Legal@2026",
        "name": "Legal Officer",
        "department": "Legal",
        "role": "officer",
        "active": True
    },

    "legal_head": {
        "username": "legal_head",
        "password": "LegalHead@2026",
        "name": "Legal Department Head",
        "department": "Legal",
        "role": "head",
        "active": True
    },

    # INVESTIGATION
    "investigator": {
        "username": "investigator",
        "password": "Invest@2026",
        "name": "Investigation Officer",
        "department": "Investigation",
        "role": "officer",
        "active": True
    },

    "investigation_head": {
        "username": "investigation_head",
        "password": "InvestHead@2026",
        "name": "Investigation Department Head",
        "department": "Investigation",
        "role": "head",
        "active": True
    },

    # COURT
    "court_officer": {
        "username": "court_officer",
        "password": "Court@2026",
        "name": "Court Officer",
        "department": "Court",
        "role": "officer",
        "active": True
    },

    "court_head": {
        "username": "court_head",
        "password": "CourtHead@2026",
        "name": "Court Department Head",
        "department": "Court",
        "role": "head",
        "active": True
    },

    # CYBERSECURITY
    "security_admin": {
        "username": "security_admin",
        "password": "Secure@2026",
        "name": "Security Administrator",
        "department": "Cybersecurity",
        "role": "officer",
        "active": True
    },

    "security_head": {
        "username": "security_head",
        "password": "SecurityHead@2026",
        "name": "Cybersecurity Head",
        "department": "Cybersecurity",
        "role": "head",
        "active": True
    }
}


# ============================================================
# JSON FUNCTIONS
# ============================================================

def load_json(file_path, default):

    if not file_path.exists():
        save_json(file_path, default)
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return default


def save_json(file_path, data):

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# INITIALIZE FILES
# ============================================================

def initialize_database():

    if not USERS_FILE.exists():
        save_json(
            USERS_FILE,
            DEFAULT_USERS
        )

    if not CASES_FILE.exists():
        save_json(
            CASES_FILE,
            []
        )

    if not DOCUMENTS_FILE.exists():
        save_json(
            DOCUMENTS_FILE,
            []
        )

    if not AUDIT_FILE.exists():
        save_json(
            AUDIT_FILE,
            []
        )

    if not ALERTS_FILE.exists():
        save_json(
            ALERTS_FILE,
            []
        )

    if not BLOCKCHAIN_FILE.exists():
        save_json(
            BLOCKCHAIN_FILE,
            []
        )

    if not LOGIN_ATTEMPTS_FILE.exists():
        save_json(
            LOGIN_ATTEMPTS_FILE,
            {}
        )


initialize_database()


# ============================================================
# LOAD DATABASE
# ============================================================

users = load_json(
    USERS_FILE,
    DEFAULT_USERS
)

cases = load_json(
    CASES_FILE,
    []
)

documents = load_json(
    DOCUMENTS_FILE,
    []
)

audit_logs = load_json(
    AUDIT_FILE,
    []
)

security_alerts = load_json(
    ALERTS_FILE,
    []
)

blockchain = load_json(
    BLOCKCHAIN_FILE,
    []
)

login_attempts = load_json(
    LOGIN_ATTEMPTS_FILE,
    {}
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def current_time():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def generate_id(prefix):

    return (
        f"{prefix}-"
        f"{uuid.uuid4().hex[:10].upper()}"
    )


# ============================================================
# AUDIT LOG
# ============================================================

def add_audit_log(
    username,
    action,
    description,
    department="System"
):

    global audit_logs

    entry = {
        "id": generate_id("AUDIT"),
        "timestamp": current_time(),
        "username": username,
        "department": department,
        "action": action,
        "description": description
    }

    audit_logs.append(entry)

    save_json(
        AUDIT_FILE,
        audit_logs
    )


# ============================================================
# SHA-256
# ============================================================

def hash_file(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:

        for chunk in iter(
            lambda: f.read(4096),
            b""
        ):

            sha256.update(chunk)

    return sha256.hexdigest()


# ============================================================
# BLOCKCHAIN
# ============================================================

def add_blockchain_record(
    username,
    action,
    document_hash="",
    details=""
):

    global blockchain

    previous_hash = "GENESIS"

    if blockchain:

        previous_hash = blockchain[-1]["block_hash"]

    block = {

        "block_id":
            len(blockchain) + 1,

        "timestamp":
            current_time(),

        "username":
            username,

        "action":
            action,

        "document_hash":
            document_hash,

        "details":
            details,

        "previous_hash":
            previous_hash
    }

    raw = json.dumps(
        block,
        sort_keys=True
    )

    block["block_hash"] = hashlib.sha256(
        raw.encode()
    ).hexdigest()

    blockchain.append(block)

    save_json(
        BLOCKCHAIN_FILE,
        blockchain
    )


# ============================================================
# FIND DEPARTMENT HEAD
# ============================================================

def get_department_head(department):

    for username, user in users.items():

        if (
            user.get("department") == department
            and user.get("role") == "head"
        ):

            return username

    return None


# ============================================================
# SECURITY ALERT
# ============================================================

def create_security_alert(
    attempted_username,
    department,
    attempt_count
):

    global security_alerts

    head_username = get_department_head(
        department
    )

    alert = {

        "id":
            generate_id("ALERT"),

        "timestamp":
            current_time(),

        "attempted_username":
            attempted_username,

        "department":
            department,

        "attempt_count":
            attempt_count,

        "head_username":
            head_username,

        "message":
            (
                "More than 3 failed login attempts "
                f"were detected for username "
                f"'{attempted_username}' in the "
                f"{department} department."
            ),

        "status":
            "Unread"
    }

    security_alerts.append(alert)

    save_json(
        ALERTS_FILE,
        security_alerts
    )

    add_audit_log(
        "SYSTEM",
        "SECURITY_ALERT",
        alert["message"],
        department
    )

    add_blockchain_record(
        "SYSTEM",
        "SECURITY_ALERT",
        details=alert["message"]
    )


# ============================================================
# LOGIN ATTEMPT TRACKING
# ============================================================

def record_failed_login(username):

    global login_attempts

    if username not in login_attempts:

        login_attempts[username] = {
            "count": 0,
            "last_attempt": ""
        }

    login_attempts[username]["count"] += 1

    login_attempts[username]["last_attempt"] = (
        current_time()
    )

    save_json(
        LOGIN_ATTEMPTS_FILE,
        login_attempts
    )

    return login_attempts[username]["count"]


def reset_failed_login(username):

    global login_attempts

    if username in login_attempts:

        login_attempts[username] = {
            "count": 0,
            "last_attempt": ""
        }

        save_json(
            LOGIN_ATTEMPTS_FILE,
            login_attempts
        )


# ============================================================
# AUTHENTICATION
# ============================================================

def authenticate(
    username,
    password
):

    if username not in users:

        return (
            False,
            "Invalid username or password."
        )

    user = users[username]

    if not user.get("active", True):

        return (
            False,
            "This account is disabled."
        )

    if password == user.get("password"):

        reset_failed_login(username)

        add_audit_log(
            username,
            "LOGIN_SUCCESS",
            "Successful login.",
            user["department"]
        )

        add_blockchain_record(
            username,
            "LOGIN_SUCCESS",
            details="Successful login"
        )

        return (
            True,
            "Login successful."
        )

    count = record_failed_login(
        username
    )

    department = user.get(
        "department",
        "Unknown"
    )

    if count > 3:

        create_security_alert(
            username,
            department,
            count
        )

        return (
            False,
            "Incorrect password. "
            f"Security alert created for "
            f"{department} Department Head."
        )

    remaining = 4 - count

    return (
        False,
        f"Incorrect password. "
        f"Failed attempt {count}. "
        f"{remaining} attempt(s) remaining."
    )


# ============================================================
# SESSION
# ============================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "username" not in st.session_state:

    st.session_state.username = ""

if "user" not in st.session_state:

    st.session_state.user = None


# ============================================================
# IMPROVED CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ================================
       MAIN PAGE
       ================================ */

    .stApp {
        background-color: #07111F;
    }

    .main {
        background-color: #07111F;
    }

    /* ================================
       SIDEBAR
       ================================ */

    section[data-testid="stSidebar"] {

        background-color: #0B1F33 !important;

    }

    section[data-testid="stSidebar"] * {

        color: #FFFFFF !important;

    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {

        color: #35B9D6 !important;

    }

    /* Sidebar radio text */

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label {

        color: #FFFFFF !important;

        background-color: transparent !important;

    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label p {

        color: #FFFFFF !important;

        font-weight: 600 !important;

    }

    /* Selected sidebar item */

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label[data-checked="true"] {

        background-color: #174B67 !important;

        border-radius: 8px;

    }

    /* ================================
       ALL MAIN TEXT
       ================================ */

    .stApp p,
    .stApp label,
    .stApp span {

        color: #FFFFFF;

    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4 {

        color: #FFFFFF !important;

    }

    /* ================================
       INPUTS
       ================================ */

    input,
    textarea {

        color: #FFFFFF !important;

        background-color: #102B42 !important;

        border: 1px solid #35728E !important;

    }

    input::placeholder,
    textarea::placeholder {

        color: #A8C5D5 !important;

    }

    /* ================================
       SELECTBOX
       ================================ */

    div[data-baseweb="select"] {

        background-color: #102B42 !important;

    }

    div[data-baseweb="select"] * {

        color: #FFFFFF !important;

    }

    /* ================================
       BUTTONS
       ================================ */

    .stButton button {

        background-color: #174B67 !important;

        color: #FFFFFF !important;

        border: 1px solid #35B9D6 !important;

        font-weight: bold;

    }

    .stButton button:hover {

        background-color: #226987 !important;

        color: #FFFFFF !important;

    }

    /* ================================
       CARDS
       ================================ */

    .security-card {

        padding: 20px;

        border-radius: 12px;

        background-color: #0D263A;

        border: 1px solid #245B78;

        margin-bottom: 15px;

    }

    .security-title {

        color: #35B9D6 !important;

        font-size: 28px;

        font-weight: bold;

    }

    .security-subtitle {

        color: #D6EAF5 !important;

        font-size: 15px;

    }

    /* ================================
       METRICS
       ================================ */

    div[data-testid="stMetric"] {

        background-color: #0D263A;

        padding: 15px;

        border-radius: 10px;

        border: 1px solid #245B78;

    }

    div[data-testid="stMetric"] label {

        color: #B9D5E5 !important;

    }

    div[data-testid="stMetric"] div {

        color: #FFFFFF !important;

    }

    /* ================================
       ALERT
       ================================ */

    .alert-box {

        padding: 15px;

        border-radius: 10px;

        background-color: #3A1820;

        border-left: 5px solid #D9534F;

        margin-bottom: 10px;

    }

    /* ================================
       EXPANDERS
       ================================ */

    .streamlit-expanderHeader {

        background-color: #102B42 !important;

        color: #FFFFFF !important;

    }

    .streamlit-expanderHeader p {

        color: #FFFFFF !important;

    }

    /* ================================
       FILE UPLOADER
       ================================ */

    [data-testid="stFileUploader"] {

        background-color: #102B42 !important;

        border-radius: 10px;

        padding: 10px;

    }

    [data-testid="stFileUploader"] * {

        color: #FFFFFF !important;

    }

    /* ================================
       INFO / SUCCESS / WARNING
       ================================ */

    .stAlert p {

        color: #FFFFFF !important;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.markdown(
        """
        <h1 style="
            text-align:center;
            color:#35B9D6 !important;
        ">
        🔐 Secure Digital Document Management System
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            color:#D6EAF5 !important;
        ">
        NCRB • Police • Investigation • Forensic • Legal • Court
        </p>
        """,
        unsafe_allow_html=True
    )

    if os.path.exists(POLICE_BG):

        st.image(
            POLICE_BG,
            use_container_width=True
        )

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.markdown(
            "<div class='security-card'>",
            unsafe_allow_html=True
        )

        if os.path.exists(LOGO):

            st.image(
                LOGO,
                width=120
            )

        st.subheader(
            "Secure Login"
        )

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        if st.button(
            "🔓 Login",
            use_container_width=True
        ):

            if not username or not password:

                st.warning(
                    "Please enter username and password."
                )

            else:

                success, message = authenticate(
                    username.strip(),
                    password
                )

                if success:

                    st.session_state.logged_in = True

                    st.session_state.username = (
                        username.strip()
                    )

                    st.session_state.user = users[
                        username.strip()
                    ]

                    st.rerun()

                else:

                    st.error(message)

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ============================================================
# SIDEBAR
# ============================================================

def sidebar():

    user = st.session_state.user

    st.sidebar.title(
        "🔐 Secure DMS"
    )

    if os.path.exists(LOGO):

        st.sidebar.image(
            LOGO,
            width=120
        )

    st.sidebar.markdown(
        f"""
        <div style="
            color:#FFFFFF;
            background:#102B42;
            padding:12px;
            border-radius:8px;
        ">
        <b>User:</b> {user['name']}<br>
        <b>Department:</b> {user['department']}<br>
        <b>Role:</b> {user['role'].upper()}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        add_audit_log(
            st.session_state.username,
            "LOGOUT",
            "User logged out.",
            user["department"]
        )

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user = None

        st.rerun()


# ============================================================
# DASHBOARD HEADER
# ============================================================

def dashboard_header():

    user = st.session_state.user

    st.markdown(
        f"""
        <div class="security-card">

            <div class="security-title">
                Secure Digital Document Management System
            </div>

            <div class="security-subtitle">

                Logged in as:
                <b>{user['name']}</b>

                &nbsp; | &nbsp;

                Department:
                <b>{user['department']}</b>

                &nbsp; | &nbsp;

                Role:
                <b>{user['role'].upper()}</b>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================

def overview_page():

    st.header(
        "📊 Dashboard"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Cases",
        len(cases)
    )

    c2.metric(
        "Documents",
        len(documents)
    )

    c3.metric(
        "Security Alerts",
        len(security_alerts)
    )

    c4.metric(
        "Audit Events",
        len(audit_logs)
    )

    st.divider()

    user = st.session_state.user

    if user["department"] == "Police":

        if os.path.exists(POLICE_BG):

            st.image(
                POLICE_BG,
                use_container_width=True
            )

    elif user["department"] == "Legal":

        if os.path.exists(LEGAL_BG):

            st.image(
                LEGAL_BG,
                use_container_width=True
            )

    elif user["department"] == "Forensic":

        if os.path.exists(FORENSIC_BG):

            st.image(
                FORENSIC_BG,
                use_container_width=True
            )

    st.subheader(
        "🔒 Security Status"
    )

    st.success(
        "SHA-256 document integrity verification: ENABLED"
    )

    st.success(
        "Audit logging: ENABLED"
    )

    st.success(
        "Blockchain-style audit chain: ENABLED"
    )

    st.success(
        "Failed-login monitoring: ENABLED"
    )


# ============================================================
# CASES
# ============================================================

def cases_page():

    st.header(
        "📁 Cases"
    )

    with st.expander(
        "➕ Create New Case"
    ):

        case_number = st.text_input(
            "Case Number"
        )

        title = st.text_input(
            "Case Title"
        )

        description = st.text_area(
            "Case Description"
        )

        department = st.selectbox(
            "Department",
            [
                "Police",
                "Investigation",
                "Forensic",
                "Legal",
                "Court"
            ]
        )

        if st.button(
            "Create Case",
            use_container_width=True
        ):

            if not case_number or not title:

                st.warning(
                    "Case number and title are required."
                )

            else:

                new_case = {

                    "case_id":
                        generate_id("CASE"),

                    "case_number":
                        case_number,

                    "title":
                        title,

                    "description":
                        description,

                    "department":
                        department,

                    "created_by":
                        st.session_state.username,

                    "created_at":
                        current_time(),

                    "status":
                        "Open"
                }

                cases.append(
                    new_case
                )

                save_json(
                    CASES_FILE,
                    cases
                )

                add_audit_log(
                    st.session_state.username,
                    "CREATE_CASE",
                    f"Created case {case_number}",
                    st.session_state.user["department"]
                )

                add_blockchain_record(
                    st.session_state.username,
                    "CREATE_CASE",
                    details=case_number
                )

                st.success(
                    "Case created successfully."
                )

                st.rerun()

    st.subheader(
        "Registered Cases"
    )

    if not cases:

        st.info(
            "No cases available."
        )

        return

    for case in cases:

        with st.expander(
            f"{case['case_number']} — {case['title']}"
        ):

            st.write(
                f"**Case ID:** {case['case_id']}"
            )

            st.write(
                f"**Department:** {case['department']}"
            )

            st.write(
                f"**Status:** {case['status']}"
            )

            st.write(
                f"**Created:** {case['created_at']}"
            )

            st.write(
                f"**Description:** {case['description']}"
            )


# ============================================================
# DOCUMENTS
# ============================================================

def documents_page():

    st.header(
        "📄 Secure Documents"
    )

    if not cases:

        st.warning(
            "Create a case before uploading documents."
        )

        return

    case_options = [
        f"{c['case_number']} | {c['title']}"
        for c in cases
    ]

    selected_case = st.selectbox(
        "Select Case",
        case_options
    )

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=[
            "pdf",
            "docx",
            "doc",
            "txt",
            "jpg",
            "jpeg",
            "png",
            "xlsx"
        ]
    )

    classification = st.selectbox(
        "Classification",
        [
            "Confidential",
            "Highly Confidential",
            "Evidence",
            "Legal Document",
            "Investigation Report",
            "Forensic Report"
        ]
    )

    if uploaded_file:

        if st.button(
            "🔒 Secure Upload",
            use_container_width=True
        ):

            safe_name = (
                uuid.uuid4().hex
                + "_"
                + uploaded_file.name
            )

            save_path = (
                UPLOAD_DIR /
                safe_name
            )

            with open(
                save_path,
                "wb"
            ) as f:

                f.write(
                    uploaded_file.getbuffer()
                )

            document_hash = hash_file(
                save_path
            )

            case_number = selected_case.split(
                " | "
            )[0]

            document = {

                "document_id":
                    generate_id("DOC"),

                "case_number":
                    case_number,

                "original_filename":
                    uploaded_file.name,

                "stored_filename":
                    safe_name,

                "classification":
                    classification,

                "uploaded_by":
                    st.session_state.username,

                "department":
                    st.session_state.user["department"],

                "uploaded_at":
                    current_time(),

                "sha256":
                    document_hash,

                "status":
                    "Verified"
            }

            documents.append(
                document
            )

            save_json(
                DOCUMENTS_FILE,
                documents
            )

            add_audit_log(
                st.session_state.username,
                "DOCUMENT_UPLOAD",
                uploaded_file.name,
                st.session_state.user["department"]
            )

            add_blockchain_record(
                st.session_state.username,
                "DOCUMENT_UPLOAD",
                document_hash,
                uploaded_file.name
            )

            st.success(
                "Document uploaded successfully."
            )

            st.write(
                "SHA-256:"
            )

            st.code(
                document_hash
            )

    st.divider()

    st.subheader(
        "Stored Documents"
    )

    for document in documents:

        with st.expander(
            document["original_filename"]
        ):

            st.write(
                f"**Case:** {document['case_number']}"
            )

            st.write(
                f"**Classification:** "
                f"{document['classification']}"
            )

            st.write(
                f"**Uploaded By:** "
                f"{document['uploaded_by']}"
            )

            st.write(
                f"**Department:** "
                f"{document['department']}"
            )

            st.code(
                document["sha256"]
            )


# ============================================================
# INTEGRITY
# ============================================================

def integrity_page():

    st.header(
        "🛡️ Document Integrity Verification"
    )

    if not documents:

        st.info(
            "No documents available."
        )

        return

    selected = st.selectbox(
        "Select Document",
        [
            d["original_filename"]
            for d in documents
        ]
    )

    document = next(
        d for d in documents
        if d["original_filename"] == selected
    )

    path = (
        UPLOAD_DIR /
        document["stored_filename"]
    )

    if not path.exists():

        st.error(
            "Document file is missing."
        )

        return

    current_hash = hash_file(
        path
    )

    st.write(
        "**Original SHA-256:**"
    )

    st.code(
        document["sha256"]
    )

    st.write(
        "**Current SHA-256:**"
    )

    st.code(
        current_hash
    )

    if current_hash == document["sha256"]:

        st.success(
            "✅ DOCUMENT INTEGRITY VERIFIED"
        )

    else:

        st.error(
            "🚨 DOCUMENT MAY HAVE BEEN MODIFIED"
        )


# ============================================================
# SECURITY ALERTS
# ============================================================

def security_alerts_page():

    st.header(
        "🚨 Security Alerts"
    )

    user = st.session_state.user

    if user["role"] == "admin":

        visible_alerts = security_alerts

    elif user["role"] == "head":

        visible_alerts = [

            alert
            for alert in security_alerts

            if alert["head_username"]
            == st.session_state.username

        ]

    else:

        st.info(
            "Only administrators and department heads "
            "can view security alerts."
        )

        return

    if not visible_alerts:

        st.success(
            "No security alerts."
        )

        return

    for alert in reversed(
        visible_alerts
    ):

        st.markdown(
            f"""
            <div class="alert-box">

            <b style="color:#FFFFFF;">
            🚨 SECURITY ALERT
            </b>

            <br><br>

            <span style="color:#FFFFFF;">
            <b>Alert ID:</b> {alert['id']}<br>
            <b>Time:</b> {alert['timestamp']}<br>
            <b>Department:</b> {alert['department']}<br>
            <b>Username:</b> {alert['attempted_username']}<br>
            <b>Failed Attempts:</b> {alert['attempt_count']}
            </span>

            <br><br>

            <span style="color:#FFFFFF;">
            {alert['message']}
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# AUDIT
# ============================================================

def audit_page():

    st.header(
        "🧾 Audit Trail"
    )

    if not audit_logs:

        st.info(
            "No audit records."
        )

        return

    for log in reversed(
        audit_logs
    ):

        st.markdown(
            f"""
            <div class="security-card">

            <span style="color:#35B9D6;">
            <b>{log['action']}</b>
            </span>

            <br><br>

            <span style="color:#FFFFFF;">
            Time: {log['timestamp']}<br>
            User: {log['username']}<br>
            Department: {log['department']}<br>
            Description: {log['description']}
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# BLOCKCHAIN
# ============================================================

def blockchain_page():

    st.header(
        "⛓️ Blockchain Audit Chain"
    )

    if not blockchain:

        st.info(
            "No blockchain records."
        )

        return

    for block in reversed(
        blockchain
    ):

        with st.expander(
            f"Block #{block['block_id']} "
            f"— {block['action']}"
        ):

            st.write(
                f"Timestamp: {block['timestamp']}"
            )

            st.write(
                f"User: {block['username']}"
            )

            st.write(
                f"Action: {block['action']}"
            )

            st.write(
                f"Details: {block['details']}"
            )

            st.write(
                "Previous Hash:"
            )

            st.code(
                block["previous_hash"]
            )

            st.write(
                "Block Hash:"
            )

            st.code(
                block["block_hash"]
            )


# ============================================================
# USER MANAGEMENT
# ============================================================

def user_management_page():

    st.header(
        "👥 User Management"
    )

    if st.session_state.user["role"] != "admin":

        st.error(
            "Administrator access required."
        )

        return

    for username, account in users.items():

        st.markdown(
            f"""
            <div class="security-card">

            <span style="color:#FFFFFF;">

            <b>{account['name']}</b><br><br>

            Username: {username}<br>

            Department: {account['department']}<br>

            Role: {account['role'].upper()}<br>

            Status:
            {"Active" if account["active"] else "Disabled"}

            </span>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# SEARCH
# ============================================================

def search_page():

    st.header(
        "🔎 Secure Search"
    )

    query = st.text_input(
        "Search cases or documents"
    )

    if not query:

        st.info(
            "Enter a search term."
        )

        return

    query = query.lower()

    st.subheader(
        "Cases"
    )

    found_case = False

    for case in cases:

        if query in json.dumps(
            case
        ).lower():

            found_case = True

            st.write(
                f"📁 {case['case_number']} "
                f"— {case['title']}"
            )

    if not found_case:

        st.write(
            "No matching cases."
        )

    st.subheader(
        "Documents"
    )

    found_document = False

    for document in documents:

        if query in json.dumps(
            document
        ).lower():

            found_document = True

            st.write(
                f"📄 {document['original_filename']}"
            )

    if not found_document:

        st.write(
            "No matching documents."
        )


# ============================================================
# SYSTEM INFO
# ============================================================

def system_info_page():

    st.header(
        "ℹ️ System Information"
    )

    st.markdown(
        """
        <div class="security-card">

        <h3 style="color:#35B9D6 !important;">
        Secure Digital Document Management System
        </h3>

        <p style="color:#FFFFFF !important;">
        <b>Problem Statement:</b> 26190
        </p>

        <p style="color:#FFFFFF !important;">
        <b>Theme:</b> Blockchain & Cybersecurity
        </p>

        <p style="color:#FFFFFF !important;">
        A secure digital document management platform
        for police, investigation, forensic, legal and
        court departments.
        </p>

        <h4 style="color:#35B9D6 !important;">
        Security Features
        </h4>

        <p style="color:#FFFFFF !important;">
        • Role-based authentication<br>
        • Department-based access<br>
        • Failed-login monitoring<br>
        • Department-head alerts<br>
        • SHA-256 document hashing<br>
        • Document integrity verification<br>
        • Audit logging<br>
        • Tamper-evident blockchain-style records<br>
        • Secure document storage<br>
        • Case management
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN DASHBOARD
# ============================================================

def dashboard():

    sidebar()

    dashboard_header()

    user = st.session_state.user

    menu = [

        "📊 Dashboard",

        "📁 Cases",

        "📄 Documents",

        "🛡️ Integrity Verification",

        "🔎 Search",

        "⛓️ Blockchain Audit",

        "ℹ️ System Information"
    ]

    if user["role"] in [
        "admin",
        "head"
    ]:

        menu.insert(
            5,
            "🚨 Security Alerts"
        )

        menu.insert(
            6,
            "🧾 Audit Trail"
        )

    if user["role"] == "admin":

        menu.insert(
            7,
            "👥 User Management"
        )

    selected = st.sidebar.radio(
        "Navigation",
        menu
    )

    if selected == "📊 Dashboard":

        overview_page()

    elif selected == "📁 Cases":

        cases_page()

    elif selected == "📄 Documents":

        documents_page()

    elif selected == "🛡️ Integrity Verification":

        integrity_page()

    elif selected == "🔎 Search":

        search_page()

    elif selected == "🚨 Security Alerts":

        security_alerts_page()

    elif selected == "🧾 Audit Trail":

        audit_page()

    elif selected == "⛓️ Blockchain Audit":

        blockchain_page()

    elif selected == "👥 User Management":

        user_management_page()

    elif selected == "ℹ️ System Information":

        system_info_page()


# ============================================================
# START APPLICATION
# ============================================================

if not st.session_state.logged_in:

    login_page()

else:
    dashboard()