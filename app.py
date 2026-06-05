
import streamlit as st
import uuid

# 初始化 session state
if 'demands' not in st.session_state:
    st.session_state.demands = []
# New: Initialize state for handling job taking
if 'current_taking_demand_id' not in st.session_state:
    st.session_state.current_taking_demand_id = None

st.set_page_config(page_title="岁晚文社·接稿小站", layout="wide")
st.title("📝 岁晚文社·接稿小站 · 发布需求 | 接稿接单")

# ---------- 侧边栏：发布需求 ----------
with st.sidebar:
    st.header("➕ 发布新需求")
    with st.form("publish_form", clear_on_submit=True):
        title = st.text_input("需求标题 *")
        description = st.text_area("详细描述")
        budget = st.text_input("预算（选填）")
        contact = st.text_input("联系方式（选填）")
        submitted = st.form_submit_button("发布")
        if submitted and title.strip():
            new_demand = {
                "id": str(uuid.uuid4()),
                "title": title,
                "description": description,
                "budget": budget,
                "contact": contact,
                "status": "open",
                "taker": None
            }
            st.session_state.demands.append(new_demand)
            st.success("发布成功！")
            st.rerun()
        elif submitted:
            st.error("标题不能为空")

# ---------- 主区域：需求列表 ----------
st.header("📋 当前需求")
if not st.session_state.demands:
    st.info("暂无需求，在左边发布第一个吧～")
else:
    for demand in st.session_state.demands:
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.subheader(f"📌 {demand['title']}")
                st.write(f"**描述**：{demand['description']}")
                if demand['budget']:
                    st.write(f"**预算**：{demand['budget']}")
                if demand['contact']:
                    st.write(f"**联系方式**：{demand['contact']}")
                status = "🟢 待接稿" if demand['status'] == 'open' else "🔒 已接稿"
                st.write(f"**状态**：{status}")
                if demand['taker']:
                    st.write(f"**接稿人**：{demand['taker']}")
            with col2:
                if demand['status'] == 'open':
                    # New: Check if this demand is currently in the process of being taken
                    if st.session_state.current_taking_demand_id == demand['id']:
                        with st.form(key=f"take_form_{demand['id']}", clear_on_submit=False):
                            taker_name = st.text_input("你的名字或昵称", key=f"taker_name_input_{demand['id']}")
                            col_confirm, col_cancel = st.columns([1, 1])
                            with col_confirm:
                                if st.form_submit_button("确认接稿"): #, type="primary"
                                    if taker_name.strip():
                                        demand['status'] = 'taken'
                                        demand['taker'] = taker_name.strip()
                                        st.session_state.current_taking_demand_id = None # Reset
                                        st.success("接稿成功！")
                                        st.rerun()
                                    else:
                                        st.error("请填写你的名字或昵称")
                            with col_cancel:
                                if st.form_submit_button("取消", help="取消接稿", type="secondary"):
                                    st.session_state.current_taking_demand_id = None # Reset
                                    st.rerun()

                    elif st.button("✍️ 接稿", key=f"btn_{demand['id']}"):
                        # New: Set the ID of the demand being taken
                        st.session_state.current_taking_demand_id = demand['id']
                        st.rerun()
                else:
                    st.button("已接", disabled=True, key=f"disabled_{demand['id']}")
            st.divider()
