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
    
    st.title("لوحة تحكم Nexus-Trade للتداول 🚀")
    
    if st.button('تحديث البيانات'):
        with st.spinner('جاري جلب وتحليل البيانات...'):
            try:
                prices = get_live_data()
                
                # التحقق من أن البيانات ليست فارغة لتجنب IndexError
                if prices is not None and not prices.empty and len(prices) > 0:
                    rsi_series = calculate_rsi(prices)
                    ema_series = calculate_ema(prices)
                    
                    if not rsi_series.empty and not ema_series.empty:
                        rsi = rsi_series.iloc[-1]
                        ema = ema_series.iloc[-1]
                        current_price = prices.iloc[-1]
                        
                        col1, col2 = st.columns(2)
                        col1.metric("السعر الحالي", f"{current_price:.2f}")
                        col2.metric("RSI", f"{rsi:.2f}")
                        
                        if rsi < 30 and current_price > ema:
                            st.success("فرصة شراء: الآن! (Strong Buy)")
                        else:
                            st.warning("الوضع الحالي: انتظار (WAIT)")
                    else:
                        st.error("خطأ في حساب المؤشرات الفنية.")
                else:
                    st.error("لم يتم جلب بيانات صحيحة من السوق. تأكد من اتصال الإنترنت.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")

elif st.session_state["authentication_status"] is False:
    st.error('اسم المستخدم أو كلمة السر غير صحيحة')
elif st.session_state["authentication_status"] is None:
    st.warning('الرجاء إدخال بيانات الدخول للوصول للوحة التحكم')