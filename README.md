# 🤖 AI Workforce Displacement Dashboard

[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![DataDNA Challenge](https://img.shields.io/badge/DataDNA-July%202026-orange)](https://datadna.ai/)

> A high-fidelity, interactive Streamlit dashboard analyzing global AI adoption and workforce displacement patterns across industries, regions, and skill categories.

**🚀 Live Demo:** [https://datadna-july-2026-u2v5gszt35cjey4hcyyfqi.streamlit.app/](https://datadna-july-2026-u2v5gszt35cjey4hcyyfqi.streamlit.app/)

## 🌟 Features

### 📊 Comprehensive Analytics
- **Global AI Overview**: Track adoption rates across development tiers and regions
- **Workforce Displacement Analysis**: Identify high-risk industries and skill categories
- **Reskilling Economics**: Analyze investment ROI and underfunded sectors
- **Cross-Dimensional Deep Dive**: Interactive filtering for granular insights

### 🎨 Premium UI/UX
- **Dark Theme Design**: Modern, professional interface with custom styling
- **Interactive Charts**: All Plotly charts feature data labels and detailed hover information
- **Dynamic KPI Cards**: Real-time metrics that update with filter changes
- **Responsive Layout**: Optimized for various screen sizes

### 🔧 Technical Excellence
- **Modular Architecture**: Separated data pipeline and dashboard logic
- **Error Handling**: Robust NaN/missing value handling throughout
- **Performance Optimized**: Cached data loading for fast page refreshes
- **Filter Reset**: One-click reset to restore default view

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/Gyanankur23/DataDNA-July-2026.git
cd DataDNA-July-2026

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
# Start the Streamlit app
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

## 📁 Project Structure

```
DataDNA-July-2026/
├── app.py                      # Main Streamlit dashboard
├── data_pipeline.py            # Data loading and processing pipeline
├── data/                       # Dataset directory
│   ├── dim_country.csv        # Country dimension table
│   ├── dim_date.csv           # Date dimension table
│   ├── dim_industry.csv       # Industry dimension table
│   ├── dim_skill_category.csv # Skill category dimension table
│   └── fact_workforce_ai_index.csv # Main fact table
├── docs/
│   └── DATA_DICTIONARY.md     # Data documentation
├── CHALLENGE_BRIEF.md         # Challenge requirements
└── README.md                  # This file
```

## 🎯 Dashboard Tabs

### Tab 1: Global Overview & Economy Divide
- AI adoption rates by development tier (Developed vs Emerging)
- Infrastructure vs displacement risk scatter analysis
- Regional AI adoption heatmap
- AI policy maturity distribution (sunburst chart)

### Tab 2: Workforce Displacement & GenAI Shift
- Top 15 industries by displacement risk
- Skill category vulnerability matrix
- AI adoption trends: Pre-GenAI vs GenAI era comparison
- Job displacement vs creation over time

### Tab 3: Reskilling Economics
- Reskilling investment vs displacement risk analysis
- Underfunded high-risk sectors identification
- Net job growth by country ranking
- Reskilling duration vs investment ROI analysis

### Tab 4: Cross-Dimensional Deep Dive
- Dynamic filtering by country, industry, and skill category
- Time series analysis for selected segments
- Comprehensive metrics radar chart
- AI tool usage trends
- Workforce distribution by industry
- Detailed data table with full dataset view

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.28.0
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express, Plotly Graph Objects
- **Styling**: Custom CSS with dark theme
- **Data Format**: CSV (dimension and fact tables)

## 📊 Data Overview

### Dataset Scope
- **Time Period**: 2021-Q1 to 2024-Q4
- **Geographic Coverage**: Global (Developed and Emerging economies)
- **Industries**: Multiple sectors with varying automation susceptibility
- **Skill Categories**: Diverse skill sets with AI replaceability scores

### Key Metrics
- AI Adoption Rate (%)
- Displacement Risk Index (0-10)
- Jobs Displaced/Created Count
- Reskilling Investment (USD)
- Workforce Size
- AI Tool Usage Hours/Week
- Productivity Impact Score

## 🎨 Color Palette

- **Background**: Deep Slate (#0F172A)
- **Surface**: Slate (#1E293B)
- **Primary**: Vibrant Indigo (#6366F1)
- **Secondary**: Teal (#14B8A6)
- **Success**: Emerald (#10B981)
- **Warning**: Amber (#F59E0B)
- **Danger**: Coral (#EF4444)
- **Text**: Light Slate (#F8FAFC)

## 🔍 Key Insights

### Global Patterns
- Developed economies show higher AI adoption rates
- Emerging markets face higher displacement risks
- GenAI era accelerated adoption across all regions

### Industry Analysis
- Manufacturing and services show highest displacement risk
- Tech and healthcare sectors lead in AI investment
- Reskilling ROI varies significantly by industry

### Skill Categories
- Routine manual skills face highest displacement risk
- Creative and complex problem-solving skills show augmentation potential
- Reskilling duration correlates with skill complexity

## 🤝 Contributing

This project was developed for the DataDNA Challenge (July 2026). For questions or suggestions, please open an issue on GitHub.

## 📝 Challenge Details

**Challenge**: DataDNA Dataset Challenge - July 2026  
**Theme**: Global AI Adoption Workforce Displacement Index  
**Objective**: Build an interactive data dashboard analyzing AI's impact on workforce dynamics  
**Dataset**: Synthetic data covering 300 records across multiple dimensions

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Gyanankur Baruah**  
- GitHub: [@Gyanankur23](https://github.com/Gyanankur23)
- DataDNA Challenge Participant - July 2026

## 🙏 Acknowledgments

- DataDNA Challenge organizers for the comprehensive dataset
- Streamlit team for the excellent framework
- Plotly community for interactive visualization tools

---

**Built with ❤️ for the DataDNA Challenge 2026**
