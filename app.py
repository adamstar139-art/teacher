import streamlit as st
import pandas as pd
import sqlite3
import datetime
from io import BytesIO

# ==========================================
# 1. إعداد الصفحة والتصميم الاحترافي (RTL & CSS)
# ==========================================
st.set_page_config(
    page_title="نظام المتابعة الصفية والإشرافية - مدارس الثغر النموذجية",
    page_icon="🏫",
    layout="wide"
)

# كود التنسيق لدعم اللغة العربية والطباعة والشعار
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .header-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .header-box h1 {
        color: #ffffff;
        font-weight: 900;
        margin: 0;
        font-size: 26px;
    }
    .header-box h3 {
        color: #fef08a;
        margin-top: 8px;
        font-weight: 700;
        font-size: 19px;
    }
    
    .card-style {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    .stButton button {
        border-radius: 8px;
        font-weight: bold;
    }

    @media print {
        .no-print, header, footer, [data-testid="stSidebar"] { display: none !important; }
        .stApp { background-color: white !important; }
        @page { size: A4 portrait; margin: 10mm; }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إنشاء قاعدة البيانات الدائمة (SQLite)
# ==========================================
DB_FILE = "thagher_evaluations.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_name TEXT,
            specialization TEXT,
            assigned_subjects TEXT,
            grade TEXT,
            class_name TEXT,
            session_num TEXT,
            visit_num TEXT,
            eval_date TEXT,
            prep_score INTEGER,
            intro_score INTEGER,
            content_score INTEGER,
            tech_score INTEGER,
            mgmt_score INTEGER,
            diff_score INTEGER,
            strategy_score INTEGER,
            act_score INTEGER,
            eval_score INTEGER,
            total_score INTEGER,
            notes TEXT,
            signed_teacher TEXT,
            signed_admin TEXT,
            admin_title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 3. بيانات معلمي وإدارة مدارس الثغر المتوسطة
# ==========================================
TEACHERS_DATA = {
    "محمد سامي السعيد": {"spec": "مهارات رقمية", "subjects": "مهارات رقمية"},
    "علي محمد معوض": {"spec": "علوم", "subjects": "علوم"},
    "أحمد عبد الحميد سعيد": {"spec": "علوم", "subjects": "علوم"},
    "محمد عبد المنعم أبو كيلة": {"spec": "لغة انجليزية", "subjects": "تربية فنية + لغة انجليزية"},
    "هيثم رضا عطية": {"spec": "لغة انجليزية", "subjects": "تربية فنية + لغة انجليزية"},
    "عماد الدين نصر كرم": {"spec": "لغة عربية", "subjects": "مهارات حياتية + لغة عربية"},
    "السيد الغريب بدوي": {"spec": "لغة عربية", "subjects": "مهارات حياتية + لغة عربية"},
    "محمد إبراهيم عبد الرحمن": {"spec": "رياضيات", "subjects": "رياضيات"},
    "أسامة أحمد سالم": {"spec": "رياضيات", "subjects": "مهارات رقمية + رياضيات"},
    "عماد بكر عارف": {"spec": "تربية بدنية", "subjects": "اجتماعيات + تربية بدنية"},
    "إبراهيم علي العتيبي": {"spec": "دراسات اسلامية", "subjects": "اجتماعيات + اسلامية"},
    "عيسى خالد العويس": {"spec": "لغة عربية", "subjects": "اسلامية"},
    "زيد بن علي التميمي": {"spec": "شريعة اسلامية", "subjects": "اسلامية"}
}

ADMIN_DATA = [
    {"name": "ابراهيم بن موسى التميمي", "title": "مدير المدرسة"},
    {"name": "محمد مبروك محمد السيد", "title": "وكيل الشؤون التعليمية"}
]

CLASSES_LIST = ["1/1", "1/2", "2/1", "2/2", "2/3", "3/1", "3/2", "3/3"]
GRADES_LIST = ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط"]
SESSIONS_LIST = ["الأولى", "الثانية", "الثالثة", "الرابعة", "الخامسة", "السادسة", "السابعة"]
VISITS_LIST = ["الأولى", "الثانية", "الثالثة", "الرابعة", "الخامسة", "السادسة", "السابعة", "الثامنة"]

# ==========================================
# 4. ترويسة البرنامج الرئيسية
# ==========================================
st.markdown("""
    <div class="header-box">
        <h1>مدارس الثغر النموذجية الأهلية - القسم المتوسط</h1>
        <h3>نظام المتابعة الصفية والإشرافية للمعلمين</h3>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "📝 استمارة تقييم جديدة", 
    "🔍 استرجاع وطباعة استمارة معلم", 
    "📊 التقارير العامة (Excel / PDF)"
])

# ==========================================
# التبويب الأول: تقييم معلم جديد
# ==========================================
with tab1:
    with st.form("evaluation_form", clear_on_submit=False):
        st.subheader("📋 البيانات الأساسية للزيارة الصفية")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_teacher = st.selectbox("اختر اسم المعلم:", list(TEACHERS_DATA.keys()))
            teacher_info = TEACHERS_DATA[selected_teacher]
            st.text_input("التخصص (تلقائي):", value=teacher_info['spec'], disabled=True)
            st.text_input("المواد المسندة:", value=teacher_info['subjects'], disabled=True)
            
        with col2:
            selected_grade = st.selectbox("الصف الدراسي:", GRADES_LIST)
            selected_class = st.selectbox("الفصل:", CLASSES_LIST)
            selected_session = st.selectbox("الحصة الدراسية:", SESSIONS_LIST)
            
        with col3:
            selected_visit = st.selectbox("رقم الزيارة:", VISITS_LIST)
            today_date = st.date_input("التاريخ (ميلادي):", datetime.date.today())

        st.markdown("---")
        st.subheader("🎯 بنود ومحاور التقييم الصفي (من 10 درجات لكل بند)")
        
        col_e1, col_e2 = st.columns(2)
        
        with col_e1:
            prep = st.slider("1. التخطيط والإعداد الجيد للدرس:", 1, 10, 9)
            intro = st.slider("2. التمهيد واستثارة دافعية الطلاب:", 1, 10, 8)
            content = st.slider("3. الإلمام بالمادة العلمية ووضوح الهدف:", 1, 10, 9)
            tech = st.slider("4. استخدام الوسائل والتقنيات التعليمية:", 1, 10, 8)
            mgmt = st.slider("5. إدارة الصف وحسن الانضباط:", 1, 10, 9)
            
        with col_e2:
            diff = st.slider("6. مراعاة الفروق الفردية بين الطلاب:", 1, 10, 8)
            strategy = st.slider("7. تطبيق استراتيجيات التدريس الحديثة:", 1, 10, 8)
            act = st.slider("8. الأنشطة الصفية والواجبات المنزلية:", 1, 10, 9)
            eval_p = st.slider("9. التقييم المستمر ومعالجة الأخطاء:", 1, 10, 9)

        total_val = prep + intro + content + tech + mgmt + diff + strategy + act + eval_p
        st.info(f"💡 **المجموع الكلي لدرجات التقييم الصفي:** {total_val} من 90")

        notes_input = st.text_area("توصيات وملحوظات المشرف الزائر:")

        st.markdown("---")
        st.subheader("✍️ التوقيعات والاعتماد الرسمي")
        
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            sign_teacher = st.selectbox("اسم المعلم المطلع:", list(TEACHERS_DATA.keys()), index=list(TEACHERS_DATA.keys()).index(selected_teacher))
            st.caption("توقيع المعلم: ______________________")
            
        with col_s2:
            admin_options = [f"{a['title']}: {a['name']}" for a in ADMIN_DATA]
            admin_choice = st.selectbox("الاعتماد الإداري:", admin_options)
            admin_title_part, admin_name_part = admin_choice.split(": ")
            st.caption(f"توقيع {admin_title_part}: ______________________")

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit_save = st.form_submit_button("💾 حفظ الاستمارة في قاعدة البيانات الدائمة", type="primary", use_container_width=True)

    if submit_save:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            INSERT INTO evaluations (
                teacher_name, specialization, assigned_subjects, grade, class_name, session_num, visit_num, 
                eval_date, prep_score, intro_score, content_score, tech_score, mgmt_score, 
                diff_score, strategy_score, act_score, eval_score, total_score, notes, 
                signed_teacher, signed_admin, admin_title
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            selected_teacher, teacher_info['spec'], teacher_info['subjects'], selected_grade, selected_class, selected_session, selected_visit,
            str(today_date), prep, intro, content, tech, mgmt, diff, strategy, act, eval_p, total_val,
            notes_input, sign_teacher, admin_name_part, admin_title_part
        ))
        conn.commit()
        conn.close()
        st.success("✅ تم حفظ استمارة التقييم بنجاح في قاعدة البيانات الدائمة!")

    if st.button("🖨️ طباعة الاستمارة الحالية (PDF)", type="secondary", use_container_width=True):
        st.components.v1.html("""<script>setTimeout(function() { window.parent.print(); }, 300);</script>""", height=0)

# ==========================================
# التبويب الثاني: استرجاع وطباعة استمارة معلم
# ==========================================
with tab2:
    st.subheader("🔎 البحث عن استمارة تقييم معلم سابقاً")
    
    col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
    
    with col_f1:
        search_teacher = st.selectbox("اختر اسم المعلم:", list(TEACHERS_DATA.keys()), key="search_t")
    with col_f2:
        search_visit = st.selectbox("اختر رقم الزيارة:", VISITS_LIST, key="search_v")
    with col_f3:
        st.markdown("<br>", unsafe_allow_html=True)
        btn_start = st.button("🚀 ابدأ البحث", type="primary", use_container_width=True)

    if btn_start:
        conn = sqlite3.connect(DB_FILE)
        df_search = pd.read_sql_query(
            "SELECT * FROM evaluations WHERE teacher_name = ? AND visit_num = ? ORDER BY id DESC LIMIT 1", 
            conn, params=(search_teacher, search_visit)
        )
        conn.close()
        
        if not df_search.empty:
            rec = df_search.iloc[0]
            st.markdown(f"""
                <div class="card-style">
                    <h2 style="text-align:center; color:#1e3a8a;">مدارس الثغر النموذجية الأهلية - القسم المتوسط</h2>
                    <h3 style="text-align:center; color:#0d9488;">استمارة المتابعة الصفية والإشرافية</h3>
                    <hr>
                    <table style="width:100%; text-align:right; font-size:16px; line-height:1.8;">
                        <tr>
                            <td><b>اسم المعلم:</b> {rec['teacher_name']}</td>
                            <td><b>التخصص:</b> {rec['specialization']}</td>
                            <td><b>التاريخ:</b> {rec['eval_date']}</td>
                        </tr>
                        <tr>
                            <td><b>الصف:</b> {rec['grade']}</td>
                            <td><b>الفصل:</b> {rec['class_name']}</td>
                            <td><b>الحصة:</b> {rec['session_num']} | <b>الزيارة:</b> {rec['visit_num']}</td>
                        </tr>
                    </table>
                    <hr>
                    <h4 style="color:#1e3a8a;">📊 ملخص تقييم البنود:</h4>
                    <ul>
                        <li><b>المجموع الكلي:</b> <span style="font-size:18px; color:#15803d;"><b>{rec['total_score']} / 90</b></span></li>
                        <li>التخطيط والإعداد: {rec['prep_score']} / 10 | التمهيد للدرس: {rec['intro_score']} / 10</li>
                        <li>المادة العلمية: {rec['content_score']} / 10 | استخدام التقنيات: {rec['tech_score']} / 10</li>
                        <li>إدارة الصف: {rec['mgmt_score']} / 10 | الفروق الفردية: {rec['diff_score']} / 10</li>
                        <li>استراتيجيات التدريس: {rec['strategy_score']} / 10 | الأنشطة والواجبات: {rec['act_score']} / 10</li>
                    </ul>
                    <p><b>التوصيات والملحوظات:</b> {rec['notes'] if rec['notes'] else 'لا يوجد'}</p>
                    <hr>
                    <table style="width:100%; text-align:center; margin-top:25px;">
                        <tr>
                            <td><b>توقيع المعلم:</b> {rec['signed_teacher']}<br>__________________</td>
                            <td><b>اعتماد {rec['admin_title']}:</b> {rec['signed_admin']}<br>__________________</td>
                        </tr>
                    </table>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🖨️ طباعة وتصدير الاستمارة (PDF)", key="print_single_rec", type="secondary"):
                st.components.v1.html("""<script>setTimeout(function() { window.parent.print(); }, 300);</script>""", height=0)
        else:
            st.warning("⚠️ لم يتم العثور على استمارة تقييم مسجلة لهذا المعلم في الزيارة المحددة.")

# ==========================================
# التبويب الثالث: التقارير العامة (Excel / PDF)
# ==========================================
with tab3:
    st.subheader("📑 التقرير العام لجميع المعلمين والتصدير")
    
    conn = sqlite3.connect(DB_FILE)
    df_all = pd.read_sql_query("SELECT * FROM evaluations ORDER BY id DESC", conn)
    conn.close()
    
    if not df_all.empty:
        st.dataframe(df_all, use_container_width=True)
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            output_excel = BytesIO()
            with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                df_all.to_excel(writer, index=False, sheet_name='تقييمات المعلمين')
            excel_bytes = output_excel.getvalue()
            
            st.download_button(
                label="📊 تحميل تقرير كافة المعلمين (Excel)",
                data=excel_bytes,
                file_name=f"تقرير_تقييم_معلمي_الثغر_{datetime.date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
        with col_exp2:
            if st.button("🖨️ طباعة وتصدير التقرير الكلي (PDF)", use_container_width=True):
                st.components.v1.html("""<script>setTimeout(function() { window.parent.print(); }, 300);</script>""", height=0)
    else:
        st.info("ℹ️ لا توجد بيانات مسجلة في قاعدة البيانات حتى الآن.")
