# Startup Performance Dashboard

## Overview
The **Startup Performance Dashboard** is a data-driven analytics tool designed to evaluate and visualize the **financial and operational health of early-stage startups**. Built using **Python and Streamlit**, it enables investors, analysts, and venture capital professionals to quickly interpret key metrics and identify **high-performing companies or potential risks**.

This project analyzes the **impact of government incentives and policy changes promoting Electric Vehicle (EV) adoption in India** on startup performance. Startups are categorized as **benefited**, **negatively impacted**, or **neutral**, translating raw financial and customer data into **actionable, VC-style insights**.

## Key Features

### Visual Financial Analysis
- Compare **monthly revenues and expenses** across startups
- Identify profitability and cost-structure trends

### KPI Tracking
- Annual Recurring Revenue (**ARR**)
- Customer Acquisition Cost (**CAC**)
- Lifetime Value (**LTV**)
- Burn Rate

### EV Policy Impact Segmentation
- Categorizes startups based on EV policy impact:
  - Benefited
  - Negatively impacted
  - Neutral

### Interactive Filtering
- Dynamically filter startups and metrics
- Compare cohorts across performance dimensions

### Data-Driven Insights
- Automatically generated insights highlighting efficiency and risk signals



## Tech Stack
- **Language:** Python  
- **Framework:** Streamlit  
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn  
- **Data Source:** Custom CSV dataset (25 Indian startups with EV impact metrics)



## Installation & Setup

1. Clone the Repository
git clone https://github.com/akxhayx/Startup-Performance-Dashboard.git
cd Startup-Performance-Dashboard

2. Create a Virtual Environment
python -m venv venv

3. Activate the Virtual Environment
venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

5. Run the Application
streamlit run dashboard.py


## Insights Generated
- Identification of EV-aligned startups benefiting from government incentives
- Detection of startups negatively impacted by EV adoption
- Comparison of efficient vs inefficient startups using revenue, expense, and customer metrics
- Signals relevant to early-stage VC decision-making

## Potential Extensions
- Integrate live startup data APIs (Crunchbase, Tracxn, PitchBook)
- Add predictive modeling for EV adoption scenarios
- Enable user-uploaded datasets
- Extend analysis to other policy-driven sectors (AI, Climate Tech, FinTech)


## Author
Akshaye Aaron Azariah
|Computer Science Undergraduate
|Aspiring VC & Data-Driven Strategist
