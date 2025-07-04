import streamlit as st
import random
from fractions import Fraction

st.title("🔢 數值大小比較小遊戲")

def generate_number():
    num_type = random.choice(["int", "float", "fraction"])
    is_negative = random.choice([True, False])

    if num_type == "int":
        value = random.randint(1, 10)
    elif num_type == "float":
        value = round(random.uniform(1, 10), 2)
    else:  # fraction
        numerator = random.randint(1, 9)
        denominator = random.randint(2, 9)
        value = Fraction(numerator, denominator)

    if is_negative:
        value = -value

    return value

def display_number(num):
    if isinstance(num, Fraction):
        return f"{num.numerator}/{num.denominator}" if num.denominator != 1 else str(num.numerator)
    else:
        return str(num)

# 初始化 session_state
if "num1" not in st.session_state or "num2" not in st.session_state:
    while True:
        n1 = generate_number()
        n2 = generate_number()
        if float(n1) != float(n2):
            st.session_state["num1"] = n1
            st.session_state["num2"] = n2
            break

num1 = st.session_state["num1"]
num2 = st.session_state["num2"]

# 顯示問題
st.subheader("請問哪個數字比較大？")
options = [display_number(num1), display_number(num2)]
choice = st.radio("選擇一個：", options=options)

# 按鈕判斷
if st.button("提交答案"):
    picked = num1 if choice == display_number(num1) else num2
    other = num2 if picked == num1 else num1

    if float(picked) > float(other):
        st.success("✅ 答對了！")
    elif float(picked) < float(other):
        st.error("❌ 錯了，再試試！")
    else:
        st.info("🤔 兩者一樣大哦！")

# 按下可刷新
if st.button("下一題（重新出題）", type="primary"):
    st.experimental_rerun()
    while True:
        n1 = generate_number()
        n2 = generate_number()
        if float(n1) != float(n2):
            st.session_state["num1"] = n1
            st.session_state["num2"] = n2
            st.experimental_rerun()
