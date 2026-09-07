import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.accounts.models import User
from apps.courses.models import CourseCategory, Course, Module, Lesson, CourseProject, InterviewQuestion
from apps.quizzes.models import Quiz, Question, Choice

class Command(BaseCommand):
    help = "Seeds complete, industry-standard curricula, detailed study notes, projects, quizzes, and interview questions across all 7 learning categories."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(">> Starting TECHSPIRE Complete Curriculum Seeding..."))

        # 1. Ensure instructor/admin user exists
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

        # 2. Define Category Structure
        categories_data = [
            {
                'name': 'Web Development',
                'slug': 'web-development',
                'icon_class': 'fas fa-code',
                'order': 1,
                'description': 'Modern Full-Stack web engineering covering Frontend, Backend architectures, REST APIs, Databases, and Production Deployment.'
            },
            {
                'name': 'Python Programming',
                'slug': 'python-programming',
                'icon_class': 'fab fa-python',
                'order': 2,
                'description': 'From basic syntax to advanced OOP, data structures, algorithms, automation scripting, and backend system development.'
            },
            {
                'name': 'Data Analytics',
                'slug': 'data-analytics',
                'icon_class': 'fas fa-chart-line',
                'order': 3,
                'description': 'Data transformation, SQL querying, Power BI dashboards, advanced Excel analytics, and business intelligence reporting.'
            },
            {
                'name': 'AI Tools',
                'slug': 'ai-tools',
                'icon_class': 'fas fa-robot',
                'order': 4,
                'description': 'Master Generative AI, Prompt Engineering, Large Language Models (LLMs), ChatGPT, Midjourney, and AI automation workflows.'
            },
            {
                'name': 'Digital Marketing',
                'slug': 'digital-marketing',
                'icon_class': 'fas fa-bullhorn',
                'order': 5,
                'description': 'Performance marketing, Search Engine Optimization (SEO), Social Media Marketing (SMM), Google Ads, and analytics-driven growth.'
            },
            {
                'name': 'Basic Computer Skills',
                'slug': 'basic-computer-skills',
                'icon_class': 'fas fa-desktop',
                'order': 6,
                'description': 'Essential computer fundamentals, OS navigation, file management, cyber safety, internet search skills, and digital productivity.'
            },
            {
                'name': 'MS Office Skills',
                'slug': 'ms-office-skills',
                'icon_class': 'fas fa-file-excel',
                'order': 7,
                'description': 'Professional mastery of Microsoft Excel (Formulas & Pivot Tables), Microsoft Word documentation, and PowerPoint presentations.'
            },
        ]

        categories_map = {}
        for cdata in categories_data:
            cat, _ = CourseCategory.objects.update_or_create(
                slug=cdata['slug'],
                defaults={
                    'name': cdata['name'],
                    'icon_class': cdata['icon_class'],
                    'order': cdata['order'],
                    'description': cdata['description'],
                }
            )
            categories_map[cat.slug] = cat
            self.stdout.write(f"  [OK] Category synced: {cat.name}")

        # 3. Seed Course Content
        self.seed_web_dev(categories_map['web-development'], admin_user)
        self.seed_python(categories_map['python-programming'], admin_user)
        self.seed_data_analytics(categories_map['data-analytics'], admin_user)
        self.seed_ai_tools(categories_map['ai-tools'], admin_user)
        self.seed_digital_marketing(categories_map['digital-marketing'], admin_user)
        self.seed_basic_computer(categories_map['basic-computer-skills'], admin_user)
        self.seed_ms_office(categories_map['ms-office-skills'], admin_user)

        self.stdout.write(self.style.SUCCESS("[SUCCESS] TECHSPIRE Learning platform curriculum successfully updated across all 7 categories!"))

    # =========================================================================
    # 1. WEB DEVELOPMENT
    # =========================================================================
    def seed_web_dev(self, category, instructor):
        course, _ = Course.objects.update_or_create(
            slug='full-stack-web-development-django',
            defaults={
                'title': 'Full-Stack Web Development with Django & Modern UI',
                'category': category,
                'instructor': instructor,
                'instructor_name': 'Prof. Vivek Jat & Senior Web Faculty',
                'short_description': 'Master HTML5, CSS3, JavaScript, Django Backend Framework, REST APIs, and PostgreSQL database architecture.',
                'description': '''This comprehensive full-stack program provides a complete hands-on journey into production-grade web application engineering. You will learn semantic frontend markup, responsive UI design with modern CSS, client-side interactions with JavaScript, robust backend logic with Django, relational data modeling, and cloud deployment.''',
                'level': 'beginner',
                'duration_hours': 32.0,
                'is_free': True,
                'price': 0.00,
                'what_you_will_learn': "Design clean, responsive web layouts using modern HTML5, CSS3, and Flexbox/Grid\nBuild robust backend applications using Python & Django MVT Architecture\nModel relational databases with Django ORM, migrations, and PostgreSQL\nImplement user authentication, session security, and access control\nDevelop and consume RESTful JSON APIs\nDeploy production web apps to cloud platforms with WhiteNoise & Gunicorn",
                'requirements': "Basic computer literacy and typing skills\nNo prior programming experience required\nA computer running Windows, macOS, or Linux with internet access",
                'roadmap_highlights': "Phase 1: Foundations of Frontend (HTML5, Semantic UI, Responsive CSS, Modern JavaScript)\nPhase 2: Backend Architecture & Data Modeling (Python, Django MVT, ORM, PostgreSQL)\nPhase 3: User Auth, Security, and Session Management\nPhase 4: Capstone Full-Stack E-Commerce / LMS Platform Deployment",
                'career_opportunities': "Junior Full-Stack Developer\nPython / Django Backend Engineer\nFrontend Web Developer\nTechnical Support Engineer",
                'is_published': True,
                'is_featured': True,
            }
        )

        # Modules & Lessons
        m1, _ = Module.objects.update_or_create(
            course=course, order=1,
            defaults={'title': 'Module 1: Foundations of Modern Web & Frontend Architecture', 'description': 'HTML5 semantics, modern CSS layout systems, and JavaScript DOM manipulation.'}
        )

        Lesson.objects.update_or_create(
            module=m1, order=1,
            defaults={
                'title': 'HTML5 Architecture & Semantic Markup',
                'duration_minutes': 25,
                'lesson_type': 'article',
                'content': 'Comprehensive guide on modern semantic HTML5 and accessibility standards.',
                'notes_markdown': '''# HTML5 Architecture & Semantic Markup

HTML5 is the backbone of modern web engineering. It provides the structured foundation upon which all web styling, scripting, and accessibility rely.

## What is Semantic HTML?

Semantic elements clearly describe their meaning to both the browser and the developer. Instead of using generic `<div>` tags for everything, HTML5 introduces purpose-driven elements.

> [!IMPORTANT]
> Semantic tags improve search engine optimization (SEO), screen reader accessibility (a11y), and code maintainability across engineering teams.

### Core Semantic Tags vs Generic Tags

| Semantic Element | Purpose | Replaces Generic |
| :--- | :--- | :--- |
| `<header>` | Contains introductory content or nav links | `<div class="header">` |
| `<nav>` | Declares primary website navigation | `<div class="nav-menu">` |
| `<main>` | Represents dominant content of the `<body>` | `<div id="main-content">` |
| `<article>` | Self-contained, syndicatable composition | `<div class="post">` |
| `<section>` | Thematic grouping of content with heading | `<div class="section">` |
| `<footer>` | Author info, copyright, legal links | `<div class="footer">` |

### Production HTML5 Document Boilerplate

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TECHSPIRE Web Architecture</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <nav aria-label="Main Navigation">
      <a href="/" class="brand-logo">TECHSPIRE</a>
    </nav>
  </header>

  <main>
    <article>
      <h1>Modern Web Engineering</h1>
      <p>Building accessible, performant software applications.</p>
    </article>
  </main>

  <footer>
    <p>&copy; 2026 TECHSPIRE Learning. All rights reserved.</p>
  </footer>
</body>
</html>
```

> [!TIP]
> Always provide meaningful `alt` attributes on `<img>` tags and descriptive `aria-label` attributes on interactive icon buttons for screen readers.

> [!WARNING]
> Never use multiple `<main>` tags on a single rendered page. Each HTML document should have exactly one top-level `<main>` element.
''',
                'key_takeaways': "Semantic tags communicate structural intent to search engines and accessibility screen readers.\nEvery web page must include a single <main> element.\nAlways specify viewport meta tags for responsive mobile rendering.",
                'interview_tips': "Interviewers frequently ask: 'Why should we prefer semantic HTML5 tags over generic <div> tags?' Answer: Semantic HTML ensures machine-readability for SEO crawlers, enhances accessibility for assistive technologies, and adheres to W3C standards.",
                'practice_exercise': "Create a single semantic HTML5 webpage representing a product landing page with header, nav, hero section, features grid section, and footer.",
                'exercise_solution': "Ensure the solution uses `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, and `<footer>` without nested redundant divs.",
                'resource_title': 'HTML5 Semantic Cheat Sheet (PDF & Code)',
            }
        )

        Lesson.objects.update_or_create(
            module=m1, order=2,
            defaults={
                'title': 'Modern CSS: Flexbox, Grid & Responsive Tokens',
                'duration_minutes': 30,
                'lesson_type': 'article',
                'content': 'Mastering modern CSS layout systems: Flexbox for 1D and Grid for 2D layouts.',
                'notes_markdown': '''# Modern CSS: Flexbox, Grid & Responsive Tokens

Modern CSS allows engineers to build highly responsive, fluid user interfaces without brittle float hacks or excessive JavaScript calculations.

## 1. Flexbox Layout System (One-Dimensional)

Flexbox excels at distributing space and aligning items along a single axis (row or column).

```css
/* Container CSS */
.flex-container {
  display: flex;
  justify-content: space-between; /* Main axis distribution */
  align-items: center;            /* Cross axis alignment */
  gap: 1.5rem;                    /* Modern gap property */
  flex-wrap: wrap;                /* Responsive wrapping */
}

/* Child item */
.flex-item {
  flex: 1 1 300px; /* grow, shrink, basis */
}
```

## 2. CSS Grid Layout System (Two-Dimensional)

CSS Grid is designed for complex, multi-row and multi-column grid layouts.

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}
```

> [!TIP]
> Using `repeat(auto-fit, minmax(280px, 1fr))` creates an intrinsically responsive grid that automatically adapts to screen width without needing a dozen `@media` queries!

### Comparison: Flexbox vs CSS Grid

| Feature | Flexbox | CSS Grid |
| :--- | :--- | :--- |
| **Dimensionality** | 1-Dimensional (Row OR Column) | 2-Dimensional (Rows AND Columns) |
| **Best Used For** | Navbars, button groups, card headers | Page layouts, dashboard widgets, photo galleries |
| **Alignment Control** | Content-first alignment | Layout-first coordinate system |
''',
                'key_takeaways': "Use Flexbox for 1D component layouts and CSS Grid for 2D full-page structures.\nPrefer CSS custom properties (variables) for scalable design systems.",
                'interview_tips': "Key interview question: 'What is the difference between auto-fill and auto-fit in CSS Grid?' Auto-fill creates empty column tracks when space allows, while auto-fit expands existing items to fill the remaining width.",
                'practice_exercise': "Build a responsive 3-column card grid using CSS Grid that collapses to 1 column on mobile screens.",
                'exercise_solution': "Use `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));` with `gap: 1.5rem;`.",
            }
        )

        m2, _ = Module.objects.update_or_create(
            course=course, order=2,
            defaults={'title': 'Module 2: Django Backend Architecture & ORM Mastery', 'description': 'MVT architecture, model relationships, database migrations, and views.'}
        )

        Lesson.objects.update_or_create(
            module=m2, order=1,
            defaults={
                'title': 'Django MVT Architecture & Project Anatomy',
                'duration_minutes': 35,
                'lesson_type': 'article',
                'notes_markdown': '''# Django MVT Architecture & Project Anatomy

Django is a high-level Python web framework designed for rapid development and clean, pragmatic architecture.

## The Model-View-Template (MVT) Pattern

Unlike traditional MVC (Model-View-Controller) where the Controller handles request routing:
- **Model**: Python representation of database tables and business logic.
- **View**: Request handler containing business logic, querying models, and returning HttpResponse or rendering Templates.
- **Template**: Presentation layer (HTML + Django Template Language).

> [!IMPORTANT]
> In Django, the framework itself acts as the Controller, matching incoming URL patterns to the appropriate View function or class.

### Django Request-Response Flowchart

1. Client sends HTTP Request -> `urls.py` matches URL pattern.
2. `urls.py` invokes View function in `views.py`.
3. View interacts with Database via `models.py` ORM.
4. View passes context data dictionary to `template.html`.
5. Django Template Engine renders final HTML and sends HTTP Response to Client.

```python
# views.py - Standard View Example
from django.shortcuts import render, get_object_or_404
from .models import Course

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    context = {
        'course': course,
        'page_title': f"{course.title} - TECHSPIRE"
    }
    return render(request, 'courses/course_detail.html', context)
```
''',
                'key_takeaways': "Django follows the MVT pattern: Models handle data, Views handle logic, Templates render HTML.\nAlways use get_object_or_404() to handle missing records gracefully.",
                'interview_tips': "Explain Django MVT vs MVC: In Django MVT, the View is responsible for the controller logic and data retrieval, while Template handles the presentation.",
                'practice_exercise': "Write a Django view function that lists only published courses ordered by creation date.",
                'exercise_solution': "`def course_list(request): courses = Course.objects.filter(is_published=True).order_by('-created_at'); return render(request, 'courses/list.html', {'courses': courses})`",
            }
        )

        # Projects & Interview Questions
        CourseProject.objects.update_or_create(
            course=course, order=1,
            defaults={
                'title': 'E-Commerce Marketplace with Django ORM & Stripe Gateway',
                'short_description': 'Build a full-featured online shop with product catalogs, shopping cart, customer checkout, and order history.',
                'description': 'Develop a complete multi-vendor e-commerce web application with user registration, inventory management, search filters, cart sessions, and webhook processing.',
                'difficulty': 'advanced',
                'estimated_hours': 18.0,
                'technologies_used': 'Python, Django, PostgreSQL, Bootstrap 5, JavaScript',
                'is_published': True,
            }
        )

        InterviewQuestion.objects.update_or_create(
            course=course, order=1,
            defaults={
                'question': 'How does Django manage database transactions and prevent SQL injection?',
                'answer': 'Django uses parameterized queries in its Object-Relational Mapper (ORM). SQL queries are constructed using parameter substitution rather than direct string interpolation, ensuring user input is safely escaped and preventing SQL injection attacks.',
                'category_tag': 'Django Security',
                'difficulty': 'intermediate',
            }
        )

        # Quiz
        quiz, _ = Quiz.objects.update_or_create(
            course=course,
            defaults={
                'title': 'Full-Stack Web & Django Certification Assessment',
                'description': 'Test your mastery of HTML5, CSS layout systems, and Django MVT backend architecture to earn your verified certificate.',
                'pass_percentage': 70,
                'time_limit_minutes': 15,
                'max_attempts': 5,
                'is_published': True,
            }
        )

        q1, _ = Question.objects.update_or_create(
            quiz=quiz, order=1,
            defaults={'prompt': 'Which HTML5 semantic element should encapsulate the central content of a webpage?', 'question_type': 'single', 'points': 10, 'explanation': '<main> represents the dominant content of the document.'}
        )
        Choice.objects.update_or_create(question=q1, choice_text='<main>', defaults={'is_correct': True})
        Choice.objects.update_or_create(question=q1, choice_text='<section>', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='<content>', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='<article>', defaults={'is_correct': False})

        q2, _ = Question.objects.update_or_create(
            quiz=quiz, order=2,
            defaults={'prompt': 'In Django MVT architecture, what is the role of the View?', 'question_type': 'single', 'points': 10, 'explanation': 'The View handles business logic, processes requests, interacts with models, and renders templates.'}
        )
        Choice.objects.update_or_create(question=q2, choice_text='Processes HTTP requests and coordinates data with templates', defaults={'is_correct': True})
        Choice.objects.update_or_create(question=q2, choice_text='Directly creates SQL database tables', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q2, choice_text='Stores CSS stylesheets', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q2, choice_text='Defines client-side JavaScript events', defaults={'is_correct': False})

    # =========================================================================
    # 2. PYTHON PROGRAMMING
    # =========================================================================
    def seed_python(self, category, instructor):
        course, _ = Course.objects.update_or_create(
            slug='python-programming-zero-to-pro',
            defaults={
                'title': 'Python Programming: Zero to Professional Masterclass',
                'category': category,
                'instructor': instructor,
                'instructor_name': 'Prof. Vivek Jat & Senior Python Mentors',
                'short_description': 'From basic syntax, control flow, functions, and data structures to Object-Oriented Programming (OOP) and automation.',
                'description': 'Learn Python 3 from ground up with hands-on coding challenges, real-world examples, OOP principles, exception handling, and automation scripting.',
                'level': 'beginner',
                'duration_hours': 28.0,
                'is_free': True,
                'price': 0.00,
                'what_you_will_learn': "Write clean, idiomatic Python 3 code conforming to PEP 8 standards\nMaster core data structures: Lists, Tuples, Dictionaries, and Sets\nUnderstand Object-Oriented Programming: Classes, Inheritance, Polymorphism\nPerform file I/O operations and JSON data serialization\nHandle exceptions and write defensive, bug-free code\nBuild automation CLI tools and web scrapers",
                'requirements': "No prior programming experience required\nA computer with Python 3 installed",
                'roadmap_highlights': "Step 1: Python Core Syntax, Variables & Types\nStep 2: Control Flow, Loops & Custom Functions\nStep 3: Data Structures Mastery (Lists, Dicts, Sets)\nStep 4: OOP Design & Exception Handling\nStep 5: Capstone Project: Automated Multi-Threaded CLI Tool",
                'career_opportunities': "Python Developer\nSoftware Automation Engineer\nData Engineer Intern\nBackend Developer",
                'is_published': True,
                'is_featured': True,
            }
        )

        m1, _ = Module.objects.update_or_create(
            course=course, order=1,
            defaults={'title': 'Module 1: Python Essentials & Data Structures', 'description': 'Variables, data types, conditional branching, loops, and built-in collections.'}
        )

        Lesson.objects.update_or_create(
            module=m1, order=1,
            defaults={
                'title': 'Python Variables, Dynamic Typing & Memory Model',
                'duration_minutes': 25,
                'lesson_type': 'article',
                'notes_markdown': '''# Python Variables, Dynamic Typing & Memory Model

Python is a dynamically-typed, interpreted language where variables are references (pointers) to objects in memory.

## What is a Variable?

In Python, you do not declare variable types explicitly. A variable is simply a name bound to an object in memory.

> [!IMPORTANT]
> A variable name points to a memory address storing the value. Changing the variable re-binds the name to a new object.

```python
# Variable assignments
student_name = "Chanchal"       # str
student_age = 22                # int
gpa = 3.85                      # float
is_enrolled = True              # bool

print(f"Student: {student_name}, Age: {student_age}, GPA: {gpa}")
```

### Mutability vs Immutability in Python

| Category | Data Types | Behavior |
| :--- | :--- | :--- |
| **Immutable** | `int`, `float`, `str`, `tuple`, `bool` | Value cannot be modified in-place; creates new object |
| **Mutable** | `list`, `dict`, `set` | Value can be modified in-place without changing object ID |

> [!TIP]
> Use Python's built-in `id()` function to inspect the unique memory address of any object.

> [!WARNING]
> Be careful when passing mutable objects (like lists or dictionaries) as default arguments in functions!
''',
                'key_takeaways': "Python variables are references to objects in memory.\nImmutable objects cannot be modified in-place, whereas mutable objects can.",
                'interview_tips': "Common interview trap: 'What happens when you use def append_to(item, target=[]): ?' Explain default argument evaluation at function definition time, leading to shared state across calls.",
                'practice_exercise': "Write a Python script that swaps two variables without using a temporary variable.",
                'exercise_solution': "`a, b = b, a` uses Python tuple packing and unpacking.",
                'resource_title': 'Python Core Cheatsheet & Memory Model PDF',
            }
        )

        # Python Quiz
        quiz, _ = Quiz.objects.update_or_create(
            course=course,
            defaults={
                'title': 'Python Programming Assessment Quiz',
                'description': 'Validate your understanding of Python variables, data structures, and OOP principles.',
                'pass_percentage': 70,
                'time_limit_minutes': 15,
                'max_attempts': 5,
                'is_published': True,
            }
        )

        q1, _ = Question.objects.update_or_create(
            quiz=quiz, order=1,
            defaults={'prompt': 'Which of the following data structures in Python is IMMUTABLE?', 'question_type': 'single', 'points': 10, 'explanation': 'Tuples are immutable; once created, their elements cannot be modified.'}
        )
        Choice.objects.update_or_create(question=q1, choice_text='Tuple', defaults={'is_correct': True})
        Choice.objects.update_or_create(question=q1, choice_text='List', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='Dictionary', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='Set', defaults={'is_correct': False})

    # =========================================================================
    # 3. DATA ANALYTICS
    # =========================================================================
    def seed_data_analytics(self, category, instructor):
        course, _ = Course.objects.update_or_create(
            slug='data-analytics-power-bi-excel',
            defaults={
                'title': 'Data Analytics & Business Intelligence with Power BI & Excel',
                'category': category,
                'instructor': instructor,
                'instructor_name': 'TECHSPIRE Data Intelligence Group',
                'short_description': 'Transform raw data into executive business dashboards using Advanced Excel, Power Query, DAX formulas, and Power BI.',
                'description': 'Master modern business intelligence workflows from data cleaning to advanced DAX calculations, interactive Power BI dashboards, and storytelling.',
                'level': 'beginner',
                'duration_hours': 24.0,
                'is_free': True,
                'price': 0.00,
                'what_you_will_learn': "Clean, transform, and merge multi-source datasets with Power Query\nBuild relational data models using Star Schema principles\nWrite high-performance DAX formulas: CALCULATE, FILTER, RELATED, Time Intelligence\nDesign interactive executive KPI dashboards in Microsoft Power BI\nExtract actionable business insights and perform cohort analysis",
                'requirements': "Basic familiarity with spreadsheets and tables\nComputer with Microsoft Power BI Desktop installed (Free)",
                'roadmap_highlights': "Module 1: Data Cleaning & Power Query ETL\nModule 2: Star Schema Modeling & Relationships\nModule 3: DAX Calculations & Time Intelligence\nModule 4: Executive Dashboard UI & Visual Storytelling",
                'career_opportunities': "Data Analyst\nBusiness Intelligence (BI) Developer\nMIS Executive\nOperations Analyst",
                'is_published': True,
                'is_featured': True,
            }
        )

        m1, _ = Module.objects.update_or_create(
            course=course, order=1,
            defaults={'title': 'Module 1: Power Query ETL & Star Schema Modeling', 'description': 'Data extraction, transformation, normalization, and dimensional modeling.'}
        )

        Lesson.objects.update_or_create(
            module=m1, order=1,
            defaults={
                'title': 'Star Schema Architecture vs Snowflake Schema',
                'duration_minutes': 25,
                'lesson_type': 'article',
                'notes_markdown': '''# Star Schema Architecture vs Snowflake Schema

A well-structured data model is the secret to high-performance Power BI reports and fast DAX query evaluation.

## Fact Tables vs Dimension Tables

- **Fact Table**: Contains numeric quantitative measurements and metrics (e.g. Sales Amount, Units Sold, Discount). Contains foreign keys to dimension tables.
- **Dimension Table**: Contains descriptive attributes used for slicing, dicing, and filtering (e.g. Customer Name, Product Category, Region, Date).

> [!IMPORTANT]
> The Star Schema is the industry gold standard for Power BI modeling. All dimension tables connect directly to the central Fact table with 1-to-Many relationships.

```
      [ Dim_Customer ]      [ Dim_Date ]
             │                   │
             └───► [ Fact_Sales ] ◄───┘
                         ▲
                         │
                  [ Dim_Product ]
```

### Star Schema vs Snowflake Schema Comparison

| Dimension | Star Schema | Snowflake Schema |
| :--- | :--- | :--- |
| **Structure** | Single-level normalized dimensions | Sub-normalized dimensional hierarchies |
| **Power BI Performance**| Maximum DAX efficiency & compression | Slower due to multi-table joins |
| **Complexity** | Simple, easy to understand for analysts | Complex relational web |
''',
                'key_takeaways': "Star Schema features a central Fact table surrounded by 1-level Dimension tables.\nAlways prioritize Star Schema for high-speed Power BI VertiPaq engine performance.",
                'interview_tips': "Interviewers love asking: 'Why is Star Schema preferred over Snowflake Schema in Power BI?' Answer: Power BI's in-memory columnar engine (VertiPaq) optimizes single-hop 1-to-many relationships far better than nested joins.",
                'resource_title': 'Data Modeling & Star Schema Blueprint PDF',
            }
        )

        # Quiz
        quiz, _ = Quiz.objects.update_or_create(
            course=course,
            defaults={
                'title': 'Data Analytics & Power BI Assessment',
                'description': 'Test your data modeling and DAX skills.',
                'pass_percentage': 70,
                'time_limit_minutes': 15,
                'max_attempts': 5,
                'is_published': True,
            }
        )
        q1, _ = Question.objects.update_or_create(
            quiz=quiz, order=1,
            defaults={'prompt': 'What type of table in a Star Schema contains quantitative transactional measurements?', 'question_type': 'single', 'points': 10, 'explanation': 'Fact tables contain quantitative metrics.'}
        )
        Choice.objects.update_or_create(question=q1, choice_text='Fact Table', defaults={'is_correct': True})
        Choice.objects.update_or_create(question=q1, choice_text='Dimension Table', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='Lookup Table', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='Bridge Table', defaults={'is_correct': False})

    # =========================================================================
    # 4. AI TOOLS
    # =========================================================================
    def seed_ai_tools(self, category, instructor):
        course, _ = Course.objects.update_or_create(
            slug='generative-ai-prompt-engineering',
            defaults={
                'title': 'Generative AI & Prompt Engineering for Professionals',
                'category': category,
                'instructor': instructor,
                'instructor_name': 'TECHSPIRE AI Innovation Labs',
                'short_description': 'Harness Large Language Models (LLMs), ChatGPT, Midjourney, Claude, and workflow automation for 10x workplace productivity.',
                'description': 'A comprehensive masterclass on prompt engineering techniques, chain-of-thought prompting, role-based instructions, AI agents, and automating routine professional workflows.',
                'level': 'beginner',
                'duration_hours': 18.0,
                'is_free': True,
                'price': 0.00,
                'what_you_will_learn': "Master Prompt Engineering frameworks: Few-Shot, Chain-of-Thought, ReAct\nLeverage ChatGPT, Claude, and Gemini for rapid code generation & debugging\nGenerate photorealistic marketing assets using Midjourney & DALL-E\nAutomate content creation, data extraction, and executive summaries\nUnderstand LLM hallucinations, limitations, and security best practices",
                'requirements': "No technical background required\nA free ChatGPT or Google Gemini account",
                'roadmap_highlights': "Module 1: LLM Architecture & Prompt Engineering Fundamentals\nModule 2: Advanced Reasoning & Structured Output Prompts\nModule 3: AI for Coding, Data Synthesis & Research\nModule 4: Multi-Modal AI & Automation Agents",
                'career_opportunities': "Prompt Engineer\nAI Workflow Specialist\nDigital Content Architect\nProductivity Consultant",
                'is_published': True,
                'is_featured': True,
            }
        )

        m1, _ = Module.objects.update_or_create(
            course=course, order=1,
            defaults={'title': 'Module 1: Prompt Engineering Mastery & Frameworks', 'description': 'Role prompting, context constraints, few-shot prompting, and chain of thought.'}
        )

        Lesson.objects.update_or_create(
            module=m1, order=1,
            defaults={
                'title': 'The CREATE Prompting Framework for Deterministic Outputs',
                'duration_minutes': 20,
                'lesson_type': 'article',
                'notes_markdown': '''# The CREATE Prompting Framework for Deterministic Outputs

Generative AI models are probabilistic next-token predictors. To obtain reliable, high-quality responses, you must structure your prompts systematically.

## The CREATE Framework Breakdown

- **C** - **Character/Role**: Define who the AI is (e.g. Senior Software Architect, Corporate Tax Attorney).
- **R** - **Request**: State the exact task clearly.
- **E** - **Examples**: Provide 1-2 few-shot input/output examples.
- **A** - **Adjustments/Constraints**: Specify negative constraints (e.g., "Do not use jargon", "Keep under 200 words").
- **T** - **Type/Format**: Specify output format (JSON, Markdown table, bulleted checklist).
- **E** - **Evaluation Criteria**: State how quality will be judged.

> [!IMPORTANT]
> Giving the model an explicit output format (e.g. valid JSON) reduces hallucination rates significantly.

### Production Prompt Template

```prompt
Act as a Senior Python Backend Architect.
Task: Review the provided Django view for SQL injection and security vulnerabilities.
Constraints:
- Output strictly in Markdown table format with columns: [Line Number, Severity, Issue, Fix Code].
- Do not include conversational greetings.
```
''',
                'key_takeaways': "Structured prompts produce deterministic and production-grade LLM responses.\nFew-shot examples and strict output schema constraints eliminate hallucination.",
                'interview_tips': "Interview question: 'What is Chain-of-Thought (CoT) prompting?' CoT prompts the model to break complex reasoning into sequential intermediate steps before giving a final answer.",
                'resource_title': 'Prompt Engineering Master Vault (PDF Guide)',
            }
        )

        # Quiz
        quiz, _ = Quiz.objects.update_or_create(
            course=course,
            defaults={
                'title': 'AI Tools & Prompt Engineering Assessment',
                'description': 'Demonstrate your prompt architecture mastery.',
                'pass_percentage': 70,
                'time_limit_minutes': 15,
                'max_attempts': 5,
                'is_published': True,
            }
        )
        q1, _ = Question.objects.update_or_create(
            quiz=quiz, order=1,
            defaults={'prompt': 'What technique involves providing 1-3 sample input/output pairs in a prompt?', 'question_type': 'single', 'points': 10, 'explanation': 'Few-shot prompting provides sample demonstrations.'}
        )
        Choice.objects.update_or_create(question=q1, choice_text='Few-Shot Prompting', defaults={'is_correct': True})
        Choice.objects.update_or_create(question=q1, choice_text='Zero-Shot Prompting', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='Temperature Inversion', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='Token Quantization', defaults={'is_correct': False})

    # =========================================================================
    # 5. DIGITAL MARKETING
    # =========================================================================
    def seed_digital_marketing(self, category, instructor):
        course, _ = Course.objects.update_or_create(
            slug='digital-marketing-seo-growth-mastery',
            defaults={
                'title': 'Digital Marketing, SEO & Performance Growth Mastery',
                'category': category,
                'instructor': instructor,
                'instructor_name': 'TECHSPIRE Growth Marketing Experts',
                'short_description': 'Master SEO, Google Search Ads, Social Media Marketing, Meta Ads, Content Strategy, and Conversion Rate Optimization (CRO).',
                'description': 'A complete roadmap to modern growth marketing. Learn how to rank websites on page 1 of Google, run profitable paid ad campaigns on Meta and Google Ads, and analyze user conversion funnels.',
                'level': 'beginner',
                'duration_hours': 22.0,
                'is_free': True,
                'price': 0.00,
                'what_you_will_learn': "Conduct keyword research, on-page SEO, technical audits, and link building\nSet up and optimize Google Search, Display, and Performance Max ad campaigns\nRun targeted Meta (Facebook & Instagram) ad funnels with custom audiences\nTrack conversions and user events with Google Analytics 4 (GA4) & GTM\nCreate high-converting landing pages and optimize sales funnels",
                'requirements': "No prior marketing experience required\nA computer with an internet connection",
                'roadmap_highlights': "Module 1: SEO Fundamentals, Keyword Research & On-Page Optimization\nModule 2: Technical SEO, Site Speed & Schema Markup\nModule 3: Google Ads (Search & Performance Max)\nModule 4: Meta Ads & Social Funnel Architecture\nModule 5: Google Analytics 4 (GA4) & Conversion Optimization",
                'career_opportunities': "Digital Marketing Executive\nSEO Specialist\nPerformance Marketing Associate\nSocial Media Manager",
                'is_published': True,
                'is_featured': True,
            }
        )

        m1, _ = Module.objects.update_or_create(
            course=course, order=1,
            defaults={'title': 'Module 1: Search Engine Optimization (SEO) & Content Strategy', 'description': 'Keyword search intent, technical on-page ranking factors, and content architecture.'}
        )

        Lesson.objects.update_or_create(
            module=m1, order=1,
            defaults={
                'title': 'Keyword Search Intent & On-Page SEO Architecture',
                'duration_minutes': 25,
                'lesson_type': 'article',
                'notes_markdown': '''# Keyword Search Intent & On-Page SEO Architecture

Search Engine Optimization (SEO) is the science of improving website visibility in organic search engine results pages (SERPs).

## The 4 Core Types of Search Intent

Understanding user intent determines what type of page you should create to rank.

| Intent Type | User Goal | Example Search Query | Best Landing Page |
| :--- | :--- | :--- | :--- |
| **Informational** | Wants an answer or guide | *"How does Django ORM work?"* | Detailed blog post / tutorial |
| **Navigational** | Wants to find a specific website | *"TECHSPIRE login page"* | Homepage or login portal |
| **Commercial** | Comparing options before buying | *"Best data analytics courses 2026"* | Comparison guide / reviews |
| **Transactional**| Ready to make a purchase | *"Buy Python masterclass course"* | Product / course sales page |

> [!IMPORTANT]
> Search engines rank pages that best satisfy the user's search intent. Aligning page content with search intent is the single biggest ranking factor.

### On-Page SEO Checklist

- **Title Tag**: Target keyword near the front (50-60 characters).
- **Meta Description**: Compelling summary with CTA (150-160 characters).
- **H1 Heading**: Exactly one `<h1>` matching the search topic.
- **H2/H3 Structure**: Subheadings addressing related user questions.
- **Internal Links**: Connect related pages with descriptive anchor text.
- **Schema Markup**: Add JSON-LD structured data for rich snippets.
''',
                'key_takeaways': "Search intent categorizes into Informational, Navigational, Commercial, and Transactional.\nEvery page must have exactly one <h1> heading and an optimized title tag.",
                'interview_tips': "Interview question: 'What is the difference between On-Page SEO and Off-Page SEO?' On-Page refers to factors on your website (content, tags, speed), while Off-Page refers to external authority signals (backlinks, brand mentions).",
                'resource_title': 'Complete 50-Point SEO Audit Checklist (PDF)',
            }
        )

        # Quiz
        quiz, _ = Quiz.objects.update_or_create(
            course=course,
            defaults={
                'title': 'Digital Marketing & SEO Certification Assessment',
                'description': 'Validate your growth marketing and SEO knowledge.',
                'pass_percentage': 70,
                'time_limit_minutes': 15,
                'max_attempts': 5,
                'is_published': True,
            }
        )
        q1, _ = Question.objects.update_or_create(
            quiz=quiz, order=1,
            defaults={'prompt': 'Which type of search intent represents a user actively looking to purchase a product or service?', 'question_type': 'single', 'points': 10, 'explanation': 'Transactional intent indicates ready-to-buy intent.'}
        )
        Choice.objects.update_or_create(question=q1, choice_text='Transactional Intent', defaults={'is_correct': True})
        Choice.objects.update_or_create(question=q1, choice_text='Informational Intent', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='Navigational Intent', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='Passive Intent', defaults={'is_correct': False})

    # =========================================================================
    # 6. BASIC COMPUTER SKILLS
    # =========================================================================
    def seed_basic_computer(self, category, instructor):
        course, _ = Course.objects.update_or_create(
            slug='computer-fundamentals-digital-literacy',
            defaults={
                'title': 'Computer Fundamentals & Essential Digital Skills',
                'category': category,
                'instructor': instructor,
                'instructor_name': 'TECHSPIRE IT Foundation Mentors',
                'short_description': 'Master essential computer operations, operating systems, file management, keyboard shortcuts, and internet security.',
                'description': 'Designed for absolute beginners, students, and professionals seeking confident digital literacy. Learn computer hardware components, Windows navigation, file organization, email communication, browser mastery, and cyber security hygiene.',
                'level': 'beginner',
                'duration_hours': 16.0,
                'is_free': True,
                'price': 0.00,
                'what_you_will_learn': "Understand computer hardware: CPU, RAM, SSD/HDD, and peripherals\nNavigate Windows OS, Task Manager, Settings, and Control Panel\nOrganize files, folders, cloud storage, and compressed ZIP archives\nMaster top 30 essential productivity keyboard shortcuts\nPractice cyber safety: password management, phishing detection, and secure browsing\nCompose professional emails and collaborate with Google Drive/OneDrive",
                'requirements': "A desktop or laptop computer with Windows or Mac\nNo prior experience needed",
                'roadmap_highlights': "Module 1: Hardware Components & Operating System Architecture\nModule 2: File Systems, Folder Hierarchies & Storage Management\nModule 3: Internet Navigation, Search Operators & Digital Communication\nModule 4: Cyber Safety, Antivirus & Data Backup Strategies",
                'career_opportunities': "Data Entry Operator\nOffice Administrative Assistant\nCustomer Support Associate\nFront Desk Coordinator",
                'is_published': True,
                'is_featured': False,
            }
        )

        m1, _ = Module.objects.update_or_create(
            course=course, order=1,
            defaults={'title': 'Module 1: Computer Architecture & File Management', 'description': 'Hardware fundamentals, memory vs storage, and file organization.'}
        )

        Lesson.objects.update_or_create(
            module=m1, order=1,
            defaults={
                'title': 'Computer Hardware Essentials: RAM vs Storage vs CPU',
                'duration_minutes': 20,
                'lesson_type': 'article',
                'notes_markdown': '''# Computer Hardware Essentials: RAM vs Storage vs CPU

Understanding the core components of a computer helps you optimize performance and troubleshoot everyday issues.

## The Core Hardware Trio

1. **CPU (Central Processing Unit)**: The brain of the computer that executes software instructions and calculations.
2. **RAM (Random Access Memory)**: Fast, volatile short-term memory that holds currently active programs and open files.
3. **Storage (SSD / HDD)**: Permanent, non-volatile long-term storage where the operating system and saved documents reside.

> [!IMPORTANT]
> RAM is temporary (volatile) — when you turn off your computer, RAM is wiped clean. Your files stay safe on your SSD or Hard Drive.

### Hardware Comparison Matrix

| Component | Function | Analogy | Speed |
| :--- | :--- | :--- | :--- |
| **CPU** | Processing logic | The Chef | Nanoseconds |
| **RAM** | Active workspace | Kitchen Countertop | Microseconds |
| **SSD / HDD** | Permanent storage | Pantry / Refrigerator | Milliseconds |

### Top Productivity Keyboard Shortcuts

- `Ctrl + C` / `Ctrl + V`: Copy and Paste
- `Ctrl + Z` / `Ctrl + Y`: Undo and Redo
- `Win + D`: Show Desktop immediately
- `Win + Shift + S`: Snipping tool for screen captures
- `Ctrl + Shift + Esc`: Open Task Manager
''',
                'key_takeaways': "RAM is temporary working memory; SSD/HDD is permanent storage.\nKeyboard shortcuts drastically accelerate daily computer productivity.",
                'resource_title': 'Windows Productivity & Shortcut Guide (PDF)',
            }
        )

        # Quiz
        quiz, _ = Quiz.objects.update_or_create(
            course=course,
            defaults={
                'title': 'Computer Fundamentals Assessment',
                'description': 'Test your computer basics and digital literacy knowledge.',
                'pass_percentage': 70,
                'time_limit_minutes': 15,
                'max_attempts': 5,
                'is_published': True,
            }
        )
        q1, _ = Question.objects.update_or_create(
            quiz=quiz, order=1,
            defaults={'prompt': 'Which computer component acts as volatile short-term memory for currently running applications?', 'question_type': 'single', 'points': 10, 'explanation': 'RAM holds active applications in volatile memory.'}
        )
        Choice.objects.update_or_create(question=q1, choice_text='RAM (Random Access Memory)', defaults={'is_correct': True})
        Choice.objects.update_or_create(question=q1, choice_text='Hard Disk Drive (HDD)', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='Power Supply Unit (PSU)', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='Optical Drive', defaults={'is_correct': False})

    # =========================================================================
    # 7. MS OFFICE SKILLS
    # =========================================================================
    def seed_ms_office(self, category, instructor):
        course, _ = Course.objects.update_or_create(
            slug='ms-office-suite-excel-word-powerpoint',
            defaults={
                'title': 'Microsoft Office Suite Mastery: Excel, Word & PowerPoint',
                'category': category,
                'instructor': instructor,
                'instructor_name': 'TECHSPIRE Corporate Productivity Faculty',
                'short_description': 'Master Microsoft Excel (Formulas, VLOOKUP, XLOOKUP, Pivot Tables), Word document styling, and professional PowerPoint decks.',
                'description': 'The definitive corporate productivity course. Master advanced Excel spreadsheet formulas, dynamic Pivot Tables, data visualization charts, executive business reports in Word, and pitch decks in PowerPoint.',
                'level': 'beginner',
                'duration_hours': 26.0,
                'is_free': True,
                'price': 0.00,
                'what_you_will_learn': "Master 50+ essential Excel formulas: XLOOKUP, VLOOKUP, INDEX/MATCH, IF, SUMIFS, COUNTIFS\nBuild interactive Pivot Tables, calculated fields, and KPI dashboards in Excel\nFormat professional corporate proposals, letters, and automated mail merges in Word\nDesign sleek, engaging executive presentation decks in Microsoft PowerPoint\nAutomate repetitive worksheet calculations with data validation and conditional formatting",
                'requirements': "A computer with Microsoft Office (Excel, Word, PowerPoint) installed",
                'roadmap_highlights': "Module 1: Microsoft Excel Core Functions & Data Organization\nModule 2: Advanced Lookup Formulas (VLOOKUP, XLOOKUP, INDEX/MATCH)\nModule 3: Pivot Tables, Calculated Fields & Slicers\nModule 4: Microsoft Word Executive Document Design\nModule 5: PowerPoint Presentation Design & Visual Delivery",
                'career_opportunities': "MIS Executive\nBusiness Operations Associate\nAdministrative Assistant\nFinancial Analyst Assistant",
                'is_published': True,
                'is_featured': True,
            }
        )

        m1, _ = Module.objects.update_or_create(
            course=course, order=1,
            defaults={'title': 'Module 1: Excel Formulas, Lookups & Pivot Tables', 'description': 'Essential formulas, conditional formatting, XLOOKUP, and pivot reporting.'}
        )

        Lesson.objects.update_or_create(
            module=m1, order=1,
            defaults={
                'title': 'VLOOKUP vs XLOOKUP vs INDEX-MATCH Mastery',
                'duration_minutes': 30,
                'lesson_type': 'article',
                'notes_markdown': '''# VLOOKUP vs XLOOKUP vs INDEX-MATCH Mastery

Lookup formulas are the backbone of financial modeling, inventory tracking, and business analytics in Microsoft Excel.

## 1. Traditional VLOOKUP Formula

```excel
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
```
- **Limitation**: Can only search from left-to-right. If your lookup value is in column B and return value is in column A, VLOOKUP fails.

## 2. Modern XLOOKUP Formula (Recommended)

XLOOKUP is the powerful successor to VLOOKUP available in modern Excel.

```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode])
```

### Key Advantages of XLOOKUP:
1. Searches both Left-to-Right and Right-to-Left.
2. Defaults to exact match (no need for `, FALSE`).
3. Built-in error handling via `[if_not_found]` argument.
4. Resilient to column insertions and deletions.

> [!TIP]
> Always use `XLOOKUP` when working on modern Excel versions. It is faster, less error-prone, and simpler to read.

### Comparison Table

| Feature | VLOOKUP | INDEX & MATCH | XLOOKUP |
| :--- | :--- | :--- | :--- |
| **Search Direction** | Left-to-Right only | Any Direction | Any Direction |
| **Column Insert Safety**| Breaks if column added | Safe | Safe |
| **Exact Match Default** | False (requires FALSE) | True | True (default) |
| **Built-in Error Catch**| Requires `IFERROR()` | Requires `IFERROR()` | Built-in `[if_not_found]` |
''',
                'key_takeaways': "XLOOKUP replaces both VLOOKUP and INDEX-MATCH in modern Excel.\nXLOOKUP can search in any direction and includes built-in error handling.",
                'interview_tips': "Interview question: 'Why does inserting a column break VLOOKUP, and how do you fix it?' VLOOKUP uses static integer column indexes (e.g. 3). Inserting a column shifts positions. Solution: Use XLOOKUP or INDEX/MATCH.",
                'resource_title': 'Master Excel Formulas & Shortcut Cheat Sheet (PDF)',
            }
        )

        # Quiz
        quiz, _ = Quiz.objects.update_or_create(
            course=course,
            defaults={
                'title': 'Microsoft Excel & Office Certification Assessment',
                'description': 'Demonstrate your Excel formula and office productivity mastery.',
                'pass_percentage': 70,
                'time_limit_minutes': 15,
                'max_attempts': 5,
                'is_published': True,
            }
        )
        q1, _ = Question.objects.update_or_create(
            quiz=quiz, order=1,
            defaults={'prompt': 'Which modern Excel formula allows two-way searching and does not break when columns are inserted?', 'question_type': 'single', 'points': 10, 'explanation': 'XLOOKUP handles multi-directional searches safely.'}
        )
        Choice.objects.update_or_create(question=q1, choice_text='XLOOKUP', defaults={'is_correct': True})
        Choice.objects.update_or_create(question=q1, choice_text='VLOOKUP', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='HLOOKUP', defaults={'is_correct': False})
        Choice.objects.update_or_create(question=q1, choice_text='CONCATENATE', defaults={'is_correct': False})
