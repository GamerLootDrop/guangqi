import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. 强制设定宽屏，且不进行任何多余的初始隐藏
st.set_page_config(page_title="Event Horizon // 全球真实视界", layout="wide")

# 🔥 真正的强效黑化滤镜：强制把 Streamlit 所有白边、底层容器全部抠成宇宙深空黑色
st.markdown("""
    <style>
    .stApp, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #05050d !important;
    }
    p, h1, h2, h3, label, .stMarkdown {
        color: #ffffff !important;
        font-family: monospace !important;
    }
    /* 美化输入框在黑色背景下的对比度 */
    .stTextInput input, .stSelectbox div {
        background-color: #111125 !important;
        color: #ffffff !important;
        border: 1px solid #333366 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌌 EVENT HORIZON // 全球真实足迹")
st.write("—— 捕捉这一秒，全球地表最真实的瞬间 ——")

# 2. 初始化本地模拟数据（这部分数据会在刷新页面时恢复初始状态）
if "global_messages" not in st.session_state:
    st.session_state.global_messages = [
        {"country": "United States 🇺🇸", "user": "Alex", "lat": 40.7128, "lon": -74.0060, "msg": "New York is raining heavily right now.", "time": "05:12"},
        {"country": "United Kingdom 🇬🇧", "user": "Emma", "lat": 51.5074, "lon": -0.1278, "msg": "Midnight coffee in London.", "time": "10:24"},
        {"country": "Japan 🇯🇵", "user": "Yuki", "lat": 35.6762, "lon": 139.6503, "msg": "Tokyo tower looks beautiful tonight.", "time": "18:45"},
        {"country": "Australia 🇦🇺", "user": "Liam", "lat": -33.8688, "lon": 151.2093, "msg": "Surfing morning!", "time": "22:15"}
    ]

# 3. 页面大排版：左边直接放控制面板，右边放 3D 地球，再也不会被遮挡！
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📸 签到你的时空")
    user_name = st.text_input("你的代号 (Username)", "匿名星人", key="username")
    user_msg = st.text_input("此刻你在想什么？(What's on your mind?)", "从中国向宇宙发出信号...", key="usermsg")
    
    location_choice = st.selectbox("选择你所在的地理坐标", [
        "China 🇨🇳 (Beijing)", "United States 🇺🇸 (LA)", "France 🇫🇷 (Paris)", "Japan 🇯🇵 (Tokyo)", "Iceland 🇮🇸 (Reykjavik)"
    ])
    
    loc_data = {
        "China 🇨🇳 (Beijing)": [39.9042, 116.4074],
        "United States 🇺🇸 (LA)": [34.0522, -118.2437],
        "France 🇫🇷 (Paris)": [48.8566, 2.3522],
        "Japan 🇯🇵 (Tokyo)": [35.6762, 139.6503],
        "Iceland 🇮🇸 (Reykjavik)": [64.1466, -21.9426]
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
            st.session_state.global_messages.append(new_footprint)
            st.toast("发射成功！已成功在地球对应坐标生成霓虹星点！")
        else:
            st.error("请先写点什么再发射吧！")

with col2:
    # 4. 渲染 3D 赛博地球
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
            showland=True, landcolor="#151530",
            showocean=True, oceancolor="#02020a",
            showcountries=True, countrycolor="#333366",
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    fig.update_traces(
        marker=dict(size=14, color="#a147ff", opacity=0.9,
                    line=dict(width=2, color="#00ffff")),
        selector=dict(mode="markers")
    )

    st.plotly_chart(fig, use_container_width=True)

# 5. 底部动态树洞流
st.write("---")
st.write("### 🛰️ 全球引力波实时动态流")
for item in reversed(st.session_state.global_messages):
    st.markdown(f"**[{item['time']}] {item['user']}** 在 **{item['country']}** 留下了印记：")
    st.code(item['msg'])
