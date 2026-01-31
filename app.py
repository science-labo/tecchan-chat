cat > app.py << 'EOF'
import streamlit as st
import ollama
import os

st.title("👨‍🏫 手塚先生Chat")

# 環境変数 OLLAMA_HOST の設定
ollama_host = os.getenv("OLLAMA_HOST", None)

if ollama_host:
    client = ollama.Client(host=ollama_host)
else:
    client = ollama

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("メッセージを入力..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        
        stream = client.chat(
            model="gemma3", 
            messages=st.session_state["messages"],
            stream=True,
        )
        
        for chunk in stream:
            content = chunk['message']['content']
            full_response += content
            response_container.markdown(full_response + "▌")
            
        response_container.markdown(full_response)
    
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
EOF
