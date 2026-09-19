# Medical Operations Dashboard

## 🔗 Team Project Repository

This is a collaborative team project developed by Team B — Batch 1.

**Common Team Repository:**
https://github.com/manoj-075/medical-operations-dashboard

A comprehensive healthcare operations analytics project designed to improve decision-making in patient flow, treatment demand, capacity planning, and resource utilization across a multi-department hospital environment.

The repository brings together a cleaned healthcare operations dataset, interactive dashboard development, KPI analysis, and executive-ready reporting in a structured, team-driven workflow.

---

## Overview

The Medical Operations Dashboard is a healthcare analytics initiative built to convert operational data into actionable business insights. It focuses on patient movement, department workload, resource availability, bed utilization, treatment demand, and geographic service pressure.

This project was developed as a collaborative Team B — Batch 1 effort and demonstrates how operational intelligence can support better hospital planning, improve bed management, highlight bottlenecks, and enable capacity-aware decision-making.

---

## Milestone 1 — Work Completed

### Dataset Generation

The project began with the generation of a realistic hospital operations dataset designed to simulate patient admissions, treatment activity, bed utilization, physician workloads, billing behavior, and geographic demand. The dataset reflects operational scenarios relevant to healthcare performance analysis and supports multiple layers of reporting and dashboarding.

### Dataset Overview

The generated dataset includes healthcare operations records covering patient demographics, admissions, discharge timelines, treatment categories, department assignments, bed occupancy, billing, and facility-level attributes. It provides enough complexity for KPI tracking and operational investigation while remaining interpretable for dashboard storytelling.

### Data Cleaning & Preparation

The raw operational data was cleaned and standardized to ensure consistency across multiple fields. This included handling missing values, validating date fields, correcting categorical inconsistency, standardizing department and bed attributes, and preparing a reusable analytical dataset for downstream KPI development.

### Data Validation

Data validation steps were performed to confirm the integrity of the dataset and ensure analytic reliability. This involved identification of invalid or incomplete records, checking core identifiers, verifying status fields, and validating that bed, treatment, and patient-related fields aligned with hospital operational logic.

### KPI Development

Key performance indicators were created to measure patient flow, operational throughput, resource use, and service demand. These KPIs were designed to help identify inefficiencies and support performance benchmarking across departments and operational units.

### Cleaned Dataset

A cleaned and structured version of the data was prepared for analysis and dashboard use. This cleaned dataset served as the foundation for all downstream reporting and visual analytics.

### KPI Summary

The KPI layer summarizes essential hospital metrics such as patient counts, treatment demand, bed utilization, average LOS, resource pressure, billing trends, and geographic demand concentration. These KPIs support immediate operational review and longer-term strategic planning.

### Milestone 1 Outcome

Milestone 1 established the analytical foundation of the project by generating, validating, and preparing a reliable healthcare operations dataset and a structured KPI framework for operational analysis.

### Next Milestone

The next milestone focused on deeper analysis of patient flow and demand patterns to identify bottlenecks, workload hotspots, and operational risk areas in treatment and departmental performance.

### Relevant Project Files

- `medical_operations_dashboard_dataset (1).csv`
- `data/medical_operations_dashboard_cleaned.csv`
- `notebooks/Data_Cleaning (1).ipynb`
- `notebooks/EDA (1).ipynb`
- `Medical_Operations/app.py`

### Milestone 1 Conclusion

Milestone 1 successfully created a clean, structured base for operational analytics and established the foundation for the dashboarding journey that followed.

---

## Milestone 2 — Patient Flow, Treatment Demand & Operational Bottleneck Analysis

### Overview

This milestone concentrated on patient movement, treatment intensity, and operational pressure points across departments and service lines. The objective was to identify which areas were experiencing the heaviest demand and where hospital resources were most strained.

### Objectives

- Analyze hospital patient flow patterns over time
- Measure treatment demand by specialty and department
- Detect operational bottlenecks in patient movement and service throughput
- Evaluate ward and department-level pressure indicators
- Highlight where operational interventions may improve patient experience and efficiency

### Key Business Questions

- Which departments experience the highest patient volumes?
- Which treatments are most in demand across the hospital?
- Where are the largest operational bottlenecks occurring?
- How do bed occupancy and patient movement patterns affect service performance?
- Which operational units require proactive intervention based on demand pressure?

### Dashboard Structure

The dashboard for this milestone was organized around key operational dimensions, including patient flow overview, treatment demand analysis, and workflow bottlenecks.

### Patient Flow & Hospital Overview

This section reviewed patient volumes, admissions, bed occupancy, gender distribution, and department-based patient demand. It provided an executive snapshot of hospital activity and flow patterns across the system.

### Treatment Demand & Departmental Workload

The treatment demand layer evaluated the most frequently observed treatments and how demand shifted by time period, department, and patient profile. It helped identify areas of sustained demand and workload concentration.

### Operational Bottlenecks & High-Demand Areas

This analysis focused on wards, departments, and treatment areas with the greatest occupancy, longest LOS, and strongest demand signals. It was intended to flag where delays and resource strain were likely affecting patient flow and hospital performance.

### Key Insights

- Certain hospital departments demonstrated much higher patient intensity than others.
- Treatment demand was uneven across time and was concentrated in a smaller set of high-volume service lines.
- Bed occupancy and LOS patterns revealed operational stress in specific departments.
- High-demand areas were more likely to experience bottlenecks that could influence throughput and patient outcomes.

### Tools & Technologies

- Python
- Pandas
- Plotly
- Streamlit
- Jupyter Notebook
- Power BI (for dashboard visualization and executive presentation) 

### Project Structure

```text
medical-operations-dashboard-team/
├── README.md
├── LICENSE
├── medical_operations_dashboard_dataset (1).csv
├── kpi document (2).xlsx
├── Dashboards/
│   ├── Dashboard_1 (1).pbix
│   ├── Dashboard_2.pbix
│   └── Executive_Dashboard.pbix
├── data/
│   └── medical_operations_dashboard_cleaned.csv
├── Medical_Operations/
│   ├── app.py
│   ├── medical_operations_dashboard_cleaned (1).csv
│   └── requirements.txt
├── notebooks/
│   ├── Data_Cleaning (1).ipynb
│   └── EDA (1).ipynb
└── Internship artifacts/
```

### Analytical Flow

The analytical process combined data preparation, validation, KPI computation, and dashboard-oriented storytelling to build a narrative from raw operational records to executive insights.

### Expected Outcome

The expected outcome of Milestone 2 was a deeper operational understanding of patient flow, treatment demand, and the high-pressure areas most likely to impede efficient care delivery.

### Business Impact

This milestone directly supports management decisions related to resource allocation, department planning, and operational optimization. The analysis helps healthcare leadership identify where process improvement and capacity management are most urgently needed.

### Future Enhancements

- Add predictive operational alerts for forecasted surges
- Expand staffing and demand simulation scenarios
- Integrate more granular workflow timing data
- Add department-level operational benchmarking

### Project Focus

This milestone emphasized patient flow and operational pain points as the clearest indicators of where hospital efficiency could be improved.

### Conclusion

Milestone 2 helped transform raw patient and operational activity into clear, decision-relevant insight about where healthcare demand and system strain were concentrated.

---

## Milestone 3 — Resource Utilization & Capacity Intelligence

### Overview

This milestone shifted focus to resource utilization and capacity intelligence. It evaluated bed status, occupancy, physician workload, and operational load intensity to understand where the hospital was effectively managing capacity and where it was approaching overload.

### Objectives

- Measure bed utilization and occupancy trends
- Assess workforce-to-patient pressure across departments
- Identify capacity strain and overloaded operational units
- Evaluate resource efficiency and utilization benchmarks
- Support capacity planning and operational forecasting

### Key Business Questions

- Which departments are operating near or above utilization thresholds?
- How are beds distributed across departments and wards?
- Are physician workloads aligned with patient demand?
- Which units are experiencing the greatest capacity pressure?
- What operational signals indicate overload risk?

### Dashboard Structure

The resource intelligence dashboard was built around resource overview, workforce utilization, capacity analysis, and operational benchmark measurement.

### Resource Overview

This section provided a high-level view of total beds, occupied beds, available beds, and overall bed occupancy. It created a clear picture of the hospital’s current physical capacity and immediate operational readiness.

### Resource Pressure Analysis

The resource pressure analysis evaluated departments and wards under different levels of occupancy and patient concentration. This helped identify areas that were nearing operational strain or requiring intervention.

### Department Resource Pressure Matrix

The department pressure matrix compared utilization intensity with patient volume and workforce pressure to identify units that had the highest operational load relative to available capacity.

### Capacity & Overload Analysis

This layer measured utilization against defined thresholds and flagged departments at risk of overload. It provided a benchmark-oriented view of where hospital operations were becoming fragile or capacity constrained.

### Key Insight

The most material operational signal was not simply total patient volume, but the combined pressure of demand, occupancy, and workforce constraints within each department.

### Operational Benchmark Framework

Benchmarking supported interpretation of utilization rates and allowed departments to be compared against operational thresholds. This made it easier to identify where capacity constraints were most significant and where interventions could yield the greatest benefit.

### Tools & Technologies

- Python
- Pandas
- Plotly
- Streamlit
- Business KPI logic
- Operational benchmarking design

### Project Structure

The repository continues to support the project through the core data and dashboard assets listed in the main project layout above, with the implementation held primarily in `Medical_Operations/app.py` and the cleaned dataset in `data/medical_operations_dashboard_cleaned.csv`.

### Analytical Flow

The analytical flow combined bed, department, and workload metrics to create a more complete picture of hospital capacity and the operational pressure underlying each department.

### Expected Outcome

The expected outcome was a capacity-aware dashboard that could help hospital teams identify stress points, optimize bed management, and align workforce planning with real demand patterns.

### Business Impact

This milestone supports better inpatient planning, improved bed utilization, and stronger operational visibility into where hospital resources may need adjustment or escalation.

### Future Enhancements

- Expand forecasting for capacity overload risk
- Add staff scheduling optimization metrics
- Monitor patient turnaround and discharge delays
- Introduce predictive staffing and occupancy scenario models

### Key Takeaway

Resource utilization is not only a counting problem; it is a capacity intelligence problem involving demand, staffing, throughput, and operational resilience.

### Project Focus

This milestone emphasized operational resilience and resource-aware planning as essential components of hospital efficiency.

### Conclusion

Milestone 3 established the project’s capacity intelligence framework and helped translate occupancy data into meaningful operational action.

---

## Milestone 4 — Geographical Analysis & Final Executive Dashboard

### Objective

The final milestone focused on geographic demand analysis and final executive storytelling. This phase connected localized patient demand with the broader operational and capacity picture to produce a decision-ready leadership dashboard.

### Geographical Analysis

Geographical analysis reviewed variation in patient demand and utilization across states and cities. This provided insight into the location-based drivers of demand, hospital stress patterns, and regional concentration of service need.

### Key Business Questions

- Which regions contribute the highest patient volume?
- Where are the most intense service demand concentrations?
- How do department and bed utilization patterns differ by geography?
- Which states or cities indicate operational risk or demand imbalance?
- What insights should committee-level or executive stakeholders see first?

### Geographical Dashboard Components

The geographical dashboard included patient volume by state and city, top-demand regions, and comparisons of operational demand and capacity across geographic clusters.

### Final Executive Dashboard Integration

The final dashboard consolidated the operational analysis into an executive-ready perspective. It merged patient flow, treatment demand, capacity load, and geographic demand into a single, clear, strategic narrative.

### Executive-Level Insights

The final executive view highlighted priority departments, operational bottlenecks, high-utilization units, and the overall hospital capacity picture in a format that supports strategic planning and leadership action.

### Dashboard Design

The final dashboard design prioritized clarity, interpretability, and decision support. It emphasized summary metrics, visual storytelling, and executive-friendly layout for operational guidance.

### Dashboard Validation

The final dashboard was validated against the underlying operational data to ensure that the visuals, KPI summaries, and geographic insights were consistent with the actual dataset and reflected realistic operational patterns.

### Milestone 4 Outcome

Milestone 4 concluded the project by integrating operational intelligence, regional analysis, and executive-ready reporting into a final decision-support dashboard.

### Live Dashboard

> Live dashboard link will be added once the team deployment URL is finalized.

### Final Outcome

The Medical Operations Dashboard project provides a complete operational analytics lens for healthcare management, combining patient flow, treatment demand, capacity pressure, and geographical service analysis into a practical, decision-oriented dashboard framework.

---

## Tools & Technologies

- Python
- Pandas
- Plotly
- Streamlit
- Jupyter Notebook
- Power BI
- GitHub for version control and project collaboration

---

## Project Structure

```text
medical-operations-dashboard-team/
├── README.md
├── LICENSE
├── medical_operations_dashboard_dataset (1).csv
├── kpi document (2).xlsx
├── Dashboards/
│   ├── Dashboard_1 (1).pbix
│   ├── Dashboard_2.pbix
│   └── Executive_Dashboard.pbix
├── data/
│   └── medical_operations_dashboard_cleaned.csv
├── Medical_Operations/
│   ├── app.py
│   ├── medical_operations_dashboard_cleaned (1).csv
│   └── requirements.txt
├── notebooks/
│   ├── Data_Cleaning (1).ipynb
│   └── EDA (1).ipynb
└── Internship artifacts/
```

> The repository structure reflects the actual files present in this project workspace. The README intentionally documents the real project assets without inventing additional dashboards, datasets, or deployment links.

---

## Analytical Flow

1. Data generation and dataset framing
2. Data cleaning and preparation
3. Validation and KPI development
4. Exploratory analysis and operational insight generation
5. Dashboard design and storyboarding
6. Executive summary and strategic decision support

---

## Expected Outcome

The project is intended to provide a realistic, operationally grounded healthcare analytics dashboard that supports better planning, performance monitoring, and strategic execution in a hospital or clinical operations setting.

---

## Business Impact

The dashboard helps leadership teams understand the balance between patient demand, bed capacity, physician workload, and treatment complexity. It supports stronger operational management, better resource planning, and more evidence-based decision-making.

---

## Future Enhancements

- Forecast-based operational planning
- Expanded departmental surgical and emergency demand analysis
- Improved patient-discharge and throughput modeling
- Integration of broader healthcare performance indicators
- Enhanced executive-ready reporting features

---

## Project Focus

This project is focused on practical, actionable healthcare operations analytics for a collaborative team environment. It demonstrates how real-world hospital data can be transformed into insight-driven dashboards for improved performance and capacity intelligence.

---

## Conclusion

The Medical Operations Dashboard is a collaborative Team B — Batch 1 project that brings together data preparation, operational analysis, KPI design, and executive-level dashboarding into a single comprehensive healthcare intelligence initiative. It reflects the team’s effort to build a meaningful and usable decision-support tool for healthcare operations management.

---

## 📌 Repository Summary

This repository contains the complete working project assets for the Medical Operations Dashboard, including:

- cleaned operational datasets
- notebook-based data cleaning and EDA workflow
- interactive hospital dashboard implementation
- Power BI dashboard assets
- KPI and executive reporting materials

The project is maintained in the common team repository:

https://github.com/manoj-075/medical-operations-dashboard
