import streamlit as st
import pandas as pd
import sqlite3
import datetime
from io import BytesIO

# ==========================================
# 1. إعداد الصفحة والتصميم الاحترافي الشامل (RTL & CSS & Responsive A4)
# ==========================================
st.set_page_config(
    page_title="نظام المتابعة الصفية والإشرافية - مدارس الثغر النموذجية",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# كود التنسيق الجمالي المتقدم ودعم الجوال والطباعة A4
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
    text-align: right;
    background-color: #f8fafc;
}

/* ترويسة رئيسية جذابة */
.header-box {
    background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%);
    color: white;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 8px 20px rgba(13, 148, 136, 0.2);
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
    font-size: 18px;
}

/* بطاقات التنسيق الممركزة والبيانات الأساسية */
.centered-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
    margin: 0 auto 25px auto;
    max-width: 950px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
}
.centered-header {
    text-align: center;
    color: #1e3a8a;
    font-weight: 700;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e2e8f0;
}

/* شكل جمالي متطور للقوائم المنسدلة والحقول */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: #0d9488 !important;
    box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15) !important;
}
div[data-baseweb="select"] span {
    font-family: 'Tajawal', sans-serif !important;
    font-weight: 600 !important;
    color: #1e293b !important;
}

/* مدخلات النصوص والتواريخ */
.stTextInput input, .stDateInput input {
    border-radius: 10px !important;
    border: 1.5px solid #cbd5e1 !important;
    font-family: 'Tajawal', sans-serif !important;
}
.stTextInput input:focus, .stDateInput input:focus {
    border-color: #0d9488 !important;
}

/* شارات وشريط دلالات مستويات التقييم مثل الصورة */
.badge-container {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;
    padding: 10px 15px;
    background-color: #f1f5f9;
    border-radius: 10px;
}
.badge-weak {
    background-color: #fee2e2;
    color: #dc2626;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 14px;
}
.badge-excellent {
    background-color: #dcfce7;
    color: #16a34a;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 14px;
}

/* جدول عناصر التقييم الصفي الميمز (مطابق للصورة تماماً) */
.eval-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
    background-color: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.eval-table th {
    background-color: #eff6ff;
    color: #1e3a8a;
    padding: 14px;
    font-weight: 800;
    font-size: 15px;
    border-bottom: 2px solid #dbeafe;
    text-align: center;
}
.eval-table td {
    padding: 12px 14px;
    border-bottom: 1px solid #f1f5f9;
    color: #334155;
    font-size: 14px;
}
.domain-cell {
    font-weight: 800;
    color: #1e3a8a;
    vertical-align: middle;
    text-align: center;
    background-color: #f8fafc;
}

/* تحسين زر الاستمارة والأزرار الرئيسية */
.stButton button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Tajawal', sans-serif !important;
    transition: all 0.3s ease !important;
}

/* التوافق التام مع الجوال */
@media (max-width: 768px) {
    .header-box h1 { font-size: 20px; }
    .header-box h3 { font-size: 15px; }
    .centered-card { padding: 15px; }
    .eval-table th, .eval-table td { padding: 8px 6px; font-size: 12px; }
    div[data-testid="column"] { width: 100% !important; margin-bottom: 10px; }
}

/* التنسيق المخصص للطباعة بحجم ورقة A4 exact portrait */
@media print {
    @page {
        size: A4 portrait;
        margin: 10mm 10mm 10mm 10mm;
    }
    body, .stApp {
        background-color: white !important;
        color: black !important;
    }
    .no-print, header, footer, [data-testid="stSidebar"], .stTabs [role="tablist"], button {
        display: none !important;
    }
    .centered-card {
        box-shadow: none !important;
        border: 1px solid #666 !important;
        max-width: 100% !important;
        width: 100% !important;
        padding: 10px !important;
        margin: 0 !important;
    }
    .header-box {
        background: #1e3a8a !important;
        color: white !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
        padding: 15px !important;
        border-radius: 8px !important;
    }
    .eval-table th {
        background-color: #e2e8f0 !important;
        color: black !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
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
            semester TEXT,
            session_num TEXT,
            visit_num TEXT,
            eval_date TEXT,
            q1_score INTEGER,
            q2_score INTEGER,
            q3_score INTEGER,
            q4_score INTEGER,
            q5_score INTEGER,
            q6_score INTEGER,
            q7_score INTEGER,
            q8_score INTEGER,
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
# 3. البيانات الأساسية والربط بين الصفوف والفصول
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

# الربط الديناميكي بين الصفوف والفصول (المطلب الخامس)
GRADE_CLASSES_MAP = {
    "الأول المتوسط": ["1/1", "1/2"],
    "الثاني المتوسط": ["2/1", "2/2", "2/3"],
    "الثالث المتوسط": ["3/1", "3/2", "3/3"]
}

SEMESTERS_LIST = ["الفصل الدراسي الأول", "الفصل الدراسي الثاني", "الفصل الدراسي الثالث"]
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
    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="centered-header">📋 البيانات الأساسية للزيارة الصفية</h2>', unsafe_allow_html=True)
    
    with st.form("evaluation_form", clear_on_submit=False):
        # الجزء الأول: البيانات الأساسية في الوسط
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_teacher = st.selectbox("اختر اسم المعلم:", list(TEACHERS_DATA.keys()))
            teacher_info = TEACHERS_DATA[selected_teacher]
            st.text_input("التخصص (تلقائي):", value=teacher_info['spec'], disabled=True)
            st.text_input("المواد المسندة:", value=teacher_info['subjects'], disabled=True)
            
        with col2:
            # الصف الدراسي والفصل الدراسي
            selected_grade = st.selectbox("الصف الدراسي:", list(GRADE_CLASSES_MAP.keys()))
            # الربط التلقائي للفصول بالصف المختار
            available_classes = GRADE_CLASSES_MAP[selected_grade]
            selected_class = st.selectbox("الفصل:", available_classes)
            # إضافة قائمة اختيار الفصل الدراسي الأول أو الثاني
            selected_semester = st.selectbox("الفصل الدراسي:", SEMESTERS_LIST)
            
        with col3:
            selected_session = st.selectbox("الحصة الدراسية:", SESSIONS_LIST)
            selected_visit = st.selectbox("رقم الزيارة:", VISITS_LIST)
            today_date = st.date_input("التاريخ (ميلادي):", datetime.date.today())

        st.markdown("---")
        
        # الجزء الثاني: استمارة التقييم بنفس شكل الصورة في المصادر
        st.markdown('<h3>🎯 عناصر التقييم ومستويات الأداء</h3>', unsafe_allow_html=True)
        
        # شريط الدلالات (مطابق للصورة تماماً)
        st.markdown("""
        <div class="badge-container">
            <span style="font-weight:700; color:#1e3a8a; margin-left:15px;">عناصر التقييم:</span>
            <span class="badge-weak">1: ضعيف</span>
            <span class="badge-excellent">4: متميز</span>
        </div>
        """, unsafe_allow_html=True)
        
        # بنود التقييم المطابقة للصورة
        rubric_items = [
            {"id": "q1", "domain": "التخطيط", "num": 1, "text": "يخطط المعلم/ة للدرس على المنصة تخطيطا متوافقا مع الخطة الفصلية للمقرر."},
            {"id": "q2", "domain": "التخطيط", "num": 2, "text": "متابعة الواجبات المنزلية وتقديم التغذية الراجعة لها."},
            {"id": "q3", "domain": "التخطيط", "num": 3, "text": "ادارة مشاركة الطالب/ة الصوتية والمكتوبة بكفاءة."},
            {"id": "q4", "domain": "التخطيط", "num": 4, "text": "متابعة الطالب/ة وتسجيل الحضور ورصد حالات الغياب في المنصة أو الصف."},
            {"id": "q5", "domain": "التنفيذ والتمهيد", "num": 5, "text": "التمهيد واستثارة دافعية الطلاب ومراعاة الفروق الفردية."},
            {"id": "q6", "domain": "التنفيذ والتمهيد", "num": 6, "text": "استخدام الوسائل والتقنيات التعليمية واستراتيجيات التدريس الحديثة."},
            {"id": "q7", "domain": "إدارة الصف والتقويم", "num": 7, "text": "إدارة وقت الحصة وحسن الانضباط والتفاعل الإيجابي."},
            {"id": "q8", "domain": "إدارة الصف والتقويم", "num": 8, "text": "التقييم المستمر ومعالجة الأخطاء وتنفيذ الأنشطة الصفية."}
        ]
        
        scores = {}
        
        # عرض الجدول التفاعلي بنفس هيئة وتنسيق الصورة
        st.markdown("""
        <table class="eval-table">
            <thead>
                <tr>
                    <th style="width: 15%;">المجال</th>
                    <th style="width: 8%;">م</th>
                    <th style="width: 52%;">عناصر التقييم</th>
                    <th style="width: 25%;">مستويات الأداء (1 - 4)</th>
                </tr>
            </thead>
        </table>
        """, unsafe_allow_html=True)
        
        for item in rubric_items:
            col_t1, col_t2, col_t3, col_t4 = st.columns([1.5, 0.8, 5.2, 2.5])
            with col_t1:
                st.markdown(f"<div style='text-align:center; font-weight:700; color:#1e3a8a; padding-top:10px;'>{item['domain']}</div>", unsafe_allow_html=True)
            with col_t2:
                st.markdown(f"<div style='text-align:center; font-weight:700; padding-top:10px;'>{item['num']}</div>", unsafe_allow_html=True)
            with col_t3:
                st.markdown(f"<div style='padding-top:10px; color:#1e293b;'>{item['text']}</div>", unsafe_allow_html=True)
            with col_t4:
                scores[item['id']] = st.radio(
                    f"الدرجة {item['num']}",
                    options=[1, 2, 3, 4],
                    index=3,
                    horizontal=True,
                    key=f"radio_{item['id']}",
                    label_visibility="collapsed"
                )
            st.markdown("<hr style='margin: 4px 0; border: 0.5px solid #f1f5f9;'>", unsafe_allow_html=True)

        total_val = sum(scores.values())
        max_val = len(rubric_items) * 4
        
        st.markdown(f"""
        <div style="background-color:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:15px; text-align:center; margin-top:20px;">
            <span style="font-size:18px; font-weight:800; color:#166534;">💡 المجموع الكلي لدرجات التقييم الصفي: {total_val} من {max_val}</span>
        </div>
        """, unsafe_allow_html=True)

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
                teacher_name, specialization, assigned_subjects, grade, class_name, semester,
                session_num, visit_num, eval_date, q1_score, q2_score, q3_score, q4_score,
                q5_score, q6_score, q7_score, q8_score, total_score, notes, 
                signed_teacher, signed_admin, admin_title
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            selected_teacher, teacher_info['spec'], teacher_info['subjects'], selected_grade, selected_class, selected_semester,
            selected_session, selected_visit, str(today_date), scores['q1'], scores['q2'], scores['q3'], scores['q4'],
            scores['q5'], scores['q6'], scores['q7'], scores['q8'], total_val, notes_input,
            sign_teacher, admin_name_part, admin_title_part
        ))
        conn.commit()
        conn.close()
        st.success("✅ تم حفظ استمارة التقييم بنجاح في قاعدة البيانات الدائمة!")

    if st.button("🖨️ طباعة الاستمارة الحالية (A4 / PDF)", type="secondary", use_container_width=True):
        st.components.v1.html("""<script>setTimeout(function() { window.parent.print(); }, 300);</script>""", height=0)

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# التبويب الثاني: استرجاع وطباعة استمارة معلم
# ==========================================
with tab2:
    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
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
                <div style="border: 2px solid #1e3a8a; border-radius:12px; padding:20px; background-color:#ffffff;">
                    <h2 style="text-align:center; color:#1e3a8a; font-weight:900;">مدارس الثغر النموذجية الأهلية - القسم المتوسط</h2>
                    <h3 style="text-align:center; color:#0d9488; font-weight:700;">بطاقة تقييم الأداء الصفي والزيارة الإشرافية</h3>
                    <hr style="border-top: 2px solid #0d9488;">
                    
                    <table style="width:100%; text-align:right; font-size:15px; line-height:2;">
                        <tr>
                            <td><b>اسم المعلم:</b> {rec['teacher_name']}</td>
                            <td><b>التخصص:</b> {rec['specialization']}</td>
                            <td><b>التاريخ:</b> {rec['eval_date']}</td>
                        </tr>
                        <tr>
                            <td><b>الصف:</b> {rec['grade']}</td>
                            <td><b>الفصل:</b> {rec['class_name']}</td>
                            <td><b>الفصل الدراسي:</b> {rec.get('semester', 'الأول')}</td>
                        </tr>
                        <tr>
                            <td><b>الحصة:</b> {rec['session_num']}</td>
                            <td><b>رقم الزيارة:</b> {rec['visit_num']}</td>
                            <td><b>المواد:</b> {rec['assigned_subjects']}</td>
                        </tr>
                    </table>
                    <hr>
                    <h4 style="color:#1e3a8a;">📊 ملخص تقييم البنود:</h4>
                    <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:14px;" border="1" cellpadding="8">
                        <tr style="background-color:#f1f5f9; text-align:center;">
                            <th>عنصر التقييم</th>
                            <th>الدرجة المستحقة (من 4)</th>
                        </tr>
                        <tr><td>تخطيط الدرس على المنصة وتوافقه مع الخطة</td><td style="text-align:center; font-weight:bold;">{rec.get('q1_score', 4)}</td></tr>
                        <tr><td>متابعة الواجبات وتغذية رجعية</td><td style="text-align:center; font-weight:bold;">{rec.get('q2_score', 4)}</td></tr>
                        <tr><td>إدارة مشاركة الطلاب الصوتية والمكتوبة</td><td style="text-align:center; font-weight:bold;">{rec.get('q3_score', 4)}</td></tr>
                        <tr><td>متابعة وتسجيل الحضور والغياب</td><td style="text-align:center; font-weight:bold;">{rec.get('q4_score', 4)}</td></tr>
                    </table>
                    
                    <div style="margin-top:15px; background-color:#f8fafc; padding:10px; border-radius:8px;">
                        <b>المجموع الكلي للتقييم:</b> <span style="font-size:18px; color:#16a34a; font-weight:bold;">{rec['total_score']} / 32</span>
                    </div>
                    
                    <p style="margin-top:15px;"><b>التوصيات والملحوظات:</b> {rec['notes'] if rec['notes'] else 'لا يوجد'}</p>
                    <hr>
                    <table style="width:100%; text-align:center; margin-top:25px;">
                        <tr>
                            <td><b>توقيع المعلم المطلع:</b> {rec['signed_teacher']}<br>__________________</td>
                            <td><b>اعتماد {rec['admin_title']}:</b> {rec['signed_admin']}<br>__________________</td>
                        </tr>
                    </table>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🖨️ طباعة الاستمارة المسترجعة (A4 / PDF)", key="print_single_rec", type="secondary"):
                st.components.v1.html("""<script>setTimeout(function() { window.parent.print(); }, 300);</script>""", height=0)
        else:
            st.warning("⚠️ لم يتم العثور على استمارة تقييم مسجلة لهذا المعلم في الزيارة المحددة.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# التبويب الثالث: التقارير العامة (Excel / PDF)
# ==========================================
with tab3:
    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
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
        
    st.markdown('</div>', unsafe_allow_html=True)

