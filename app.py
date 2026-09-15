import streamlit as st
import pandas as pd
import sqlite3
import datetime
from io import BytesIO

# ==========================================
# 1. إعداد الصفحة والتصميم الاحترافي الشامل (RTL & Right-Aligned & Responsive A4)
# ==========================================
st.set_page_config(
    page_title="نظام المتابعة الصفية والإشرافية - مدارس الثغر النموذجية",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# كود التنسيق الجمالي المتقدم مع المحاذاة الكاملة لليمين ودعم الطباعة A4
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
    background-color: #f8fafc;
}

/* محاذاة كافة المدخلات والنصوص والعناوين لليمين */
div, p, h1, h2, h3, h4, h5, h6, label, span, input, select, textarea, button {
    text-align: right !important;
    direction: rtl !important;
}

/* ترويسة رئيسية جذابة ومحاذاة ممتازة */
.header-box {
    background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%);
    color: white;
    padding: 22px;
    border-radius: 16px;
    text-align: center !important;
    margin-bottom: 25px;
    box-shadow: 0 8px 20px rgba(13, 148, 136, 0.2);
}
.header-box h1 {
    color: #ffffff;
    font-weight: 900;
    margin: 0;
    font-size: 26px;
    text-align: center !important;
}
.header-box h3 {
    color: #fef08a;
    margin-top: 8px;
    font-weight: 700;
    font-size: 18px;
    text-align: center !important;
}

/* بطاقات التنسيق الممركزة والبيانات الأساسية */
.centered-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
    margin: 0 auto 25px auto;
    max-width: 1050px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
}
.centered-header {
    text-align: right !important;
    color: #1e3a8a;
    font-weight: 800;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e2e8f0;
}

/* شكل جمالي متطور للقوائم المنسدلة والحقول وتنسيق يمين */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    text-align: right !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: #0d9488 !important;
    box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15) !important;
}
div[data-baseweb="select"] span {
    font-family: 'Tajawal', sans-serif !important;
    font-weight: 600 !important;
    color: #1e293b !important;
    text-align: right !important;
}

/* مدخلات النصوص والتواريخ */
.stTextInput input, .stDateInput input, .stTextArea textarea {
    border-radius: 10px !important;
    border: 1.5px solid #cbd5e1 !important;
    font-family: 'Tajawal', sans-serif !important;
    text-align: right !important;
}

/* شارات وشريط دلالات مستويات التقييم (مستويات 1 إلى 5) */
.badge-container {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;
    padding: 12px 18px;
    background-color: #f1f5f9;
    border-radius: 10px;
    direction: rtl !important;
}
.badge-item {
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 14px;
}
.badge-1 { background-color: #fee2e2; color: #dc2626; }
.badge-2 { background-color: #ffedd5; color: #c2410c; }
.badge-3 { background-color: #fef9c3; color: #ca8a04; }
.badge-4 { background-color: #e0f2fe; color: #0369a1; }
.badge-5 { background-color: #dcfce7; color: #16a34a; }

/* جدول عناصر التقييم الصفي محاذى لليمين بالكامل */
.eval-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
    background-color: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    direction: rtl !important;
}
.eval-table th {
    background-color: #eff6ff;
    color: #1e3a8a;
    padding: 12px 15px;
    font-weight: 800;
    font-size: 15px;
    border-bottom: 2px solid #dbeafe;
    text-align: right !important;
}
.eval-table td {
    padding: 12px 15px;
    border-bottom: 1px solid #f1f5f9;
    text-align: right !important;
}

/* محاذاة أزرار الخيارات الراديو (Radio buttons) لليمين */
div[role="radiogroup"] {
    display: flex !important;
    flex-direction: row-reverse !important;
    justify-content: flex-end !important;
    gap: 15px !important;
}

/* التوافق مع الجوال */
@media (max-width: 768px) {
    .header-box h1 { font-size: 20px; }
    .header-box h3 { font-size: 15px; }
    .centered-card { padding: 15px; }
    div[data-testid="column"] { width: 100% !important; margin-bottom: 10px; }
    div[role="radiogroup"] { gap: 8px !important; }
}

/* التنسيق المخصص للطباعة بحجم ورقة A4 portrait */
@media print {
    @page {
        size: A4 portrait;
        margin: 8mm 8mm 8mm 8mm;
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
        padding: 8px !important;
        margin: 0 !important;
    }
    .header-box {
        background: #1e3a8a !important;
        color: white !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
        padding: 12px !important;
        border-radius: 6px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إنشاء قاعدة البيانات الدائمة (SQLite)
# ==========================================
DB_FILE = "thagher_evaluations_v5.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_name TEXT,
            specialization TEXT,
            assigned_subjects TEXT,
            selected_subject TEXT,
            grade TEXT,
            class_name TEXT,
            semester TEXT,
            session_num TEXT,
            visit_num TEXT,
            eval_date TEXT,
            q1_score INTEGER, q2_score INTEGER, q3_score INTEGER, q4_score INTEGER,
            q5_score INTEGER, q6_score INTEGER, q7_score INTEGER, q8_score INTEGER,
            q9_score INTEGER, q10_score INTEGER, q11_score INTEGER, q12_score INTEGER,
            q13_score INTEGER, q14_score INTEGER, q15_score INTEGER, q16_score INTEGER,
            q17_score INTEGER, q18_score INTEGER, q19_score INTEGER, q20_score INTEGER,
            total_score INTEGER,
            notes TEXT,
            signed_teacher TEXT,
            signed_vp TEXT,
            signed_principal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS custom_teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_name TEXT UNIQUE,
            specialization TEXT,
            assigned_subjects TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 3. البيانات الأساسية لقائمة المعلمين والإدارة
# ==========================================
DEFAULT_TEACHERS = {
    "محمد سامي السعيد": {"spec": "مهارات رقمية", "subjects": ["مهارات رقمية"]},
    "علي محمد معوض": {"spec": "علوم", "subjects": ["علوم"]},
    "أحمد عبد الحميد سعيد": {"spec": "علوم", "subjects": ["علوم"]},
    "محمد عبد المنعم أبو كيلة": {"spec": "لغة انجليزية", "subjects": ["تربية فنية", "لغة انجليزية"]},
    "هيثم رضا عطية": {"spec": "لغة انجليزية", "subjects": ["تربية فنية", "لغة انجليزية"]},
    "عماد الدين نصر كرم": {"spec": "لغة عربية", "subjects": ["مهارات حياتية", "لغة عربية"]},
    "السيد الغريب بدوي": {"spec": "لغة عربية", "subjects": ["مهارات حياتية", "لغة عربية"]},
    "محمد إبراهيم عبد الرحمن": {"spec": "رياضيات", "subjects": ["رياضيات"]},
    "أسامة أحمد سالم": {"spec": "رياضيات", "subjects": ["مهارات رقمية", "رياضيات"]},
    "عماد بكر عارف": {"spec": "تربية بدنية", "subjects": ["اجتماعيات", "تربية بدنية"]},
    "إبراهيم علي العتيبي": {"spec": "دراسات اسلامية", "subjects": ["اجتماعيات", "اسلامية"]},
    "عيسى خالد العويس": {"spec": "لغة عربية", "subjects": ["اسلامية"]},
    "زيد بن علي التميمي": {"spec": "شريعة اسلامية", "subjects": ["اسلامية"]}
}

def get_all_teachers():
    teachers = DEFAULT_TEACHERS.copy()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT teacher_name, specialization, assigned_subjects FROM custom_teachers")
    rows = c.fetchall()
    conn.close()
    for r in rows:
        name, spec, subs = r[0], r[1], r[2]
        sub_list = [s.strip() for s in subs.split('+') if s.strip()] if '+' in subs else [subs]
        teachers[name] = {"spec": spec, "subjects": sub_list}
    return teachers

GRADE_CLASSES_MAP = {
    "الأول المتوسط": ["1/1", "1/2"],
    "الثاني المتوسط": ["2/1", "2/2", "2/3"],
    "الثالث المتوسط": ["3/1", "3/2", "3/3"]
}

SEMESTERS_LIST = ["الفصل الدراسي الأول", "الفصل الدراسي الثاني"]
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

tab1, tab2, tab3, tab4 = st.tabs([
    "📝 استمارة تقييم جديدة",
    "🔍 استرجاع وتعديل / حذف استمارة",
    "➕ إضافة معلم جديد",
    "📊 التقارير العامة (Excel / PDF)"
])

# ==========================================
# التبويب الأول: تقييم معلم جديد
# ==========================================
with tab1:
    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="centered-header">📋 البيانات الأساسية للزيارة الصفية (ربط المعلم والتخصص)</h2>', unsafe_allow_html=True)
    
    teachers_data = get_all_teachers()
    teacher_names = list(teachers_data.keys())
    
    # اختيار المعلم والربط الديناميكي الفوري بالتخصص والمواد
    col_top1, col_top2, col_top3 = st.columns(3)
    
    with col_top1:
        selected_teacher = st.selectbox("اختر اسم المعلم:", teacher_names, key="eval_t_select")
        teacher_info = teachers_data[selected_teacher]
        # إظهار التخصص المرتبط بالمعلم تلقائياً بشكل واضح ورسمي
        teacher_spec = teacher_info['spec']
        st.text_input("التخصص (مرتبط تلقائياً):", value=teacher_spec, disabled=True, key="teacher_spec_disp")
        
    with col_top2:
        subjects_list = teacher_info['subjects']
        if len(subjects_list) > 1:
            selected_subject = st.selectbox("المادة المراد تقييمها في هذه الزيارة:", subjects_list, key="eval_sub_select")
        else:
            selected_subject = subjects_list[0]
            st.text_input("المادة المسندة:", value=selected_subject, disabled=True, key="teacher_sub_disp")
            
        selected_semester = st.selectbox("الفصل الدراسي:", SEMESTERS_LIST, key="eval_sem_select")
        
    with col_top3:
        selected_grade = st.selectbox("الصف الدراسي:", list(GRADE_CLASSES_MAP.keys()), key="eval_g_select")
        available_classes = GRADE_CLASSES_MAP[selected_grade]
        selected_class = st.selectbox("الفصل:", available_classes, key="eval_c_select")
        
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        selected_session = st.selectbox("الحصة الدراسية:", SESSIONS_LIST, key="eval_sess_select")
    with col_sub2:
        selected_visit = st.selectbox("رقم الزيارة:", VISITS_LIST, key="eval_v_select")
        today_date = st.date_input("التاريخ (ميلادي):", datetime.date.today(), key="eval_date_select")

    st.markdown("---")
    st.markdown('<h3>🎯 عناصر التقييم الصفي الـ 20 (احتساب من 100 درجة - 5 درجات لكل بند)</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="badge-container">
        <span style="font-weight:800; color:#1e3a8a; margin-left:15px;">مستويات الأداء والدرجات (من 1 إلى 5 درجات):</span>
        <span class="badge-item badge-1">1: ضعيف</span>
        <span class="badge-item badge-2">2: مقبول</span>
        <span class="badge-item badge-3">3: جيد</span>
        <span class="badge-item badge-4">4: جيد جداً</span>
        <span class="badge-item badge-5">5: متميز</span>
    </div>
    """, unsafe_allow_html=True)
    
    # قائمة البنود الـ 20 الكاملة من المصدر
    rubric_items = [
        # المجال الأول: التخطيط
        {"id": "q1", "domain": "التخطيط", "num": 1, "text": "يخطط المعلم/ة للدرس على المنصة تخطيطا متوافقا مع الخطة الفصلية للمقرر."},
        {"id": "q2", "domain": "التخطيط", "num": 2, "text": "متابعة الواجبات المنزلية وتقديم التغذية الراجعة لها."},
        {"id": "q3", "domain": "التخطيط", "num": 3, "text": "ادارة مشاركة الطالب/ة الصوتية والمكتوبة بكفاءة."},
        {"id": "q4", "domain": "التخطيط", "num": 4, "text": "متابعة الطالب/ة وتسجيل الحضور ورصد حالات الغياب في المنصة أو الصف."},
        
        # المجال الثاني: التعلم والتعليم
        {"id": "q5", "domain": "التعلم والتعليم", "num": 5, "text": "ينفذ المعلم/ة إجراءات الدرس وفق خارطة سير الدرس (التمهيد، أنشطة التعلم والتقويم، التقويم الختامي)."},
        {"id": "q6", "domain": "التعلم والتعليم", "num": 6, "text": "الالتزام باللغة العربية الفصحى عند طرح الأسئلة الصفية."},
        {"id": "q7", "domain": "التعلم والتعليم", "num": 7, "text": "يطبق المعلم/ة إستراتيجيات تدريس تراعي قدرات المتعلمين والفروق الفردية بينهم وتتسق مع الموقف التعليمي."},
        {"id": "q8", "domain": "التعلم والتعليم", "num": 8, "text": "يستخدم المعلم/ة أساليب تحفيز تعزز الدافعية لدى المتعلمين."},
        {"id": "q9", "domain": "التعلم والتعليم", "num": 9, "text": "ينخرط المتعلمون في أنشطة تعلم متنوعة ومتمايزة ويجيبون عن أسئلة صفية تنمي مهارات التفكير العليا."},
        {"id": "q10", "domain": "التعلم والتعليم", "num": 10, "text": "يحصل المتعلمون على تغذية راجعة تركز على تحسن أدائهم وفق الموقف التعليمي."},
        {"id": "q11", "domain": "التعلم والتعليم", "num": 11, "text": "يمارس المتعلمون أنشطة أدائية تقيس مدى فهمهم وتمكنهم من المهارات (أنشطة كتابية/ ملفات/ مطويات/ أوراق عمل/ مجسمات /تجارب عملية، إلخ)."},
        {"id": "q12", "domain": "التعلم والتعليم", "num": 12, "text": "يستخدم المتعلمون أدوات رقمية لجمع المعلومات ويوظفونها في عملية التعلم."},
        {"id": "q13", "domain": "التعلم والتعليم", "num": 13, "text": "يربط المتعلمون أنشطة التعلم بتطبيقات عملية من واقع الحياة."},
        {"id": "q14", "domain": "التعلم والتعليم", "num": 14, "text": "يظهر المتعلمون تمكنا من مهارات القراءة والكتابة والحساب، وينمون ثروتهم اللغوية."},
        {"id": "q15", "domain": "التعلم والتعليم", "num": 15, "text": "يتمكن المتعلمون من المعارف والمهارات في المقرر الدراسي بنسبة ما لا يقل عن 85% (اختبار الوحدات والمقننة - اختبار الفترة – الاختبار النهائي)."},
        
        # المجال الثالث: الشخصية المتوازنة
        {"id": "q16", "domain": "الشخصية المتوازنة", "num": 16, "text": "يتمثل المتعلمون القيم الإسلامية والمواطنة والسلوك الصفي الحسن."},
        {"id": "q17", "domain": "الشخصية المتوازنة", "num": 17, "text": "يتحمل المتعلمون مسؤولية تعلمهم ويمارسون التوجه الذاتي (القيادة، التنسيق. الخ) – الصف المقلوب."},
        {"id": "q18", "domain": "الشخصية المتوازنة", "num": 18, "text": "يشارك المتعلمون في أنشطة جماعية ويعملون بروح الفريق ويسود الاحترام المتبادل والتعاطف بينهم."},
        {"id": "q19", "domain": "الشخصية المتوازنة", "num": 19, "text": "يبادر المتعلمون للتعبير عن أفكارهم وآرائهم بثقة ووضوح في بيئة التعلم."},
        {"id": "q20", "domain": "الشخصية المتوازنة", "num": 20, "text": "القدرة على إدارة وضبط النظام داخل الصف وفق القواعد التنظيمية."}
    ]
    
    scores = {}
    
    st.markdown("""
    <table class="eval-table">
        <thead>
            <tr>
                <th style="width: 15%;">المجال</th>
                <th style="width: 5%;">م</th>
                <th style="width: 50%;">عناصر التقييم</th>
                <th style="width: 30%;">الدرجة المحددة (من 1 إلى 5 درجات)</th>
            </tr>
        </thead>
    </table>
    """, unsafe_allow_html=True)
    
    for item in rubric_items:
        col_t1, col_t2, col_t3, col_t4 = st.columns([1.5, 0.5, 5.0, 3.0])
        with col_t1:
            st.markdown(f"<div style='text-align:right; font-weight:700; color:#1e3a8a; padding-top:8px;'>{item['domain']}</div>", unsafe_allow_html=True)
        with col_t2:
            st.markdown(f"<div style='text-align:right; font-weight:700; padding-top:8px;'>{item['num']}</div>", unsafe_allow_html=True)
        with col_t3:
            st.markdown(f"<div style='text-align:right; padding-top:8px; color:#1e293b; line-height:1.5;'>{item['text']}</div>", unsafe_allow_html=True)
        with col_t4:
            # كل بند يتضمن الخيارات من 1 إلى 5 درجات (20 بند × 5 درجات = 100)
            scores[item['id']] = st.radio(
                f"الدرجة {item['num']}",
                options=[1, 2, 3, 4, 5],
                index=4, # افتراضياً 5 درجات
                horizontal=True,
                key=f"radio_v5_{item['id']}",
                label_visibility="collapsed"
            )
        st.markdown("<hr style='margin: 3px 0; border: 0.5px solid #f1f5f9;'>", unsafe_allow_html=True)

    # احتساب المجموع النهائي من 100 درجة (كل بند من 5)
    total_val = sum(scores.values())
    max_val = 100
    percentage = (total_val / max_val) * 100
    
    st.markdown(f"""
    <div style="background-color:#f0fdf4; border:2px solid #bbf7d0; border-radius:14px; padding:18px; text-align:center !important; margin-top:20px; box-shadow:0 4px 12px rgba(22, 163, 74, 0.1);">
        <span style="font-size:22px; font-weight:900; color:#166534;">🌟 المجموع الكلي لدرجات المعلم: {total_val} من {max_val} درجات ({percentage:.1f}%)</span>
    </div>
    """, unsafe_allow_html=True)

    notes_input = st.text_area("توصيات وملحوظات المشرف الزائر:", key="notes_v5_input")

    st.markdown("---")
    st.subheader("✍️ الاعتمادات والتوقيعات الرسمية")
    
    col_sig1, col_sig2, col_sig3 = st.columns(3)
    
    with col_sig1:
        st.markdown(f"""
        <div style="text-align:right; background:#f8fafc; padding:15px; border-radius:12px; border:1px solid #cbd5e1;">
            <h5 style="color:#1e3a8a; font-weight:800; margin-bottom:8px; text-align:right;">المعلم المطلع</h5>
            <p style="font-weight:700; color:#0f172a; margin-bottom:15px; text-align:right;">{selected_teacher}</p>
            <p style="color:#64748b; margin:0; text-align:right;">التوقيع: __________________</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_sig2:
        st.markdown("""
        <div style="text-align:right; background:#f8fafc; padding:15px; border-radius:12px; border:1px solid #cbd5e1;">
            <h5 style="color:#1e3a8a; font-weight:800; margin-bottom:8px; text-align:right;">وكيل المدرسة للشؤون التعليمية</h5>
            <p style="font-weight:700; color:#0f172a; margin-bottom:15px; text-align:right;">محمد مبروك محمد السيد</p>
            <p style="color:#64748b; margin:0; text-align:right;">التوقيع: __________________</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_sig3:
        st.markdown("""
        <div style="text-align:right; background:#f8fafc; padding:15px; border-radius:12px; border:1px solid #cbd5e1;">
            <h5 style="color:#1e3a8a; font-weight:800; margin-bottom:8px; text-align:right;">مدير المدرسة</h5>
            <p style="font-weight:700; color:#0f172a; margin-bottom:15px; text-align:right;">إبراهيم بن موسى التميمي</p>
            <p style="color:#64748b; margin:0; text-align:right;">التوقيع: __________________</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_save_btn1, col_save_btn2 = st.columns(2)
    with col_save_btn1:
        submit_save = st.button("💾 حفظ استمارة التقييم الحالية (من 100)", type="primary", use_container_width=True, key="save_eval_v5")
    with col_save_btn2:
        if st.button("🖨️ طباعة الاستمارة مباشرة (A4)", type="secondary", use_container_width=True, key="print_eval_v5"):
            st.components.v1.html("""<script>setTimeout(function() { window.parent.print(); }, 300);</script>""", height=0)

    if submit_save:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            INSERT INTO evaluations (
                teacher_name, specialization, assigned_subjects, selected_subject, grade, class_name,
                semester, session_num, visit_num, eval_date,
                q1_score, q2_score, q3_score, q4_score, q5_score, q6_score, q7_score, q8_score, q9_score, q10_score,
                q11_score, q12_score, q13_score, q14_score, q15_score, q16_score, q17_score, q18_score, q19_score, q20_score,
                total_score, notes, signed_teacher, signed_vp, signed_principal
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            selected_teacher, teacher_spec, ", ".join(subjects_list), selected_subject, selected_grade, selected_class,
            selected_semester, selected_session, selected_visit, str(today_date),
            scores['q1'], scores['q2'], scores['q3'], scores['q4'], scores['q5'], scores['q6'], scores['q7'], scores['q8'], scores['q9'], scores['q10'],
            scores['q11'], scores['q12'], scores['q13'], scores['q14'], scores['q15'], scores['q16'], scores['q17'], scores['q18'], scores['q19'], scores['q20'],
            total_val, notes_input, selected_teacher, "محمد مبروك محمد السيد", "إبراهيم بن موسى التميمي"
        ))
        conn.commit()
        conn.close()
        st.success(f"✅ تم حفظ تقييم المعلم ({selected_teacher}) بنجاح بمرتبة ({total_val} من 100) في قاعدة البيانات!")

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# التبويب الثاني: استرجاع وتعديل / حذف استمارة
# ==========================================
with tab2:
    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
    st.subheader("🔍 استرجاع وإدارة استمارات التقييم (من 100)")
    
    teachers_data = get_all_teachers()
    
    col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
    with col_f1:
        search_teacher = st.selectbox("اختر اسم المعلم للبحث:", list(teachers_data.keys()), key="search_t_v5")
    with col_f2:
        search_visit = st.selectbox("اختر رقم الزيارة:", VISITS_LIST, key="search_v_v5")
    with col_f3:
        st.markdown("<br>", unsafe_allow_html=True)
        btn_start = st.button("🚀 ابدأ البحث", type="primary", use_container_width=True, key="btn_search_v5")

    if btn_start or st.session_state.get('search_active_v5'):
        st.session_state['search_active_v5'] = True
        conn = sqlite3.connect(DB_FILE)
        df_search = pd.read_sql_query(
            "SELECT * FROM evaluations WHERE teacher_name = ? AND visit_num = ? ORDER BY id DESC LIMIT 1", 
            conn, params=(search_teacher, search_visit)
        )
        conn.close()
        
        if not df_search.empty:
            rec = df_search.iloc[0]
            rec_id = int(rec['id'])
            
            st.markdown(f"""
                <div style="border:2px solid #1e3a8a; border-radius:14px; padding:22px; background-color:#ffffff; text-align:right;">
                    <h2 style="text-align:center !important; color:#1e3a8a; font-weight:900;">مدارس الثغر النموذجية الأهلية - القسم المتوسط</h2>
                    <h3 style="text-align:center !important; color:#0d9488; font-weight:700;">بطاقة تقييم الأداء الصفي الرسمية (20 بنداً - من 100)</h3>
                    <hr style="border-top: 2px solid #0d9488;">
                    
                    <table style="width:100%; text-align:right; font-size:15px; line-height:2.2; direction:rtl;">
                        <tr>
                            <td><b>اسم المعلم:</b> {rec['teacher_name']}</td>
                            <td><b>التخصص:</b> {rec['specialization']}</td>
                            <td><b>المادة المزارة:</b> {rec['selected_subject']}</td>
                        </tr>
                        <tr>
                            <td><b>الصف والفصل:</b> {rec['grade']} ({rec['class_name']})</td>
                            <td><b>الفصل الدراسي:</b> {rec['semester']}</td>
                            <td><b>التاريخ:</b> {rec['eval_date']}</td>
                        </tr>
                        <tr>
                            <td><b>الحصة:</b> {rec['session_num']}</td>
                            <td><b>رقم الزيارة:</b> {rec['visit_num']}</td>
                            <td><b>المواد المسندة:</b> {rec['assigned_subjects']}</td>
                        </tr>
                    </table>
                    <hr>
                    <h4 style="color:#1e3a8a; font-weight:800;">📊 النتيجة الكلية المستحقة:</h4>
                    <div style="background-color:#f0fdf4; padding:12px; border-radius:10px; text-align:center !important; border:1px solid #bbf7d0;">
                        <span style="font-size:22px; color:#15803d; font-weight:900;">المجموع الكلي: {rec['total_score']} / 100 درجة</span>
                    </div>
                    <p style="margin-top:15px; line-height:1.8;"><b>التوصيات والملحوظات:</b> {rec['notes'] if rec['notes'] else 'لا توجد ملحوظات مسجلة'}</p>
                    <hr>
                    <table style="width:100%; text-align:center; margin-top:25px; direction:rtl;">
                        <tr>
                            <td style="width:33%;"><b>المعلم المطلع:</b><br>{rec['signed_teacher']}<br>__________________</td>
                            <td style="width:33%;"><b>وكيل الشؤون التعليمية:</b><br>{rec['signed_vp']}<br>__________________</td>
                            <td style="width:33%;"><b>مدير المدرسة:</b><br>{rec['signed_principal']}<br>__________________</td>
                        </tr>
                    </table>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                if st.button("🖨️ طباعة الاستمارة المسترجعة (A4)", key="print_rec_v5", type="secondary", use_container_width=True):
                    st.components.v1.html("""<script>setTimeout(function() { window.parent.print(); }, 300);</script>""", height=0)
            with col_b2:
                show_edit = st.button("✏️ تعديل الاستمارة", key="btn_edit_v5", type="primary", use_container_width=True)
            with col_b3:
                show_del = st.button("🗑️ حذف الاستمارة", key="btn_del_v5", type="primary", use_container_width=True)

            if show_del:
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("DELETE FROM evaluations WHERE id = ?", (rec_id,))
                conn.commit()
                conn.close()
                st.success("✅ تم حذف استمارة التقييم من قاعدة البيانات بنجاح!")
                st.session_state.pop('search_active_v5', None)
                st.rerun()

            if show_edit:
                with st.form("edit_form_v5"):
                    st.subheader("✏️ تعديل الملحوظات أو الدرجة الكلية")
                    updated_notes = st.text_area("التوصيات والملحوظات المعدلة:", value=rec['notes'])
                    updated_score = st.number_input("الدرجة الكلية (من 100):", min_value=0, max_value=100, value=int(rec['total_score']))
                    save_edit = st.form_submit_button("💾 حفظ التعديلات", type="primary")
                    
                    if save_edit:
                        conn = sqlite3.connect(DB_FILE)
                        c = conn.cursor()
                        c.execute("UPDATE evaluations SET notes = ?, total_score = ? WHERE id = ?", (updated_notes, updated_score, rec_id))
                        conn.commit()
                        conn.close()
                        st.success("✅ تم تحديث بيانات استمارة المعلم بنجاح!")
                        st.rerun()
        else:
            st.warning("⚠️ لم يتم العثور على استمارة تقييم مسجلة لهذا المعلم في الزيارة المحددة.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# التبويب الثالث: إضافة معلم جديد
# ==========================================
with tab3:
    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
    st.subheader("➕ إضافة معلم جديد للنظام (ربط التخصص والمواد)")
    
    with st.form("add_teacher_form_v5", clear_on_submit=True):
        col_in1, col_in2, col_in3 = st.columns(3)
        with col_in1:
            new_t_name = st.text_input("اسم المعلم الثلاثي/الرباعي:")
        with col_in2:
            new_t_spec = st.text_input("التخصص:")
        with col_in3:
            new_t_subs = st.text_input("المواد المسندة (افصل بـ + إن كانت متعددة):")
            
        btn_add = st.form_submit_button("➕ حفظ المعلم الجديد", type="primary", use_container_width=True)
        
        if btn_add:
            if new_t_name.strip() and new_t_spec.strip() and new_t_subs.strip():
                try:
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute("INSERT INTO custom_teachers (teacher_name, specialization, assigned_subjects) VALUES (?, ?, ?)",
                              (new_t_name.strip(), new_t_spec.strip(), new_t_subs.strip()))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ تم إضافة المعلم ({new_t_name}) بتخصص ({new_t_spec}) بنجاح!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("⚠️ هذا المعلم مُسجل بالفعل في النظام.")
            else:
                st.warning("⚠️ يرجى تعبئة كافة الحقول (الاسم، التخصص، والمواد المسندة).")

    st.markdown("---")
    st.subheader("📋 قائمة المعلمين المسجلين حالياً")
    all_teachers = get_all_teachers()
    t_data_list = []
    for name, info in all_teachers.items():
        t_data_list.append({
            "اسم المعلم": name,
            "التخصص": info['spec'],
            "المواد المسندة": ", ".join(info['subjects'])
        })
    st.dataframe(pd.DataFrame(t_data_list), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# التبويب الرابع: التقارير العامة (Excel / PDF)
# ==========================================
with tab4:
    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
    st.subheader("📑 التقرير السجل العام لكافة تقييمات المعلمين (من 100)")
    
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
                label="📊 تحميل السجل العام (Excel)",
                data=excel_bytes,
                file_name=f"تقرير_تقييمات_المعلمين_الثغر_{datetime.date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        with col_exp2:
            if st.button("🖨️ طباعة السجل العام (A4)", use_container_width=True, key="print_all_v5"):
                st.components.v1.html("""<script>setTimeout(function() { window.parent.print(); }, 300);</script>""", height=0)
    else:
        st.info("ℹ️ لا توجد تقييمات مسجلة في السجل العام حتى الآن.")
        
    st.markdown('</div>', unsafe_allow_html=True)
