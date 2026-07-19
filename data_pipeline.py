import pandas as pd
import numpy as np
from pathlib import Path

def load_data():
    """Load all dimension and fact tables."""
    base_path = Path(__file__).parent / "data"
    
    dim_country = pd.read_csv(base_path / "dim_country.csv")
    dim_date = pd.read_csv(base_path / "dim_date.csv")
    dim_industry = pd.read_csv(base_path / "dim_industry.csv")
    dim_skill_category = pd.read_csv(base_path / "dim_skill_category.csv")
    fact_workforce_ai_index = pd.read_csv(base_path / "fact_workforce_ai_index.csv")
    
    return dim_country, dim_date, dim_industry, dim_skill_category, fact_workforce_ai_index

def clean_and_merge_data(dim_country, dim_date, dim_industry, dim_skill_category, fact_workforce_ai_index):
    """Clean data and merge dimension tables with fact table."""
    
    # Convert date column to datetime
    dim_date['period_start_date'] = pd.to_datetime(dim_date['period_start_date'])
    
    # Merge fact table with dimensions
    df = fact_workforce_ai_index.merge(dim_country, on='country_id', how='left')
    df = df.merge(dim_date, on='date_id', how='left')
    df = df.merge(dim_industry, on='industry_id', how='left')
    df = df.merge(dim_skill_category, on='skill_category_id', how='left')
    
    # Handle missing values
    df['ai_tool_usage_hours_per_week'] = df['ai_tool_usage_hours_per_week'].fillna(0)
    df['avg_wage_change_pct'] = df['avg_wage_change_pct'].fillna(0)
    df['productivity_impact_score'] = df['productivity_impact_score'].fillna(0)
    df['digital_infrastructure_score'] = df['digital_infrastructure_score'].fillna(0)
    df['stem_graduates_per_100k'] = df['stem_graduates_per_100k'].fillna(0)
    df['automation_susceptibility'] = df['automation_susceptibility'].fillna(0)
    df['avg_ai_investment_pct_revenue'] = df['avg_ai_investment_pct_revenue'].fillna(0)
    
    # Calculate derived metrics
    df['net_job_growth'] = df['jobs_created_count'] - df['jobs_displaced_count']
    df['net_job_growth_rate'] = (df['net_job_growth'] / df['workforce_size'].replace(0, np.nan)) * 100
    df['reskilling_investment_per_worker'] = df['reskilling_investment_usd'] / df['workforce_size'].replace(0, np.nan)
    df['displacement_to_reskilling_ratio'] = df['displacement_risk_index'] / (df['reskilling_investment_per_worker'].replace(0, np.nan) + 1)
    
    # Create era-based analysis columns
    df['era'] = np.where(df['generative_ai_era'] == True, 'GenAI Era', 'Pre-GenAI')
    
    # Calculate job creation to displacement ratio
    df['job_creation_to_displacement_ratio'] = np.where(
        df['jobs_displaced_count'] > 0,
        df['jobs_created_count'] / df['jobs_displaced_count'],
        np.inf
    )
    
    # Risk categorization
    df['risk_category'] = pd.cut(
        df['displacement_risk_index'],
        bins=[0, 3, 6, 10],
        labels=['Low Risk', 'Medium Risk', 'High Risk']
    )
    
    # Adoption categorization
    df['adoption_category'] = pd.cut(
        df['ai_adoption_rate'],
        bins=[0, 25, 50, 75, 100],
        labels=['Low Adoption', 'Moderate Adoption', 'High Adoption', 'Very High Adoption']
    )
    
    # Sort by date
    df = df.sort_values(['year', 'quarter'])
    
    return df

def create_aggregated_views(df):
    """Create aggregated views for dashboard analysis."""
    
    # Country-level aggregation
    country_agg = df.groupby(['country_name', 'development_tier', 'region']).agg({
        'ai_adoption_rate': 'mean',
        'displacement_risk_index': 'mean',
        'jobs_displaced_count': 'sum',
        'jobs_created_count': 'sum',
        'reskilling_investment_usd': 'sum',
        'workforce_size': 'sum',
        'digital_infrastructure_score': 'mean',
        'ai_policy_maturity': 'first',
        'stem_graduates_per_100k': 'mean'
    }).reset_index()
    
    country_agg['net_job_growth'] = country_agg['jobs_created_count'] - country_agg['jobs_displaced_count']
    
    # Industry-level aggregation
    industry_agg = df.groupby(['industry_name', 'industry_sector', 'automation_susceptibility']).agg({
        'ai_adoption_rate': 'mean',
        'displacement_risk_index': 'mean',
        'jobs_displaced_count': 'sum',
        'jobs_created_count': 'sum',
        'reskilling_investment_usd': 'sum',
        'workforce_size': 'sum',
        'avg_ai_investment_pct_revenue': 'mean'
    }).reset_index()
    
    industry_agg['net_job_growth'] = industry_agg['jobs_created_count'] - industry_agg['jobs_displaced_count']
    
    # Skill category aggregation
    skill_agg = df.groupby(['skill_category_name', 'ai_replaceability_score']).agg({
        'ai_adoption_rate': 'mean',
        'displacement_risk_index': 'mean',
        'jobs_displaced_count': 'sum',
        'jobs_created_count': 'sum',
        'reskilling_investment_usd': 'sum',
        'workforce_size': 'sum',
        'median_reskilling_duration_months': 'mean'
    }).reset_index()
    
    skill_agg['net_job_growth'] = skill_agg['jobs_created_count'] - skill_agg['jobs_displaced_count']
    
    # Time series aggregation
    time_agg = df.groupby(['year', 'quarter', 'year_quarter_label', 'era']).agg({
        'ai_adoption_rate': 'mean',
        'displacement_risk_index': 'mean',
        'jobs_displaced_count': 'sum',
        'jobs_created_count': 'sum',
        'reskilling_investment_usd': 'sum',
        'workforce_size': 'sum',
        'ai_tool_usage_hours_per_week': 'mean'
    }).reset_index()
    
    time_agg['net_job_growth'] = time_agg['jobs_created_count'] - time_agg['jobs_displaced_count']
    
    return country_agg, industry_agg, skill_agg, time_agg

def get_kpi_metrics(df):
    """Calculate key performance indicators for dashboard."""
    
    kpi = {
        'total_countries': df['country_name'].nunique(),
        'total_industries': df['industry_name'].nunique(),
        'total_skill_categories': df['skill_category_name'].nunique(),
        'total_workforce': df['workforce_size'].sum(),
        'avg_ai_adoption': df['ai_adoption_rate'].mean(),
        'avg_displacement_risk': df['displacement_risk_index'].mean(),
        'total_jobs_displaced': df['jobs_displaced_count'].sum(),
        'total_jobs_created': df['jobs_created_count'].sum(),
        'total_reskilling_investment': df['reskilling_investment_usd'].sum(),
        'net_job_growth': (df['jobs_created_count'] - df['jobs_displaced_count']).sum(),
        'genai_adoption_increase': df[df['era'] == 'GenAI Era']['ai_adoption_rate'].mean() - df[df['era'] == 'Pre-GenAI']['ai_adoption_rate'].mean(),
        'high_risk_countries': len(df[df['displacement_risk_index'] > 7]['country_name'].unique()),
        'underfunded_sectors': len(df[(df['displacement_risk_index'] > 5) & (df['reskilling_investment_per_worker'] < 100)]['industry_name'].unique())
    }
    
    return kpi

def process_data():
    """Main processing function."""
    print("Loading data...")
    dim_country, dim_date, dim_industry, dim_skill_category, fact_workforce_ai_index = load_data()
    
    print("Cleaning and merging data...")
    df = clean_and_merge_data(dim_country, dim_date, dim_industry, dim_skill_category, fact_workforce_ai_index)
    
    print("Creating aggregated views...")
    country_agg, industry_agg, skill_agg, time_agg = create_aggregated_views(df)
    
    print("Calculating KPI metrics...")
    kpi = get_kpi_metrics(df)
    
    print(f"Data processing complete. {len(df)} records processed.")
    
    return df, country_agg, industry_agg, skill_agg, time_agg, kpi

if __name__ == "__main__":
    df, country_agg, industry_agg, skill_agg, time_agg, kpi = process_data()
    print("\nKPI Summary:")
    for key, value in kpi.items():
        print(f"{key}: {value}")
