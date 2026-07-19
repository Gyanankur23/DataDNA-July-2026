import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data_pipeline import process_data

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

def create_chart_template(fig):
    """Apply unified chart styling."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_THEME['background'],
        plot_bgcolor=COLOR_THEME['surface'],
        font=dict(color='#F8FAFC'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400
    )
    return fig

# Tab 1: Global Overview & Economy Divide
with tab1:
    st.subheader("Global AI Adoption & Infrastructure Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # AI Adoption by Development Tier
        tier_adoption = filtered_df.groupby(['development_tier', 'era'])['ai_adoption_rate'].mean().reset_index()
        fig1 = px.bar(
            tier_adoption,
            x='development_tier',
            y='ai_adoption_rate',
            color='era',
            barmode='group',
            title="AI Adoption Rate by Development Tier",
            color_discrete_map={'GenAI Era': COLOR_THEME['primary'], 'Pre-GenAI': COLOR_THEME['secondary']},
            text='ai_adoption_rate'
        )
        fig1.update_yaxes(title_text="Adoption Rate (%)")
        fig1.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
        st.plotly_chart(create_chart_template(fig1), use_container_width=True)
    
    with col2:
        # Infrastructure vs Policy Maturity
        country_filtered = country_agg[
            country_agg['country_name'].isin(filtered_df['country_name'].unique())
        ].copy()
        country_filtered['ai_adoption_rate'] = country_filtered['ai_adoption_rate'].fillna(0)
        fig2 = px.scatter(
            country_filtered,
            x='digital_infrastructure_score',
            y='displacement_risk_index',
            size='ai_adoption_rate',
            color='development_tier',
            hover_data=['country_name', 'ai_adoption_rate'],
            title="Infrastructure vs Displacement Risk",
            color_discrete_map={'Developed': COLOR_THEME['primary'], 'Emerging': COLOR_THEME['warning']},
            custom_data=['country_name', 'ai_adoption_rate']
        )
        fig2.update_xaxes(title_text="Digital Infrastructure Score")
        fig2.update_yaxes(title_text="Displacement Risk Index")
        fig2.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                           'Infrastructure: %{x:.1f}<br>' +
                           'Displacement Risk: %{y:.1f}<br>' +
                           'AI Adoption: %{customdata[1]:.1f}%<extra></extra>'
        )
        st.plotly_chart(create_chart_template(fig2), use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Regional AI Adoption Heatmap
        regional_adoption = filtered_df.groupby(['region', 'year'])['ai_adoption_rate'].mean().reset_index()
        fig3 = px.imshow(
            regional_adoption.pivot(index='region', columns='year', values='ai_adoption_rate'),
            title="Regional AI Adoption Heatmap",
            color_continuous_scale='Blues',
            aspect='auto',
            text_auto=True
        )
        fig3.update_traces(
            hovertemplate='Region: %{y}<br>Year: %{x}<br>Adoption: %{z:.1f}%<extra></extra>'
        )
        st.plotly_chart(create_chart_template(fig3), use_container_width=True)
    
    with col4:
        # Policy Maturity Distribution
        policy_dist = filtered_df.groupby(['ai_policy_maturity', 'development_tier']).size().reset_index(name='count')
        fig4 = px.sunburst(
            policy_dist,
            path=['development_tier', 'ai_policy_maturity'],
            values='count',
            title="AI Policy Maturity Distribution"
        )
        fig4.update_traces(
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        st.plotly_chart(create_chart_template(fig4), use_container_width=True)

# Tab 2: Workforce Displacement & GenAI Shift
with tab2:
    st.subheader("Workforce Displacement Risk & Generative AI Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Displacement Risk by Industry
        industry_risk = filtered_df.groupby('industry_name')['displacement_risk_index'].mean().sort_values(ascending=False).head(15).reset_index()
        fig5 = px.bar(
            industry_risk,
            x='displacement_risk_index',
            y='industry_name',
            orientation='h',
            title="Top 15 Industries by Displacement Risk",
            color='displacement_risk_index',
            color_continuous_scale='Reds',
            text='displacement_risk_index'
        )
        fig5.update_xaxes(title_text="Displacement Risk Index (0-10)")
        fig5.update_yaxes(title_text="")
        fig5.update_traces(texttemplate='%{x:.1f}', textposition='outside')
        st.plotly_chart(create_chart_template(fig5), use_container_width=True)
    
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
        fig6 = px.scatter(
            skill_risk,
            x='ai_replaceability_score',
            y='displacement_risk_index',
            size='workforce_size',
            hover_data=['skill_category_name'],
            title="Skill Category Vulnerability Matrix",
            color='displacement_risk_index',
            color_continuous_scale='Reds',
            custom_data=['skill_category_name', 'workforce_size']
        )
        fig6.update_xaxes(title_text="AI Replaceability Score")
        fig6.update_yaxes(title_text="Displacement Risk Index")
        fig6.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                           'Replaceability: %{x:.1f}<br>' +
                           'Displacement Risk: %{y:.1f}<br>' +
                           'Workforce: %{customdata[1]:,.0f}<extra></extra>'
        )
        st.plotly_chart(create_chart_template(fig6), use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # GenAI Era Impact on Adoption
        era_comparison = filtered_df.groupby(['era', 'year_quarter_label'])['ai_adoption_rate'].mean().reset_index()
        fig7 = px.line(
            era_comparison,
            x='year_quarter_label',
            y='ai_adoption_rate',
            color='era',
            title="AI Adoption Trends: Pre-GenAI vs GenAI Era",
            markers=True,
            color_discrete_map={'GenAI Era': COLOR_THEME['primary'], 'Pre-GenAI': COLOR_THEME['secondary']},
            text='ai_adoption_rate'
        )
        fig7.update_yaxes(title_text="Adoption Rate (%)")
        fig7.update_xaxes(title_text="")
        fig7.update_traces(texttemplate='%{y:.1f}%', textposition='top center')
        st.plotly_chart(create_chart_template(fig7), use_container_width=True)
    
    with col4:
        # Job Displacement vs Creation Over Time
        time_jobs = filtered_df.groupby(['year_quarter_label']).agg({
            'jobs_displaced_count': 'sum',
            'jobs_created_count': 'sum'
        }).reset_index()
        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(
            x=time_jobs['year_quarter_label'],
            y=time_jobs['jobs_displaced_count'],
            mode='lines+markers+text',
            name='Jobs Displaced',
            line=dict(color=COLOR_THEME['danger']),
            text=time_jobs['jobs_displaced_count'],
            texttemplate='%{y:,.0f}',
            textposition='top center'
        ))
        fig8.add_trace(go.Scatter(
            x=time_jobs['year_quarter_label'],
            y=time_jobs['jobs_created_count'],
            mode='lines+markers+text',
            name='Jobs Created',
            line=dict(color=COLOR_THEME['success']),
            text=time_jobs['jobs_created_count'],
            texttemplate='%{y:,.0f}',
            textposition='bottom center'
        ))
        fig8.update_layout(
            title="Job Displacement vs Creation Over Time",
            xaxis_title="",
            yaxis_title="Number of Jobs"
        )
        st.plotly_chart(create_chart_template(fig8), use_container_width=True)

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
        fig9 = px.scatter(
            industry_investment,
            x='displacement_risk_index',
            y='reskilling_investment_usd',
            size='jobs_displaced_count',
            hover_data=['industry_name'],
            title="Reskilling Investment vs Displacement Risk",
            color='displacement_risk_index',
            color_continuous_scale='Reds',
            custom_data=['industry_name', 'jobs_displaced_count']
        )
        fig9.update_xaxes(title_text="Displacement Risk Index")
        fig9.update_yaxes(title_text="Reskilling Investment (USD)")
        fig9.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                           'Displacement Risk: %{x:.1f}<br>' +
                           'Investment: $%{y:,.0f}<br>' +
                           'Jobs Displaced: %{customdata[1]:,.0f}<extra></extra>'
        )
        st.plotly_chart(create_chart_template(fig9), use_container_width=True)
    
    with col2:
        # Underfunded Sectors Analysis
        industry_investment['investment_per_displaced'] = industry_investment['reskilling_investment_usd'] / (industry_investment['jobs_displaced_count'] + 1)
        underfunded = industry_investment[industry_investment['investment_per_displaced'] < industry_investment['investment_per_displaced'].median()].sort_values('displacement_risk_index', ascending=False).head(10)
        fig10 = px.bar(
            underfunded,
            x='investment_per_displaced',
            y='industry_name',
            orientation='h',
            title="Underfunded High-Risk Sectors",
            color='displacement_risk_index',
            color_continuous_scale='Reds',
            text='investment_per_displaced'
        )
        fig10.update_xaxes(title_text="Investment per Displaced Job (USD)")
        fig10.update_yaxes(title_text="")
        fig10.update_traces(texttemplate='$%{x:,.0f}', textposition='outside')
        st.plotly_chart(create_chart_template(fig10), use_container_width=True)
    
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
        fig11 = px.bar(
            country_net,
            x='net_growth',
            y='country_name',
            orientation='h',
            color='development_tier',
            title="Net Job Growth by Country (Top 15)",
            color_discrete_map={'Developed': COLOR_THEME['primary'], 'Emerging': COLOR_THEME['warning']},
            text='net_growth'
        )
        fig11.update_xaxes(title_text="Net Job Growth")
        fig11.update_yaxes(title_text="")
        fig11.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
        st.plotly_chart(create_chart_template(fig11), use_container_width=True)
    
    with col4:
        # Reskilling ROI Analysis
        skill_reskilling = filtered_df.groupby('skill_category_name').agg({
            'reskilling_investment_usd': 'sum',
            'net_job_growth': 'sum',
            'median_reskilling_duration_months': 'mean'
        }).reset_index()
        skill_reskilling['abs_net_growth'] = skill_reskilling['net_job_growth'].abs()
        skill_reskilling['abs_net_growth'] = skill_reskilling['abs_net_growth'].fillna(0)
        fig12 = px.scatter(
            skill_reskilling,
            x='median_reskilling_duration_months',
            y='reskilling_investment_usd',
            size='abs_net_growth',
            hover_data=['skill_category_name', 'net_job_growth'],
            title="Reskilling Duration vs Investment",
            color='net_job_growth',
            color_continuous_scale='RdYlGn',
            custom_data=['skill_category_name', 'net_job_growth']
        )
        fig12.update_xaxes(title_text="Median Reskilling Duration (Months)")
        fig12.update_yaxes(title_text="Total Reskilling Investment (USD)")
        fig12.update_traces(
            marker=dict(sizemode='diameter', sizeref=0.1),
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                           'Duration: %{x:.1f} months<br>' +
                           'Investment: $%{y:,.0f}<br>' +
                           'Net Job Growth: %{customdata[1]:,.0f}<extra></extra>'
        )
        st.plotly_chart(create_chart_template(fig12), use_container_width=True)

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
            
            fig13 = go.Figure()
            fig13.add_trace(go.Scatter(
                x=time_series['year_quarter_label'],
                y=time_series['ai_adoption_rate'],
                mode='lines+markers+text',
                name='AI Adoption Rate',
                yaxis='y',
                text=time_series['ai_adoption_rate'],
                texttemplate='%{y:.1f}%',
                textposition='top center'
            ))
            fig13.add_trace(go.Scatter(
                x=time_series['year_quarter_label'],
                y=time_series['displacement_risk_index'],
                mode='lines+markers+text',
                name='Displacement Risk',
                yaxis='y2',
                text=time_series['displacement_risk_index'],
                texttemplate='%{y:.1f}',
                textposition='bottom center'
            ))
            fig13.update_layout(
                title="AI Adoption & Displacement Risk Over Time",
                yaxis=dict(title="Adoption Rate (%)", side="left"),
                yaxis2=dict(title="Risk Index", overlaying="y", side="right"),
                legend=dict(x=0.01, y=0.99)
            )
            st.plotly_chart(create_chart_template(fig13), use_container_width=True)
        
        with col2:
            # Comprehensive Metrics Radar
            metrics = cross_filtered[['ai_adoption_rate', 'displacement_risk_index', 
                                     'productivity_impact_score', 'avg_wage_change_pct']].mean()
            
            fig14 = go.Figure(data=go.Scatterpolar(
                r=metrics.values,
                theta=metrics.index,
                fill='toself',
                name='Current Selection',
                text=metrics.values,
                texttemplate='%{r:.1f}',
                textposition='top center'
            ))
            fig14.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                title="Comprehensive Metrics Overview"
            )
            fig14.update_traces(
                hovertemplate='<b>%{theta}</b><br>Value: %{r:.1f}<extra></extra>'
            )
            st.plotly_chart(create_chart_template(fig14), use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            # AI Tool Usage Analysis
            usage_data = cross_filtered.groupby(['year_quarter_label'])['ai_tool_usage_hours_per_week'].mean().reset_index()
            fig15 = px.area(
                usage_data,
                x='year_quarter_label',
                y='ai_tool_usage_hours_per_week',
                title="AI Tool Usage Hours Per Week",
                color_discrete_sequence=[COLOR_THEME['primary']],
                text='ai_tool_usage_hours_per_week'
            )
            fig15.update_yaxes(title_text="Hours per Week")
            fig15.update_traces(texttemplate='%{y:.1f}h', textposition='top center')
            st.plotly_chart(create_chart_template(fig15), use_container_width=True)
        
        with col4:
            # Workforce Size Distribution
            workforce_dist = cross_filtered.groupby('industry_name')['workforce_size'].sum().sort_values(ascending=False).head(10)
            fig16 = px.pie(
                values=workforce_dist.values,
                names=workforce_dist.index,
                title="Workforce Distribution by Industry"
            )
            fig16.update_traces(
                textinfo='label+percent+value',
                hovertemplate='<b>%{label}</b><br>Workforce: %{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
            )
            st.plotly_chart(create_chart_template(fig16), use_container_width=True)
        
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
