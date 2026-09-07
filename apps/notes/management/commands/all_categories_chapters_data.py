"""
Rich Chapters Data for Web Development, Data Analytics, AI Tools, Digital Marketing, Basic Computer Skills, and MS Office.
"""

WEB_DEV_CHAPTERS = [
    {
        'order': 1,
        'title': 'Chapter 1: Modern Semantic HTML5, CSS Grid & Responsive Flexbox Architecture',
        'is_preview': True,
        'read_time_mins': 30,
        'summary': 'Semantic HTML structure, Flexbox layouts, 2D CSS Grid systems, mobile-first media queries, and accessibility (a11y).',
        'content': '''# Chapter 1: Modern Semantic HTML5 & Responsive CSS Architecture

## Learning Objectives
- Write accessible, SEO-optimized semantic HTML5 code.
- Master 1D layouts with Flexbox and 2D layouts with CSS Grid.
- Implement mobile-first responsive breakpoints.

---

## 1. Semantic Layout Architecture
```
┌──────────────────────────────────────────────┐
│                  <header>                    │
├──────────────────────────────────────────────┤
│                   <nav>                      │
├───────────────────────┬──────────────────────┤
│        <main>         │       <aside>        │
│   ┌───────────────┐   │  (Sidebar, Widgets)  │
│   │   <article>   │   │                      │
│   │   <section>   │   │                      │
│   └───────────────┘   │                      │
├───────────────────────┴──────────────────────┤
│                  <footer>                    │
└──────────────────────────────────────────────┘
```

## 2. Flexbox vs CSS Grid Quick Rules
- Use **Flexbox** for 1-dimensional components (Navigation bars, button groups, centering items).
- Use **CSS Grid** for 2-dimensional page layouts (Photo galleries, dashboard card layouts, magazine columns).

```css
/* Responsive 12-column CSS Grid without media queries */
.ts-dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
```
''',
        'takeaways': 'Always use semantic HTML tags for SEO and accessibility; prefer CSS Grid for multi-column dashboards.',
        'interview': 'Explain the CSS Box Model: Content, Padding, Border, and Margin.',
        'exercise': 'Build a responsive 3-column pricing card layout that stacks to 1 column on mobile screens using CSS Flexbox.',
        'solution': '`.pricing-wrapper { display: flex; flex-wrap: wrap; gap: 1rem; } .pricing-card { flex: 1 1 300px; }`'
    },
    {
        'order': 2,
        'title': 'Chapter 2: JavaScript ES6+, DOM Manipulation, Async/Await & Event Loops',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'let/const, arrow functions, destructuring, Promises, async/await, Fetch API, and Event Bubbling.',
        'content': '''# Chapter 2: Modern JavaScript & Asynchronous Programming

## 1. The JavaScript Event Loop & Microtask Queue
```
[ Call Stack ] ──► (Async API call) ──► [ Web APIs (Browser) ]
      ▲                                         │
      │                                         ▼
[ Event Loop ] ◄── (Pushes callbacks) ◄── [ Callback / Promise Queue ]
```

## 2. Modern Async/Await Fetch API
```javascript
async function fetchCourseNotes(slug) {
  try {
    const response = await fetch(`/api/notes/${slug}/`, {
      headers: { 'Accept': 'application/json' }
    });
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }
    const data = await response.json();
    console.log('Loaded Notes:', data.title);
    return data;
  } catch (error) {
    console.error('Fetch Failed:', error.message);
  }
}
```
''',
        'takeaways': 'Async/await is syntactic sugar over Promises; understand the Event Loop and non-blocking I/O.',
        'interview': 'What is the difference between `==` and `===` in JavaScript, and what is closure?',
    },
    {
        'order': 3,
        'title': 'Chapter 3: Backend Engineering with Python & Django MVT Architecture',
        'is_preview': False,
        'read_time_mins': 40,
        'summary': 'Django settings, MTV architecture, Model design, ORM query optimization, Views, and Template inheritance.',
        'content': '''# Chapter 3: Django Web Framework Architecture

## 1. Django Model-Template-View (MVT) Flow
```
[ Browser Request ]
         │
         ▼
[ urls.py (Routing) ] ──► [ views.py (Business Logic) ] ◄──► [ models.py (ORM / DB) ]
                                   │
                                   ▼
                         [ templates/ (HTML Output) ]
```

## 2. Query Optimization with `select_related` and `prefetch_related`
```python
# Avoid N+1 Query Problems
# 1 Query for courses + categories
courses = Course.objects.select_related('category').prefetch_related('modules__lessons').filter(is_published=True)
```
''',
        'takeaways': 'Django ORM translates Python classes into SQL; always use select_related for ForeignKeys and prefetch_related for ManyToMany.',
        'interview': 'What is the N+1 query problem in Django ORM and how is it resolved?',
    },
    {
        'order': 4,
        'title': 'Chapter 4: RESTful API Design & Django REST Framework (DRF)',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'REST principles, Serializers, ViewSets, JWT authentication, pagination, and API versioning.',
        'content': '''# Chapter 4: RESTful API Engineering with DRF

## 1. REST Architectural Constraints
- **Client-Server**: Separation of UI and data storage.
- **Stateless**: Every request contains all necessary credentials.
- **Cacheable**: Explicit Cache-Control headers.
- **Uniform Interface**: Predictable standard URIs (`/api/v1/notes/`).
''',
        'takeaways': 'REST APIs use standard HTTP verbs (GET, POST, PUT, PATCH, DELETE) and return structured JSON payloads.',
        'interview': 'What is the difference between PUT and PATCH HTTP methods?',
    },
    {
        'order': 5,
        'title': 'Chapter 5: Production Deployment, Security, Docker & Vercel Architecture',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'WSGI/ASGI, Whitenoise static asset compression, CSRF, CORS, environment security, and serverless deployment.',
        'content': '''# Chapter 5: Production Web Deployment & Security

## 1. Essential Security Checklist
- `DEBUG = False` in production.
- `SECRET_KEY` stored securely in environment variables.
- `SECURE_PROXY_SSL_HEADER` enabled behind reverse proxies.
- `CSRF_COOKIE_SECURE = True` and `SESSION_COOKIE_SECURE = True`.
''',
        'takeaways': 'Never expose database credentials in source code; configure proper HTTPS and cookie flags.',
        'interview': 'What is Cross-Site Request Forgery (CSRF) and how does Django protect against it?',
    }
]

DATA_ANALYTICS_CHAPTERS = [
    {
        'order': 1,
        'title': 'Chapter 1: Complete Data Analytics & Business Intelligence Lifecycle',
        'is_preview': True,
        'read_time_mins': 25,
        'summary': 'The 5 stages of business analytics: Ingestion, Cleaning, Modeling, Visualization, and Executive Decision-Making.',
        'content': '''# Chapter 1: Data Analytics & Business Intelligence Foundations

## 1. The Analytics Value Chain
```
[ Raw Data Sources ] ──► [ ETL / Data Cleaning ] ──► [ SQL / Relational Modeling ]
                                                               │
                                                               ▼
[ Executive Decisions ] ◄── [ Power BI Dashboards ] ◄── [ Statistical Analysis (Pandas) ]
```

## 2. Descriptive, Diagnostic, Predictive & Prescriptive Analytics
- **Descriptive**: *What happened?* (e.g. Sales dropped 12% in Q3)
- **Diagnostic**: *Why did it happen?* (e.g. Supply chain delays in regional warehouse)
- **Predictive**: *What will happen?* (e.g. Demand forecasting for holiday season)
- **Prescriptive**: *What action should we take?* (e.g. Reroute inventory from central depot)
''',
        'takeaways': 'Clean data is the foundation of trustworthy business decisions; understand the 4 analytics categories.',
        'interview': 'Explain the difference between Data Science and Data Analytics.',
    },
    {
        'order': 2,
        'title': 'Chapter 2: Advanced SQL for Business Analytics (JOINs, CTEs & Window Functions)',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'INNER/LEFT/FULL JOINs, GROUP BY, HAVING, Common Table Expressions (WITH), and Window Functions (ROW_NUMBER, RANK, DENSE_RANK).',
        'content': '''# Chapter 2: High-Performance SQL for Data Analysis

## 1. Advanced Window Functions & CTEs
```sql
WITH MonthlySales AS (
  SELECT
    DATE_TRUNC('month', order_date) AS sales_month,
    category_id,
    SUM(amount) AS total_revenue
  FROM orders
  GROUP BY 1, 2
)
SELECT
  sales_month,
  category_id,
  total_revenue,
  RANK() OVER (PARTITION BY sales_month ORDER BY total_revenue DESC) AS rank_in_month,
  LAG(total_revenue, 1) OVER (PARTITION BY category_id ORDER BY sales_month) AS prev_month_revenue
FROM MonthlySales;
```
''',
        'takeaways': 'Window functions calculate running totals and rankings without collapsing result set rows like GROUP BY.',
        'interview': 'What is the difference between RANK(), DENSE_RANK(), and ROW_NUMBER() in SQL?',
    },
    {
        'order': 3,
        'title': 'Chapter 3: Python for Data Analysis (NumPy, Pandas DataFrames & Data Cleaning)',
        'is_preview': False,
        'read_time_mins': 40,
        'summary': 'NumPy vectorized arrays, Pandas DataFrame indexing, handling missing data (NaN), merge, concat, and groupby.',
        'content': '''# Chapter 3: Data Wrangling with Pandas & NumPy

## 1. Cleaning & Transforming Real-World Datasets
```python
import pandas as pd
import numpy as np

# Load transaction data
df = pd.read_csv('ecommerce_sales.csv')

# Handle missing values & convert datatypes
df['order_date'] = pd.to_datetime(df['order_date'])
df['customer_age'].fillna(df['customer_age'].median(), inplace=True)

# Feature engineering: Customer Lifetime Value (CLV)
customer_clv = df.groupby('customer_id').agg(
    total_orders=('order_id', 'count'),
    total_spend=('amount', 'sum'),
    avg_basket_value=('amount', 'mean')
).reset_index()

print(customer_clv.head())
```
''',
        'takeaways': 'Vectorized operations in NumPy and Pandas execute in optimized C code, running 50x faster than raw Python loops.',
        'interview': 'How does loc[] differ from iloc[] in Pandas DataFrames?',
    },
    {
        'order': 4,
        'title': 'Chapter 4: Exploratory Data Analysis & Visual Storytelling (Matplotlib & Seaborn)',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'Distribution plots, histograms, scatter matrices, correlation heatmaps, box plots, and chart selection best practices.',
        'content': '''# Chapter 4: Visual Storytelling & Exploratory Analysis

## 1. Chart Selection Guide
- **Distribution**: Histogram, KDE plot, Box plot.
- **Relationship / Correlation**: Scatter plot, Heatmap.
- **Comparison over Time**: Line chart, Area chart.
- **Categorical Composition**: Stacked bar chart, Treemap.
''',
        'takeaways': 'Visual storytelling translates raw statistics into intuitive visual cues for non-technical stakeholders.',
        'interview': 'What is the purpose of a Box Plot and what do the 5 summary points represent? (Min, Q1, Median, Q3, Max).',
    },
    {
        'order': 5,
        'title': 'Chapter 5: Power BI & DAX Mastery (Data Modeling, Star Schemas & Executive Dashboards)',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'Power Query ETL transformations, Fact vs Dimension tables, Star Schema design, DAX measures (CALCULATE, SUMX, FILTER).',
        'content': '''# Chapter 5: Power BI & DAX Architecture

## 1. The Star Schema Architecture
```
             ┌─────────────────────────┐
             │   Dim_Customer (1)      │
             └────────────┬────────────┘
                          │ (1:N)
┌──────────────────────┐  │   ┌──────────────────────┐
│   Dim_Product (1)    ├──┼──►│   Fact_Sales (*)     │
└──────────────────────┘  │   └──────────┬───────────┘
                          │ (1:N)        │ (1:N)
             ┌────────────┴──────────┐   │
             │     Dim_Date (1)      ◄───┘
             └───────────────────────┘
```

## 2. High-Performance DAX Measures
```dax
-- Year-over-Year (YoY) Sales Growth Measure
Total Revenue = SUM(Fact_Sales[Revenue])

Revenue Last Year = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))

YoY Growth % = DIVIDE([Total Revenue] - [Revenue Last Year], [Revenue Last Year], 0)
```
''',
        'takeaways': 'Always design relational star schemas (Fact + Dimensions) for optimal Power BI query performance.',
        'interview': 'Explain the difference between a Calculated Column and a DAX Measure in Power BI.',
    }
]

AI_TOOLS_CHAPTERS = [
    {
        'order': 1,
        'title': 'Chapter 1: Generative AI, Large Language Models (LLMs) & Transformer Foundations',
        'is_preview': True,
        'read_time_mins': 25,
        'summary': 'Transformer architecture, self-attention, tokenization, temperature, context windows, and how LLMs predict next tokens.',
        'content': '''# Chapter 1: Generative AI & LLM Foundations

## 1. How Large Language Models Work
```
[ Input Text / Prompt ]
         │
         ▼
[ Tokenizer (BPE) ] ──► Converts words into integer tokens
         │
         ▼
[ Transformer Self-Attention Layers ] ──► Calculates contextual weights & relationships
         │
         ▼
[ Probability Distribution over Vocabulary ] ──► Selects next most probable token (Temperature control)
```

> [!IMPORTANT]
> LLMs are statistical prediction engines trained on massive corpora to predict the next token based on learned probability weights.
''',
        'takeaways': 'LLMs operate on tokens, not words; parameters like temperature control randomness vs determinism.',
        'interview': 'What is Tokenization and how does Temperature affect LLM generation?',
    },
    {
        'order': 2,
        'title': 'Chapter 2: Systematic Prompt Engineering Frameworks & Prompt Patterns',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'The RTCO framework (Role, Task, Context, Output), Few-Shot prompting, Chain-of-Thought (CoT), and constraint enforcement.',
        'content': '''# Chapter 2: The Science of Prompt Engineering

## 1. The RTCO Enterprise Prompt Blueprint
```markdown
# ROLE:
You are a Principal Python Architect with 15+ years of enterprise experience.

# CONTEXT:
We are refactoring an e-commerce checkout backend processing 10,000 orders/minute.

# TASK:
Design a thread-safe idempotent payment processing function in Python using Redis locks.

# CONSTRAINTS & OUTPUT FORMAT:
- Use type hints and docstrings.
- Output ONLY verified, executable Python code with no markdown chatter.
```
''',
        'takeaways': 'Specific context, explicit negative constraints, and structured output formatting dramatically reduce LLM hallucinations.',
        'interview': 'What is Chain-of-Thought (CoT) prompting and why does it improve reasoning performance?',
    },
    {
        'order': 3,
        'title': 'Chapter 3: AI Developer Tools & Coding Workflows (Cursor, Copilot & ChatGPT)',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'AI-assisted coding, unit test generation, codebase indexing, automated refactoring, and AI pair programming workflows.',
        'content': '''# Chapter 3: High-Speed AI Developer Workflows

## 1. Best Practices for AI Pair Programming
- **Small Context Windows**: Give the AI specific functions to refactor rather than entire thousand-line modules.
- **Test-Driven AI Generation**: Ask the AI to write unit test assertions before generating implementation logic.
- **Human in the Loop**: Always read and verify AI generated code for security vulnerabilities and subtle edge cases.
''',
        'takeaways': 'AI coding tools accelerate boilerplate and test generation; human verification ensures architecture integrity.',
        'interview': 'How do you prevent security leaks and sensitive data exposure when using AI developer tools?',
    },
    {
        'order': 4,
        'title': 'Chapter 4: Retrieval-Augmented Generation (RAG) & Agentic AI Architecture',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'Vector databases (Pinecone, ChromaDB), embeddings, semantic search, RAG pipelines, and autonomous AI agents.',
        'content': '''# Chapter 4: Enterprise RAG & Vector Search

## 1. The RAG Pipeline Architecture
```
[ User Query ]
      │
      ▼
[ Embedding Model ] ──► Converts query into vector floats
      │
      ▼
[ Vector Database ] ──► Performs cosine similarity search against company docs
      │
      ▼
[ Augmented Prompt ] (Query + Relevant Retrieved Document Chunks)
      │
      ▼
[ LLM ] ──► Generates accurate, grounded answer with zero hallucinations!
```
''',
        'takeaways': 'RAG grounds LLM generation in private company data without requiring expensive model fine-tuning.',
        'interview': 'Explain the difference between Fine-Tuning an LLM and building a RAG architecture.',
    }
]

DIGITAL_MARKETING_CHAPTERS = [
    {
        'order': 1,
        'title': 'Chapter 1: Modern Digital Marketing Architecture & The Conversion Funnel',
        'is_preview': True,
        'read_time_mins': 25,
        'summary': 'TOFU, MOFU, BOFU funnels, Customer Acquisition Cost (CAC), Lifetime Value (LTV), and multi-channel attribution.',
        'content': '''# Chapter 1: The Modern Digital Marketing Growth Blueprint

## 1. The Full-Funnel Growth Framework
```
[ Top of Funnel (TOFU) - Awareness ]
  └── Channels: SEO, Viral Reels, YouTube, Organic Content
         │
         ▼
[ Middle of Funnel (MOFU) - Consideration ]
  └── Channels: Free Previews, Email Newsletters, Case Studies, Retargeting
         │
         ▼
[ Bottom of Funnel (BOFU) - Conversion ]
  └── Channels: Discount Coupons, High-Converting Landing Pages, Checkout Urgency
```

## 2. Core Financial Metrics Every Marketer Must Master
- **CAC (Customer Acquisition Cost)**: Total Ad Spend / Total Customers Acquired
- **ROAS (Return on Ad Spend)**: Revenue Generated / Ad Spend (e.g. 4.5x ROAS)
- **LTV:CAC Ratio**: Target healthy business benchmark is **3:1 or higher**.
''',
        'takeaways': 'Sustainable digital marketing balances organic SEO (long-term equity) with paid ad funnels (immediate volume).',
        'interview': 'What is a good LTV to CAC ratio for a SaaS or EdTech platform and why?',
    },
    {
        'order': 2,
        'title': 'Chapter 2: Search Engine Optimization (SEO) Masterclass (Technical, On-Page & Off-Page)',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'Keyword intent, Core Web Vitals, schema markup, backlink authority, title tags, and search indexing.',
        'content': '''# Chapter 2: Comprehensive SEO Playbook

## 1. The 3 Pillars of Search Engine Ranking
1. **Technical SEO**: Fast page loads, mobile responsiveness, XML sitemaps, clean canonical tags, and structured JSON-LD data.
2. **On-Page SEO**: Search intent matching, descriptive H1/H2 headings, internal linking, and keyword density.
3. **Off-Page Authority**: Natural editorial backlinks, brand mentions, and domain authority.
''',
        'takeaways': 'Match user search intent (Informational, Commercial, Transactional) to rank in top Google search results.',
        'interview': 'What are Google Core Web Vitals (LCP, FID/INP, CLS) and how do they impact SEO rankings?',
    },
    {
        'order': 3,
        'title': 'Chapter 3: Paid Performance Advertising (Google Ads, Meta Funnels & Retargeting)',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'Google Search & PMax campaigns, Meta Ads Manager, pixel tracking, lookalike audiences, and ad creative optimization.',
        'content': '''# Chapter 3: High-ROI Paid Advertising

## 1. High-Converting Meta Ad Creative Structure
- **Hook (0-3s)**: Stop the scroll with a bold statement or compelling question.
- **Problem Formulation**: Highlight the pain point (e.g. "Struggling to find clean Python notes for technical interviews?").
- **Solution / Value Proposition**: Introduce TECHSPIRE notes with specific highlights.
- **Call to Action (CTA)**: Direct instruction ("Download Free Sample Chapter Now").
''',
        'takeaways': 'Retargeting website visitors who visited checkout has the highest conversion rate and ROAS in paid ads.',
        'interview': 'Explain the difference between Cost-per-Click (CPC) and Cost-per-Thousand-Impressions (CPM).',
    }
]

BASIC_COMPUTER_CHAPTERS = [
    {
        'order': 1,
        'title': 'Chapter 1: Computer Hardware, Architecture, CPU, RAM & Storage Essentials',
        'is_preview': True,
        'read_time_mins': 20,
        'summary': 'How computers work: CPU clock cycles, RAM vs SSD/HDD, motherboard buses, input/output peripherals, and power delivery.',
        'content': '''# Chapter 1: Computer Hardware & Von Neumann Architecture

## 1. The 4 Essential Hardware Components
```
┌─────────────────────────────────────────────────────────────┐
│                       Motherboard                           │
│  ┌─────────────────┐       ┌─────────────────┐              │
│  │   CPU (Brain)   │◄─────►│  RAM (Fast Mem) │              │
│  │ (ALU + Control) │       │   (Volatile)    │              │
│  └────────┬────────┘       └─────────────────┘              │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────────────────┐                            │
│  │  SSD / Storage (Non-Volatile│                            │
│  │  Files, OS, Permanent Data) │                            │
│  └─────────────────────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

## 2. Volatile RAM vs Non-Volatile Storage
- **RAM (Random Access Memory)**: Ultra-fast temporary memory for currently open apps. Data is erased when the computer powers down.
- **SSD / HDD**: Permanent storage for Windows, installed programs, and files. Retains data permanently with no power.
''',
        'takeaways': 'CPU processes instructions; RAM holds active application data; SSD stores permanent files.',
        'interview': 'What is the difference between volatile and non-volatile computer memory?',
    },
    {
        'order': 2,
        'title': 'Chapter 2: Operating Systems, Windows Management, CLI & Keyboard Shortcuts',
        'is_preview': False,
        'read_time_mins': 25,
        'summary': 'Windows Task Manager, disk partitioning, file explorer shortcuts, PowerShell/Command Prompt basics, and process management.',
        'content': '''# Chapter 2: Windows OS Mastery & Productivity Shortcuts

## 1. High-Speed Windows Productivity Shortcuts
- `Win + D`: Minimize all windows and show desktop immediately.
- `Win + Shift + S`: Open Snipping Tool for custom area screenshots.
- `Ctrl + Shift + Esc`: Launch Task Manager directly.
- `Win + E`: Launch File Explorer.
- `Alt + Tab`: Switch between active applications.
''',
        'takeaways': 'Keyboard shortcuts and proper folder hierarchy save hours of manual navigation weekly.',
        'interview': 'What is an Operating System kernel and what is its primary responsibility?',
    },
    {
        'order': 3,
        'title': 'Chapter 3: Internet, Cloud Storage, Cybersecurity & Phishing Defense',
        'is_preview': False,
        'read_time_mins': 25,
        'summary': 'How the Internet works, browsers, cookies, password managers, two-factor authentication (2FA), and avoiding phishing scams.',
        'content': '''# Chapter 3: Internet Essentials & Cyber Hygiene

## 1. The 5 Rules of Personal Cyber Safety
1. **Never reuse passwords**: Use an encrypted password manager.
2. **Enable 2-Factor Authentication (2FA)**: Prefer authenticator apps over SMS.
3. **Inspect URL Domains**: Watch for typosquatting (`paypa1.com` instead of `paypal.com`).
4. **Never open unexpected email attachments**: Suspicious `.exe`, `.scr`, or `.zip` files.
5. **Keep Operating System & Antivirus Updated**: Apply security patches promptly.
''',
        'takeaways': 'Two-factor authentication and vigilant domain inspection prevent 99% of common cyber credential thefts.',
        'interview': 'What is Phishing and how do you identify a malicious email or link?',
    }
]

MS_OFFICE_CHAPTERS = [
    {
        'order': 1,
        'title': 'Chapter 1: Microsoft Word Complete Professional Guide',
        'is_preview': True,
        'read_time_mins': 25,
        'summary': 'Document styling, heading hierarchies, table of contents automation, headers/footers, mail merge, and export.',
        'content': '''# Chapter 1: Microsoft Word Professional Document Design

## 1. Automated Document Hierarchy & Table of Contents
1. Apply **Heading 1**, **Heading 2**, and **Heading 3** styles consistently across chapters.
2. Go to **References** tab -> **Table of Contents** -> Click **Automatic Table 1**.
3. Word will generate and maintain page numbers automatically!
''',
        'takeaways': 'Always use Word Styles (Heading 1/2) rather than manual font resizing to enable automatic Table of Contents.',
        'interview': 'What is Mail Merge in Microsoft Word and how is it used in business communications?',
    },
    {
        'order': 2,
        'title': 'Chapter 2: Microsoft Excel Mastery (Formulas, XLOOKUP, Pivot Tables & Dashboards)',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'SUMIFS, COUNTIFS, XLOOKUP vs VLOOKUP, INDEX/MATCH, Pivot Tables, slicers, conditional formatting, and KPI charts.',
        'content': '''# Chapter 2: Microsoft Excel Professional Mastery

## 1. The Power of `XLOOKUP` (Modern Replacement for VLOOKUP)
```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode])

-- Example: Find student name from ID
=XLOOKUP(A2, Students!A:A, Students!B:B, "Student Not Found")
```

### Why XLOOKUP Beats VLOOKUP:
- Looks both left and right (VLOOKUP only searches to the right).
- Defaults to exact match (no need for `, FALSE`).
- Immune to column insertion or deletion errors.
''',
        'takeaways': 'XLOOKUP and Pivot Tables with Slicers form the backbone of modern executive business reporting in Excel.',
        'interview': 'What are the key advantages of XLOOKUP over traditional VLOOKUP?',
    },
    {
        'order': 3,
        'title': 'Chapter 3: Microsoft PowerPoint Executive Presentation Design',
        'is_preview': False,
        'read_time_mins': 25,
        'summary': 'Slide layouts, color harmony, typography, SmartArt, charting, transition subtlety, and executive storytelling.',
        'content': '''# Chapter 3: Executive PowerPoint Presentation Design

## 1. The 6x6 Rule of Professional Slides
- No more than **6 bullet points** per slide.
- No more than **6 words** per bullet point.
- Use high-contrast color palettes (Dark Navy `#0F172A` with Gold accents `#D97706`).
- Emphasize key takeaways with callout boxes and clean chart graphics.
''',
        'takeaways': 'Less is more on presentation slides; let charts and concise takeaways drive the executive narrative.',
        'interview': 'How do you structure a corporate slide deck to communicate complex technical data to non-technical executives?',
    }
]
