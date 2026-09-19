import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from pathlib import Path

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Hospital Operations Dashboard", layout="wide")

# ---------- LOAD DATA (kept in session_state so edits persist across interactions) ----------
if "df" not in st.session_state:
    df_init = pd.read_csv(Path(__file__).parent / "medical_operations_dashboard_cleaned.csv")
    df_init["Admission_Date"] = pd.to_datetime(df_init["Admission_Date"], errors="coerce")
    df_init["Discharge_Date"] = pd.to_datetime(df_init["Discharge_Date"], errors="coerce")
    st.session_state.df = df_init

df = st.session_state.df

st.title("🏥 Hospital Operations Dashboard")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Patient Flow & Hospital Overview",
    "Treatment Demand Analysis",
    "Operational Bottlenecks & High-Demand Areas",
    "Resource Overview",
    "Resource Utilization & Workforce",
    "Capacity & Overload Analysis",
    "Geographical Analysis",
    "Executive Summary",
    "🔴 Live Control Panel"
])

# ==========================================================
# TAB 1 — PATIENT FLOW & HOSPITAL OVERVIEW
# ==========================================================
with tab1:
    st.header("Patient Flow & Hospital Overview")

    total_patients = df["patient_id"].nunique()
    total_admissions = df["Admission_Id"].nunique()
    beds_unique = df.drop_duplicates(subset="Bed_Id")
    beds_occupied = int((beds_unique["Bed_Status"] == "Occupied").sum())

    los_df = df.dropna(subset=["Discharge_Date"]).copy()
    los_df["LOS"] = (los_df["Discharge_Date"] - los_df["Admission_Date"]).dt.days
    avg_los = round(los_df["LOS"].mean(), 2) if len(los_df) else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Patients", total_patients)
    c2.metric("Total Admissions", total_admissions)
    c3.metric("Beds Occupied", beds_occupied)
    c4.metric("Average Length of Stay", f"{avg_los} days")

    col1, col2 = st.columns(2)
    with col1:
        trend = df.copy()
        trend["Quarter"] = trend["Admission_Date"].dt.to_period("Q").astype(str)
        trend_counts = trend.groupby("Quarter")["Admission_Id"].nunique().reset_index()
        trend_counts.columns = ["Quarter", "Admissions"]
        fig = px.line(trend_counts, x="Quarter", y="Admissions", title="Quarterly Admission Trend", markers=True)
        st.plotly_chart(fig, use_container_width=True, key="plot_1")
    with col2:
        dept_adm = df.groupby("Department_Name")["Admission_Id"].nunique().sort_values(ascending=True).reset_index()
        dept_adm.columns = ["Department_Name", "Admissions"]
        fig = px.bar(dept_adm, x="Admissions", y="Department_Name", orientation="h", title="Admissions by Department")
        st.plotly_chart(fig, use_container_width=True, key="plot_2")

    col3, col4 = st.columns(2)
    with col3:
        gender_dist = df.drop_duplicates(subset="patient_id")["gender"].value_counts().reset_index()
        gender_dist.columns = ["Gender", "Count"]
        fig = px.pie(gender_dist, names="Gender", values="Count", hole=0.55, title="Patient Distribution by Gender")
        st.plotly_chart(fig, use_container_width=True, key="plot_3")
    with col4:
        status_dist = beds_unique["Bed_Status"].value_counts().reset_index()
        status_dist.columns = ["Bed_Status", "Count"]
        fig = px.pie(status_dist, names="Bed_Status", values="Count", hole=0.55, title="Bed Status Distribution")
        st.plotly_chart(fig, use_container_width=True, key="plot_4")

# ==========================================================
# TAB 2 — TREATMENT DEMAND ANALYSIS
# ==========================================================
with tab2:
    st.header("Treatment Demand Analysis")

    fcol1, fcol2, fcol3 = st.columns(3)
    year_options = sorted(df["Admission_Date"].dt.year.dropna().unique().tolist())
    sel_year = fcol1.selectbox("Year", options=["All"] + year_options)
    sel_gender = fcol2.selectbox("Gender", options=["All"] + sorted(df["gender"].dropna().unique().tolist()))
    sel_treatment = fcol3.selectbox("Treatment", options=["All"] + sorted(df["Treatment"].dropna().unique().tolist()))

    tdf = df.copy()
    if sel_year != "All":
        tdf = tdf[tdf["Admission_Date"].dt.year == sel_year]
    if sel_gender != "All":
        tdf = tdf[tdf["gender"] == sel_gender]
    if sel_treatment != "All":
        tdf = tdf[tdf["Treatment"] == sel_treatment]

    col1, col2 = st.columns(2)
    with col1:
        top5 = tdf["Treatment"].value_counts().head(5).index.tolist()
        trend5 = tdf[tdf["Treatment"].isin(top5)].copy()
        trend5["Month"] = trend5["Admission_Date"].dt.strftime("%b")
        month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        trend_counts = trend5.groupby(["Month", "Treatment"]).size().reset_index(name="Count")
        trend_counts["Month"] = pd.Categorical(trend_counts["Month"], categories=month_order, ordered=True)
        trend_counts = trend_counts.sort_values("Month")
        fig = px.line(trend_counts, x="Month", y="Count", color="Treatment", title="Top 5 Treatment Demand Trend", markers=True)
        st.plotly_chart(fig, use_container_width=True, key="plot_5")
    with col2:
        top5_counts = tdf[tdf["Treatment"].isin(top5)]["Treatment"].value_counts().reset_index()
        top5_counts.columns = ["Treatment", "Count"]
        fig = px.pie(top5_counts, names="Treatment", values="Count", hole=0.55, title="Treatment Demand Share (Top 5)")
        st.plotly_chart(fig, use_container_width=True, key="plot_6")

    col3, col4 = st.columns(2)
    with col3:
        all_treat = tdf["Treatment"].value_counts().reset_index()
        all_treat.columns = ["Treatment", "Count"]
        fig = px.bar(all_treat, x="Count", y="Treatment", orientation="h", title="Total Patients by Treatment")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True, key="plot_7")
    with col4:
        by_year = tdf.copy()
        by_year["Year"] = by_year["Admission_Date"].dt.year
        year_counts = by_year.groupby("Year").size().reset_index(name="Count")
        fig = px.bar(year_counts, x="Year", y="Count", title="Treatment Demand by Year")
        st.plotly_chart(fig, use_container_width=True, key="plot_8")

# ==========================================================
# TAB 3 — OPERATIONAL BOTTLENECKS & HIGH-DEMAND AREAS
# ==========================================================
with tab3:
    st.header("Operational Bottlenecks & High-Demand Areas")

    ward_counts = df.groupby("Ward")["patient_id"].nunique()
    highest_ward = ward_counts.idxmax()
    highest_ward_val = ward_counts.max()

    los_df2 = df.dropna(subset=["Discharge_Date"]).copy()
    los_df2["LOS"] = (los_df2["Discharge_Date"] - los_df2["Admission_Date"]).dt.days
    los_by_dept = los_df2.groupby("Department_Name")["LOS"].mean().sort_values(ascending=False)
    highest_los_dept = los_by_dept.index[0] if len(los_by_dept) else "N/A"

    avg_billing = round(df["Total_Amount"].mean(), 2)

    c1, c2, c3 = st.columns(3)
    c1.metric("Highest Patient Volume (Ward)", f"{highest_ward_val} ({highest_ward})")
    c2.metric("Highest Avg LOS Department", highest_los_dept)
    c3.metric("Average Billing", f"₹{avg_billing:,.0f}")

    col1, col2 = st.columns(2)
    with col1:
        ward_vol = ward_counts.sort_values(ascending=True).reset_index()
        ward_vol.columns = ["Ward", "Patients"]
        fig = px.bar(ward_vol, x="Patients", y="Ward", orientation="h", title="Number of Patients by Ward")
        st.plotly_chart(fig, use_container_width=True, key="plot_9")
    with col2:
        beds_unique2 = df.drop_duplicates(subset="Bed_Id")
        ward_status = beds_unique2.groupby(["Ward", "Bed_Status"]).size().reset_index(name="Count")
        fig = px.bar(ward_status, x="Count", y="Ward", color="Bed_Status", orientation="h",
                     title="Bed Availability by Ward", barmode="stack")
        st.plotly_chart(fig, use_container_width=True, key="plot_10")

    col3, col4 = st.columns(2)
    with col3:
        los_chart = los_by_dept.sort_values(ascending=True).reset_index()
        los_chart.columns = ["Department_Name", "Avg_LOS"]
        fig = px.bar(los_chart, x="Avg_LOS", y="Department_Name", orientation="h", title="Average Length of Stay by Department")
        st.plotly_chart(fig, use_container_width=True, key="plot_11")
    with col4:
        billing_by_dept = df.groupby("Department_Name")["Total_Amount"].mean().sort_values(ascending=True).reset_index()
        billing_by_dept.columns = ["Department_Name", "Avg_Billing"]
        fig = px.bar(billing_by_dept, x="Avg_Billing", y="Department_Name", orientation="h", title="Average Billing by Department")
        st.plotly_chart(fig, use_container_width=True, key="plot_12")

# ==========================================================
# TAB 4 — RESOURCE OVERVIEW
# ==========================================================
with tab4:
    st.header("Resource Overview")

    beds_resource = df.drop_duplicates(subset="Bed_Id").copy()
    total_beds = len(beds_resource)
    occupied_beds = int((beds_resource["Bed_Status"] == "Occupied").sum())
    available_beds = int((beds_resource["Bed_Status"] == "Available").sum())
    occupancy_rate = round((occupied_beds / total_beds) * 100, 2) if total_beds else 0

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Total Beds", total_beds)
    r2.metric("Occupied Beds", occupied_beds)
    r3.metric("Available Beds", available_beds)
    r4.metric("Bed Occupancy Rate", f"{occupancy_rate:.2f}%")

    col1, col2 = st.columns(2)
    with col1:
        status_counts = beds_resource["Bed_Status"].value_counts().reindex(
            ["Occupied", "Available", "Cleaning", "Reserved"], fill_value=0
        ).reset_index()
        status_counts.columns = ["Bed_Status", "Count"]
        fig = px.bar(status_counts, x="Bed_Status", y="Count",
                     title="Bed Status Distribution")
        st.plotly_chart(fig, use_container_width=True, key="plot_13")

    with col2:
        occupied_by_ward = (
            beds_resource[beds_resource["Bed_Status"] == "Occupied"]
            .groupby("Ward")["Bed_Id"].nunique()
            .sort_values(ascending=False)
            .reset_index(name="Occupied_Beds")
        )
        fig = px.bar(
            occupied_by_ward.sort_values("Occupied_Beds", ascending=True),
            x="Occupied_Beds", y="Ward", orientation="h",
            title="Occupied Beds By Ward"
        )
        st.plotly_chart(fig, use_container_width=True, key="plot_14")

    col3, col4 = st.columns(2)
    with col3:
        available_by_ward = (
            beds_resource[beds_resource["Bed_Status"] == "Available"]
            .groupby("Ward")["Bed_Id"].nunique()
            .sort_values(ascending=False)
            .reset_index(name="Available_Beds")
        )
        fig = px.bar(
            available_by_ward.sort_values("Available_Beds", ascending=True),
            x="Available_Beds", y="Ward", orientation="h",
            title="Available Beds By Ward"
        )
        st.plotly_chart(fig, use_container_width=True, key="plot_15")

    with col4:
        capacity_by_ward = (
            beds_resource.groupby("Ward")
            .agg(Total_Beds=("Bed_Id", "nunique"),
                 Occupied_Beds=("Bed_Status", lambda x: (x == "Occupied").sum()))
            .reset_index()
        )
        capacity_by_ward["Utilization_%"] = (
            capacity_by_ward["Occupied_Beds"] /
            capacity_by_ward["Total_Beds"].replace(0, pd.NA) * 100
        ).fillna(0).round(1)

        fig = px.bar(
            capacity_by_ward.sort_values("Utilization_%", ascending=True),
            x="Utilization_%", y="Ward", orientation="h",
            title="Overall Bed Capacity Utilization"
        )
        fig.update_xaxes(ticksuffix="%")
        st.plotly_chart(fig, use_container_width=True, key="plot_16")


# ==========================================================
# TAB 5 — RESOURCE UTILIZATION & WORKFORCE
# ==========================================================
with tab5:
    st.header("Resource Utilization & Workforce")

    beds_workforce = df.drop_duplicates(subset="Bed_Id").copy()
    total_beds_w = len(beds_workforce)
    occupied_beds_w = int((beds_workforce["Bed_Status"] == "Occupied").sum())
    available_beds_w = int((beds_workforce["Bed_Status"] == "Available").sum())
    bed_util_w = round((occupied_beds_w / total_beds_w) * 100, 1) if total_beds_w else 0

    total_doctors = df["Doctor_Id"].nunique()
    total_patients_w = df["patient_id"].nunique()
    patients_per_doctor = round(total_patients_w / total_doctors, 1) if total_doctors else 0

    w1, w2, w3, w4, w5 = st.columns(5)
    w1.metric("Total Doctors", total_doctors)
    w2.metric("Patients per Doctor", patients_per_doctor)
    w3.metric("Bed Utilization %", f"{bed_util_w}%")
    w4.metric("Total Beds", total_beds_w)
    w5.metric("Available Beds", available_beds_w)

    col1, col2, col3 = st.columns([1, 1.5, 1.5])
    with col1:
        doctor_workload = (
            df.groupby("Doctor_Id")["patient_id"].nunique()
            .sort_values(ascending=True).reset_index(name="Patients")
        )
        fig = px.bar(
            doctor_workload, x="Patients", y="Doctor_Id", orientation="h",
            title="Doctor Workload"
        )
        st.plotly_chart(fig, use_container_width=True, key="plot_17")

    with col2:
        bed_status_w = beds_workforce["Bed_Status"].value_counts().reset_index()
        bed_status_w.columns = ["Bed_Status", "Count"]
        fig = px.pie(
            bed_status_w, names="Bed_Status", values="Count",
            hole=0.55, title="Bed Status Distribution"
        )
        st.plotly_chart(fig, use_container_width=True, key="plot_18")

    with col3:
        shift_col = next(
            (c for c in ["Shift", "shift", "Admission_Shift", "admission_shift"]
             if c in df.columns), None
        )
        if shift_col:
            shift_counts = df[shift_col].value_counts().reset_index()
            shift_counts.columns = ["Shift", "Count"]
            fig = px.pie(
                shift_counts, names="Shift", values="Count",
                hole=0.55, title="Patient Workload by Shift"
            )
            st.plotly_chart(fig, use_container_width=True, key="plot_19")
        else:
            st.info("Shift data is not available in the current dataset.")

    st.subheader("Bed Status by Ward")
    ward_status_w = (
        beds_workforce.groupby(["Ward", "Bed_Status"])
        .size().reset_index(name="Count")
    )
    fig = px.bar(
        ward_status_w, x="Count", y="Ward", color="Bed_Status",
        orientation="h", title="Bed Status by Ward", barmode="stack"
    )
    st.plotly_chart(fig, use_container_width=True, key="plot_20")


# ==========================================================
# TAB 6 — CAPACITY & OVERLOAD ANALYSIS
# ==========================================================
with tab6:
    st.header("Capacity & Overload Analysis")

    beds_unique3 = df.drop_duplicates(subset="Bed_Id")
    dept_util = beds_unique3.groupby("Department_Name").apply(
        lambda x: round((x["Bed_Status"].eq("Occupied").sum() / len(x)) * 100, 1)
    ).reset_index(name="Bed_Utilization_%")

    dept_doctors = df.groupby("Department_Name").agg(
        Patients=("patient_id", "nunique"),
        Doctors=("Doctor_Id", "nunique")
    ).reset_index()
    dept_doctors["Patients_per_Doctor"] = (
        dept_doctors["Patients"] / dept_doctors["Doctors"].replace(0, pd.NA)
    ).fillna(0).round(1)
    combined = dept_util.merge(dept_doctors, on="Department_Name")

    overall_util = round(beds_unique3["Bed_Status"].eq("Occupied").mean() * 100, 1) if len(beds_unique3) else 0
    high_util_count = int((combined["Bed_Utilization_%"] >= 60).sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Bed Utilization %", f"{overall_util}%")
    c2.metric("Highest Dept Utilization %", f"{combined['Bed_Utilization_%'].max()}%" if len(combined) else "0%")
    c3.metric("Avg Patients per Doctor", round(dept_doctors["Patients_per_Doctor"].mean(), 1) if len(dept_doctors) else 0)
    c4.metric("High Utilization Depts (>=60%)", high_util_count)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            combined.sort_values("Bed_Utilization_%", ascending=True),
            x="Bed_Utilization_%", y="Department_Name", orientation="h",
            title="Bed Utilization % by Department"
        )
        fig.add_vline(x=60, line_dash="dash", line_color="red", annotation_text="Benchmark 60%")
        fig.update_xaxes(ticksuffix="%")
        st.plotly_chart(fig, use_container_width=True, key="plot_21")

    with col2:
        fig = px.scatter(
            combined, x="Bed_Utilization_%", y="Patients_per_Doctor",
            text="Department_Name", color="Department_Name",
            title="Bed Utilization % vs Patients per Doctor"
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True, key="plot_22")

    st.subheader("Bed Type Breakdown by Department")
    bt = beds_unique3.groupby(["Department_Name", "Bed_Type"]).apply(
        lambda x: round((x["Bed_Status"].eq("Occupied").sum() / len(x)) * 100, 1)
    ).reset_index(name="Utilization_%")
    pivot_bt = bt.pivot(index="Department_Name", columns="Bed_Type", values="Utilization_%")
    st.dataframe(
        pivot_bt.style.background_gradient(
            cmap="RdYlGn_r", axis=None, vmin=0, vmax=100
        ).format("{:.1f}%", na_rep="-"),
        use_container_width=True
    )


# ==========================================================
# TAB 7 — GEOGRAPHICAL ANALYSIS
# ==========================================================
with tab7:
    st.header("Geographical Analysis")

    total_states = df["state"].nunique()
    total_cities = df["city"].nunique()
    avg_per_state = round(df["patient_id"].nunique() / total_states, 1) if total_states else 0
    state_patient_counts = df.groupby("state")["patient_id"].nunique()
    high_demand_states = int((state_patient_counts > avg_per_state).sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total States", total_states)
    c2.metric("Total Cities", total_cities)
    c3.metric("Avg Patients per State", avg_per_state)
    c4.metric("High Demand States", high_demand_states)

    col1, col2 = st.columns(2)
    with col1:
        state_vol = state_patient_counts.sort_values(ascending=True).reset_index()
        state_vol.columns = ["State", "Patients"]
        fig = px.bar(state_vol, x="Patients", y="State", orientation="h", title="Patient Volume by State")
        st.plotly_chart(fig, use_container_width=True, key="plot_23")
    with col2:
        city_vol = df.groupby("city")["patient_id"].nunique().sort_values(ascending=False).head(10).sort_values(ascending=True).reset_index()
        city_vol.columns = ["City", "Patients"]
        fig = px.bar(city_vol, x="Patients", y="City", orientation="h", title="Top 10 Cities by Patient Volume")
        st.plotly_chart(fig, use_container_width=True, key="plot_24")

    col3, col4 = st.columns(2)
    with col3:
        top10_states = state_patient_counts.sort_values(ascending=False).head(10).index.tolist()
        beds_unique4 = df.drop_duplicates(subset="Bed_Id")
        bt_state = beds_unique4[beds_unique4["state"].isin(top10_states)].groupby(["state", "Bed_Type"]).size().reset_index(name="Count")
        fig = px.bar(bt_state, x="Count", y="state", color="Bed_Type", orientation="h",
                     title="Bed Type Demand by State (Top 10)", barmode="stack")
        st.plotly_chart(fig, use_container_width=True, key="plot_25")
    with col4:
        gdf = df[df["state"].isin(top10_states)].drop_duplicates(subset="patient_id")
        gender_state = gdf.groupby(["state", "gender"]).size().reset_index(name="Count")
        gender_state["Percent"] = gender_state.groupby("state")["Count"].transform(lambda x: round(x / x.sum() * 100, 1))
        fig = px.bar(gender_state, x="Percent", y="state", color="gender", orientation="h",
                     title="Gender Distribution by State (Top 10, %)", barmode="stack")
        fig.update_xaxes(ticksuffix="%")
        st.plotly_chart(fig, use_container_width=True, key="plot_26")


# ==========================================================
# TAB 8 — EXECUTIVE SUMMARY
# ==========================================================
with tab8:
    st.header("Executive Summary")

    # Filters mirror the Power BI executive page.
    f1, f2, f3 = st.columns(3)
    exec_years = sorted(df["Admission_Date"].dt.year.dropna().unique().tolist())
    exec_year = f1.selectbox("Year", options=["All"] + exec_years, key="exec_year")
    exec_gender = f2.selectbox(
        "Gender", options=["All"] + sorted(df["gender"].dropna().unique().tolist()),
        key="exec_gender"
    )
    exec_dept = f3.selectbox(
        "Department_Name",
        options=["All"] + sorted(df["Department_Name"].dropna().unique().tolist()),
        key="exec_dept"
    )

    edf = df.copy()
    if exec_year != "All":
        edf = edf[edf["Admission_Date"].dt.year == exec_year]
    if exec_gender != "All":
        edf = edf[edf["gender"] == exec_gender]
    if exec_dept != "All":
        edf = edf[edf["Department_Name"] == exec_dept]

    e_beds = edf.drop_duplicates(subset="Bed_Id")
    e_total_adm = edf["Admission_Id"].nunique()
    e_bed_util = round(
        e_beds["Bed_Status"].eq("Occupied").mean() * 100, 1
    ) if len(e_beds) else 0
    e_los = edf.dropna(subset=["Discharge_Date"]).copy()
    e_los["LOS"] = (e_los["Discharge_Date"] - e_los["Admission_Date"]).dt.days
    e_avg_los = round(e_los["LOS"].mean(), 2) if len(e_los) else 0
    e_avg_bill = round(edf["Total_Amount"].mean(), 0) if len(edf) else 0
    e_doctors = edf["Doctor_Id"].nunique()
    e_patients_doctor = round(edf["patient_id"].nunique() / e_doctors, 1) if e_doctors else 0

    e1, e2, e3, e4, e5 = st.columns(5)
    e1.metric("Total Admissions", e_total_adm)
    e2.metric("Bed Utilization %", f"{e_bed_util}%")
    e3.metric("Average Length Of Stay", e_avg_los)
    e4.metric("Avg Billing", f"₹{e_avg_bill:,.0f}")
    e5.metric("Average Patients Per Doctor", e_patients_doctor)

    col1, col2 = st.columns(2)
    with col1:
        ex_trend = edf.copy()
        ex_trend["Quarter"] = ex_trend["Admission_Date"].dt.to_period("Q").astype(str)
        ex_q = ex_trend.groupby("Quarter")["Admission_Id"].nunique().reset_index(name="Admissions")
        fig = px.line(ex_q, x="Quarter", y="Admissions", markers=True, title="Quarterly Admission Trend")
        st.plotly_chart(fig, use_container_width=True, key="plot_27")

    with col2:
        ex_dept = (
            edf.groupby("Department_Name")["Admission_Id"].nunique()
            .sort_values(ascending=True).reset_index(name="Admissions")
        )
        fig = px.bar(
            ex_dept, x="Admissions", y="Department_Name",
            orientation="h", title="Admissions by Department"
        )
        st.plotly_chart(fig, use_container_width=True, key="plot_28")

    col3, col4 = st.columns(2)
    with col3:
        ex_util = (
            e_beds.groupby("Department_Name")
            .apply(lambda x: round(
                x["Bed_Status"].eq("Occupied").sum() / len(x) * 100, 1
            ) if len(x) else 0)
            .reset_index(name="Bed_Utilization_%")
        )
        fig = px.bar(
            ex_util.sort_values("Bed_Utilization_%", ascending=True),
            x="Bed_Utilization_%", y="Department_Name",
            orientation="h", title="Bed Utilization By Department"
        )
        fig.update_xaxes(ticksuffix="%")
        st.plotly_chart(fig, use_container_width=True, key="plot_29")

    with col4:
        ex_gender = e_beds["Bed_Status"].value_counts().reset_index()
        ex_gender.columns = ["Bed_Status", "Count"]
        fig = px.pie(
            ex_gender, names="Bed_Status", values="Count",
            hole=0.55, title="Bed Status Distribution"
        )
        st.plotly_chart(fig, use_container_width=True, key="plot_30")


# ==========================================================
# TAB 9 — LIVE CONTROL PANEL (bed status + admission status)
# ==========================================================
with tab9:
    st.header("🔴 Live Control Panel")
    st.caption("Every change here updates the KPIs and charts across ALL tabs instantly — switch tabs after clicking to see it.")

    live1, live2 = st.columns(2)

    # ---------- BED STATUS CONTROL ----------
    with live1:
        st.subheader("Bed Status")
        beds_unique5 = df.drop_duplicates(subset="Bed_Id")[["Bed_Id", "Department_Name", "Bed_Type", "Bed_Status"]]
        selected_bed = st.selectbox("Select a Bed ID", options=beds_unique5["Bed_Id"].sort_values().tolist(), key="bed_select")
        bed_row = beds_unique5[beds_unique5["Bed_Id"] == selected_bed].iloc[0]
        st.write(f"**Dept:** {bed_row['Department_Name']} | **Type:** {bed_row['Bed_Type']} | **Status:** `{bed_row['Bed_Status']}`")

        def set_bed_status(bed_id, new_status):
            st.session_state.df.loc[st.session_state.df["Bed_Id"] == bed_id, "Bed_Status"] = new_status

        bcol1, bcol2 = st.columns(2)
        bcol3, bcol4 = st.columns(2)
        if bcol1.button("Mark Occupied", use_container_width=True):
            set_bed_status(selected_bed, "Occupied"); st.rerun()
        if bcol2.button("Mark Available", use_container_width=True):
            set_bed_status(selected_bed, "Available"); st.rerun()
        if bcol3.button("Mark Cleaning", use_container_width=True):
            set_bed_status(selected_bed, "Cleaning"); st.rerun()
        if bcol4.button("Mark Reserved", use_container_width=True):
            set_bed_status(selected_bed, "Reserved"); st.rerun()

    # ---------- ADMISSION STATUS CONTROL ----------
    with live2:
        st.subheader("Admission Status")
        adm_unique = df.drop_duplicates(subset="Admission_Id")[["Admission_Id", "patient_name", "Department_Name", "Admission_status"]]
        selected_adm = st.selectbox("Select an Admission ID", options=adm_unique["Admission_Id"].sort_values().tolist(), key="adm_select")
        adm_row = adm_unique[adm_unique["Admission_Id"] == selected_adm].iloc[0]
        st.write(f"**Patient:** {adm_row['patient_name']} | **Dept:** {adm_row['Department_Name']} | **Status:** `{adm_row['Admission_status']}`")

        acol1, acol2 = st.columns(2)
        if acol1.button("Mark Discharged", use_container_width=True):
            st.session_state.df.loc[st.session_state.df["Admission_Id"] == selected_adm, "Admission_status"] = "Discharged"
            st.session_state.df.loc[st.session_state.df["Admission_Id"] == selected_adm, "Discharge_Date"] = pd.Timestamp(date.today())
            st.rerun()
        if acol2.button("Mark Admitted (Re-admit)", use_container_width=True):
            st.session_state.df.loc[st.session_state.df["Admission_Id"] == selected_adm, "Admission_status"] = "Admitted"
            st.session_state.df.loc[st.session_state.df["Admission_Id"] == selected_adm, "Discharge_Date"] = pd.NaT
            st.rerun()

    st.divider()

    # ---------- LIVE SNAPSHOT ----------
    st.subheader("Live Snapshot")
    live_beds = df.drop_duplicates(subset="Bed_Id")
    live_adm = df.drop_duplicates(subset="Admission_Id")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Occupied Beds (live)", int((live_beds["Bed_Status"] == "Occupied").sum()))
    s2.metric("Available Beds (live)", int((live_beds["Bed_Status"] == "Available").sum()))
    s3.metric("Currently Admitted (live)", int((live_adm["Admission_status"] == "Admitted").sum()))
    s4.metric("Discharged (live)", int((live_adm["Admission_status"] == "Discharged").sum()))

    st.divider()
    if st.button("🔄 Reset All Data to Original"):
        df_reset = pd.read_csv("medical_operations_dashboard_cleaned.csv")
        df_reset["Admission_Date"] = pd.to_datetime(df_reset["Admission_Date"], errors="coerce")
        df_reset["Discharge_Date"] = pd.to_datetime(df_reset["Discharge_Date"], errors="coerce")
        st.session_state.df = df_reset
        st.rerun()
