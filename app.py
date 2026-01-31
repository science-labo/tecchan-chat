import streamlit as st
import ollama
import os  

# タイトル設定
st.title("👨‍🏫 手塚先生Chat")

# --- 変更点ここから ---
# 環境変数 OLLAMA_HOST があればそれを使い、なければローカルを使う
ollama_host = os.getenv("OLLAMA_HOST", None)

if ollama_host:
    # クラウドから自宅のPCに接続する場合
    client = ollama.Client(host=ollama_host)
else:
    # 通常のローカル接続
    client = ollama
# --- 変更点ここまで ---

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
        
        # client.chat を使うように変更
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
