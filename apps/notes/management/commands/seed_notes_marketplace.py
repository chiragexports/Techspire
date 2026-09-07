import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.accounts.models import User
from apps.courses.models import CourseCategory, Course
from apps.notes.models import NotesProduct, NotesBundle, NotesChapter, Coupon
from .python_chapters_data import PYTHON_CHAPTERS_23
from .all_categories_chapters_data import (
    WEB_DEV_CHAPTERS, DATA_ANALYTICS_CHAPTERS, AI_TOOLS_CHAPTERS,
    DIGITAL_MARKETING_CHAPTERS, BASIC_COMPUTER_CHAPTERS, MS_OFFICE_CHAPTERS
)

class Command(BaseCommand):
    help = "Seeds all 7 premium technical notes products, detailed chapters, cheat sheets, interview kits, bundles, and coupons."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(">> Seeding TECHSPIRE Premium Notes Marketplace..."))

        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin@techspire.in',
                email='admin@techspire.in',
                password='TechspireAdmin2026!',
                first_name='TECHSPIRE',
                last_name='Academic Director',
                role='admin'
            )

        # 1. Coupons
        Coupon.objects.update_or_create(code='TECH10', defaults={'discount_type': 'percentage', 'discount_value': 10, 'max_uses': 1000, 'is_active': True})
        Coupon.objects.update_or_create(code='NOTES50', defaults={'discount_type': 'fixed', 'discount_value': 50, 'max_uses': 500, 'is_active': True})
        Coupon.objects.update_or_create(code='PYTHON20', defaults={'discount_type': 'percentage', 'discount_value': 20, 'max_uses': 500, 'is_active': True})
        Coupon.objects.update_or_create(code='FIRSTBUY', defaults={'discount_type': 'fixed', 'discount_value': 100, 'max_uses': 200, 'is_active': True})

        # 2. Seed All 7 Notes Products
        p_python = self.seed_python_notes(admin_user)
        p_web = self.seed_web_notes(admin_user)
        p_data = self.seed_data_notes(admin_user)
        p_ai = self.seed_ai_notes(admin_user)
        p_marketing = self.seed_marketing_notes(admin_user)
        p_computer = self.seed_computer_notes(admin_user)
        p_msoffice = self.seed_msoffice_notes(admin_user)

        # 3. Seed Bundles
        self.seed_bundles(p_python, p_web, p_data, p_ai, p_marketing, p_computer, p_msoffice)

        self.stdout.write(self.style.SUCCESS("[SUCCESS] All 7 Premium Notes Products, 4 Bundles, and Chapters seeded successfully!"))

    # =========================================================================
    # 1. PYTHON PREMIUM NOTES (23 Parts)
    # =========================================================================
    def seed_python_notes(self, author):
        cat = CourseCategory.objects.get(slug='python-programming')
        course = Course.objects.filter(slug='python-programming-zero-to-pro').first()

        prod, _ = NotesProduct.objects.update_or_create(
            slug='python-programming-zero-to-professional',
            defaults={
                'title': 'Python Programming: Zero to Professional — Complete Notes',
                'subtitle': 'The Definitive Study Notes, OOP Architecture, Socket Networking & Interview Vault',
                'short_description': '23 In-depth Parts covering Core Python, Memory Model, OOP, Sockets, Concurrency, Regex, APIs, 50+ Interview Q&As & Cheat Sheets.',
                'full_description': '''The most comprehensive, beautifully structured Python technical study guide in India. Designed for college students, aspiring software engineers, and working developers. Covers complete fundamentals, memory references, internal data structures, advanced OOP, multithreading, socket programming, regular expressions, and high-frequency technical interview solutions.''',
                'category': cat,
                'related_course': course,
                'author_name': 'Prof. Vivek Jat & Senior Python Faculty',
                'version': 'v2.4 (2026 Comprehensive Edition)',
                'difficulty': 'beginner',
                'estimated_reading_hours': 28.0,
                'page_count_est': 280,
                'exercise_count': 45,
                'project_count': 10,
                'interview_q_count': 60,
                'price': 299.00,
                'original_price': 599.00,
                'currency': 'INR',
                'what_you_will_learn': "Master Python 3 syntax, dynamic typing, and memory pointers\nUnderstand mutable vs immutable data structures with internal mechanics\nBuild clean OOP systems: Inheritance, Polymorphism, Abstraction, and MRO\nWrite multi-client TCP/UDP socket servers and client applications\nHandle concurrency with Threading, Multiprocessing, and Asyncio\nAce 60+ top technical interview questions asked at top software companies",
                'prerequisites': "No prior programming experience required\nA computer running Python 3",
                'target_audience': "Computer Science & Engineering Students\nAspiring Backend & Full-Stack Developers\nData Analysts & Automation Engineers\nCandidates preparing for Python technical interviews",
                'is_published': True,
                'is_featured': True,
            }
        )

        chapters_data = PYTHON_CHAPTERS_23

        for cdata in chapters_data:
            NotesChapter.objects.update_or_create(
                product=prod, order=cdata['order'],
                defaults={
                    'title': cdata['title'],
                    'is_preview': cdata['is_preview'],
                    'read_time_mins': cdata['read_time_mins'],
                    'summary': cdata['summary'],
                    'content_markdown': cdata['content'],
                    'key_takeaways': cdata.get('takeaways', ''),
                    'interview_tips': cdata.get('interview', ''),
                    'practice_exercise': cdata.get('exercise', ''),
                    'exercise_solution': cdata.get('solution', ''),
                }
            )

        self.stdout.write(f"  [OK] Seeded Python Notes ({len(chapters_data)} chapters)")
        return prod

    # =========================================================================
    # 2. WEB DEVELOPMENT PREMIUM NOTES
    # =========================================================================
    def seed_web_notes(self, author):
        cat = CourseCategory.objects.get(slug='web-development')
        course = Course.objects.filter(slug='full-stack-web-development-django').first()

        prod, _ = NotesProduct.objects.update_or_create(
            slug='full-stack-web-development-django-notes',
            defaults={
                'title': 'Full-Stack Web Development — Complete Professional Notes',
                'subtitle': 'HTML5, Modern CSS Grid, JavaScript ES6+, Django MVT, REST APIs & Production Deployment',
                'short_description': 'Complete engineering notes covering modern semantic HTML5, Flexbox, CSS Grid, JavaScript async/await, Django ORM, and REST APIs.',
                'full_description': '''Comprehensive full-stack web engineering study material. Designed to help developers build accessible, performant, and secure web applications with Python and Django. Includes architecture schematics, REST API blueprints, and deployment checklists.''',
                'category': cat,
                'related_course': course,
                'author_name': 'Prof. Vivek Jat & Senior Web Engineers',
                'version': 'v2.2 (2026 Edition)',
                'difficulty': 'beginner',
                'estimated_reading_hours': 24.0,
                'page_count_est': 240,
                'exercise_count': 35,
                'project_count': 7,
                'interview_q_count': 50,
                'price': 399.00,
                'original_price': 799.00,
                'currency': 'INR',
                'what_you_will_learn': "Modern semantic HTML5 accessibility and SEO markup\nResponsive UI design with CSS Grid, Flexbox, and CSS Tokens\nJavaScript ES6+, DOM manipulation, Fetch API, and asynchronous events\nDjango MVT Architecture, ORM relationships, migrations, and model forms\nBuilding RESTful APIs with Django REST Framework\nDeploying web apps with Gunicorn, WhiteNoise, and PostgreSQL",
                'prerequisites': "Basic computer literacy\nNo prior coding experience needed",
                'target_audience': "Frontend & Backend Web Developers\nDjango Engineers\nTech Enthusiasts and Freelancers",
                'is_published': True,
                'is_featured': True,
                'order': 2,
            }
        )

        chapters_data = WEB_DEV_CHAPTERS

        for cdata in chapters_data:
            NotesChapter.objects.update_or_create(
                product=prod, order=cdata['order'],
                defaults={
                    'title': cdata['title'],
                    'is_preview': cdata['is_preview'],
                    'read_time_mins': cdata['read_time_mins'],
                    'summary': cdata['summary'],
                    'content_markdown': cdata['content'],
                    'key_takeaways': cdata.get('takeaways', ''),
                    'interview_tips': cdata.get('interview', ''),
                    'practice_exercise': cdata.get('exercise', ''),
                    'exercise_solution': cdata.get('solution', ''),
                }
            )

        self.stdout.write(f"  [OK] Seeded Web Dev Notes ({len(chapters_data)} chapters)")
        return prod

    # =========================================================================
    # 3. DATA ANALYTICS PREMIUM NOTES
    # =========================================================================
    def seed_data_notes(self, author):
        cat = CourseCategory.objects.get(slug='data-analytics')
        course = Course.objects.filter(slug='data-analytics-power-bi-excel').first()

        prod, _ = NotesProduct.objects.update_or_create(
            slug='data-analytics-power-bi-business-intelligence',
            defaults={
                'title': 'Data Analytics & Business Intelligence — Complete Notes',
                'subtitle': 'Power Query ETL, Star Schema Data Modeling, DAX Formulas & Power BI Dashboards',
                'short_description': 'Transform raw operational data into executive dashboards with Power Query, DAX functions, Star Schema models, and SQL querying.',
                'full_description': '''Complete end-to-end guide to modern Business Intelligence. Learn how top data analysts clean dirty data, build scalable relational dimensional models, write high-performance DAX calculations, and build interactive Power BI executive KPI dashboards.''',
                'category': cat,
                'related_course': course,
                'author_name': 'TECHSPIRE Data Intelligence Group',
                'version': 'v2.0 (2026 Edition)',
                'difficulty': 'intermediate',
                'estimated_reading_hours': 22.0,
                'page_count_est': 220,
                'exercise_count': 30,
                'project_count': 6,
                'interview_q_count': 45,
                'price': 399.00,
                'original_price': 799.00,
                'currency': 'INR',
                'what_you_will_learn': "Data ingestion and transformation with Power Query (M Language)\nStar Schema vs Snowflake dimensional data modeling\nWriting advanced DAX: CALCULATE, FILTER, RELATED, Time Intelligence\nDesigning executive KPI cards, charts, and drill-through pages in Power BI\nPerforming Cohort, Churn, and Sales trend analyses",
                'prerequisites': "Basic familiarity with spreadsheets and tabular data",
                'target_audience': "Aspiring Data Analysts, BI Developers, MIS Executives",
                'is_published': True,
                'is_featured': True,
                'order': 3,
            }
        )

        chapters_data = DATA_ANALYTICS_CHAPTERS

        for cdata in chapters_data:
            NotesChapter.objects.update_or_create(
                product=prod, order=cdata['order'],
                defaults={
                    'title': cdata['title'],
                    'is_preview': cdata['is_preview'],
                    'read_time_mins': cdata['read_time_mins'],
                    'summary': cdata['summary'],
                    'content_markdown': cdata['content'],
                    'key_takeaways': cdata.get('takeaways', ''),
                    'interview_tips': cdata.get('interview', ''),
                    'practice_exercise': cdata.get('exercise', ''),
                    'exercise_solution': cdata.get('solution', ''),
                }
            )

        self.stdout.write(f"  [OK] Seeded Data Analytics Notes ({len(chapters_data)} chapters)")
        return prod

    # =========================================================================
    # 4. AI TOOLS PREMIUM NOTES
    # =========================================================================
    def seed_ai_notes(self, author):
        cat = CourseCategory.objects.get(slug='ai-tools')
        course = Course.objects.filter(slug='generative-ai-prompt-engineering').first()

        prod, _ = NotesProduct.objects.update_or_create(
            slug='generative-ai-prompt-engineering-notes',
            defaults={
                'title': 'Generative AI & AI Tools — Complete Practical Notes',
                'subtitle': 'Prompt Engineering Frameworks, LLMs, ChatGPT, Claude, Midjourney & Workflow Automation',
                'short_description': 'Master prompt architecture, Chain-of-Thought prompting, AI code generation, research synthesis, and multi-modal productivity.',
                'full_description': '''The ultimate guide to leveraging Large Language Models and modern AI productivity tools for 10x output. Covers deterministic prompting frameworks, reducing hallucinations, AI coding assistants, and automated business workflows.''',
                'category': cat,
                'related_course': course,
                'author_name': 'TECHSPIRE AI Innovation Labs',
                'version': 'v2.1 (2026 Edition)',
                'difficulty': 'beginner',
                'estimated_reading_hours': 18.0,
                'page_count_est': 180,
                'exercise_count': 25,
                'project_count': 5,
                'interview_q_count': 35,
                'price': 249.00,
                'original_price': 499.00,
                'currency': 'INR',
                'what_you_will_learn': "The CREATE and CRISPE Prompting Frameworks\nFew-Shot, Chain-of-Thought, and ReAct prompt engineering\nAI for rapid code debugging and automated documentation\nMitigating AI hallucinations with source grounding and schema constraints",
                'prerequisites': "No technical background required",
                'target_audience': "Developers, Writers, Marketers, Product Managers, Entrepreneurs",
                'is_published': True,
                'is_featured': True,
                'order': 4,
            }
        )

        chapters_data = AI_TOOLS_CHAPTERS

        for cdata in chapters_data:
            NotesChapter.objects.update_or_create(
                product=prod, order=cdata['order'],
                defaults={
                    'title': cdata['title'],
                    'is_preview': cdata['is_preview'],
                    'read_time_mins': cdata['read_time_mins'],
                    'summary': cdata['summary'],
                    'content_markdown': cdata['content'],
                    'key_takeaways': cdata.get('takeaways', ''),
                    'interview_tips': cdata.get('interview', ''),
                    'practice_exercise': cdata.get('exercise', ''),
                    'exercise_solution': cdata.get('solution', ''),
                }
            )

        self.stdout.write(f"  [OK] Seeded AI Tools Notes ({len(chapters_data)} chapters)")
        return prod

    # =========================================================================
    # 5. DIGITAL MARKETING PREMIUM NOTES
    # =========================================================================
    def seed_marketing_notes(self, author):
        cat = CourseCategory.objects.get(slug='digital-marketing')
        course = Course.objects.filter(slug='digital-marketing-seo-growth-mastery').first()

        prod, _ = NotesProduct.objects.update_or_create(
            slug='digital-marketing-seo-growth-notes',
            defaults={
                'title': 'Digital Marketing & SEO Master Notes',
                'subtitle': 'Search Engine Optimization, Google Ads, Meta Ads & Conversion Funnels',
                'short_description': 'Complete guide to keyword intent, on-page & technical SEO, performance advertising, and Google Analytics 4 (GA4).',
                'full_description': '''A masterclass in organic and paid user acquisition. Covers keyword research, technical SEO audits, Google Ads search campaigns, Meta conversion funnels, and landing page conversion rate optimization.''',
                'category': cat,
                'related_course': course,
                'author_name': 'TECHSPIRE Growth Marketing Experts',
                'version': 'v2.0 (2026 Edition)',
                'difficulty': 'beginner',
                'estimated_reading_hours': 20.0,
                'page_count_est': 200,
                'exercise_count': 25,
                'project_count': 5,
                'interview_q_count': 35,
                'price': 249.00,
                'original_price': 499.00,
                'currency': 'INR',
                'what_you_will_learn': "4 Core Search Intents & Keyword Mapping\nTechnical SEO: Core Web Vitals, Schema markup, and crawl budgets\nGoogle Search & Meta Ad Funnel Architectures\nConversion Rate Optimization (CRO) & GA4 Event Tracking",
                'prerequisites': "No prior marketing experience required",
                'target_audience': "Digital Marketers, Business Owners, Content Creators",
                'is_published': True,
                'is_featured': False,
                'order': 5,
            }
        )

        chapters_data = DIGITAL_MARKETING_CHAPTERS

        for cdata in chapters_data:
            NotesChapter.objects.update_or_create(
                product=prod, order=cdata['order'],
                defaults={
                    'title': cdata['title'],
                    'is_preview': cdata['is_preview'],
                    'read_time_mins': cdata['read_time_mins'],
                    'summary': cdata['summary'],
                    'content_markdown': cdata['content'],
                    'key_takeaways': cdata.get('takeaways', ''),
                    'interview_tips': cdata.get('interview', ''),
                    'practice_exercise': cdata.get('exercise', ''),
                    'exercise_solution': cdata.get('solution', ''),
                }
            )

        self.stdout.write(f"  [OK] Seeded Marketing Notes ({len(chapters_data)} chapters)")
        return prod

    # =========================================================================
    # 6. BASIC COMPUTER SKILLS PREMIUM NOTES
    # =========================================================================
    def seed_computer_notes(self, author):
        cat = CourseCategory.objects.get(slug='basic-computer-skills')
        course = Course.objects.filter(slug='computer-fundamentals-digital-literacy').first()

        prod, _ = NotesProduct.objects.update_or_create(
            slug='basic-computer-skills-digital-literacy-notes',
            defaults={
                'title': 'Basic Computer Skills — Complete Beginner Notes',
                'subtitle': 'Hardware Architecture, Operating Systems, File Management, Shortcuts & Cyber Safety',
                'short_description': 'Crystal-clear explanations of CPU, RAM, SSD, Windows OS navigation, top keyboard shortcuts, and internet security hygiene.',
                'full_description': '''The perfect foundation for absolute beginners, students, and office staff. Explains how computers work, hardware vs software, folder hierarchies, internet navigation, and essential digital safety.''',
                'category': cat,
                'related_course': course,
                'author_name': 'TECHSPIRE Foundation Mentors',
                'version': 'v2.0 (2026 Edition)',
                'difficulty': 'beginner',
                'estimated_reading_hours': 14.0,
                'page_count_est': 140,
                'exercise_count': 20,
                'project_count': 3,
                'interview_q_count': 25,
                'price': 149.00,
                'original_price': 299.00,
                'currency': 'INR',
                'what_you_will_learn': "Hardware Components: CPU, RAM, SSD vs HDD, GPU\nWindows File Explorer, Path navigation & Cloud sync\nTop 30 productivity keyboard shortcuts\nCybersecurity: Phishing detection and password management",
                'prerequisites': "None",
                'target_audience': "Beginners, School & College Students, Office Assistants",
                'is_published': True,
                'is_featured': False,
                'order': 6,
            }
        )

        chapters_data = BASIC_COMPUTER_CHAPTERS

        for cdata in chapters_data:
            NotesChapter.objects.update_or_create(
                product=prod, order=cdata['order'],
                defaults={
                    'title': cdata['title'],
                    'is_preview': cdata['is_preview'],
                    'read_time_mins': cdata['read_time_mins'],
                    'summary': cdata['summary'],
                    'content_markdown': cdata['content'],
                    'key_takeaways': cdata.get('takeaways', ''),
                    'interview_tips': cdata.get('interview', ''),
                    'practice_exercise': cdata.get('exercise', ''),
                    'exercise_solution': cdata.get('solution', ''),
                }
            )

        self.stdout.write(f"  [OK] Seeded Basic Computer Notes ({len(chapters_data)} chapters)")
        return prod

    # =========================================================================
    # 7. MS OFFICE SKILLS PREMIUM NOTES
    # =========================================================================
    def seed_msoffice_notes(self, author):
        cat = CourseCategory.objects.get(slug='ms-office-skills')
        course = Course.objects.filter(slug='ms-office-suite-excel-word-powerpoint').first()

        prod, _ = NotesProduct.objects.update_or_create(
            slug='ms-office-professional-skills-notes',
            defaults={
                'title': 'MS Office Professional Skills — Complete Notes',
                'subtitle': 'Microsoft Excel (XLOOKUP & Pivot Tables), Word Documentation & PowerPoint Decks',
                'short_description': 'Master 50+ Excel formulas, XLOOKUP, Pivot Tables, corporate Word formatting, and executive PowerPoint presentation decks.',
                'full_description': '''The definitive workplace productivity study pack. Covers modern Microsoft Excel spreadsheet formulas, dynamic pivot tables, formatting business proposals in Word, and designing pitch decks in PowerPoint.''',
                'category': cat,
                'related_course': course,
                'author_name': 'TECHSPIRE Corporate Faculty',
                'version': 'v2.0 (2026 Edition)',
                'difficulty': 'beginner',
                'estimated_reading_hours': 22.0,
                'page_count_est': 210,
                'exercise_count': 30,
                'project_count': 6,
                'interview_q_count': 35,
                'price': 249.00,
                'original_price': 499.00,
                'currency': 'INR',
                'what_you_will_learn': "Master 50+ Excel formulas: XLOOKUP, VLOOKUP, INDEX/MATCH, SUMIFS, COUNTIFS\nBuild interactive Pivot Tables, calculated fields, and KPI slicers\nFormat corporate reports and automated mail merges in Word\nDesign engaging slide layouts and animations in PowerPoint",
                'prerequisites': "A computer with MS Office (Excel, Word, PowerPoint)",
                'target_audience': "MIS Executives, Accountants, Office Administrators, Business Analysts",
                'is_published': True,
                'is_featured': False,
                'order': 7,
            }
        )

        chapters_data = MS_OFFICE_CHAPTERS

        for cdata in chapters_data:
            NotesChapter.objects.update_or_create(
                product=prod, order=cdata['order'],
                defaults={
                    'title': cdata['title'],
                    'is_preview': cdata['is_preview'],
                    'read_time_mins': cdata['read_time_mins'],
                    'summary': cdata['summary'],
                    'content_markdown': cdata['content'],
                    'key_takeaways': cdata.get('takeaways', ''),
                    'interview_tips': cdata.get('interview', ''),
                    'practice_exercise': cdata.get('exercise', ''),
                    'exercise_solution': cdata.get('solution', ''),
                }
            )

        self.stdout.write(f"  [OK] Seeded MS Office Notes ({len(chapters_data)} chapters)")
        return prod

    # =========================================================================
    # 8. BUNDLES
    # =========================================================================
    def seed_bundles(self, p_python, p_web, p_data, p_ai, p_marketing, p_computer, p_msoffice):
        # 1. Tech Career Starter Bundle
        b1, _ = NotesBundle.objects.update_or_create(
            slug='tech-career-starter-bundle',
            defaults={
                'title': 'Tech Career Starter Bundle',
                'short_description': 'Python Programming + Full-Stack Web Dev + Data Analytics (Save ₹698)',
                'description': 'The ultimate trifecta for aspiring software engineers, backend developers, and data specialists. Includes complete study notes, interview vaults, and PDF downloads for Python, Web Development with Django, and Data Analytics with Power BI.',
                'price': 799.00,
                'original_price': 1499.00,
                'is_published': True,
                'is_featured': True,
                'order': 1,
            }
        )
        b1.products.set([p_python, p_web, p_data])

        # 2. Digital Skills Bundle
        b2, _ = NotesBundle.objects.update_or_create(
            slug='digital-skills-bundle',
            defaults={
                'title': 'Digital Skills & Office Mastery Bundle',
                'short_description': 'Basic Computer Skills + MS Office Suite + Digital Marketing (Save ₹548)',
                'description': 'Everything needed for office administration, computer literacy, data entry, spreadsheet modeling, and digital growth marketing.',
                'price': 499.00,
                'original_price': 1047.00,
                'is_published': True,
                'is_featured': True,
                'order': 2,
            }
        )
        b2.products.set([p_computer, p_msoffice, p_marketing])

        # 3. AI + Python Bundle
        b3, _ = NotesBundle.objects.update_or_create(
            slug='ai-python-developer-bundle',
            defaults={
                'title': 'AI Tools + Python Developer Bundle',
                'short_description': 'Python Programming + Generative AI & Prompt Engineering (Save ₹649)',
                'description': 'Master core Python programming alongside cutting-edge Generative AI and prompt engineering workflows.',
                'price': 449.00,
                'original_price': 1098.00,
                'is_published': True,
                'is_featured': True,
                'order': 3,
            }
        )
        b3.products.set([p_python, p_ai])

        # 4. Complete TECHSPIRE Notes Bundle
        b4, _ = NotesBundle.objects.update_or_create(
            slug='complete-techspire-all-in-one-bundle',
            defaults={
                'title': 'Complete TECHSPIRE All-in-One Notes Library',
                'short_description': 'All 7 Complete Premium Notes Packs & E-Books (Save ₹1,744)',
                'description': 'Complete lifetime access to all 7 TECHSPIRE notes packs: Web Dev, Python, Data Analytics, AI Tools, Digital Marketing, Basic Computer Skills, and MS Office. Includes all future chapter updates.',
                'price': 1299.00,
                'original_price': 3043.00,
                'is_published': True,
                'is_featured': True,
                'order': 4,
            }
        )
        b4.products.set([p_python, p_web, p_data, p_ai, p_marketing, p_computer, p_msoffice])

        self.stdout.write("  [OK] Seeded 4 Notes Bundles")
