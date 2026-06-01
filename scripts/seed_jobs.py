import sqlite3
from config import JOBS_DB

conn = sqlite3.connect(JOBS_DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    company      TEXT NOT NULL,
    role         TEXT NOT NULL,
    status       TEXT NOT NULL,
    applied_date TEXT,
    source       TEXT,
    notes        TEXT
)
""")

jobs = [
    ("Internet Brands",  "Associate AI Research and Operations Analyst", "active",    "2025-04-15", "LinkedIn",   "Completed 2nd round with Morgan Rollins"),
    ("KBR",              "Junior Software Engineer",                      "submitted", "2025-04-20", "USAJobs",    "Defense/national security — closest to actual interests"),
    ("DISA",             "IT Specialist",                                 "submitted", "2025-04-18", "USAJobs",    "Federal — drafted essays using capstone + law office experience"),
    ("Schlossberg & Umholtz", "IT Intern (current)",                     "active",    "2024-09-01", "Direct",     "Part-time, document engineering focus"),
    ("LA Tech Rising",   "Project Co-Lead (current)",                    "active",    "2024-09-01", "Program",    "Retail Intelligence Dashboard, Python/Streamlit, with Mira Bhakta"),
    ("Northrop Grumman", "Software Engineer",                             "rejected",  "2025-03-10", "LinkedIn",   None),
    ("Raytheon",         "Associate Systems Engineer",                    "rejected",  "2025-03-22", "Indeed",     None),
    ("Palantir",         "Forward Deployed Engineer",                     "submitted", "2025-04-25", "Direct",     "Stretch role"),
    ("Leidos",           "Junior Software Developer",                     "submitted", "2025-04-12", "LinkedIn",   None),
    ("SAIC",             "Software Engineer I",                           "submitted", "2025-04-08", "Indeed",     None),
    ("Booz Allen Hamilton", "Junior Data Scientist",                      "submitted", "2025-04-05", "LinkedIn",   None),
    ("L3Harris",         "Associate Software Engineer",                   "submitted", "2025-04-02", "LinkedIn",   None),
    ("General Dynamics", "Software Developer",                            "submitted", "2025-03-30", "Company site", None),
    ("Lockheed Martin",  "Software Engineer Asc",                        "submitted", "2025-03-28", "LinkedIn",   None),
    ("Boeing",           "Associate Software Engineer",                   "submitted", "2025-03-25", "Company site", None),
    ("Accenture Federal","IT Analyst",                                    "rejected",  "2025-03-15", "LinkedIn",   None),
    ("Deloitte",         "Technology Analyst",                            "submitted", "2025-04-30", "LinkedIn",   None),
    ("MITRE",            "Junior Systems Engineer",                       "submitted", "2025-04-28", "Direct",     None),
    ("Peraton",          "Software Engineer",                             "submitted", "2025-04-22", "Indeed",     None),
    ("ManTech",          "Junior Developer",                              "submitted", "2025-04-10", "LinkedIn",   None),
    ("Parsons",          "Associate Engineer",                            "submitted", "2025-04-03", "LinkedIn",   None),
    ("Jacobs",           "Technology Associate",                          "submitted", "2025-03-20", "Indeed",     None),
    ("Guidehouse",       "Technology Consultant",                         "submitted", "2025-04-27", "LinkedIn",   None),
]

cur.executemany("""
INSERT INTO applications (company, role, status, applied_date, source, notes)
VALUES (?, ?, ?, ?, ?, ?)
""", jobs)

conn.commit()
conn.close()
print(f"Seeded {len(jobs)} job applications to {JOBS_DB}")
