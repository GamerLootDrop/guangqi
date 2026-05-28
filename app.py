import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. 网页基础配置（严格修正为官方标准的 wide 宽屏模式）
st.set_page_config(page_title="Event Horizon // 全球真实视界", layout="wide", initial_sidebar_state="collapsed")

# 注入一点深色背景的样式
st.markdown("""
    <style>
    .reportview-container { background: #020208; }
    h1, h3, p { color: #ffffff !important; font-family: monospace; letter-spacing: 2px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🌌 EVENT HORIZON // 全球真实足迹")
st.write("—— 捕捉这一秒，全球地表最真实的瞬间 ——")

# 2. 初始化模拟数据库
if "global_messages" not in st.session_state:
    st.session_state.global_messages = [
        {"country": "United States 🇺🇸", "user": "Alex", "lat": 40.7128, "lon": -74.0060, "msg": "New York is raining heavily right now.", "time": "05:12"},
        {"country": "United Kingdom 🇬🇧", "user": "Emma", "lat": 51.5074, "lon": -0.1278, "msg": "Midnight coffee in London.", "time": "10:24"},
        {"country": "Japan 🇯🇵", "user": "Yuki", "lat": 35.6762, "lon": 139.6503, "msg": "Tokyo tower looks beautiful tonight.", "time": "18:45"},
        {"country": "Australia 🇦🇺", "user": "Liam", "lat": -33.8688, "lon": 151.2093, "msg": "Surfing morning!", "time": "22:15"}
    ]

# 3. 社交侧边栏
with st.sidebar:
    st.header("📸 签到你的时空")
    user_name = st.text_input("你的代号 (Username)", "匿名星人")
    
    # 调用摄像头直拍（测试时如果不方便开摄像头，也可以直接填留言发射）
    picture = st.camera_input("定格此刻最真实的你")
    user_msg = st.text_input("此刻你在想什么？(What's on your mind?)", "")
    
    location_choice = st.selectbox("选择你所在的地理视界", [
        "China 🇨🇳 (Beijing)", "United States 🇺🇸 (LA)", "France 🇫🇷 (Paris)", "Japan 🇯🇵 (Tokyo)", "Iceland 🇮🇸 (Reykjavik)"
    ])
    
    loc_data = {
        "China 🇨🇳 (Beijing)": [39.9042, 116.4074],
        "United States 🇺🇸 (LA)": [34.0522, -118.2437],
        "France 🇫🇷 (Paris)": [48.8566, 2.3522],
        "Japan 🇯🇵 (Tokyo)": [35.6762, 139.6503],
        "Iceland 🇮🇸 (Reykjavik)": [64.1466, -21.9426]
    }

    if st.button("发射足迹到全球 3D 星图 // LAUNCH"):
        if user_msg:
            new_footprint = {
                "country": location_choice,
                "user": user_name,
                "lat": loc_data[location_choice][0],
                "lon": loc_data[location_choice][1],
                "msg": user_msg,
                "time": datetime.now().strftime("%H:%M")
            }
            st.session_state.global_messages.append(new_footprint)
            st.success("发射成功！转动右侧 3D 地球即可查看你的星点！")
        else:
            st.warning("请先写下留言才能发射哦！")

# 4. 渲染 3D 全球社交图（这里也同步修正为了上一步提到的 px 模式）
df = pd.DataFrame(st.session_state.global_messages)

fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    hover_name="user",
    hover_data={"country": True, "msg": True, "time": True, "lat": False, "lon": False},
    projection="orthographic"
)

fig.update_layout(
    geo=dict(
        showland=True, landcolor="#111125",
        showocean=True, oceancolor="#02020a",
        showcountries=True, countrycolor="#222244",
        bgcolor="rgba(0,0,0,0)"
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

fig.update_traces(
    marker=dict(size=12, color="#9437ff", opacity=0.8,
                line=dict(width=2, color="#00ffff")),
    selector=dict(mode="markers")
)

st.plotly_chart(fig, use_container_width=True)

# 5. 底部动态树洞流
st.write("### 🛰️ 正在接收的宇宙引力波...")
for item in reversed(st.session_state.global_messages):
    st.markdown(f"**[{item['time']}] {item['user']}** 来自 *{item['country']}*：")
    st.info(item['msg'])
