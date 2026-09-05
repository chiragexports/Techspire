import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import SiteSetting, FAQ, Testimonial
from apps.courses.models import CourseCategory, Course, Module, Lesson
from apps.quizzes.models import Quiz, Question, Choice

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds initial production-ready data for TECHSPIRE Learning platform'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE(">> Seeding TECHSPIRE Learning Platform Data..."))

        # 1. Site Settings
        setting, _ = SiteSetting.objects.get_or_create(pk=1)
        setting.brand_name = "TECHSPIRE Learning"
        setting.tagline = "Learn Today, Lead Tomorrow."
        setting.business_name = "TECHSPIRE"
        setting.proprietor_name = "Vivek Jat"
        setting.business_type = "Proprietorship / Micro Enterprise"
        setting.location = "Indore, Madhya Pradesh, India"
        setting.address = "53/43 Radhaswami Nagar, Nowlakha, Indore, Madhya Pradesh 452001"
        setting.email = "vivekjat301@gmail.com"
        setting.phone = "+91 9713931301"
        setting.udyam_registration = "UDYAM-MP-23-0283495"
        setting.gstin = "23BEZPJ5728J1ZW"
        setting.hero_title = "Master High-Demand Tech Skills & Transform Your Career"
        setting.hero_subtitle = "Industry-accredited online learning with hands-on projects, expert mentorship from Indore, and downloadable verified certificates."
        setting.save()
        self.stdout.write(self.style.SUCCESS("[OK] Site settings configured."))

        # 2. Users (Superadmin & Demo Student)
        admin_user, created = User.objects.get_or_create(
            email="admin@techspire.in",
            defaults={
                'username': "admin@techspire.in",
                'first_name': "Vivek",
                'last_name': "Jat",
                'role': "admin",
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password("Admin@12345")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("[OK] Admin user created: admin@techspire.in (Pass: Admin@12345)"))

        student_user, s_created = User.objects.get_or_create(
            email="student@techspire.in",
            defaults={
                'username': "student@techspire.in",
                'first_name': "Rahul",
                'last_name': "Sharma",
                'role': "student",
                'phone_number': "9876543210",
            }
        )
        if s_created:
            student_user.set_password("Student@12345")
            student_user.save()
            student_user.profile.headline = "Aspiring Full Stack Web Developer"
            student_user.profile.city = "Indore"
            student_user.profile.save()
            self.stdout.write(self.style.SUCCESS("[OK] Demo Student created: student@techspire.in (Pass: Student@12345)"))

        # 3. Categories
        categories_data = [
            ("Web Development", "web-development", "fas fa-code", "Build modern, dynamic web applications with HTML, CSS, JavaScript, and Django.", 1),
            ("Python Programming", "python-programming", "fab fa-python", "Master Python from syntax fundamentals to object-oriented architecture and automation.", 2),
            ("Data Analytics", "data-analytics", "fas fa-chart-line", "Analyze datasets, build interactive dashboards, and drive business intelligence with Power BI & Python.", 3),
            ("AI Tools", "ai-tools", "fas fa-robot", "Leverage cutting-edge generative AI, prompt engineering, and productivity AI workflows.", 4),
            ("Digital Marketing", "digital-marketing", "fas fa-bullhorn", "Master SEO, social media marketing, content strategies, and Google analytics.", 5),
            ("Basic Computer Skills", "basic-computer-skills", "fas fa-desktop", "Fundamental computing, internet navigation, operating systems, and file management.", 6),
            ("MS Office Skills", "ms-office-skills", "fas fa-file-excel", "Comprehensive mastery of Microsoft Excel, Word, and PowerPoint for business efficiency.", 7),
        ]

        cat_objs = {}
        for name, slug, icon, desc, order in categories_data:
            cat, _ = CourseCategory.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'icon_class': icon, 'description': desc, 'order': order}
            )
            cat_objs[slug] = cat
        self.stdout.write(self.style.SUCCESS("[OK] 7 Course categories created."))

        # 4. Detailed Courses, Modules, Lessons, and Quizzes
        courses_data = [
            {
                "category": cat_objs["web-development"],
                "title": "Full-Stack Web Development with Django & Modern UI",
                "slug": "full-stack-web-development-django",
                "instructor_name": "Vivek Jat",
                "short_description": "Master end-to-end full stack web development by building real-world dynamic web applications with Python, Django, and modern CSS.",
                "description": """Become an industry-ready full stack developer with TECHSPIRE Learning. This course covers everything from foundational HTML5, CSS3, and modern responsive layouts to robust Django backend systems, PostgreSQL database modeling, user authentication, and deployment.""",
                "level": "beginner",
                "duration_hours": 24.0,
                "is_free": True,
                "price": 0.00,
                "is_featured": True,
                "what_you_will_learn": """Build responsive web applications from scratch with HTML5, CSS3, and Bootstrap 5
Understand Django MTV (Model-Template-View) architecture thoroughly
Design normalized relational databases and handle complex migrations
Implement robust user authentication, session security, and access control
Generate dynamic PDF reports and integrate RESTful backend logic
Deploy production-ready web applications on cloud servers with Nginx and Gunicorn""",
                "requirements": """Basic computer literacy and enthusiasm to learn programming
A computer with Windows, Mac, or Linux operating system
No prior coding experience required - we start from the very basics!""",
                "modules": [
                    {
                        "title": "Module 1: Foundations of Modern Web Development",
                        "order": 1,
                        "lessons": [
                            ("Introduction to Web Architecture & HTTP", "video", 15, "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ", "Understand how client-server architecture, DNS resolution, and HTTP request-response lifecycles work in modern web applications."),
                            ("HTML5 Semantic Structure & Best Practices", "article", 20, "", "# HTML5 Semantic Layouts\n\nSemantic HTML provides meaning to web page elements rather than just presentation.\n\n### Key Semantic Elements:\n- `<header>`: Page or section branding\n- `<nav>`: Primary navigation links\n- `<main>`: Central content unique to the document\n- `<section>`: Thematic grouping of content\n- `<footer>`: Author, copyright, and legal information"),
                            ("Modern CSS & Responsive Design with Flexbox and Grid", "article", 25, "", "# Mastering CSS Layouts\n\nFlexbox is designed for 1-dimensional layouts (row or column), while CSS Grid excels at 2-dimensional layouts.\n\n```css\n.container {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));\n  gap: 1.5rem;\n}\n```"),
                        ]
                    },
                    {
                        "title": "Module 2: Django Backend Architecture & Data Modeling",
                        "order": 2,
                        "lessons": [
                            ("Django Project Setup & MTV Architecture", "video", 25, "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ", "Detailed walkthrough of setting up virtual environments, Django settings, apps structure, and the Model-Template-View paradigm."),
                            ("Designing Models, QuerySets & Migrations", "article", 30, "", "# Django ORM & Migrations\n\nThe Django Object-Relational Mapper (ORM) translates Python classes directly into SQL tables.\n\n```python\nclass Student(models.Model):\n    full_name = models.CharField(max_length=100)\n    email = models.EmailField(unique=True)\n    enrolled_at = models.DateTimeField(auto_now_add=True)\n```"),
                            ("Building Views, Forms and URL Routing", "article", 25, "", "# Handling User Input Securely\n\nDjango Forms automatically handle HTML rendering, type validation, and CSRF token verification against cross-site request forgery attacks."),
                        ]
                    }
                ],
                "quiz": {
                    "title": "Full-Stack Web Development Certification Assessment",
                    "description": "Comprehensive test evaluating your understanding of HTML5 semantics, CSS layouts, and Django ORM architecture.",
                    "pass_percentage": 70,
                    "questions": [
                        ("What does the Django ORM stand for and do?", [
                            ("Object-Relational Mapping: maps database tables to Python objects", True),
                            ("Online Request Manager: handles HTTP requests", False),
                            ("Open Resource Model: creates web templates", False),
                            ("Operational Real-time Module", False)
                        ], "Django ORM stands for Object-Relational Mapping and provides an expressive Python interface to execute SQL queries."),
                        ("Which CSS property activates 2-dimensional grid layouts?", [
                            ("display: grid;", True),
                            ("display: flex;", False),
                            ("float: left;", False),
                            ("position: relative;", False)
                        ], "display: grid initializes CSS Grid layout for 2-dimensional row and column structures."),
                        ("What is the primary role of CSRF tokens in Django forms?", [
                            ("Prevent Cross-Site Request Forgery security attacks", True),
                            ("Speed up page load performance", False),
                            ("Colorize form input borders", False),
                            ("Store user passwords in plain text", False)
                        ], "CSRF (Cross-Site Request Forgery) tokens ensure form submissions originate from authentic users."),
                    ]
                }
            },
            {
                "category": cat_objs["python-programming"],
                "title": "Python Programming: Zero to Professional Masterclass",
                "slug": "python-programming-zero-to-pro",
                "instructor_name": "Vivek Jat",
                "short_description": "Master Python programming syntax, data structures, object-oriented design, error handling, and automation scripting.",
                "description": """Python is one of the most versatile and in-demand programming languages globally. This masterclass by TECHSPIRE Learning takes you from fundamental variables, conditional logic, and loops to advanced object-oriented programming (OOP), file I/O, and real-world project automation.""",
                "level": "beginner",
                "duration_hours": 18.0,
                "is_free": True,
                "price": 0.00,
                "is_featured": True,
                "what_you_will_learn": """Master core Python syntax, variables, expressions, and type casting
Work fluently with Python data structures: Lists, Dictionaries, Tuples, Sets
Write modular, reusable functions with positional, default, and keyword arguments
Understand Object-Oriented Programming (OOP): Classes, Inheritance, Polymorphism
Automate repetitive file system tasks and parse JSON/CSV files
Implement clean exception handling and defensive programming patterns""",
                "requirements": """No prior programming background required
Laptop or Desktop computer with Python 3.x installed""",
                "modules": [
                    {
                        "title": "Module 1: Python Core Essentials",
                        "order": 1,
                        "lessons": [
                            ("Python Installation, Environment & Hello World", "video", 15, "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ", "Step-by-step installation of Python 3.10+, VS Code configuration, and running your very first Python script."),
                            ("Data Types, Control Flow & Loops", "article", 25, "", "# Python Control Flow\n\nConditionals and loops allow logic branching:\n\n```python\nfor i in range(1, 6):\n    if i % 2 == 0:\n        print(f'{i} is even')\n    else:\n        print(f'{i} is odd')\n```"),
                            ("Working with Lists, Tuples & Dictionaries", "article", 25, "", "# Python Collections\n\nDictionaries store key-value associations with average O(1) lookup time:\n\n```python\nstudent = {\n    'name': 'Rahul',\n    'course': 'Python Masterclass',\n    'score': 95\n}\n```"),
                        ]
                    },
                    {
                        "title": "Module 2: Object-Oriented Python & File Operations",
                        "order": 2,
                        "lessons": [
                            ("Classes, Objects & Dunder Methods", "article", 30, "", "# Object Oriented Programming\n\nClasses encapsulate state and behaviors:\n\n```python\nclass Student:\n    def __init__(self, name, roll_no):\n        self.name = name\n        self.roll_no = roll_no\n\n    def __str__(self):\n        return f'{self.name} (#{self.roll_no})'\n```"),
                            ("File I/O, CSV Parsing & Exception Handling", "article", 20, "", "# Safe File Handling\n\nAlways use context managers (`with`) to ensure resources are properly closed: \n\n```python\nwith open('data.csv', 'r') as file:\n    content = file.read()\n```"),
                        ]
                    }
                ],
                "quiz": {
                    "title": "Python Fundamentals Certification Exam",
                    "description": "Test your grasp of Python data structures, syntax rules, and object-oriented principles.",
                    "pass_percentage": 70,
                    "questions": [
                        ("Which of the following Python data structures is mutable?", [
                            ("List", True),
                            ("Tuple", False),
                            ("String", False),
                            ("Frozenset", False)
                        ], "Lists in Python are mutable sequences that can be modified in place."),
                        ("What keyword is used to define a function in Python?", [
                            ("def", True),
                            ("func", False),
                            ("function", False),
                            ("define", False)
                        ], "'def' is the standard Python keyword used to define functions."),
                        ("What is the output of bool([]) in Python?", [
                            ("False", True),
                            ("True", False),
                            ("None", False),
                            ("SyntaxError", False)
                        ], "Empty sequences such as empty lists [] evaluate to False in boolean contexts.")
                    ]
                }
            },
            {
                "category": cat_objs["data-analytics"],
                "title": "Data Analytics & Business Intelligence with Power BI & Excel",
                "slug": "data-analytics-power-bi-excel",
                "instructor_name": "TECHSPIRE Faculty",
                "short_description": "Learn to extract actionable business insights, clean messy datasets, write DAX formulas, and craft dynamic dashboards.",
                "description": """Transform raw data into meaningful executive dashboards. In this course, you will learn data cleaning with Power Query, advanced formula calculation with DAX, and storytelling visualization with Power BI and Excel.""",
                "level": "intermediate",
                "duration_hours": 16.0,
                "is_free": True,
                "price": 0.00,
                "is_featured": True,
                "what_you_will_learn": """Import and transform messy datasets using Power Query ETL
Build relational data models with star and snowflake schemas
Write calculated columns and measures with DAX (Data Analysis Expressions)
Design interactive KPI scorecards and trend visualizations
Publish and share reports with business stakeholders""",
                "requirements": """Basic familiarity with Microsoft Excel spreadsheets
Windows computer to install Power BI Desktop (free)""",
                "modules": [
                    {
                        "title": "Module 1: Data Preparation & Modeling",
                        "order": 1,
                        "lessons": [
                            ("Introduction to Business Intelligence Lifecycles", "video", 20, "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ", "Overview of the data analysis lifecycle: Ingestion, Transformation, Modeling, Visualization, and Action."),
                            ("Power Query ETL Transformations & Cleaning", "article", 25, "", "# Power Query Best Practices\n\n- Remove duplicate rows early\n- Ensure correct data typing (Decimal vs Integer vs Date)\n- Unpivot crosstab columns into flat rows for analytical modeling"),
                        ]
                    },
                    {
                        "title": "Module 2: DAX Formulas & Visualization",
                        "order": 2,
                        "lessons": [
                            ("Essential DAX Measures (CALCULATE, SUMX, RELATED)", "article", 30, "", "# Understanding CALCULATE in DAX\n\n`CALCULATE` is the most important function in DAX, allowing you to modify filter context:\n\n```dax\nTotal Sales YTD = CALCULATE(SUM(Sales[Amount]), DATESYTD(DimDate[Date]))\n```"),
                            ("Building Executive KPI Dashboards", "video", 25, "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ", "How to place cards, charts, and slicers to create an intuitive user experience for business leadership."),
                        ]
                    }
                ],
                "quiz": {
                    "title": "Data Analytics & Power BI Assessment",
                    "description": "Assess your skills in data transformation, DAX expressions, and dashboard design.",
                    "pass_percentage": 70,
                    "questions": [
                        ("What is the primary role of Power Query in Power BI?", [
                            ("Data extraction, transformation, and cleaning (ETL)", True),
                            ("Drawing 3D animated graphs", False),
                            ("Sending emails to customers", False),
                            ("Writing web application code", False)
                        ], "Power Query is the dedicated ETL engine in Power BI used to clean and transform data."),
                        ("Which DAX function is used to modify the filter context of a measure?", [
                            ("CALCULATE", True),
                            ("SUM", False),
                            ("FILTER_NOW", False),
                            ("LOOKUP_ROW", False)
                        ], "CALCULATE is the cornerstone DAX function used to evaluate expressions under modified filter contexts.")
                    ]
                }
            },
            {
                "category": cat_objs["ai-tools"],
                "title": "Generative AI & Prompt Engineering for Professionals",
                "slug": "generative-ai-prompt-engineering",
                "instructor_name": "Vivek Jat",
                "short_description": "Boost productivity 10x using modern AI tools, prompt engineering frameworks, automated workflows, and LLM integrations.",
                "description": """Unlock the power of artificial intelligence to accelerate research, copywriting, coding, and decision making. Learn structured prompt engineering techniques (Few-Shot, Chain-of-Thought, Persona-based prompting).""",
                "level": "all",
                "duration_hours": 12.0,
                "is_free": True,
                "price": 0.00,
                "is_featured": True,
                "what_you_will_learn": """Understand Large Language Model (LLM) architectures and tokens
Apply advanced prompt engineering frameworks: Few-shot, Chain of Thought
Use AI for automated content generation, code debugging, and summarizing
Integrate AI tools into everyday office and business workflows
Navigate AI ethics, privacy safeguards, and bias mitigation""",
                "requirements": """Curiosity about modern AI tools
No technical or mathematics background required""",
                "modules": [
                    {
                        "title": "Module 1: Prompt Engineering Mastery",
                        "order": 1,
                        "lessons": [
                            ("The Science of Prompt Engineering", "video", 20, "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ", "Learn why specific context, explicit constraints, and step-by-step instructions yield superior LLM responses."),
                            ("Few-Shot & Role-Based Prompting Frameworks", "article", 25, "", "# The CRISP Prompting Framework\n\n1. **C**ontext: Background situation\n2. **R**ole: Expert persona assigned to the AI\n3. **I**nstruction: Exact task to perform\n4. **S**pecification: Output format (table, bullet list, JSON)\n5. **P**arameters: Negative constraints and length"),
                        ]
                    }
                ],
                "quiz": {
                    "title": "Generative AI Practitioner Assessment",
                    "description": "Evaluate your mastery of prompt engineering principles and ethical AI usage.",
                    "pass_percentage": 70,
                    "questions": [
                        ("What is 'Few-Shot' prompting in Large Language Models?", [
                            ("Providing a few examples of desired input-output pairs in the prompt", True),
                            ("Taking screenshots while prompting", False),
                            ("Limiting the AI to 3 words only", False),
                            ("Prompting without any text", False)
                        ], "Few-shot prompting provides concrete sample demonstrations within the prompt context.")
                    ]
                }
            }
        ]

        for cdata in courses_data:
            course, _ = Course.objects.get_or_create(
                slug=cdata["slug"],
                defaults={
                    "category": cdata["category"],
                    "title": cdata["title"],
                    "instructor": admin_user,
                    "instructor_name": cdata["instructor_name"],
                    "short_description": cdata["short_description"],
                    "description": cdata["description"],
                    "level": cdata["level"],
                    "duration_hours": cdata["duration_hours"],
                    "is_free": cdata["is_free"],
                    "price": cdata["price"],
                    "is_featured": cdata["is_featured"],
                    "what_you_will_learn": cdata["what_you_will_learn"],
                    "requirements": cdata["requirements"],
                    "is_published": True,
                }
            )

            for mdata in cdata["modules"]:
                module, _ = Module.objects.get_or_create(
                    course=course,
                    order=mdata["order"],
                    defaults={"title": mdata["title"]}
                )

                for l_idx, (ltitle, ltype, ldur, lvid, lcnt) in enumerate(mdata["lessons"], start=1):
                    Lesson.objects.get_or_create(
                        module=module,
                        order=l_idx,
                        defaults={
                            "title": ltitle,
                            "lesson_type": ltype,
                            "duration_minutes": ldur,
                            "video_url": lvid,
                            "content": lcnt,
                            "is_preview": (l_idx == 1)
                        }
                    )

            # Quiz
            qdata = cdata.get("quiz")
            if qdata:
                quiz, _ = Quiz.objects.get_or_create(
                    course=course,
                    title=qdata["title"],
                    defaults={
                        "description": qdata["description"],
                        "pass_percentage": qdata["pass_percentage"],
                        "time_limit_minutes": 15,
                        "is_published": True,
                    }
                )
                for q_idx, (qprompt, choices, qexpl) in enumerate(qdata["questions"], start=1):
                    question, _ = Question.objects.get_or_create(
                        quiz=quiz,
                        order=q_idx,
                        defaults={
                            "prompt": qprompt,
                            "explanation": qexpl,
                            "points": 1
                        }
                    )
                    for ctext, is_corr in choices:
                        Choice.objects.get_or_create(
                            question=question,
                            choice_text=ctext,
                            defaults={"is_correct": is_corr}
                        )

        self.stdout.write(self.style.SUCCESS("[OK] 4 Production-ready Courses, Modules, Lessons, and Quizzes seeded."))

        # 5. FAQs
        faqs_data = [
            ("Are the certificates issued by TECHSPIRE Learning verifiable online?", "Yes! Every certificate issued comes with a unique Certificate ID (e.g. TS-2026-XXXXX) and an embedded QR code that can be verified in real time on our public verification portal.", "certificates", 1),
            ("How do I earn my course completion certificate?", "To earn your verified certificate, complete all lesson modules in the course and achieve at least 70% score in the final assessment quiz.", "certificates", 2),
            ("Is TECHSPIRE a registered educational organization?", "Yes. TECHSPIRE is an officially registered micro-enterprise headquartered in Indore, Madhya Pradesh (Udyam Reg: UDYAM-MP-23-0283495, GSTIN: 23BEZPJ5728J1ZW).", "general", 3),
            ("Can I learn at my own pace?", "Absolutely. All TECHSPIRE Learning courses are self-paced. You have lifetime access to lessons, readings, and assessments to learn whenever convenient.", "courses", 4),
            ("Are the courses accessible on mobile devices?", "Yes. The TECHSPIRE Learning portal is built with a 100% responsive modern design that looks and works seamlessly on smartphones, tablets, and desktops.", "enrollment", 5),
        ]
        for q, a, cat, ord_n in faqs_data:
            FAQ.objects.get_or_create(question=q, defaults={'answer': a, 'category': cat, 'order': ord_n, 'is_active': True})

        # 6. Testimonials
        testimonials_data = [
            ("Aman Verma", "Junior Python Developer at Infosys", "Python Programming: Zero to Hero", "The structured lessons and hands-on examples at TECHSPIRE gave me the confidence to crack my technical interview. The certificate verification helped prove my practical skills!", 5),
            ("Pooja Patidar", "Web Developer at TechIndore", "Full-Stack Web Development with Django", "Hands down the best Django and Web development LMS platform! The lesson progression, quizzes, and instant PDF certificate generation are top-notch.", 5),
            ("Siddharth Chouhan", "BI Analyst at FinTech Solutions", "Data Analytics & Business Intelligence", "Clear explanations of Power BI DAX and real-world datasets. Being able to download the verified certificate signed by Vivek Jat Sir added huge credibility to my resume.", 5),
        ]
        for name, role, course_taken, content, rating in testimonials_data:
            Testimonial.objects.get_or_create(name=name, defaults={'role': role, 'course_taken': course_taken, 'content': content, 'rating': rating, 'is_featured': True})

        self.stdout.write(self.style.SUCCESS("[SUCCESS] Successfully seeded all TECHSPIRE Learning database records!"))
