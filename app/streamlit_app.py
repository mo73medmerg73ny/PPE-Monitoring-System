import streamlit as st
import requests

page = st.sidebar.selectbox("Menu", ["Video Analysis", "Violations Log", "Realtime"])

if page == "Video Analysis":
    st.title("PPE Monitoring System")
    st.header("Video Analysis")

    video_file = st.file_uploader('Upload Video', type= ['mp4'])

    if video_file:
       st.video(video_file)

       if st.button("Analyze"):
          with st.spinner("Analyzing..."):
             response = requests.post(
                "http://localhost:8000/analyze/video",
                files= {"file" : video_file}
             )
             data = response.json()
             st.success(f"Done! Violations found: {data['violations']}")
 
elif page == "Violations Log":
    st.header("Violations Log")

    response = requests.get("http://localhost:8000/violations/")
    data = response.json()

    st.dataframe(data)

elif page == "Realtime":
    st.header("Realtime Monitoring")

    start = st.button("start")
    stop = st.button("stop")

    frame_placeholder = st.empty()
    violations_placeholder = st.empty()

    if start:
        import websocket
        import json

        ws = websocket.WebSocket()
        ws.connect("ws://localhost:8000/analyze/live")

        while not stop:
            data = json.loads(ws.recv())
            violations_placeholder.write(f"Violations: {data['violations']}")

