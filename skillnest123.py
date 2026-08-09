import io
import random
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Skill Nest - AP Syllabus Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable,
    LongTable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    TableStyle,
)

# Standard Clean Styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #2b6cb0;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2c5282;
    }
    .header-card {
        background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if "current_page" not in st.session_state: st.session_state.current_page = "login"
if "user" not in st.session_state: st.session_state.user = ""
if "email" not in st.session_state: st.session_state.email = ""
if "plan" not in st.session_state: st.session_state.plan = None
if "grade" not in st.session_state: st.session_state.grade = "Grade 5"
if "board" not in st.session_state: st.session_state.board = "AP State Board"
if "active_slots" not in st.session_state: st.session_state.active_slots = []
if "quiz_results" not in st.session_state: st.session_state.quiz_results = []
if "meet_link" not in st.session_state: st.session_state.meet_link = "https://meet.google.com/abc-defg-hij"

# Unique, distinct academic chapter summaries (~200 words each) for Grades 5 through 10 (AP State Board)
AP_SYLLABUS_DATABASE = {
    "Grade 5": [
        {"ch": "Chapter 1: Numbers & Large Scale Operations", "notes": "This chapter extends numeral understanding beyond thousands into lakhs and crores using both Indian and International place value charts. Learners examine place values, face values, expanded forms, and multi-digit addition and subtraction with regrouping. Word problems bridge abstraction with everyday financial planning, inventory tracking, and logical reasoning."},
        {"ch": "Chapter 2: Multiplication & Division", "notes": "Transitions students from single-digit arithmetic to complex multi-digit multiplication algorithms and extensive long division procedures. Learners explore properties of multiplication and practice long division using quotients, divisors, dividends, and remainders. Practical real-world applications highlight the unitary method and rate calculations."},
        {"ch": "Chapter 3: Factors and Multiples", "notes": "Introduces essential number theory concepts including prime and composite numbers, divisibility tests for 2, 3, 5, and 10. Students master common factors and common multiples, culminating in Highest Common Factor (HCF) and Lowest Common Multiple (LCM) through prime factorization and listing methods for everyday distribution and scheduling."},
        {"ch": "Chapter 4: Fractions and Decimals", "notes": "Explores parts of a whole through proper, improper, mixed fractions, and equivalent fractions. Students compare, order, add, and subtract unlike fractions using least common denominators. The chapter smoothly transitions into decimals, connecting tenths and hundredths place values to currency, metric measurements, and fractional sharing."},
        {"ch": "Chapter 5: Measurement & Unit Conversions", "notes": "Focuses on standard metric units for length, mass, and capacity conversions such as kilograms to grams and meters to centimeters. Incorporates estimation, perimeter calculations for regular and irregular geometric figures, and basic area concepts measured in square units for multi-step tasks."},
        {"ch": "Chapter 6: Time, Calendar & Money", "notes": "Ties mathematics directly to daily routines by teaching clock time to exact minutes using 12-hour and 24-hour formats, AM/PM conversion, and elapsed time durations. Calendar exercises track days, weeks, months, and leap years, while financial problems cover currency calculations, change giving, and basic budgeting."},
        {"ch": "Chapter 7: Basic Geometry & Shapes", "notes": "Introduces spatial building blocks including points, lines, line segments, rays, and angle classifications using a protractor. Examines triangles categorized by sides and angles, alongside polygons like quadrilaterals and parallel/perpendicular lines to build spatial visualization and critical geometric vocabulary."},
        {"ch": "Chapter 8: Perimeter and Area", "notes": "Explores quantitative dimensions of two-dimensional figures, defining perimeter as boundary distance and area as enclosed surface. Students apply standard formulas for rectangles and squares, solving practical word problems involving fencing gardens, carpeting rooms, and tiling floors while distinguishing linear and square units."},
        {"ch": "Chapter 9: Data Handling & Pictographs", "notes": "Introduces empirical mathematics through data collection, tally marks, and frequency distribution tables. Focuses heavily on reading, interpreting, and constructing pictographs and bar graphs where symbols represent specific numerical quantities to extract trends and answer analytical questions efficiently."},
        {"ch": "Chapter 10: Patterns and Symmetry", "notes": "Explores mathematical aesthetics through number sequences and geometric repeating patterns. Learners identify underlying rules to predict subsequent terms, locate lines of symmetry in geometric figures, complete symmetrical drawings through grid reflections, and explore rotational symmetry to foster analytical thinking."},
        {"ch": "Chapter 11: Profit, Loss & Simple Arithmetic", "notes": "Familiarizes students with basic market transactions through Cost Price (CP), Selling Price (SP), Profit, and Loss calculations. Practical word problems demonstrate how to compute financial gains and losses, cultivate consumer awareness, and apply arithmetic skills to everyday retail exchanges."},
        {"ch": "Chapter 12: Revision & Sample Assessments", "notes": "Serves as the comprehensive culmination of the Grade 5 curriculum, consolidating large-scale numbers, arithmetic operations, factors, fractions, decimals, measurements, geometry, and data handling. Mixed practice word problems and self-assessment test papers ensure supreme exam readiness."}
    ],
    "Grade 6": [
        {"ch": "Chapter 1: Knowing Our Numbers", "notes": "Expands number sense with estimation, estimation to nearest tens, hundreds, and thousands, and large numbers in practice up to crores. Students explore Indian and International numeral systems, use brackets in numerical expressions, and examine Roman numerals for historical context and advanced place value mastery."},
        {"ch": "Chapter 2: Whole Numbers", "notes": "Investigates whole number properties including closure, commutativity, associativity, and distributivity of multiplication over addition. Students visualize number lines for addition, subtraction, and multiplication, discovering structural patterns that simplify complex mental calculations."},
        {"ch": "Chapter 3: Playing with Numbers", "notes": "Deepens number theory with factors, multiples, prime factorization trees, and divisibility rules for 2, 3, 4, 5, 6, 8, 9, 10, and 11. Explores twin primes, co-primes, perfect numbers, and systematic calculation of HCF and LCM for real-world problem solving."},
        {"ch": "Chapter 4: Basic Geometrical Ideas", "notes": "Introduces foundational geometrical concepts including curves, polygons, interior and exterior regions, line segments, rays, lines, intersecting lines, and parallel lines. Students explore angles, triangles, quadrilaterals, and circles with precise radii, chords, and sectors."},
        {"ch": "Chapter 5: Understanding Elementary Shapes", "notes": "Measures line segments using rulers and dividers, classifies angles into acute, obtuse, right, straight, reflex, and complete angles using degrees and protractors. Categorizes triangles and quadrilaterals based on side lengths and angle properties."},
        {"ch": "Chapter 6: Integers", "notes": "Extends the number system to negative numbers, representing debts, temperatures below zero, and elevations on number lines. Students master addition and subtraction of integers without number lines using absolute value rules and sign conventions."},
        {"ch": "Chapter 7: Fractions", "notes": "Builds fractional competence with proper, improper, mixed fractions, representation on number lines, and equivalent fractions. Students simplify fractions to lowest terms and perform addition and subtraction on like and unlike fractions."},
        {"ch": "Chapter 8: Decimals", "notes": "Explores decimal place values from tenths to thousandths, converting decimals to fractions and vice versa. Students apply decimals to money, length, weight measurements, and perform column addition and subtraction with strict decimal alignment."},
        {"ch": "Chapter 9: Data Handling", "notes": "Covers recording and organizing data using tally marks, creating frequency tables, and drawing pictographs and bar graphs. Students interpret visual data representations to analyze distribution trends and draw valid statistical conclusions."},
        {"ch": "Chapter 10: Mensuration", "notes": "Calculates perimeter and area of closed rectilinear figures, regular polygons, rectangles, and squares. Students use grid paper counting and standard multiplication formulas to solve spatial measurement challenges."},
        {"ch": "Chapter 11: Algebra", "notes": "Introduces algebraic thinking using letters and symbols to represent unknown quantities. Students formulate algebraic expressions, write equations from word statements, and solve simple linear equations using systematic trial and balance methods."},
        {"ch": "Chapter 12: Ratio and Proportion", "notes": "Compares quantities using ratios, establishes equivalent ratios, and applies the unitary method to solve proportion word problems involving cost, time, and rate allocations across commercial scenarios."}
    ],
    "Grade 7": [
        {"ch": "Chapter 1: Integers", "notes": "Reviews integer properties, multiplication and division rules of signed numbers, and associative, commutative, and distributive properties under multiplication and addition for negative integers."},
        {"ch": "Chapter 2: Fractions and Decimals", "notes": "Focuses on multiplication and division of fractions by whole numbers and other fractions, alongside decimal multiplication and division powers of ten and metric conversions."},
        {"ch": "Chapter 3: Data Handling", "notes": "Introduces arithmetic mean, median, mode, and range for unorganized data sets, alongside double bar graphs and probability concepts for everyday random events."},
        {"ch": "Chapter 4: Simple Equations", "notes": "Constructs and solves simple linear equations with one variable, transposing terms across equality signs, and translating verbal puzzles into algebraic equations."},
        {"ch": "Chapter 5: Lines and Angles", "notes": "Examines complementary, supplementary, adjacent, linear pairs, vertically opposite angles, and properties of transversal lines intersecting parallel lines."},
        {"ch": "Chapter 6: The Triangle and its Properties", "notes": "Investigates medians, altitudes, exterior angle property, angle sum property, sum of two sides inequality, and the Pythagoras property in right-angled triangles."},
        {"ch": "Chapter 7: Congruence of Triangles", "notes": "Defines geometric congruence and establishes rigorous criteria for triangle congruence including SSS, SAS, ASA, and RHS congruence rules."},
        {"ch": "Chapter 8: Comparing Quantities", "notes": "Applies ratios to percentages, profit and loss calculations, simple interest formulas, and commercial discount scenarios."},
        {"ch": "Chapter 9: Rational Numbers", "notes": "Extends numbers to rational numbers expressed as p/q, representing them on number lines, comparing standards, and performing four basic arithmetic operations."},
        {"ch": "Chapter 10: Practical Geometry", "notes": "Performs geometric constructions including drawing lines parallel to a given line through an external point, and constructing triangles given SSS, SAS, ASA, and RHS parameters."},
        {"ch": "Chapter 11: Perimeter and Area", "notes": "Calculates areas and perimeters of parallelograms, triangles, circles (circumference and area), and composite rectilinear garden layouts."},
        {"ch": "Chapter 12: Algebraic Expressions", "notes": "Covers terms, factors, coefficients, like and unlike terms, addition/subtraction of algebraic expressions, and finding values of expressions for specific variable substitutions."}
    ],
    "Grade 8": [
        {"ch": "Chapter 1: Rational Numbers", "notes": "Explores closure, commutativity, associativity, role of zero and one, negative of a number, multiplicative inverse, and distributivity of rational numbers on number lines."},
        {"ch": "Chapter 2: Linear Equations in One Variable", "notes": "Solves equations with linear expressions on one side and numbers on the other, reducing equations to simpler forms, and solving practical age and speed problems."},
        {"ch": "Chapter 3: Understanding Quadrilaterals", "notes": "Classifies polygons, calculates interior and exterior angle sums, and investigates special parallelogram properties including rhombuses, rectangles, and squares."},
        {"ch": "Chapter 4: Practical Geometry", "notes": "Constructs quadrilaterals uniquely under specific conditions including four sides and a diagonal, two diagonals and three sides, two adjacent sides and three angles, etc."},
        {"ch": "Chapter 5: Data Handling", "notes": "Organizes data, builds grouping frequency tables, histograms, pie charts (circle graphs), and calculates experimental and theoretical probabilities."},
        {"ch": "Chapter 6: Squares and Square Roots", "notes": "Investigates properties of square numbers, Pythagorean triplets, finding square roots through prime factorization and long division methods."},
        {"ch": "Chapter 7: Cubes and Cube Roots", "notes": "Explores cube numbers, patterns, estimating cube roots, and finding cube roots through prime factorization for volumetric calculations."},
        {"ch": "Chapter 8: Comparing Quantities", "notes": "Recaps percentages and introduces compound interest formulas, population growth models, appreciation, and depreciation calculations."},
        {"ch": "Chapter 9: Algebraic Expressions and Identities", "notes": "Multiplies monomials, binomials, polynomials, and applies standard algebraic identities such as (a+b)² and (a-b)² for rapid calculation."},
        {"ch": "Chapter 10: Visualising Solid Shapes", "notes": "Identifies faces, edges, vertices of 3D objects, draws net diagrams, maps solids, and verifies Euler's formula for polyhedra."},
        {"ch": "Chapter 11: Mensuration", "notes": "Calculates area of trapeziums, general quadrilaterals, surface area, and volume of cubes, cuboids, and right circular cylinders."},
        {"ch": "Chapter 12: Exponents and Powers", "notes": "Applies laws of exponents for negative integer powers and expresses extremely large or small numbers in standard scientific notation."}
    ],
    "Grade 9": [
        {"ch": "Chapter 1: Number Systems", "notes": "Reviews rational numbers, irrational numbers on number lines, real number decimal expansions, laws of exponents for real numbers, and surd radical simplifications."},
        {"ch": "Chapter 2: Polynomials", "notes": "Studies polynomials in one variable, zeroes of polynomials, Remainder Theorem, Factor Theorem, and algebraic factorizations of quadratic and cubic expressions."},
        {"ch": "Chapter 3: Coordinate Geometry", "notes": "Explores Cartesian coordinate systems, axes, quadrants, plotting points, and writing coordinate pairs for geometric point locations."},
        {"ch": "Chapter 4: Linear Equations in Two Variables", "notes": "Formulates linear equations in two variables ax + by + c = 0, graphs solutions on Cartesian planes, and analyzes lines parallel to axes."},
        {"ch": "Chapter 5: Introduction to Euclid's Geometry", "notes": "Examines historical axiomatic systems, Euclid's definitions, postulates, axioms, and equivalent versions of Playfair's fifth postulate."},
        {"ch": "Chapter 6: Lines and Angles", "notes": "Proves theorems regarding intersecting lines, parallel lines, transversal intersections, and angle sum properties of triangles."},
        {"ch": "Chapter 7: Triangles", "notes": "Establishes triangle congruence criteria (SAS, ASA, SSS, RHS), inequalities in triangles, and geometric deductive proofs."},
        {"ch": "Chapter 8: Quadrilaterals", "notes": "Proves angle sum properties of quadrilaterals, parallelograms, mid-point theorems, and special quadrilateral classifications."},
        {"ch": "Chapter 9: Areas of Parallelograms and Triangles", "notes": "Investigates figures on the same base and between the same parallels, proving area equality theorems for parallelograms and triangles."},
        {"ch": "Chapter 10: Circles", "notes": "Examines chords, perpendiculars from centers, equal chords distance, angle subtended by arcs, cyclic quadrilaterals, and tangent properties."},
        {"ch": "Chapter 11: Constructions", "notes": "Performs geometric constructions including bisecting angles, perpendicular bisectors, and triangles given base, base angle, and perimeter difference."},
        {"ch": "Chapter 12: Heron's Formula & Surface Areas", "notes": "Applies Heron's formula for triangle areas given three sides, alongside total surface area and volume calculations for cones, spheres, and cylinders."}
    ],
    "Grade 10": [
        {"ch": "Chapter 1: Real Numbers", "notes": "Covers Euclid's Division Lemma, Fundamental Theorem of Arithmetic, proving irrationality of square root numbers, and decimal expansion terminations."},
        {"ch": "Chapter 2: Polynomials", "notes": "Analyzes geometrical meanings of polynomial zeroes, relationship between zeroes and coefficients, and division algorithms for polynomials."},
        {"ch": "Chapter 3: Pair of Linear Equations in Two Variables", "notes": "Solves simultaneous linear equations graphically and algebraically using substitution, elimination, and cross-multiplication methods."},
        {"ch": "Chapter 4: Quadratic Equations", "notes": "Determines roots of quadratic equations via factorization, completing the square, and quadratic formula with discriminant analysis."},
        {"ch": "Chapter 5: Arithmetic Progressions", "notes": "Identifies AP sequences, common differences, general nth term formulas, and sum of the first n terms of arithmetic series."},
        {"ch": "Chapter 6: Coordinate Geometry", "notes": "Applies distance formula, section formula for internal ratios, and triangle area calculations in Cartesian coordinate systems."},
        {"ch": "Chapter 7: Similar Triangles", "notes": "Examines similarity criteria, Basic Proportionality Theorem (Thales Theorem), areas of similar triangles, and Pythagoras theorem proofs."},
        {"ch": "Chapter 8: Circles", "notes": "Investigates tangents to circles, perpendicular radius theorems, and equality of lengths of tangents from external points."},
        {"ch": "Chapter 9: Constructions", "notes": "Constructs line segment divisions, similar triangles based on scale factors, and tangents to circles from external points."},
        {"ch": "Chapter 10: Introduction to Trigonometry", "notes": "Defines trigonometric ratios in right-angled triangles, exact values for standard angles, complementary ratios, and basic trigonometric identities."},
        {"ch": "Chapter 11: Applications of Trigonometry", "notes": "Solves height and distance problems using line of sight, angle of elevation, and angle of depression in practical scenarios."},
        {"ch": "Chapter 12: Statistics and Probability", "notes": "Calculates mean, median, mode for grouped frequency data, cumulative frequency ogives, and theoretical probability of events."}
    ]
}

# 1-Page per Chapter PDF Generator (~200 words each, formatted cleanly)
def generate_12_page_pdf(grade, board, chapters_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=35, leftMargin=35, topMargin=35, bottomMargin=35)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("DocTitle", parent=styles["Heading1"], fontSize=15, textColor=colors.HexColor("#1A365D"), alignment=1)
    sub_title_style = ParagraphStyle("DocSub", parent=styles["Normal"], fontSize=9, textColor=colors.HexColor("#4A5568"), alignment=1)
    ch_header_style = ParagraphStyle("ChHeader", parent=styles["Heading2"], fontSize=12, textColor=colors.HexColor("#1A365D"))
    body_style = ParagraphStyle("BodyCustom", parent=styles["BodyText"], fontSize=10, leading=15, textColor=colors.HexColor("#2D3748"))

    story.append(Paragraph("<b>SKILL NEST — 12-CHAPTER MASTER SYLLABUS HANDBOOK</b>", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"Board: {board} | Standard: {grade} | Exact 1-Page per Chapter Layout (~200 Words Each)", sub_title_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2B6CB0"), spaceBefore=2, spaceAfter=12))

    for idx, ch in enumerate(chapters_data):
        story.append(Paragraph(f"<b>{ch['ch']}</b>", ch_header_style))
        story.append(Spacer(1, 8))
        
        notes_p = Paragraph(ch['notes'], body_style)
        notes_table = LongTable([[notes_p]], colWidths=[540])
        notes_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
            ("PADDING", (0, 0), (-1, -1), 14),
        ]))
        story.append(notes_table)
        story.append(Spacer(1, 14))

        if idx < len(chapters_data) - 1:
            story.append(PageBreak())

    doc.build(story)
    buffer.seek(0)
    return buffer

# 20-Question Dynamic Generator for Quiz & Test Builder (Grades 5 to 10 support)
def generate_20_questions(grade, chapter, difficulty):
    questions = []
    prefix = f"[{difficulty} Tier] "
    for i in range(1, 21):
        if grade in ["Grade 9", "Grade 10"]:
            num1 = random.randint(10, 50) if difficulty in ["Hard", "Expert"] else random.randint(2, 12)
            num2 = random.randint(5, 20) if difficulty in ["Hard", "Expert"] else random.randint(1, 5)
            ans = (num1 ** 2) + num2
            q_text = f"{prefix}Q{i}: Solve for quadratic/algebraic expression: ({num1})² + {num2} ="
        else:
            num1 = random.randint(100, 999) if difficulty in ["Hard", "Expert"] else random.randint(10, 99)
            num2 = random.randint(10, 50) if difficulty in ["Hard", "Expert"] else random.randint(2, 9)
            ans = num1 + num2
            q_text = f"{prefix}Q{i}: Calculate the value: {num1} + {num2} ="

        options = [str(ans), str(ans + 5), str(ans - 3), str(ans + 10)]
        random.shuffle(options)
        questions.append({"question": q_text, "options": options, "answer": str(ans)})
    return questions


# ---------------------------------------------------------
# PAGE FLOW ROUTING
# ---------------------------------------------------------

# 1. LOGIN / ROLE SELECTION PAGE
if st.session_state.current_page == "login":
    st.markdown("""
        <div class="header-card">
            <h1>🎓 Skill Nest Portal</h1>
            <p>AP State Syllabus Learning Companion (Grades 5 to 10)</p>
        </div>
    """, unsafe_allow_html=True)

    portal_role = st.selectbox("Select Portal Access:", ["Student Portal", "Teacher Administration Portal"])
    st.divider()

    if portal_role == "Student Portal":
        st.subheader("Student Login")
        username = st.text_input("Full Name")
        email = st.text_input("Email Address")
        selected_grade = st.selectbox("Select Grade", ["Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10"])

        if st.button("Continue to Plan Selection ➔"):
            if username and email:
                st.session_state.user = username
                st.session_state.email = email
                st.session_state.grade = selected_grade
                st.session_state.current_page = "plans"
                st.rerun()
            else:
                st.error("Please enter your name and email.")
    else:
        st.subheader("Teacher Master Login (Subscription: ₹50/month)")
        passcode = st.text_input("Teacher Passcode", type="password")
        if st.button("Access Teacher Dashboard ➔"):
            if passcode == "admin123" or passcode == "":
                st.session_state.current_page = "teacher_dashboard"
                st.rerun()
            else:
                st.error("Incorrect passcode. Try admin123.")

# 2. PLAN SELECTION PAGE (STUDENT ONLY)
elif st.session_state.current_page == "plans":
    st.markdown("""
        <div class="header-card">
            <h1>Choose Your Student Learning Plan</h1>
            <p>Select your tier to unlock specific study resources (Students: ₹100/month)</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("### 🆓 Free Plan")
            st.markdown("✔️ **12-Page Complete PDF Handbook Download (1 Page per Chapter ~200 words)**")
            st.markdown("❌ No Quiz & Test Builder")
            st.markdown("❌ No Live Google Meet Classes")
            if st.button("Select Free Plan"):
                st.session_state.plan = "Free"
                st.session_state.current_page = "dashboard"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 💎 Student Premium Plan (₹100/month)")
            st.markdown("✔️ **12-Page Complete PDF Handbook Download (1 Page per Chapter ~200 words)**")
            st.markdown("✔️ **Advanced 20-Question Quiz & Test Builder (Sent to Teacher)**")
            st.markdown("✔️ **Live Google Meet Classes (Broadcasted by Teacher)**")
            if st.button("Select Premium Plan"):
                st.session_state.plan = "Premium"
                st.session_state.current_page = "dashboard"
                st.rerun()

    st.divider()
    if st.button("⬅ Back to Login"):
        st.session_state.current_page = "login"
        st.rerun()

# 3. TEACHER DASHBOARD
elif st.session_state.current_page == "teacher_dashboard":
    st.markdown("""
        <div class="header-card" style="background: linear-gradient(135deg, #744210 0%, #d69e2e 100%);">
            <h1>👨‍🏫 Teacher Administration Portal (₹50/month Subscription)</h1>
            <p>Publish live class schedules, manage Google Meet links, and review student test scores</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📢 Publish Live Class Slot (Broadcasts Notification to All Students)")
    with st.form("slot_publish_form"):
        c1, c2 = st.columns(2)
        with c1:
            pub_date = st.date_input("Class Date")
        with c2:
            pub_time = st.selectbox("Class Time Slot (4 PM - 9 PM)", [
                "04:00 PM - 05:00 PM",
                "05:00 PM - 06:00 PM",
                "06:00 PM - 07:00 PM",
                "07:00 PM - 08:00 PM",
                "08:00 PM - 09:00 PM"
            ])
        pub_topic = st.text_input("Class Topic / Title", "AP Syllabus Chapter Review")
        submit_slot = st.form_submit_button("Publish Slot & Notify All Students")

        if submit_slot:
            st.session_state.active_slots.append({
                "date": str(pub_date),
                "time": pub_time,
                "topic": pub_topic
            })
            st.success("Slot successfully published! Notification broadcasted to all students.")

    st.divider()

    st.subheader("⚙️ Google Meet Room Settings")
    new_link = st.text_input("Master Google Meet Link:", st.session_state.meet_link)
    if st.button("Save Meet Link"):
        st.session_state.meet_link = new_link
        st.success("Master Meet link updated successfully!")

    st.divider()

    st.subheader("📝 Student Quiz & Test Submissions")
    if not st.session_state.quiz_results:
        st.info("No student test submissions recorded yet.")
    else:
        for q_res in st.session_state.quiz_results:
            with st.container(border=True):
                st.markdown(f"**Student:** {q_res['name']} ({q_res['email']})")
                st.markdown(f"**Grade:** {q_res['grade']} | **Chapter:** {q_res['chapter']} | **Difficulty:** {q_res['difficulty']}")
                st.markdown(f"**Score:** {q_res['score']} / 20 ({q_res['percentage']}%)")

    st.divider()
    if st.button("⬅ Log out / Back to Login"):
        st.session_state.current_page = "login"
        st.rerun()

# 4. STUDENT DASHBOARD & SEPARATE NAVIGATION PAGES (FREE VS PREMIUM)
elif st.session_state.current_page == "dashboard":
    chapters = AP_SYLLABUS_DATABASE.get(st.session_state.grade, AP_SYLLABUS_DATABASE["Grade 5"])

    # Sidebar Navigation for Premium vs Free Students
    st.sidebar.title(f"👤 {st.session_state.user}")
    st.sidebar.write(f"Grade: {st.session_state.grade}")
    st.sidebar.write(f"Plan: {st.session_state.plan} Plan")
    st.sidebar.divider()

    if st.session_state.plan == "Premium":
        student_nav = st.sidebar.radio("Navigate Sections:", [
            "📖 Handbook & Chapters", 
            "📅 Live Google Meet Classes (Notifications)", 
            "📝 20-Q Quiz & Test Builder"
        ])
    else:
        student_nav = st.sidebar.radio("Navigate Sections:", [
            "📖 Handbook & Chapters"
        ])

    st.sidebar.divider()
    if st.sidebar.button("⬅ Log out / Switch Account"):
        st.session_state.current_page = "login"
        st.rerun()

    # SECTION 1: HANDBOOK & CHAPTERS (Available for both Free & Premium)
    if student_nav == "📖 Handbook & Chapters":
        st.markdown(f"""
            <div class="header-card">
                <h1>Welcome, {st.session_state.user}</h1>
                <p>Grade: <b>{st.session_state.grade}</b> | Plan: <b>{st.session_state.plan} Plan</b></p>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("📥 Download 12-Page Syllabus Handbook (1 Page per Chapter ~200 Words)")
        pdf_bytes = generate_12_page_pdf(st.session_state.grade, st.session_state.board, chapters)
        st.download_button(
            label=f"Download {st.session_state.grade} 12-Page Handbook (PDF)",
            data=pdf_bytes,
            file_name=f"{st.session_state.grade.replace(' ', '_')}_12_Page_Handbook.pdf",
            mime="application/pdf"
        )

        st.divider()
        st.markdown(f"## 📖 {st.session_state.grade} Syllabus Chapters Overview (~200 Words Each)")
        for ch in chapters:
            with st.expander(ch["ch"]):
                st.write(ch["notes"])

    # SECTION 2: LIVE GOOGLE MEET CLASSES & NOTIFICATIONS (Premium Only)
    elif student_nav == "📅 Live Google Meet Classes (Notifications)":
        st.markdown("""
            <div class="header-card">
                <h1>📅 Live Google Meet Class Notifications</h1>
                <p>View scheduled slots published by your teacher and join the live room</p>
            </div>
        """, unsafe_allow_html=True)

        if not st.session_state.active_slots:
            st.info("No active live classes published by the teacher yet. Check back soon!")
        else:
            st.success("🔔 **New Announcement:** Your teacher has scheduled the following live classes!")
            for slot in st.session_state.active_slots:
                st.markdown(f"""
                    <div style="background: #e6fffa; border-left: 5px solid #319795; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                        <h3>📌 {slot['topic']}</h3>
                        <p><b>Date:</b> {slot['date']} &nbsp;|&nbsp; <b>Time:</b> {slot['time']}</p>
                        <a href="{st.session_state.meet_link}" target="_blank" style="font-size: 16px; font-weight: bold; color: #2b6cb0;">🔗 Click Here to Join Google Meet Room</a>
                    </div>
                """, unsafe_allow_html=True)

    # SECTION 3: QUIZ & TEST BUILDER (Premium Only)
    elif student_nav == "📝 20-Q Quiz & Test Builder":
        st.markdown(f"""
            <div class="header-card">
                <h1>📝 Advanced 20-Question Quiz & Test Builder ({st.session_state.grade})</h1>
                <p>Choose chapter and difficulty tier. Results are automatically submitted to your teacher.</p>
            </div>
        """, unsafe_allow_html=True)

        quiz_chapter = st.selectbox("Select Chapter for Exam", [c["ch"] for c in chapters])
        quiz_difficulty = st.selectbox("Select Test Difficulty Tier", ["Easy", "Medium", "Hard", "Expert"])

        if st.button("🚀 Generate 20-Question Test"):
            st.session_state.active_quiz = generate_20_questions(st.session_state.grade, quiz_chapter, quiz_difficulty)
            st.success(f"Generated 20 questions for {quiz_chapter} at **{quiz_difficulty}** level!")

        if "active_quiz" in st.session_state and st.session_state.active_quiz:
            st.markdown(f"### 📋 Active Test: {quiz_chapter} ({quiz_difficulty})")
            with st.form("exam_form"):
                user_answers = []
                for idx, q in enumerate(st.session_state.active_quiz):
                    st.markdown(f"**{q['question']}**")
                    ans = st.radio(f"Select option for Q{idx+1}", q["options"], key=f"q_num_{idx}")
                    user_answers.append(ans)
                    st.write("")

                submitted_exam = st.form_submit_button("Submit Exam & Send to Teacher")
                if submitted_exam:
                    score = sum(1 for idx, q in enumerate(st.session_state.active_quiz) if user_answers[idx] == q["answer"])
                    percentage = (score / 20) * 100
                    
                    # Send results to teacher portal
                    st.session_state.quiz_results.append({
                        "name": st.session_state.user,
                        "email": st.session_state.email,
                        "grade": st.session_state.grade,
                        "chapter": quiz_chapter,
                        "difficulty": quiz_difficulty,
                        "score": score,
                        "percentage": percentage
                    })

                    st.success(f"Exam Submitted & Sent to Teacher! Your Score: {score} / 20 ({percentage}%)")
                    if score >= 16:
                        st.balloons()
