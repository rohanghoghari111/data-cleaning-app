# 🧹 Universal Data Cleaning Pipeline

## ▶ Run Application

```bash
streamlit run app.py

**Industry-Grade, Reusable & Scalable Data Cleaning Framework (Pandas-Based)**

This project provides a **production-ready data cleaning pipeline** designed for real-world datasets (CSV, Excel, Pandas DataFrames). It is suitable for analytics, machine learning preprocessing, research datasets, ETL workflows, and dashboard applications (Streamlit, FastAPI, etc.).

---

## 🚀 Key Highlights 

* ✅ **Universal Cleaner** – Works without dataset-specific hardcoding
* ✅ **Logical Validation** – Automatically fixes unrealistic or invalid values
* ✅ **Null Normalization** – Handles missing values using industry standards
* ✅ **Data Type Enforcement** – Ensures consistent numeric, categorical, and date types
* ✅ **Business Logic Enforcement** – Automatically computes derived fields (e.g., profit)
* ✅ **Reusable Module** – `utils.py` is fully plug-and-play
* ✅ **Future-Proof Pandas Usage** – Avoids deprecated and unsafe operations

---

## 📁 Project Structure

```
project-root/
│
├── app.py          # Entry point / application usage
├── utils.py        # Core data cleaning and validation logic
└── README.md       # Project documentation
```

---

## 🧠 Design Philosophy

This pipeline goes beyond cosmetic cleaning.

It enforces:

* Logical correctness
* Statistical sanity
* Business consistency
* Machine-learning-ready formatting

The goal is **trustworthy data**, not just clean-looking data.

---

## 🔧 Core Components Explained

### 1️⃣ Textual Null Normalization

Real-world datasets represent missing values in many forms.

Handled values include:

* `""`, `" "`, `"nan"`, `"NaN"`, `"NULL"`, `"None"`, `"undefined"`, `"-"`

All such values are normalized to **`np.nan`**, ensuring a single, reliable missing-value representation.

---

### 2️⃣ Whitespace & Noise Cleaning

* Removes leading and trailing spaces
* Collapses multiple internal spaces into one
* Converts accidental string values like `"nan"` back to actual NaN

Result: clean, comparable string columns.

---

### 3️⃣ Text Standardization

* All textual columns are converted to **Title Case**
* Exception: `certificate` column (handled separately)
* Mapping-based spelling corrections are applied

Examples:

* `Amazom Prime` → `Amazon Prime`
* `Zee 5` → `Zee5`
* `Indai` → `India`

---

### 4️⃣ Certificate Validation (Rule-Based)

Allowed values:

* `U`, `UA`, `A`

Any invalid or unexpected value is automatically set to `NaN`.

This ensures regulatory and categorical consistency.

---

### 5️⃣ Numeric Conversion & Validation

Safely converts and validates the following columns (if present):

* `release_year`
* `duration_min`
* `imdb_rating`
* `budget_cr`
* `box_office_cr`
* `profit_cr`

**Validation Rules:**

* Release year must be between `1800` and `current_year + 1`
* IMDb rating must be between `0` and `10`
* Duration must be positive
* Budget and box office values must be non-negative

Invalid values are converted to `NaN` and logically imputed (median where appropriate).

---

### 6️⃣ Date Handling

Recognized date columns:

* `order_date`
* `Order Date`

Dates are converted using:

```
pd.to_datetime(errors="coerce")
```

Invalid dates are safely ignored without raising exceptions.

---

### 7️⃣ Business Logic Enforcement

When both columns are present:

```
profit_cr = box_office_cr - budget_cr
```

This guarantees consistency for derived business metrics.

---

### 8️⃣ Final Data Type Enforcement

* `release_year` → `Int64`
* `duration_min` → `Int64`
* `imdb_rating` → Rounded to 1 decimal place

This ensures compatibility with ML models, BI tools, and databases.

---

### 9️⃣ Deduplication

* Removes exact duplicate rows
* Resets index after cleaning

Result: a clean and reliable dataset.

---

## 🔄 Full Cleaning Pipeline

The `full_clean_pipeline(df)` function executes all steps in the correct order:

1. Normalize textual nulls
2. Clean whitespace
3. Standardize text fields
4. Convert and validate numeric columns
5. Convert date columns
6. Enforce business logic
7. Remove duplicate rows
8. Finalize data types

A single function call produces a **production-ready dataset**.

---

## 📊 Reporting Utilities

### Data Type Table

Returns a column-to-datatype mapping for schema audits and documentation.

### Cleaning Summary Report

Provides before-vs-after metrics for:

* Total missing values
* Duplicate row count

This improves transparency and explainability.

---

## 🧪 Supported Use Cases

* Data science preprocessing
* Machine learning pipelines
* Research datasets
* Business analytics
* Streamlit dashboards
* ETL and data quality jobs

---

## ⚙️ Dependencies

* Python 3.9+
* pandas
* numpy

No heavy or unnecessary dependencies.

---

## 🏆 Quality Standard

This is **not** a demo or tutorial-level cleaner.

✔ Industry-grade
✔ Research-safe
✔ ML-ready
✔ Scalable
✔ Maintainable

---

## 📌 Recommendation

Use `utils.py` as a **core data quality layer** in every analytics, ML, or data engineering project.

> "Bad data is more dangerous than no data." — This pipeline is designed to prevent that.

---

## 👨‍💻 Author Note

This pipeline is designed using real-world dirty datasets, not idealized examples.

It can be easily extended with additional validation rules, mappings, or integrated into any frontend or backend system.
