import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from app.data.fetcher import get_live_data
from app.engine.indicators import calculate_rsi, calculate_ema

# 1. إعدادات المستخدمين
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# 2. إنشاء المصادق
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 3. عرض بوابة الدخول
authenticator.login()

# 4. التحقق من حالة الدخول
if st.session_state["authentication_status"]:
    st.sidebar.success(f'أهلاً بك يا {st.session_state["name"]}!')
    authenticator.logout('تسجيل الخروج', 'sidebar')
    
    st.title("لوحة تحكم Nexus-Trade 🚀")
    
    # قائمة اختيار الأصل المالي
    assets = {
        "بيتكوين": "BTC-USD",
        "الذهب": "GC=F",
        "الفضة": "SI=F",
        "سهم أبل": "AAPL",
        "يورو/دولار": "EURUSD=X"
    }
    
    selected_name = st.selectbox("اختر الأصل المالي للمراقبة:", list(assets.keys()))
    symbol = assets[selected_name]
    
    if st.button('تحديث البيانات'):
        with st.spinner(f'جاري جلب بيانات {selected_name}...'):
            try:
                # نمرر الرمز المختار للدالة
                prices = get_live_data(symbol=symbol)
                
                if prices is not None and not prices.empty:
                    rsi = calculate_rsi(prices).iloc[-1]
                    ema = calculate_ema(prices).iloc[-1]
                    current_price = prices.iloc[-1]
                    
                    col1, col2 = st.columns(2)
                    col1.metric("السعر الحالي", f"{current_price:.2f}")
                    col2.metric("RSI", f"{rsi:.2f}")
                    
                    if rsi < 30 and current_price > ema:
                        st.success("فرصة شراء: الآن! (Strong Buy)")
                    else:
                        st.warning("الوضع الحالي: انتظار (WAIT)")
                else:
                    st.error("لم يتم العثور على بيانات لهذا الأصل.")
            except Exception as e:
                st.error(f"خطأ: {e}")

elif st.session_state["authentication_status"] is False:
    st.error('اسم المستخدم أو كلمة السر غير صحيحة')
elif st.session_state["authentication_status"] is None:
    st.warning('الرجاء إدخال بيانات الدخول')