# SkillNova — AI-Powered Skill Gap Analyzer

**Analyze your skills. Discover your gaps. Build your career roadmap.**

SkillNova is an AI-powered web application that analyzes a candidate's resume against a target job description, identifies matching and missing skills, calculates a skill coverage score, and recommends personalized learning resources. It also generates an AI-assisted learning plan, stores analysis history in MySQL, and allows users to download a PDF career analysis report.

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Dataset and Knowledge Sources](#dataset-and-knowledge-sources)
- [Installation and Setup](#installation-and-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [Application Workflow](#application-workflow)
- [Skill Coverage Calculation](#skill-coverage-calculation)
- [Database Design](#database-design)
- [PDF Report Generation](#pdf-report-generation)
- [Testing](#testing)
- [Security Considerations](#security-considerations)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

## Project Overview

Finding the right job requires more than submitting a resume. Candidates need to understand whether their existing skills align with a job's requirements and which skills they should develop next.

SkillNova addresses this challenge by comparing resume information with job requirements and presenting the results through an interactive dashboard.

The system identifies existing skills, highlights missing skills, calculates skill coverage, recommends learning resources, and generates a personalized learning roadmap. Users can also review previous analyses and download reports for future reference.

## Problem Statement

Job seekers often struggle to identify the gap between their current skills and the skills expected by employers. Manually comparing resumes with job descriptions can be time-consuming and may overlook important technical or professional skills.

SkillNova provides an automated approach to skill-gap identification and personalized learning recommendations, helping users make more informed career-development decisions.

## Objectives

- Extract and analyze information from uploaded resumes.
- Compare candidate skills with target job requirements.
- Identify matched skills and missing skills.
- Calculate a skill coverage percentage.
- Prioritize skill-development recommendations.
- Generate an AI-assisted learning plan.
- Store analysis records in a MySQL database.
- Provide downloadable PDF career analysis reports.
- Support data exploration and preprocessing through Jupyter notebooks.

## Key Features

### 1. Resume Upload and Analysis

- Upload resumes in PDF, DOCX, or TXT format.
- Extract resume text for analysis.
- Enter a target job title and job description.
- Process the submitted information through the skill-analysis engine.

### 2. Skill-Gap Identification

- Identify skills found in the resume.
- Compare candidate skills with required skills.
- Display matched and missing skills.
- Calculate a skill coverage score.
- Provide a clearer view of areas that need improvement.

### 3. Personalized Learning Recommendations

- Recommend resources for missing skills.
- Prioritize skills for further learning.
- Display resource links when available.
- Present an AI-assisted learning roadmap with learning activities and project suggestions when generated successfully.

### 4. AI-Assisted Learning Plan

SkillNova integrates with Google's Gemini API to generate a personalized learning plan. If AI generation is unavailable, the application can use its fallback plan instead.

AI-generated suggestions should be reviewed before being used for important career decisions.

### 5. Interactive Results Dashboard

- Display the skill coverage percentage.
- Visualize skill-matching results using charts.
- Present matched and missing skills.
- Show prioritized recommendations.
- Display the generated learning roadmap.

### 6. PDF Career Analysis Report

Generate a downloadable PDF containing the analysis results and relevant recommendations.

### 7. Analysis History

- Store analysis records in MySQL.
- View previous analyses.
- Review saved skill matches and coverage scores.
- Search or filter history where supported by the interface.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming language | Python |
| Web framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| Data visualization | Chart.js |
| Database | MySQL |
| Database connectivity | Python MySQL connector used by the project |
| Resume parsing | pypdf, python-docx |
| AI integration | Google Gemini API using `google-genai` |
| PDF generation | ReportLab |
| Data processing | Pandas, NumPy |
| Machine learning and analysis | Scikit-learn, where used in the analysis pipeline |
| Development tools | VS Code, Jupyter Notebook, Git, GitHub |
| Configuration | python-dotenv |

## System Architecture

```text
                USER
                  |
                  v
       Flask Web Application
                  |
                  v
         Resume and Job Input
                  |
                  v
           Resume Parsing
          PDF / DOCX / TXT
                  |
                  v
          Skill Analysis Engine
                  |
                  v
       Skill Matching and Gap Analysis
                  |
          +-------+-------+
          |               |
          v               v
   Recommendations    Coverage Score
          |               |
          +-------+-------+
                  |
                  v
       AI-Assisted Learning Plan
          Gemini API / Fallback
                  |
                  v
          Results Dashboard
                  |
          +-------+-------+
          |               |
          v               v
    MySQL History      PDF Report
```

The Jupyter notebooks support data exploration, preprocessing, skill extraction, and skill-gap analysis during development.

## Project Structure

The following structure represents the main application files and the data and notebook components used in development. Keep the actual paths and filenames aligned with your repository.

```text
skill-gap-analyzer/
│
├── app.py
├── skill_engine.py
├── llm_engine.py
├── pdf_report.py
├── db.py
├── test_db.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env                    # Local only; do not commit
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── history.html
│
├── static/
│   └── css/
│       └── style.css
│
├── data/
│   ├── resumes/
│   ├── job_postings/
│   ├── onet/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_skill_extraction.ipynb
│   └── 04_skill_gap_analysis.ipynb
│
└── reports/
    └── generated analysis charts
```

**Note:** Your current notebook files may be in the project root rather than a `notebooks/` directory. Do not move files just to match this illustrative tree; update the README structure to reflect the final repository.

## Dataset and Knowledge Sources

The development workflow uses resume data, job-posting data, and occupational skill information.

| Data source | Purpose |
|---|---|
| Resume dataset (`Resume.csv`) | Explore resume text and develop resume-processing workflows |
| Job-posting dataset (`postings.csv`) | Explore job descriptions and employer requirements |
| Job skills dataset (`job_skills.csv`) | Support job-skill analysis |
| O*NET occupation data | Provide occupational information |
| O*NET essential skills | Support analysis of important workplace skills |
| O*NET software skills | Support software-skill analysis |

Processed files include cleaned datasets and skill-enriched resume and job records used during development.

**Dataset notes:**

- The datasets support the development and analysis pipeline; the live application also accepts user-provided resume and job-description inputs.
- Verify the original dataset licenses and attribution requirements before redistributing the datasets.
- Large raw files should generally be stored outside GitHub and documented with download instructions rather than committed to the repository.
- Do not upload real resumes containing personal information without appropriate permission and privacy safeguards.

## Installation and Setup

### Prerequisites

Install the following before starting:

- Python compatible with the project's dependencies.
- MySQL Server.
- Git.
- VS Code or another Python editor.
- A Google Gemini API key if you want to use AI-generated learning plans.

### 1. Clone the repository

Replace `YOUR_GITHUB_USERNAME` with your GitHub username and `YOUR_REPOSITORY_NAME` with the actual repository name.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use a terminal with the appropriate execution policy or activate the environment using your preferred Python terminal.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Ensure `requirements.txt` includes all packages imported by the application, including Flask, pypdf, python-docx, ReportLab, python-dotenv, the Google Gen AI SDK, and the MySQL connector used by `db.py`.

### 4. Configure MySQL

Start MySQL Server and create the application database:

```sql
CREATE DATABASE skill_gap_analyzer;
```

Ensure the `analyses` table is created using the schema expected by `db.py`. If the project does not create the table automatically, run the appropriate table-creation SQL before launching the application.

### 5. Configure environment variables

Create a local `.env` file in the project root. Add your own database credentials and API key:

```dotenv
FLASK_SECRET_KEY=replace_with_a_long_random_secret
GEMINI_API_KEY=your_gemini_api_key

DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=skill_gap_analyzer
```

The variable names for database credentials must match those read by your `db.py` implementation. Likewise, use the Gemini variable name expected by `llm_engine.py`.

Do not share your API key, database password, or Flask secret key publicly.

## Running the Application

From the project root, activate the virtual environment and run:

```powershell
python app.py
```

Open the local address displayed in the terminal, typically:

```text
http://127.0.0.1:5000
```

If the application defines a health endpoint, you can also test:

```text
http://127.0.0.1:5000/health
```

## Application Workflow

1. Open the SkillNova homepage.
2. Upload a resume in a supported file format.
3. Enter the target job title and job description.
4. Submit the form for analysis.
5. Review the extracted or recognized skills.
6. Examine matched skills, missing skills, and coverage.
7. Review recommended learning resources.
8. Review the AI-generated learning plan or fallback plan.
9. Download the PDF career analysis report.
10. Open analysis history to review saved records.

## Skill Coverage Calculation

SkillNova compares the required skills with the skills identified in the candidate's resume.

A typical coverage calculation is:

\[
\text{Skill Coverage} =
\frac{\text{Number of Matched Required Skills}}
{\text{Total Number of Required Skills}}
\times 100
\]

For example, if 8 of 10 required skills match, the coverage is 80%.

The actual result depends on the matching and normalization logic implemented in `skill_engine.py`. A coverage score is an indicator of skill overlap, not a guarantee of employment or job suitability.

## Database Design

The `skill_gap_analyzer` database stores analysis history in an `analyses` table.

The table used by the application includes the following fields:

| Field | Purpose |
|---|---|
| `id` | Unique analysis identifier |
| `resume_filename` | Uploaded resume's filename |
| `target_role` | Job title being analyzed |
| `required_skills` | Required skills stored as JSON |
| `matched_skills` | Matched skills stored as JSON |
| `missing_skills` | Missing skills stored as JSON |
| `coverage_percentage` | Calculated skill coverage |
| `created_at` | Analysis creation timestamp |

The precise column types and constraints should match the SQL schema used by your application.

## PDF Report Generation

The PDF report feature uses ReportLab to create a downloadable career analysis report.

The report can present relevant analysis information, including:

- Target role and analysis summary.
- Skill coverage.
- Matched and missing skills.
- Learning recommendations.
- AI-assisted learning roadmap, when available.

The report is generated through the Flask `/download-report` route. The user should run an analysis before requesting its report.

## Testing

Test the following workflows before publishing the project:

- Homepage and input form load successfully.
- PDF, DOCX, and TXT uploads work as expected.
- Invalid files and oversized uploads are handled safely.
- Skill matching and coverage calculations produce sensible results.
- Missing skills and recommendations are displayed correctly.
- AI learning-plan generation works when the API is available.
- A fallback learning plan is available when AI generation fails.
- MySQL saves and retrieves analysis records.
- The PDF report downloads and contains the correct analysis.
- Analysis history and search/filter controls work.
- Environment variables and error handling are configured correctly.

## Security Considerations

- Never commit `.env`, API keys, passwords, or secret keys.
- Add `.env` and `.venv/` to `.gitignore`.
- Validate uploaded file types and sizes.
- Do not trust uploaded filenames or file contents.
- Use parameterized database queries.
- Use a strong secret key in production.
- Use HTTPS and appropriate authentication and authorization before handling private user data in a public deployment.
- Avoid logging full resumes or other sensitive personal information.
- Review session storage and report-download behavior before production deployment.
- Follow the licenses and usage restrictions of all datasets and external services.

## Future Enhancements

Potential improvements include:

- User registration and secure authentication.
- Candidate profiles and saved career goals.
- More advanced semantic skill matching using embeddings.
- Improved skill normalization and synonym handling.
- Job-role recommendations based on skill profiles.
- Progress tracking across repeated assessments.
- More detailed learning analytics.
- Expanded report customization.
- Automated testing and continuous integration.
- Cloud deployment with secure database hosting.
- Evaluation of skill extraction accuracy and recommendation quality.

## Author

**Developed by:** S. Gayathri

**Project:** SkillNova — AI-Powered Skill Gap Analyzer and Personalized Learning Recommendation System

**GitHub:** [Add your GitHub profile URL]

---

*SkillNova is a career-development support tool. Its recommendations and coverage scores are informational and should not be treated as guarantees of employment or professional qualification.*
