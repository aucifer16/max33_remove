import streamlit as st
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
from pythainlp.tokenize import word_tokenize
import joblib

# ---------- โหลดโมเดล ----------
model = joblib.load('sentiment_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

def predict_sentiment(text):
    tokenized = ' '.join(word_tokenize(text, engine='newmm'))
    vec = vectorizer.transform([tokenized])
    pred = model.predict(vec)[0]
    return 'Positive 😊' if pred == 1 else 'Negative 😠'

# ---------- YouTube API ----------
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

@st.cache_resource
def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=credentials)

def get_latest_videos(youtube, channel_id, max_results=2):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        order="date",
        type="video"
    )
    response = request.execute()
    return response['items']

def list_comments(youtube, video_id, max_comments=20):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_comments,
        textFormat="plainText"
    )
    response = request.execute()
    return response['items']

# 🔄 เพิ่มฟังก์ชันลบคอมเมนต์
def delete_comment(youtube, comment_id):
    try:
        youtube.comments().delete(id=comment_id).execute()
        return True
    except Exception as e:
        st.warning(f"❌ ลบไม่สำเร็จ: {e}")
        return False

# ---------- GUI ----------
st.title("🎬 YouTube Comment Sentiment Viewer (ภาษาไทย)")
channel_id = st.text_input("🔗 ใส่ Channel ID (เช่น UCzr22Ehy1VrqJfWu3-5rfgggfgfdg):")

if channel_id:
    youtube = get_authenticated_service()
    with st.spinner("🔄 กำลังดึงข้อมูลวิดีโอล่าสุด..."):
        videos = get_latest_videos(youtube, channel_id)

    for video in videos:
        video_id = video['id']['videoId']
        title = video['snippet']['title']
        published = video['snippet']['publishedAt']

        st.subheader(f"📹 {title}")
        st.caption(f"🕒 เผยแพร่: {published}")
        st.video(f"https://www.youtube.com/watch?v={video_id}")

        comments = list_comments(youtube, video_id)

        for item in comments:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_id = item['snippet']['topLevelComment']['id']
            sentiment = predict_sentiment(comment)

            if "Negative" in sentiment:
                success = delete_comment(youtube, comment_id)  # 🔄 เรียกลบ
                if success:
                    st.error(f"💬 {comment}\n\n🆔 `{comment_id}`\n🔎 วิเคราะห์: {sentiment} → ✅ ลบสำเร็จ")
                else:
                    st.error(f"💬 {comment}\n\n🆔 `{comment_id}`\n🔎 วิเคราะห์: {sentiment} → ❌ ลบไม่สำเร็จ")
            else:
                st.success(f"💬 {comment}\n\n🆔 `{comment_id}`\n🔎 วิเคราะห์: {sentiment}")
# ---------- Footer / Credits ----------
st.markdown("---")
st.markdown("## 🙏 Credits")
st.markdown("""
💻 Developed by [Sittiphong] )  
🧠 Sentiment model trained with Thai data  
🔧 Built with: Streamlit, PyThaiNLP, scikit-learn, Google APIs  
📅 Project started: March 2025
""")
