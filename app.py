import streamlit as st
import ollama
import os

# タイトル設定
st.title("👨‍🏫 手塚先生Chat")

# --- 設定変更エリア ---
# 環境変数 OLLAMA_HOST があればそれを使い、なければローカルを使う
ollama_host = os.getenv("OLLAMA_HOST", None)

if ollama_host:
    # クラウド等から指定された接続先がある場合
    client = ollama.Client(host=ollama_host)
else:
    # 通常のローカル接続（自分のPC内）
    client = ollama
# --------------------

# 履歴の保存場所を作る
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 過去の会話を表示
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# チャット入力時の処理
if prompt := st.chat_input("メッセージを入力..."):
    # ユーザーの入力を表示
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIの応答を表示
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        
        # ここで接続先を切り替えた client を使う
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
    
    # 履歴に追加
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
