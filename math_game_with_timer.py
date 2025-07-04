import streamlit as st
import random
from fractions import Fraction
from decimal import Decimal

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

# 產生兩個數字
num1 = generate_number()
num2 = generate_number()

# 顯示問題
st.subheader("請問哪個數字比較大？")
choice = st.radio("選擇一個：", options=[str(num1), str(num2)])

# 按鈕判斷
if st.button("提交答案"):
    if str(num1) == choice:
        picked = num1
        other = num2
    else:
        picked = num2
        other = num1

    if float(picked) > float(other):
        st.success("✅ 答對了！")
    elif float(picked) < float(other):
        st.error("❌ 錯了，再試試！")
    else:
        st.info("🤔 兩者一樣大哦！")

# 按下可刷新
st.markdown("---")
st.button("下一題（重新出題）", type="primary")
