import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from data_pipeline import process_data

# Set style
plt.style.use('dark_background')
sns.set_palette("husl")

# Page Configuration
st.set_page_config(
    page_title="Global AI Adoption & Workforce Displacement Index",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown("""
    <style>
    .main {
        background-color: #0F172A;
    }
    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #475569;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 13px;
        color: #94A3B8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 8px;
    }
    .metric-delta {
        font-size: 12px;
        margin-top: 4px;
    }
    .positive { color: #10B981; }
    .negative { color: #EF4444; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 10px 20px;
        color: #94A3B8;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3B82F6;
        color: white;
    }
    h1, h2, h3 {
        color: #F8FAFC;
    }
    .stSelectbox, .stMultiSelect {
        background-color: #1E293B;
    }
    </style>
""", unsafe_allow_html=True)

# Load and cache data
@st.cache_data
def load_dashboard_data():
    df, country_agg, industry_agg, skill_agg, time_agg, kpi = process_data()
    return df, country_agg, industry_agg, skill_agg, time_agg

df, country_agg, industry_agg, skill_agg, time_agg = load_dashboard_data()

# Sidebar Filters
st.sidebar.title("Framework Filters")

# Reset Filters Button
if st.sidebar.button("Reset All Filters"):
    st.session_state.clear()
    st.rerun()

# Development Tier Filter
selected_tiers = st.sidebar.multiselect(
    "Development Tier",
    options=df['development_tier'].unique(),
    default=df['development_tier'].unique()
)

# Region Filter
selected_regions = st.sidebar.multiselect(
    "Region",
    options=df['region'].unique(),
    default=df['region'].unique()
)

# Industry Sector Filter
selected_sectors = st.sidebar.multiselect(
    "Industry Sector",
    options=df['industry_sector'].unique(),
    default=df['industry_sector'].unique()
)

# Era Filter
selected_eras = st.sidebar.multiselect(
    "Time Period",
    options=df['era'].unique(),
    default=df['era'].unique()
)

# Risk Category Filter
selected_risks = st.sidebar.multiselect(
    "Risk Category",
    options=df['risk_category'].unique(),
    default=df['risk_category'].unique()
)

# Apply filters
filtered_df = df[
    df['development_tier'].isin(selected_tiers) &
    df['region'].isin(selected_regions) &
    df['industry_sector'].isin(selected_sectors) &
    df['era'].isin(selected_eras) &
    df['risk_category'].isin(selected_risks)
]

# Title
st.title("Global AI Adoption & Workforce Displacement Monitor")
st.markdown("---")

# KPI Cards
def render_kpi_card(title, value, delta=None, delta_positive=True):
    delta_html = ""
    if delta is not None:
        delta_class = "positive" if delta_positive else "negative"
        delta_sign = "+" if delta_positive and delta > 0 else ""
        delta_html = f'<div class="metric-delta {delta_class}">{delta_sign}{delta}</div>'
    
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

# Calculate filtered KPIs
filtered_kpi = {
    'avg_adoption': filtered_df['ai_adoption_rate'].mean(),
    'avg_displacement': filtered_df['displacement_risk_index'].mean(),
    'net_jobs': (filtered_df['jobs_created_count'] - filtered_df['jobs_displaced_count']).sum(),
    'total_investment': filtered_df['reskilling_investment_usd'].sum() / 1e9,
    'workforce_affected': filtered_df['workforce_size'].sum() / 1e6
}

# Handle NaN values in KPIs
for key in filtered_kpi:
    if pd.isna(filtered_kpi[key]):
        filtered_kpi[key] = 0

# Display KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    render_kpi_card("Avg AI Adoption Rate", f"{filtered_kpi['avg_adoption']:.1f}%")
with col2:
    render_kpi_card("Avg Displacement Risk", f"{filtered_kpi['avg_displacement']:.1f}/10")
with col3:
    render_kpi_card("Net Job Growth", f"{filtered_kpi['net_jobs']:,.0f}", delta_positive=filtered_kpi['net_jobs'] >= 0)
with col4:
    render_kpi_card("Reskilling Investment", f"${filtered_kpi['total_investment']:.2f}B")
with col5:
    render_kpi_card("Workforce Affected", f"{filtered_kpi['workforce_affected']:.1f}M")

st.markdown("---")

# Tab Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "Global Overview & Economy Divide",
    "Workforce Displacement & GenAI Shift",
    "Reskilling Economics",
    "Cross-Dimensional Analysis"
])

# Color theme
COLOR_THEME = {
    'primary': '#3B82F6',
    'secondary': '#6366F1',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'background': '#0F172A',
    'surface': '#1E293B'
}

def create_matplotlib_figure():
    """Create a matplotlib figure with dark theme styling."""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(COLOR_THEME['background'])
    ax.set_facecolor(COLOR_THEME['surface'])
    ax.tick_params(colors='#F8FAFC')
    ax.xaxis.label.set_color('#F8FAFC')
    ax.yaxis.label.set_color('#F8FAFC')
    ax.title.set_color('#F8FAFC')
    for spine in ax.spines.values():
        spine.set_edgecolor('#475569')
    return fig, ax

# Tab 1: Global Overview & Economy Divide
with tab1:
    st.subheader("Global AI Adoption & Infrastructure Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # AI Adoption by Development Tier
        tier_adoption = filtered_df.groupby(['development_tier', 'era'])['ai_adoption_rate'].mean().reset_index()
        fig, ax = create_matplotlib_figure()
        tiers = tier_adoption['development_tier'].unique()
        x = np.arange(len(tiers))
        width = 0.35
        
        genai_data = tier_adoption[tier_adoption['era'] == 'GenAI Era']['ai_adoption_rate'].values
        pre_genai_data = tier_adoption[tier_adoption['era'] == 'Pre-GenAI']['ai_adoption_rate'].values
        
        bars1 = ax.bar(x - width/2, genai_data, width, label='GenAI Era', color=COLOR_THEME['primary'])
        bars2 = ax.bar(x + width/2, pre_genai_data, width, label='Pre-GenAI', color=COLOR_THEME['secondary'])
        
        ax.set_xlabel('Development Tier')
        ax.set_ylabel('Adoption Rate (%)')
        ax.set_title('AI Adoption Rate by Development Tier')
        ax.set_xticks(x)
        ax.set_xticklabels(tiers)
        ax.legend()
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}%', ha='center', va='bottom')
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        # Infrastructure vs Policy Maturity
        country_filtered = country_agg[
            country_agg['country_name'].isin(filtered_df['country_name'].unique())
        ].copy()
        country_filtered['ai_adoption_rate'] = country_filtered['ai_adoption_rate'].fillna(0)
        fig, ax = create_matplotlib_figure()
        
        developed = country_filtered[country_filtered['development_tier'] == 'Developed']
        emerging = country_filtered[country_filtered['development_tier'] == 'Emerging']
        
        ax.scatter(developed['digital_infrastructure_score'], developed['displacement_risk_index'], 
                  s=developed['ai_adoption_rate']*10, c=COLOR_THEME['primary'], label='Developed', alpha=0.6)
        ax.scatter(emerging['digital_infrastructure_score'], emerging['displacement_risk_index'], 
                  s=emerging['ai_adoption_rate']*10, c=COLOR_THEME['warning'], label='Emerging', alpha=0.6)
        
        ax.set_xlabel('Digital Infrastructure Score')
        ax.set_ylabel('Displacement Risk Index')
        ax.set_title('Infrastructure vs Displacement Risk')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Regional AI Adoption Heatmap
        regional_adoption = filtered_df.groupby(['region', 'year'])['ai_adoption_rate'].mean().reset_index()
        fig, ax = create_matplotlib_figure()
        
        pivot_data = regional_adoption.pivot(index='region', columns='year', values='ai_adoption_rate')
        im = ax.imshow(pivot_data.values, cmap='Blues', aspect='auto')
        
        ax.set_xticks(np.arange(len(pivot_data.columns)))
        ax.set_yticks(np.arange(len(pivot_data.index)))
        ax.set_xticklabels(pivot_data.columns)
        ax.set_yticklabels(pivot_data.index)
        ax.set_title('Regional AI Adoption Heatmap')
        
        # Add text annotations
        for i in range(len(pivot_data.index)):
            for j in range(len(pivot_data.columns)):
                text = ax.text(j, i, f'{pivot_data.values[i, j]:.1f}%',
                             ha="center", va="center", color="white")
        
        plt.colorbar(im, ax=ax, label='Adoption Rate (%)')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col4:
        # Policy Maturity Distribution
        policy_dist = filtered_df.groupby(['ai_policy_maturity', 'development_tier']).size().reset_index(name='count')
        fig, ax = create_matplotlib_figure()
        
        # Create a simple bar chart instead of sunburst
        policy_pivot = policy_dist.pivot(index='ai_policy_maturity', columns='development_tier', values='count').fillna(0)
        policy_pivot.plot(kind='bar', ax=ax, color=[COLOR_THEME['primary'], COLOR_THEME['warning']])
        
        ax.set_xlabel('AI Policy Maturity')
        ax.set_ylabel('Count')
        ax.set_title('AI Policy Maturity Distribution')
        ax.legend(title='Development Tier')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

# Tab 2: Workforce Displacement & GenAI Shift
with tab2:
    st.subheader("Workforce Displacement Risk & Generative AI Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Displacement Risk by Industry
        industry_risk = filtered_df.groupby('industry_name')['displacement_risk_index'].mean().sort_values(ascending=False).head(15).reset_index()
        fig, ax = create_matplotlib_figure()
        
        bars = ax.barh(industry_risk['industry_name'], industry_risk['displacement_risk_index'], 
                      color=COLOR_THEME['danger'])
        ax.set_xlabel('Displacement Risk Index (0-10)')
        ax.set_ylabel('')
        ax.set_title('Top 15 Industries by Displacement Risk')
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, f'{width:.1f}', 
                   ha='left', va='center')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        # Skill Category Vulnerability
        skill_risk = filtered_df.groupby('skill_category_name').agg({
            'displacement_risk_index': 'mean',
            'ai_replaceability_score': 'mean',
            'workforce_size': 'sum'
        }).reset_index()
        skill_risk = skill_risk.copy()
        skill_risk['workforce_size'] = skill_risk['workforce_size'].fillna(0)
        skill_risk['ai_replaceability_score'] = skill_risk['ai_replaceability_score'].fillna(0)
        fig, ax = create_matplotlib_figure()
        
        scatter = ax.scatter(skill_risk['ai_replaceability_score'], skill_risk['displacement_risk_index'], 
                           s=skill_risk['workforce_size']/1000, c=skill_risk['displacement_risk_index'], 
                           cmap='Reds', alpha=0.6)
        ax.set_xlabel('AI Replaceability Score')
        ax.set_ylabel('Displacement Risk Index')
        ax.set_title('Skill Category Vulnerability Matrix')
        plt.colorbar(scatter, ax=ax, label='Displacement Risk')
        plt.tight_layout()
        st.pyplot(fig)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # GenAI Era Impact on Adoption
        era_comparison = filtered_df.groupby(['era', 'year_quarter_label'])['ai_adoption_rate'].mean().reset_index()
        fig, ax = create_matplotlib_figure()
        
        genai_data = era_comparison[era_comparison['era'] == 'GenAI Era']
        pre_genai_data = era_comparison[era_comparison['era'] == 'Pre-GenAI']
        
        ax.plot(genai_data['year_quarter_label'], genai_data['ai_adoption_rate'], 
               marker='o', color=COLOR_THEME['primary'], label='GenAI Era')
        ax.plot(pre_genai_data['year_quarter_label'], pre_genai_data['ai_adoption_rate'], 
               marker='o', color=COLOR_THEME['secondary'], label='Pre-GenAI')
        
        ax.set_ylabel('Adoption Rate (%)')
        ax.set_xlabel('')
        ax.set_title('AI Adoption Trends: Pre-GenAI vs GenAI Era')
        ax.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col4:
        # Job Displacement vs Creation Over Time
        time_jobs = filtered_df.groupby(['year_quarter_label']).agg({
            'jobs_displaced_count': 'sum',
            'jobs_created_count': 'sum'
        }).reset_index()
        fig, ax = create_matplotlib_figure()
        
        ax.plot(time_jobs['year_quarter_label'], time_jobs['jobs_displaced_count'], 
               marker='o', color=COLOR_THEME['danger'], label='Jobs Displaced')
        ax.plot(time_jobs['year_quarter_label'], time_jobs['jobs_created_count'], 
               marker='o', color=COLOR_THEME['success'], label='Jobs Created')
        
        ax.set_ylabel('Number of Jobs')
        ax.set_xlabel('')
        ax.set_title('Job Displacement vs Creation Over Time')
        ax.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

# Tab 3: Reskilling Economics
with tab3:
    st.subheader("Economics of Reskilling & Investment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Reskilling Investment vs Displacement Risk
        industry_investment = filtered_df.groupby('industry_name').agg({
            'displacement_risk_index': 'mean',
            'reskilling_investment_usd': 'sum',
            'jobs_displaced_count': 'sum'
        }).reset_index()
        industry_investment = industry_investment.copy()
        industry_investment['jobs_displaced_count'] = industry_investment['jobs_displaced_count'].fillna(0)
        industry_investment['reskilling_investment_usd'] = industry_investment['reskilling_investment_usd'].fillna(0)
        fig, ax = create_matplotlib_figure()
        
        scatter = ax.scatter(industry_investment['displacement_risk_index'], industry_investment['reskilling_investment_usd'], 
                           s=industry_investment['jobs_displaced_count']/100, c=industry_investment['displacement_risk_index'], 
                           cmap='Reds', alpha=0.6)
        ax.set_xlabel('Displacement Risk Index')
        ax.set_ylabel('Reskilling Investment (USD)')
        ax.set_title('Reskilling Investment vs Displacement Risk')
        plt.colorbar(scatter, ax=ax, label='Displacement Risk')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        # Underfunded Sectors Analysis
        industry_investment['investment_per_displaced'] = industry_investment['reskilling_investment_usd'] / (industry_investment['jobs_displaced_count'] + 1)
        underfunded = industry_investment[industry_investment['investment_per_displaced'] < industry_investment['investment_per_displaced'].median()].sort_values('displacement_risk_index', ascending=False).head(10)
        fig, ax = create_matplotlib_figure()
        
        bars = ax.barh(underfunded['industry_name'], underfunded['investment_per_displaced'], 
                      color=COLOR_THEME['danger'])
        ax.set_xlabel('Investment per Displaced Job (USD)')
        ax.set_ylabel('')
        ax.set_title('Underfunded High-Risk Sectors')
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, f'${width:,.0f}', 
                   ha='left', va='center')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Net Job Growth by Country
        country_net = filtered_df.groupby('country_name').agg({
            'jobs_created_count': 'sum',
            'jobs_displaced_count': 'sum',
            'development_tier': 'first'
        }).reset_index()
        country_net['net_growth'] = country_net['jobs_created_count'] - country_net['jobs_displaced_count']
        country_net = country_net.sort_values('net_growth', ascending=False).head(15)
        fig, ax = create_matplotlib_figure()
        
        colors = [COLOR_THEME['primary'] if tier == 'Developed' else COLOR_THEME['warning'] 
                 for tier in country_net['development_tier']]
        bars = ax.barh(country_net['country_name'], country_net['net_growth'], color=colors)
        ax.set_xlabel('Net Job Growth')
        ax.set_ylabel('')
        ax.set_title('Net Job Growth by Country (Top 15)')
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, f'{width:,.0f}', 
                   ha='left', va='center')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col4:
        # Reskilling ROI Analysis
        skill_reskilling = filtered_df.groupby('skill_category_name').agg({
            'reskilling_investment_usd': 'sum',
            'net_job_growth': 'sum',
            'median_reskilling_duration_months': 'mean'
        }).reset_index()
        skill_reskilling['abs_net_growth'] = skill_reskilling['net_job_growth'].abs()
        skill_reskilling['abs_net_growth'] = skill_reskilling['abs_net_growth'].fillna(0)
        fig, ax = create_matplotlib_figure()
        
        scatter = ax.scatter(skill_reskilling['median_reskilling_duration_months'], skill_reskilling['reskilling_investment_usd'], 
                           s=skill_reskilling['abs_net_growth']/100, c=skill_reskilling['net_job_growth'], 
                           cmap='RdYlGn', alpha=0.6)
        ax.set_xlabel('Median Reskilling Duration (Months)')
        ax.set_ylabel('Total Reskilling Investment (USD)')
        ax.set_title('Reskilling Duration vs Investment')
        plt.colorbar(scatter, ax=ax, label='Net Job Growth')
        plt.tight_layout()
        st.pyplot(fig)

# Tab 4: Cross-Dimensional Analysis
with tab4:
    st.subheader("Interactive Cross-Dimensional Deep Dive")
    
    # Dynamic filtering controls
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        selected_country = st.selectbox(
            "Select Country",
            options=["All"] + sorted(filtered_df['country_name'].unique().tolist()),
            index=0
        )
    
    with filter_col2:
        selected_industry = st.selectbox(
            "Select Industry",
            options=["All"] + sorted(filtered_df['industry_name'].unique().tolist()),
            index=0
        )
    
    with filter_col3:
        selected_skill = st.selectbox(
            "Select Skill Category",
            options=["All"] + sorted(filtered_df['skill_category_name'].unique().tolist()),
            index=0
        )
    
    # Apply cross-filters
    cross_filtered = filtered_df.copy()
    if selected_country != "All":
        cross_filtered = cross_filtered[cross_filtered['country_name'] == selected_country]
    if selected_industry != "All":
        cross_filtered = cross_filtered[cross_filtered['industry_name'] == selected_industry]
    if selected_skill != "All":
        cross_filtered = cross_filtered[cross_filtered['skill_category_name'] == selected_skill]
    
    if len(cross_filtered) == 0:
        st.warning("No data available for the selected combination. Please adjust your filters.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            # Time Series for Selected Segment
            time_series = cross_filtered.groupby(['year_quarter_label']).agg({
                'ai_adoption_rate': 'mean',
                'displacement_risk_index': 'mean',
                'jobs_displaced_count': 'sum',
                'jobs_created_count': 'sum'
            }).reset_index()
            
            fig, ax1 = create_matplotlib_figure()
            ax2 = ax1.twinx()
            
            ax1.plot(time_series['year_quarter_label'], time_series['ai_adoption_rate'], 
                    marker='o', color=COLOR_THEME['primary'], label='AI Adoption Rate')
            ax2.plot(time_series['year_quarter_label'], time_series['displacement_risk_index'], 
                    marker='o', color=COLOR_THEME['danger'], label='Displacement Risk')
            
            ax1.set_ylabel('Adoption Rate (%)', color=COLOR_THEME['primary'])
            ax2.set_ylabel('Risk Index', color=COLOR_THEME['danger'])
            ax1.set_xlabel('')
            ax1.set_title('AI Adoption & Displacement Risk Over Time')
            ax1.tick_params(axis='y', labelcolor=COLOR_THEME['primary'])
            ax2.tick_params(axis='y', labelcolor=COLOR_THEME['danger'])
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            # Comprehensive Metrics Overview (Bar chart instead of radar)
            metrics = cross_filtered[['ai_adoption_rate', 'displacement_risk_index', 
                                     'productivity_impact_score', 'avg_wage_change_pct']].mean()
            
            fig, ax = create_matplotlib_figure()
            
            bars = ax.bar(metrics.index, metrics.values, color=COLOR_THEME['primary'])
            ax.set_ylabel('Value')
            ax.set_title('Comprehensive Metrics Overview')
            plt.xticks(rotation=45, ha='right')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}', 
                       ha='center', va='bottom')
            
            plt.tight_layout()
            st.pyplot(fig)
        
        col3, col4 = st.columns(2)
        
        with col3:
            # AI Tool Usage Analysis
            usage_data = cross_filtered.groupby(['year_quarter_label'])['ai_tool_usage_hours_per_week'].mean().reset_index()
            fig, ax = create_matplotlib_figure()
            
            ax.fill_between(usage_data['year_quarter_label'], usage_data['ai_tool_usage_hours_per_week'], 
                           alpha=0.3, color=COLOR_THEME['primary'])
            ax.plot(usage_data['year_quarter_label'], usage_data['ai_tool_usage_hours_per_week'], 
                   marker='o', color=COLOR_THEME['primary'])
            ax.set_ylabel('Hours per Week')
            ax.set_xlabel('')
            ax.set_title('AI Tool Usage Hours Per Week')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col4:
            # Workforce Size Distribution
            workforce_dist = cross_filtered.groupby('industry_name')['workforce_size'].sum().sort_values(ascending=False).head(10)
            fig, ax = create_matplotlib_figure()
            
            ax.pie(workforce_dist.values, labels=workforce_dist.index, autopct='%1.1f%%', 
                  startangle=90, colors=sns.color_palette("husl", len(workforce_dist)))
            ax.set_title('Workforce Distribution by Industry')
            plt.tight_layout()
            st.pyplot(fig)
        
        # Detailed Data Table
        st.subheader("Detailed Data View")
        available_cols = [col for col in ['country_name', 'industry_name', 'skill_category_name', 'year_quarter_label',
                                          'ai_adoption_rate', 'displacement_risk_index', 'jobs_displaced_count',
                                          'jobs_created_count', 'reskilling_investment_usd', 'workforce_size'] 
                         if col in cross_filtered.columns]
        if available_cols:
            st.dataframe(
                cross_filtered[available_cols].sort_values('year_quarter_label') if 'year_quarter_label' in available_cols else cross_filtered[available_cols],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No columns available for display.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; padding: 20px;'>
    <p>Global AI Adoption & Workforce Displacement Index Dashboard</p>
    <p style='font-size: 12px;'>DataDNA Challenge - July 2026</p>
</div>
""", unsafe_allow_html=True)
