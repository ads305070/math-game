import streamlit as st
import random
from fractions import Fraction
import time
import pandas as pd
import os

DATA_FILE = "scores.csv"
ADMIN_PASSWORD = "teacher123"  # 可自行更改

def random_number():
    num_type = random.choice(['int', 'float', 'fraction'])
    sign = random.choice([1, -1])
    if num_type == 'int':
        value = sign * random.randint(1, 20)
        display = str(value)
        real_value = value
    elif num_type == 'float':
        value = sign * round(random.uniform(0.1, 20), 2)
        display = str(value)
        real_value = value
    else:  # fraction
        numerator = random.randint(1, 20)
        denominator = random.randint(2, 20)
        value = sign * Fraction(numerator, denominator)
        display = f"{'-' if sign == -1 else ''}{numerator}/{denominator}"
        real_value = float(value)
    return display, real_value

def save_score(data):
    df = pd.DataFrame([data])
    if os.path.exists(DATA_FILE):
        df.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        df.to_csv(DATA_FILE, mode='w', header=True, index=False, encoding='utf-8-sig')

def load_scores():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    else:
        return pd.DataFrame(columns=["班級", "座號", "姓名", "分數", "總題數", "時間(秒)", "時間戳記"])

def game_page():
    st.title("數的大小比較小遊戲")
    st.write(f"遊戲時間：{st.session_state['game_time']} 分鐘")
    st.write(f"玩家：{st.session_state['class']}班 {st.session_state['number']}號 {st.session_state['name']}")

    if 'score' not in st.session_state:
        st.session_state.score = 0
        st.session_state.total = 0
        st.session_state.left, st.session_state.left_val = random_number()
        st.session_state.right, st.session_state.right_val = random_number()
        st.session_state.start_time = time.time()
        st.session_state.end_time = st.session_state.start_time + st.session_state['game_time'] * 60
        st.session_state.finished = False

    # 倒數計時
    remaining = int(st.session_state.end_time - time.time())
    if remaining <= 0:
        st.session_state.finished = True
        remaining = 0

    st.header(f"剩餘時間：{remaining // 60}分{remaining % 60}秒")

    if st.session_state.finished:
        st.success(f"遊戲結束！你在 {st.session_state['game_time']} 分鐘內答對了 {st.session_state.score} 題，共作答 {st.session_state.total} 題。")
        # 儲存分數
        if not st.session_state.get('score_saved', False):
            save_score({
                "班級": st.session_state['class'],
                "座號": st.session_state['number'],
                "姓名": st.session_state['name'],
                "分數": st.session_state.score,
                "總題數": st.session_state.total,
                "時間(秒)": st.session_state['game_time'] * 60,
                "時間戳記": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            })
            st.session_state.score_saved = True
        st.button("重新開始", on_click=reset_all)
        return

    col1, col2 = st.columns(2)
    with col1:
        st.header(st.session_state.left)
    with col2:
        st.header(st.session_state.right)

    choice = st.radio("你的選擇：", ["左邊大", "右邊大", "一樣大"], key=st.session_state.total)

    if st.button("提交答案"):
        st.session_state.total += 1
        left = st.session_state.left_val
        right = st.session_state.right_val
        if (choice == "左邊大" and left > right) or \
           (choice == "右邊大" and right > left) or \
           (choice == "一樣大" and abs(left - right) < 1e-8):
            st.success("答對了！")
            st.session_state.score += 1
        else:
            st.error("答錯了！")
        st.session_state.left, st.session_state.left_val = random_number()
        st.session_state.right, st.session_state.right_val = random_number()
        st.experimental_rerun()

    st.write(f"目前分數：{st.session_state.score} / {st.session_state.total}")

def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def login_page():
    st.title("數的大小比較小遊戲 - 登入")
    st.write("請先輸入班級、座號、姓名，選擇遊戲時間後開始遊戲。")
    class_ = st.text_input("班級", key="class")
    number = st.text_input("座號", key="number")
    name = st.text_input("姓名", key="name")
    game_time = st.selectbox("選擇遊戲時間（分鐘）", [1, 2, 3], key="game_time")
    if st.button("開始遊戲"):
        if class_ and number and name:
            st.session_state['class'] = class_
            st.session_state['number'] = number
            st.session_state['name'] = name
            st.session_state['game_time'] = game_time
            st.experimental_rerun()
        else:
            st.warning("請完整填寫所有欄位！")

def admin_page():
    st.title("後台查詢 - 分數紀錄")
    pwd = st.text_input("請輸入管理密碼", type="password")
    if st.button("查詢"):
        if pwd == ADMIN_PASSWORD:
            df = load_scores()
            st.dataframe(df)
            st.success("查詢成功！")
        else:
            st.error("密碼錯誤！")

# 主程式
menu = st.sidebar.selectbox("選單", ["遊戲開始", "後台查詢"])
if menu == "遊戲開始":
    if 'class' in st.session_state and 'number' in st.session_state and 'name' in st.session_state and 'game_time' in st.session_state:
        game_page()
    else:
        login_page()
elif menu == "後台查詢":
    admin_page()
