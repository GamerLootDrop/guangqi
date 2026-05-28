import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import json

# 1. 网页基础配置
st.set_page_config(page_title="Event Horizon // 全球真实视界", layout="wide")

# 🔥 赛博暗黑视觉引擎：干掉一切白花花，锁死霓虹科技感
st.markdown("""
    <style>
    /* 强行拉黑所有底层容器 */
    .stApp, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #03030c !important;
    }
    /* 全局文字等宽白化 */
    p, h1, h2, h3, label, .stMarkdown {
        color: #ffffff !important;
        font-family: monospace !important;
    }
    /* 输入框暗黑科技化 */
    .stTextInput input, .stSelectbox div {
        background-color: #0d0d1e !important;
        color: #00ffff !important;
        border: 1px solid #444499 !important;
    }
    /* 火箭按钮：霓虹渐变与悬停动画 */
    div.stButton > button {
        background: linear-gradient(135deg, #7928ca, #ff0080) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.8rem 2rem !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(121, 40, 202, 0.5) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        cursor: pointer !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 4px 25px rgba(255, 0, 128, 0.8) !important;
        transform: translateY(-2px) !important;
    }
    /* 弹出 Toast 提示暗黑化 */
    [data-testid="stToast"] {
        background-color: #0d0d1e !important;
        border: 2px solid #ff0080 !important;
        box-shadow: 0 4px 20px rgba(255, 0, 128, 0.3) !important;
    }
    [data-testid="stToast"] span {
        color: #00ffff !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌌 EVENT HORIZON // 全球真实足迹")
st.write("—— 捕捉这一秒，全球地表最真实的瞬间 ——")

# 2. 本地轻量级文件数据库逻辑（确保刷新、换设备后数据不丢失）
DB_FILE = "global_posts.json"
INITIAL_DATA = [
    {"country": "United States 🇺🇸", "user": "Alex", "lat": 40.7128, "lon": -74.0060, "msg": "New York is raining heavily right now.", "time": "05:12"},
    {"country": "United Kingdom 🇬🇧", "user": "Emma", "lat": 51.5074, "lon": -0.1278, "msg": "Midnight coffee in London.", "time": "10:24"},
    {"country": "Japan 🇯🇵", "user": "Yuki", "lat": 35.6762, "lon": 139.6503, "msg": "Tokyo tower looks beautiful tonight.", "time": "18:45"},
    {"country": "Australia 🇦🇺", "user": "Liam", "lat": -33.8688, "lon": 151.2093, "msg": "Surfing morning!", "time": "22:15"}
]

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return INITIAL_DATA
    else:
        return INITIAL_DATA

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 将数据载入当前会话
if "posts" not in st.session_state:
    st.session_state.posts = load_data()

# 3. 页面大排版
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📸 签到你的时空")
    user_name = st.text_input("你的代号 (Username)", "匿名星人")
    user_msg = st.text_input("此刻你在想什么？(What's on your mind?)", "从中国向宇宙发出信号...")
    
    location_choice = st.selectbox("选择你所在的地理坐标", [
        "China 🇨🇳 (Beijing)", 
        "United States 🇺🇸 (New York)", 
        "United States 🇺🇸 (Los Angeles)",
        "France 🇫🇷 (Paris)", 
        "Japan 🇯🇵 (Tokyo)", 
        "Iceland 🇮🇸 (Reykjavik)",
        "Australia 🇦🇺 (Sydney)"
    ])
    
    loc_data = {
        "China 🇨🇳 (Beijing)": [39.9042, 116.4074],
        "United States 🇺🇸 (New York)": [40.7128, -74.0060],
        "United States 🇺🇸 (Los Angeles)": [34.0522, -118.2437],
        "France 🇫🇷 (Paris)": [48.8566, 2.3522],
        "Japan 🇯🇵 (Tokyo)": [35.6762, 139.6503],
        "Iceland 🇮🇸 (Reykjavik)": [64.1466, -21.9426],
        "Australia 🇦🇺 (Sydney)": [-33.8688, 151.2093]
    }

    if st.button("🚀 发射足迹到全球 3D 星图"):
        if user_msg:
            new_footprint = {
                "country": location_choice,
                "user": user_name,
                "lat": loc_data[location_choice][0],
                "lon": loc_data[location_choice][1],
                "msg": user_msg,
                "time": datetime.now().strftime("%H:%M")
            }
            # 同时更新内存和本地文件
            st.session_state.posts.append(new_footprint)
            save_data(st.session_state.posts)
            
            st.toast(f"📡 信号已成功定位至 {location_choice}！")
            st.rerun()  # 强制刷新页面渲染最新星球状态
        else:
            st.error("请先写点什么再发射吧！")

with col2:
    # 4. 渲染 3D 赛博地球
    df = pd.DataFrame(st.session_state.posts)

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
            showland=True, landcolor="#121225",
            showocean=True, oceancolor="#02020a",
            showcountries=True, countrycolor="#333366",
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    fig.update_traces(
        marker=dict(size=15, color="#00ffff", opacity=0.9,
                    line=dict(width=2, color="#ff0080")),
        selector=dict(mode="markers")
    )

    st.plotly_chart(fig, use_container_width=True)

# 5. 底部动态树洞流
st.write("---")
st.write("### 🛰️ 全球引力波实时动态流")
for item in reversed(st.session_state.posts):
    st.markdown(f"**[{item['time']}] {item['user']}** 在 **{item['country']}** 留下了印记：")
    st.code(item['msg'])
