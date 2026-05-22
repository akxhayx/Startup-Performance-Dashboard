import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle

# Page Configuration
st.set_page_config(
    page_title="Startup Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Main styling */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Header styling */
    .header-text {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    
    .subheader-text {
        font-size: 1.1rem;
        color: #666666;
        margin-bottom: 2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #f8f9fa;
        border-left: 4px solid #2E86AB;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .metric-title {
        font-size: 0.875rem;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: #1a1a1a;
    }
    
    .metric-delta-positive {
        color: #28a745;
        font-size: 0.875rem;
    }
    
    .metric-delta-negative {
        color: #dc3545;
        font-size: 0.875rem;
    }
    
    /* Insight boxes */
    .insight-box {
        background-color: #f0f7ff;
        border-left: 4px solid #0066cc;
        padding: 1.25rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .insight-title {
        font-weight: 600;
        color: #0066cc;
        margin-bottom: 0.5rem;
    }
    
    /* Warning box */
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1.25rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    /* Section divider */
    .section-divider {
        border-top: 1px solid #e0e0e0;
        margin: 2rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Remove streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_data(uploaded_file):
    """Load and preprocess the dataset"""
    df = pd.read_csv(uploaded_file)
    
    # Calculate additional metrics
    df['Profitability'] = df['Revenue_Monthly'] - df['Expenses']
    df['Revenue_per_User'] = df['Revenue_Monthly'] / df['Users']
    df['Expense_Ratio'] = df['Expenses'] / df['Revenue_Monthly']
    df['CAC_Payback_Months'] = df['CAC'] / (df['Revenue_Monthly'] / df['Users'])
    df['Growth_Efficiency'] = df['New_Customers_Monthly'] / df['Expenses']
    
    return df

def create_metric_card(title, value, delta=None, prefix="", suffix=""):
    """Create a styled metric card"""
    delta_html = ""
    if delta is not None:
        delta_class = "metric-delta-positive" if delta >= 0 else "metric-delta-negative"
        delta_symbol = "▲" if delta >= 0 else "▼"
        delta_html = f'<div class="{delta_class}">{delta_symbol} {abs(delta):.1f}%</div>'
    
    return f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{prefix}{value:,.0f}{suffix}</div>
            {delta_html}
        </div>
    """

def format_currency(value):
    """Format currency in Indian notation"""
    if value >= 10000000:  # Crores
        return f"₹{value/10000000:.2f}Cr"
    elif value >= 100000:  # Lakhs
        return f"₹{value/100000:.2f}L"
    else:
        return f"₹{value:,.0f}"

def plot_quadrant_analysis(df):
    """Create a strategic quadrant chart (Growth vs Efficiency)"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Calculate metrics for axes
    growth_metric = df['New_Customers_Monthly']
    efficiency_metric = df['LTV'] / df['CAC']
    
    # Calculate medians for quadrant lines
    growth_median = growth_metric.median()
    efficiency_median = efficiency_metric.median()
    
    # Color by impact
    colors = {'Benefited': '#28a745', 'Hurt': '#dc3545', 'Neutral': '#6c757d'}
    
    for impact in df['Impact'].unique():
        mask = df['Impact'] == impact
        ax.scatter(efficiency_metric[mask], growth_metric[mask], 
                  s=df[mask]['Revenue_Monthly']/1000000, 
                  alpha=0.6, 
                  c=colors[impact],
                  label=impact,
                  edgecolors='black',
                  linewidth=0.5)
    
    # Add quadrant lines
    ax.axvline(efficiency_median, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax.axhline(growth_median, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    
    # Add quadrant labels
    ax.text(efficiency_median * 1.5, growth_median * 1.8, 'STARS', 
            fontsize=12, fontweight='bold', color='green', alpha=0.3)
    ax.text(efficiency_median * 0.3, growth_median * 1.8, 'QUESTION MARKS', 
            fontsize=12, fontweight='bold', color='orange', alpha=0.3)
    ax.text(efficiency_median * 1.5, growth_median * 0.2, 'CASH COWS', 
            fontsize=12, fontweight='bold', color='blue', alpha=0.3)
    ax.text(efficiency_median * 0.3, growth_median * 0.2, 'PETS', 
            fontsize=12, fontweight='bold', color='red', alpha=0.3)
    
    ax.set_xlabel('Unit Economics (LTV/CAC Ratio)', fontsize=12, fontweight='600')
    ax.set_ylabel('Growth (New Customers/Month)', fontsize=12, fontweight='600')
    ax.set_title('Strategic Portfolio Analysis', fontsize=14, fontweight='bold', pad=20)
    ax.legend(title='EV Impact', loc='upper right', frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def plot_revenue_distribution(df, filter_impact):
    """Create revenue vs expenses comparison"""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Sort by revenue
    df_sorted = df.sort_values('Revenue_Monthly', ascending=False)
    
    x = np.arange(len(df_sorted))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, df_sorted['Revenue_Monthly']/1000000, width, 
                   label='Revenue', color='#2E86AB', alpha=0.8)
    bars2 = ax.bar(x + width/2, df_sorted['Expenses']/1000000, width, 
                   label='Expenses', color='#A23B72', alpha=0.8)
    
    # Add profitability indicator
    for i, (rev, exp) in enumerate(zip(df_sorted['Revenue_Monthly'], df_sorted['Expenses'])):
        if rev < exp:
            ax.plot([i], [max(rev, exp)/1000000 + 10], 'rv', markersize=8)
    
    ax.set_xticks(x)
    ax.set_xticklabels(df_sorted['Startup'], rotation=45, ha='right')
    ax.set_xlabel('Startup', fontsize=11, fontweight='600')
    ax.set_ylabel('Amount (₹ Million)', fontsize=11, fontweight='600')
    ax.set_title(f'Revenue vs Expenses Analysis - {filter_impact}', 
                fontsize=13, fontweight='bold', pad=15)
    ax.legend(loc='upper right', frameon=True, shadow=True)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig

def plot_efficiency_metrics(df):
    """Create efficiency comparison chart"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # CAC/LTV Ratio
    df_sorted = df.nsmallest(10, 'CAC/LTV Ratio')
    colors_cac = ['#28a745' if x < 0.3 else '#ffc107' if x < 0.5 else '#dc3545' 
                  for x in df_sorted['CAC/LTV Ratio']]
    
    ax1.barh(df_sorted['Startup'], df_sorted['CAC/LTV Ratio'], color=colors_cac, alpha=0.8)
    ax1.axvline(0.33, color='green', linestyle='--', alpha=0.5, label='Healthy (<0.33)')
    ax1.set_xlabel('CAC/LTV Ratio', fontsize=11, fontweight='600')
    ax1.set_title('Unit Economics Efficiency (Top 10)', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='x', alpha=0.3)
    
    # Revenue to Expense Ratio
    df_sorted2 = df.nlargest(10, 'Rev_to_Exp')
    colors_ratio = ['#28a745' if x > 1.5 else '#ffc107' if x > 1.0 else '#dc3545' 
                    for x in df_sorted2['Rev_to_Exp']]
    
    ax2.barh(df_sorted2['Startup'], df_sorted2['Rev_to_Exp'], color=colors_ratio, alpha=0.8)
    ax2.axvline(1.0, color='red', linestyle='--', alpha=0.5, label='Breakeven')
    ax2.axvline(1.5, color='green', linestyle='--', alpha=0.5, label='Profitable')
    ax2.set_xlabel('Revenue/Expense Ratio', fontsize=11, fontweight='600')
    ax2.set_title('Profitability Ratio (Top 10)', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    return fig

def plot_impact_analysis(df):
    """Create EV impact analysis visualization"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Impact distribution pie chart
    impact_counts = df['Impact'].value_counts()
    colors_impact = {'Benefited': '#28a745', 'Hurt': '#dc3545', 'Neutral': '#6c757d'}
    pie_colors = [colors_impact[label] for label in impact_counts.index]
    
    wedges, texts, autotexts = ax1.pie(impact_counts, labels=impact_counts.index, 
                                        autopct='%1.1f%%', colors=pie_colors, 
                                        startangle=90, textprops={'fontsize': 11})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax1.set_title('EV Policy Impact Distribution', fontsize=12, fontweight='bold')
    
    # Revenue comparison by impact
    impact_revenue = df.groupby('Impact')['Revenue_Monthly'].mean() / 1000000
    bars = ax2.bar(impact_revenue.index, impact_revenue.values, 
                   color=[colors_impact[x] for x in impact_revenue.index], alpha=0.8)
    ax2.set_ylabel('Average Monthly Revenue (₹ Million)', fontsize=11, fontweight='600')
    ax2.set_title('Average Revenue by Impact Category', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{height:.1f}M',
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    return fig

def generate_insights(df, filter_impact):
    """Generate automated insights based on data analysis"""
    insights = []
    
    # Portfolio-level insights
    total_startups = len(df)
    profitable = len(df[df['Profitability'] > 0])
    avg_ltv_cac = df['LTV'].sum() / df['CAC'].sum()
    
    insights.append({
        'type': 'portfolio',
        'title': 'Portfolio Overview',
        'text': f"Analyzing {total_startups} startups. {profitable} ({profitable/total_startups*100:.1f}%) are currently profitable. Average portfolio LTV/CAC ratio: {avg_ltv_cac:.2f}x"
    })
    
    # EV Impact insights
    benefited = df[df['Impact'] == 'Benefited']
    if len(benefited) > 0:
        avg_benefit_growth = benefited['New_Customers_Monthly'].mean()
        insights.append({
            'type': 'success',
            'title': 'EV Policy Winners',
            'text': f"{len(benefited)} startups are benefiting from EV policies with average monthly customer acquisition of {avg_benefit_growth:,.0f} users."
        })
    
    # Efficiency leaders
    efficient = df.nsmallest(3, 'CAC/LTV Ratio')
    insights.append({
        'type': 'success',
        'title': 'Efficiency Leaders',
        'text': f"Top performers: {', '.join(efficient['Startup'].tolist())} with exceptional unit economics (CAC/LTV < {efficient['CAC/LTV Ratio'].max():.2f})"
    })
    
    # Risk signals
    high_burn = df[df['Burn Rate'] < -50000000]
    if len(high_burn) > 0:
        insights.append({
            'type': 'warning',
            'title': '⚠️ High Burn Alert',
            'text': f"{len(high_burn)} startups burning >₹50Cr/month. Runway monitoring recommended for: {', '.join(high_burn.nsmallest(3, 'Burn Rate')['Startup'].tolist())}"
        })
    
    # Growth opportunities
    question_marks = df[(df['New_Customers_Monthly'] > df['New_Customers_Monthly'].median()) & 
                       (df['CAC/LTV Ratio'] > 0.5)]
    if len(question_marks) > 0:
        insights.append({
            'type': 'info',
            'title': 'Growth Stage Investments',
            'text': f"{len(question_marks)} startups showing strong growth but need unit economics optimization. Consider operational support for scaling."
        })
    
    return insights

# ===========================
# MAIN APPLICATION
# ===========================

def main():
    # Header
    st.markdown('<p class="header-text">Startup Performance Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="subheader-text">VC-Grade Analytics for EV Policy Impact Assessment</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/bar-chart.png", width=80)
        st.markdown("### Dashboard Controls")
        
        uploaded_file = st.file_uploader("Upload Dataset (CSV)", type=["csv"])
        
        st.markdown("---")
        st.markdown("### Filters")
        
        if uploaded_file is not None:
            df = load_data(uploaded_file)
            
            # Impact filter
            impact_options = ['All'] + sorted(df['Impact'].unique().tolist())
            filter_impact = st.selectbox("EV Policy Impact", impact_options)
            
            # Metric threshold filters
            st.markdown("##### Metric Thresholds")
            min_revenue = st.slider("Min Monthly Revenue (₹Cr)", 0, 100, 0)
            max_cac_ltv = st.slider("Max CAC/LTV Ratio", 0.0, 2.0, 2.0, 0.1)
            
            # Apply filters
            df_filtered = df.copy()
            if filter_impact != 'All':
                df_filtered = df_filtered[df_filtered['Impact'] == filter_impact]
            df_filtered = df_filtered[df_filtered['Revenue_Monthly'] >= min_revenue * 10000000]
            df_filtered = df_filtered[df_filtered['CAC/LTV Ratio'] <= max_cac_ltv]
            
            st.markdown("---")
            st.markdown(f"**{len(df_filtered)}** startups match filters")
            
            # Export option
            st.markdown("### Export Data")
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                label="Download Filtered Data",
                data=csv,
                file_name="filtered_startups.csv",
                mime="text/csv"
            )
        
        st.markdown("---")
        st.markdown("##### About")
        st.markdown("Built with Streamlit • Python • Pandas")
        st.markdown("*Data-driven insights for venture capital*")
    
    # Main content
    if uploaded_file is None:
        st.info("👆 Upload a CSV file to begin analysis")
        
        # Sample data structure
        with st.expander("📋 Required Data Format"):
            st.markdown("""
            Your CSV should include these columns:
            - `Startup`: Company name
            - `Revenue_Monthly`: Monthly revenue (₹)
            - `Users`: Total users
            - `New_Customers_Monthly`: Monthly new customers
            - `CAC`: Customer acquisition cost
            - `Expenses`: Monthly expenses
            - `ARR`: Annual recurring revenue
            - `LTV`: Lifetime value
            - `Burn Rate`: Monthly burn rate
            - `Impact`: EV policy impact (Benefited/Hurt/Neutral)
            """)
        
        return
    
    # Load and display data
    df = load_data(uploaded_file)
    df_filtered = df.copy()
    
    # Apply filters
    if filter_impact != 'All':
        df_filtered = df_filtered[df_filtered['Impact'] == filter_impact]
    df_filtered = df_filtered[df_filtered['Revenue_Monthly'] >= min_revenue * 10000000]
    df_filtered = df_filtered[df_filtered['CAC/LTV Ratio'] <= max_cac_ltv]
    
    # Key Metrics Row
    st.markdown("### Portfolio Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df_filtered['Revenue_Monthly'].sum()
        st.markdown(create_metric_card("Total Monthly Revenue", total_revenue, 
                                      prefix="₹", suffix=""), unsafe_allow_html=True)
    
    with col2:
        avg_ltv_cac = (df_filtered['LTV'].sum() / df_filtered['CAC'].sum())
        health_delta = ((avg_ltv_cac - 3) / 3) * 100 if avg_ltv_cac > 0 else 0
        st.markdown(create_metric_card("Avg LTV/CAC Ratio", avg_ltv_cac, 
                                      delta=health_delta, suffix="x"), unsafe_allow_html=True)
    
    with col3:
        total_customers = df_filtered['New_Customers_Monthly'].sum()
        st.markdown(create_metric_card("Monthly New Customers", total_customers), 
                   unsafe_allow_html=True)
    
    with col4:
        avg_burn = abs(df_filtered['Burn Rate'].mean())
        st.markdown(create_metric_card("Avg Monthly Burn", avg_burn, prefix="₹"), 
                   unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Insights Section
    st.markdown("### Key Insights")
    insights = generate_insights(df_filtered, filter_impact)
    
    for insight in insights:
        if insight['type'] == 'warning':
            st.markdown(f"""
                <div class="warning-box">
                    <div class="insight-title">{insight['title']}</div>
                    <div>{insight['text']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="insight-box">
                    <div class="insight-title">{insight['title']}</div>
                    <div>{insight['text']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Visualizations
    st.markdown("### Strategic Analysis")
    
    # Quadrant Analysis
    st.pyplot(plot_quadrant_analysis(df_filtered))
    st.caption("Bubble size represents monthly revenue. Stars (high growth + efficiency) are prime investment targets.")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Revenue Analysis
    st.markdown("### Financial Performance")
    st.pyplot(plot_revenue_distribution(df_filtered, filter_impact))
    st.caption("Red triangles (▼) indicate startups with expenses exceeding revenue.")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Efficiency Metrics
    st.markdown("### Efficiency Benchmarks")
    st.pyplot(plot_efficiency_metrics(df_filtered))
    st.caption("Healthy CAC/LTV ratios are below 0.33 (green zone). Revenue/Expense ratios above 1.5 indicate strong profitability.")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # EV Impact Analysis
    st.markdown("### EV Policy Impact Assessment")
    st.pyplot(plot_impact_analysis(df_filtered))
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Detailed Data Table
    with st.expander("📊 View Detailed Data Table"):
        # Select key columns for display
        display_cols = ['Startup', 'Revenue_Monthly', 'Expenses', 'Profitability', 
                       'Users', 'CAC', 'LTV', 'CAC/LTV Ratio', 'Impact']
        
        df_display = df_filtered[display_cols].copy()
        df_display['Revenue_Monthly'] = df_display['Revenue_Monthly'].apply(format_currency)
        df_display['Expenses'] = df_display['Expenses'].apply(format_currency)
        df_display['Profitability'] = df_display['Profitability'].apply(format_currency)
        df_display['CAC'] = df_display['CAC'].apply(lambda x: f"₹{x:,.0f}")
        df_display['LTV'] = df_display['LTV'].apply(lambda x: f"₹{x:,.0f}")
        df_display['CAC/LTV Ratio'] = df_display['CAC/LTV Ratio'].apply(lambda x: f"{x:.3f}")
        
        st.dataframe(df_display, use_container_width=True, height=400)
    
    # Comparison Tool
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Startup Comparison Tool")
    
    col1, col2 = st.columns(2)
    with col1:
        startup1 = st.selectbox("Select First Startup", df_filtered['Startup'].tolist(), key='s1')
    with col2:
        startup2 = st.selectbox("Select Second Startup", 
                               [s for s in df_filtered['Startup'].tolist() if s != startup1], key='s2')
    
    if startup1 and startup2:
        comp_cols = st.columns(2)
        
        for idx, startup in enumerate([startup1, startup2]):
            with comp_cols[idx]:
                data = df_filtered[df_filtered['Startup'] == startup].iloc[0]
                
                st.markdown(f"#### {startup}")
                st.markdown(f"**Impact:** {data['Impact']}")
                st.markdown(f"**Revenue:** {format_currency(data['Revenue_Monthly'])}/mo")
                st.markdown(f"**Expenses:** {format_currency(data['Expenses'])}/mo")
                st.markdown(f"**Profitability:** {format_currency(data['Profitability'])}/mo")
                st.markdown(f"**CAC/LTV:** {data['CAC/LTV Ratio']:.3f}")
                st.markdown(f"**Users:** {data['Users']:,.0f}")
                st.markdown(f"**New Customers:** {data['New_Customers_Monthly']:,.0f}/mo")

if __name__ == "__main__":
    main()