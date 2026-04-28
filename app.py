import streamlit as st
import requests
import sqlite3
import json
import uuid
from datetime import datetime
from groq import Groq

#db setup
conn = sqlite3.connect('chats.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chats
             (session_id TEXT PRIMARY KEY, user_id TEXT, title TEXT, messages TEXT, timestamp DATETIME)''')
conn.commit()


#groq api
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)


#funcs

def translate_text(text, source_lang, target_lang):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {"client": "gtx", "sl": source_lang, "tl": target_lang, "dt": "t", "q": text}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            full_translation = ""
            for sentence in response.json()[0]:
                full_translation += sentence[0]
            return full_translation
        return "Translation Error"
    except Exception as e:
        return f"Error: {e}"

def generate_ai_response(current_prompt):
    api_messages = [
        {"role": "system", "content": "You are a helpful, smart, and concise AI assistant. Keep answers brief (1-3 sentences)."}
    ]
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            api_messages.append({"role": "user", "content": msg.get("english_user", msg["content"])})
        elif msg["role"] == "assistant":
            api_messages.append({"role": "assistant", "content": msg.get("english_ans", msg["content"])})
            
    api_messages.append({"role": "user", "content": current_prompt})
    
    try:
        chat_completion = client.chat.completions.create(
            messages=api_messages,
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def save_chat_to_db():
    if st.session_state.messages:
        title = st.session_state.messages[0]['content'][:30] + "..."
        msgs_json = json.dumps(st.session_state.messages)
        timestamp = datetime.now()
        c.execute("REPLACE INTO chats (session_id, user_id, title, messages, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (st.session_state.current_session_id, st.session_state.user_id, title, msgs_json, timestamp))
        conn.commit()

def delete_chat(session_id):
    """Deletes a specific chat from the database."""
    c.execute("DELETE FROM chats WHERE session_id=?", (session_id,))
    conn.commit()
    if st.session_state.current_session_id == session_id:
        start_new_chat()

def load_chat(session_id):
    c.execute("SELECT messages FROM chats WHERE session_id=?", (session_id,))
    result = c.fetchone()
    if result:
        st.session_state.messages = json.loads(result[0])
        st.session_state.current_session_id = session_id

def start_new_chat():
    st.session_state.messages = []
    st.session_state.current_session_id = str(uuid.uuid4())


#streamlit interface

st.set_page_config(page_title="Santali AI Assistant", page_icon="🤖")
#css
st.markdown("""
<style>
    /* 1. WhatsApp Web Background Color */
    .stApp {
        background-color: #efeae2;
    }

    /* 2. Push User Message to the Right & Style the Bubble (WhatsApp Green) */
    .stChatMessage:has([data-testid="chatAvatarIcon-user"]) {
        flex-direction: row-reverse;
        text-align: right;
    }
    .stChatMessage:has([data-testid="chatAvatarIcon-user"]) [data-testid="stMarkdownContainer"] {
        background-color: #d9fdd3; /* WhatsApp Light Green */
        color: #111b21;
        padding: 10px 15px;
        border-radius: 15px 0px 15px 15px;
        box-shadow: 0px 1px 2px rgba(0,0,0,0.1);
        display: inline-block;
    }

    /* 3. Style the AI Message Bubble (Clean White) */
    .stChatMessage:has([data-testid="chatAvatarIcon-assistant"]) {
        background-color: transparent;
    }
    .stChatMessage:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stMarkdownContainer"] {
        background-color: #ffffff;
        color: #111b21;
        padding: 10px 15px;
        border-radius: 0px 15px 15px 15px;
        box-shadow: 0px 1px 2px rgba(0,0,0,0.1);
        display: inline-block;
    }
    
    /* 4. Fix Expander Colors so text is readable */
    .streamlit-expanderHeader {
        color: #111b21 !important;
    }
    .streamlit-expanderContent {
        color: #111b21 !important;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = str(uuid.uuid4())
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

with st.sidebar:
    st.title("💬 Past Chats")
    
    if st.button("➕ New Chat", use_container_width=True):
        start_new_chat()
        st.rerun()
        
    st.divider()
    
    c.execute("SELECT session_id, title FROM chats ORDER BY timestamp DESC")
    past_chats = c.fetchall()
    
    for chat in past_chats:
        chat_id = chat[0]
        chat_title = chat[1]
        
        col1, col2 = st.columns([0.75, 0.25])
        
        with col1:
            if st.button(f"📝 {chat_title}", key=f"load_{chat_id}", use_container_width=True):
                load_chat(chat_id)
                st.rerun()
                
        with col2:
            if st.button("🗑️", key=f"del_{chat_id}"):
                delete_chat(chat_id)
                st.rerun()
            
    st.divider()
    
    if len(st.session_state.messages) > 0:
        st.write("Save this conversation:")
        chat_text = "--- Santali AI Chat History ---\n\n"
        for msg in st.session_state.messages:
            role = "You" if msg["role"] == "user" else "AI"
            chat_text += f"{role}: {msg['content']}\n"
            if "english_user" in msg:
                chat_text += f"(Translated Input: {msg['english_user']})\n"
            if "english_ans" in msg:
                chat_text += f"(Translated Output: {msg['english_ans']})\n"
            chat_text += "-" * 40 + "\n"
            
        st.download_button(
            label="📥 Download Current Chat",
            data=chat_text,
            file_name="santali_conversation.txt",
            mime="text/plain",
            use_container_width=True
        )


#main chat interface
st.title("Santali AI Assistant 🤖")
st.markdown("Ask me anything! Type in Santali or English.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        if msg["role"] == "user" and "english_user" in msg:
            st.caption(f"*Translated to English:* {msg['english_user']}")
            
        if msg["role"] == "assistant" and "english_ans" in msg:
            with st.expander("View English Translation 👀"):
                st.write(f"**AI English Output:** {msg['english_ans']}")

user_input = st.chat_input("Type your message here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking & Translating..."):
            
            english_prompt = translate_text(user_input, "auto", "en")
            
            english_answer = generate_ai_response(english_prompt)
            
            santali_answer = translate_text(english_answer, "en", "sat")
            
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input,
        "english_user": english_prompt 
    })
    
    st.session_state.messages.append({
        "role": "assistant", 
        "content": santali_answer,
        "english_ans": english_answer
    })
    
    save_chat_to_db() 
    
    st.rerun()
