import streamlit as st
import re

st.set_page_config(page_title="Register Form", layout="centered")

st.markdown("""
<style>
.stApp {
    background-color: #ffffff;
}

header,
footer,
#MainMenu {
    visibility: hidden;
}

.block-container {
    max-width: 100%;
    padding: 2px 4px 0;
}

div[data-testid="stForm"] {
    background-color: #101218;
    border: 2px solid #2b3038;
    border-radius: 16px;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.03);
    padding: 26px 42px 34px;
}

div[data-testid="stForm"] label p {
    color: #f4f4f5 !important;
    font-size: 18px;
    font-weight: 800;
    line-height: 1.25;
}

div[data-testid="stForm"] label {
    margin-bottom: 12px;
}

div[data-testid="stForm"] [data-testid="stTextInput"] {
    margin-bottom: 28px;
}

div[data-testid="stForm"] [data-testid="stMarkdownContainer"]:has(.password-label) {
    margin-bottom: 12px;
}

.password-label {
    align-items: center;
    color: #f4f4f5;
    display: flex;
    font-size: 18px;
    font-weight: 800;
    line-height: 1.25;
}

.password-icon {
    display: block;
    flex: 0 0 auto;
    font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
    font-size: 24px;
    font-weight: 800;
    line-height: 1;
}

div[data-testid="stForm"] [data-testid="stTextInput"] div[data-baseweb="input"] {
    background-color: #292a33;
    border: 0;
    border-radius: 12px;
    min-height: 56px;
}

div[data-testid="stForm"] [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
    box-shadow: 0 0 0 1px #4b5563;
}

div[data-testid="stForm"] input {
    background-color: transparent;
    color: #f9fafb;
    font-size: 22px;
    font-weight: 700;
    min-height: 56px;
    padding-left: 18px;
}

div[data-testid="stForm"] input::placeholder {
    color: #a1a1aa;
    opacity: 0.75;
}

div[data-testid="stForm"] [data-testid="stTextInput"] button {
    color: #ffffff;
    margin-right: 14px;
}

div[data-testid="stForm"] [data-testid="stVerticalBlock"] {
    gap: 0;
}

div[data-testid="stFormSubmitButton"] button {
    background-color: #111720;
    color: #f9fafb;
    border: 2px solid #333a45;
    border-radius: 8px;
    padding: 10px 18px;
    min-height: 56px;
    font-size: 22px;
    font-weight: 800;
}

div[data-testid="stFormSubmitButton"] button p {
    font-size: 22px;
    font-weight: 800;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background-color: #161d27;
    border-color: #48515f;
    color: #ffffff;
}

div[data-testid="stFormSubmitButton"] button:focus:not(:active) {
    border-color: #64748b;
    color: #ffffff;
    box-shadow: none;
}

.rules {
    color: #111827;
    font-size: 24px;
    line-height: 1.7;
    margin: 34px 0 0 72px;
    max-width: 1180px;
}

.rules h3,
.rules li,
.rules p {
    display: table;
    background-color: #d8e9ff;
    margin: 0 0 20px;
    padding: 2px 4px;
}

.rules h3 {
    font-size: 24px;
    font-weight: 800;
}

.rules ul {
    margin: 0 0 24px 60px;
    padding-left: 0;
}

.rules li {
    padding-left: 10px;
}

.rules .sub-rule {
    margin-left: 60px;
}
</style>
""", unsafe_allow_html=True)

EMAIL_PATTERN = r"^[\w\.-]+@gmail\.com$"
PASSWORD_PATTERN = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"


def main():
    with st.form("register_form"):
        email = st.text_input(
            "📧 Địa chỉ Email",
            placeholder="Nhập email theo mẫu hợp lệ..."
        )
        st.markdown(
            """
            <div class="password-label">
                <span class="password-icon">🔒</span>
                <span>Mật khẩu</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        password = st.text_input(
            "Mật khẩu",
            placeholder="Nhập mật khẩu theo quy tắc trên",
            label_visibility="collapsed",
            type="password"
        )
    
        submitted = st.form_submit_button("Tạo Tài Khoản")

    if submitted:
        if not re.match(EMAIL_PATTERN, email):
            st.error("Email của bạn không hợp lệ. Vui lòng kiểm tra định dạng (ví dụ: `ten.ban@domain.com`).")
        elif not re.match(PASSWORD_PATTERN, password):
            st.error("Mật khẩu không đáp ứng các yêu cầu về độ mạnh (8 ký tự, hoa, thường, số, đặc biệt).")
        else:
            st.balloons()
            st.success("Tạo tài khoản thành công!")


if __name__ == "__main__":
    main()
