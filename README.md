Startup Performance Dashboard
Overview

The Startup Performance Dashboard is a data-driven analytics tool designed to evaluate and visualize the financial and operational health of early-stage startups. It enables investors, analysts, and venture capital professionals to quickly interpret key metrics and identify high-performing companies or potential risks through an interactive dashboard built with Streamlit and Python.

This project specifically analyzes the impact of government incentives and policy changes promoting electric vehicle (EV) adoption in India on startup performance. The dashboard identifies which startups in the ecosystem benefited, were hurt, or remained neutral due to this trend, transforming raw startup data (revenue, expenses, customer metrics) into actionable insights reflecting real-world VC decision-making.

Features

Visual Financial Analysis: Compare monthly revenues and expenses across startups.

KPI Tracking: Evaluate key metrics such as ARR, CAC, LTV, and burn rate.

Impact Segmentation: Categorize startups based on whether they benefited, were hurt, or remained neutral due to the EV mobility trend.

Interactive Filtering: Adjust displayed startups or metrics dynamically.

Data-Driven Insights: Automatically generate observations to help assess startup performance and efficiency.

Tech Stack

Language: Python

Framework: Streamlit

Libraries: Pandas, Matplotlib, Seaborn, NumPy

Data Source: Custom CSV dataset (25 Indian startups with key metrics and EV trend impact)

Installation

Clone the repository:

git clone https://github.com/<your-username>/Startup-Performance-Dashboard.git
cd Startup-Performance-Dashboard


Create a virtual environment and activate it:

python -m venv venv
venv\Scripts\activate  # Windows


Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run dashboard.py

Files Included

dashboard.py — Main Streamlit application file

startups_data.csv — Dataset containing startup metrics and EV mobility trend impact

README.md — Documentation and usage guide

Insights Generated

The dashboard produces insights such as:

EV-related startups benefiting from government policies (e.g., EV manufacturers, battery and charging tech companies).

Startups negatively impacted (e.g., ICE vehicle suppliers, traditional fuel-based services).

Efficient vs. inefficient startups based on revenue, expenses, and customer acquisition metrics.

Potential Extensions

Integrate live data from startup funding APIs (e.g., Crunchbase, Tracxn).

Predictive modeling to forecast startup growth under EV adoption scenarios.

User-upload functionality for custom datasets.

Author

Akshaye Aaron
Computer Science Undergraduate | Aspiring VC Analyst & Data-Driven Strategist