import streamlit as st
import pandas as pd
from utils import *

st.set_page_config(page_title="Professional Data Cleaner", layout="wide")
st.title("🧹 Data Cleaning & Advanced Analytics App")

if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None

uploaded_file = st.file_uploader("Upload CSV / Excel", ["csv", "xlsx"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    df_before = df_raw.copy()

    st.subheader("📄 Raw Data Preview")
    st.dataframe(df_raw, width="stretch")

    st.subheader("✍️ Manual Missing Value Imputation")
    cols_with_nan = df_raw.columns[df_raw.isnull().any()].tolist()
    manual_impute_values = {}

    if cols_with_nan:
        input_cols = st.columns(4)
        for idx, col in enumerate(cols_with_nan):
            with input_cols[idx % 4]:
                val = st.text_input(f"Fill NaN in '{col}'", key=f"impute_{col}")
                if val.strip():
                    manual_impute_values[col] = val

    c1, c2 = st.columns(2)       
    with c1:
        num_strat = st.radio("Numeric Strategy", ["Median", "Mean", "Do Not Fill"], horizontal=True)
    with c2:
        cat_strat = st.radio("Categorical Strategy", ["Mode", "Do Not Fill"], horizontal=True)

    if st.button("🚀 Run Cleaning Pipeline"):
        df = full_clean_pipeline(df_raw)

        for col, val in manual_impute_values.items():
            if col in df.columns:
                try:
                    val = float(val)
                except:
                    pass
                df[col] = df[col].fillna(val)

        if num_strat != "Do Not Fill":
            for col in df.select_dtypes(include="number"):
                fill_val = df[col].median() if num_strat == "Median" else df[col].mean()
                df[col] = df[col].fillna(fill_val)

        if cat_strat == "Mode":
            for col in df.select_dtypes(include="object"):
                if not df[col].mode().empty:
                    df[col] = df[col].fillna(df[col].mode()[0])

        st.session_state.cleaned_df = finalize_types(df)
        st.success("✅ Data Cleaning Completed")

    if st.session_state.cleaned_df is not None:
        final_df = st.session_state.cleaned_df

        st.subheader("🧼 Cleaned Data")
        st.dataframe(final_df, width="stretch")

        r1, r2 = st.columns(2)
        with r1:
            st.table(generate_report(df_before, final_df))
        with r2:
            st.dataframe(get_datatype_table(final_df), width="stretch")

        st.download_button(
            "⬇️ Download Cleaned Data",
            final_df.to_csv(index=False).encode("utf-8"),
            "cleaned_data.csv"
        )

        # ================= ADVANCED ANALYTICS ==================

        st.divider()
        st.subheader("📊 Advanced Analytics (Dynamic X–Y)")

        chart_type = st.selectbox(
            "Select Chart Type",
            ["-- Select Chart --", "Scatter Plot", "Line Chart", "Bar Chart", "Area Chart"]
        )

        if chart_type != "-- Select Chart --":
            numeric_cols = final_df.select_dtypes(include="number").columns.tolist()
            all_cols = final_df.columns.tolist()

            x_col = st.selectbox("Select X Axis", all_cols)
            y_col = st.selectbox("Select Y Axis", numeric_cols)

            if chart_type == "Scatter Plot":
                st.scatter_chart(final_df, x=x_col, y=y_col)

            elif chart_type == "Line Chart":
                st.line_chart(final_df, x=x_col, y=y_col)

            elif chart_type == "Bar Chart":
                st.bar_chart(final_df, x=x_col, y=y_col)

            elif chart_type == "Area Chart":
                st.area_chart(final_df, x=x_col, y=y_col)






