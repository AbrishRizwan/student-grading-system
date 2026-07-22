import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Student Grading System", page_icon="🎓", layout="wide"
)

st.title("🎓 Student Grading & Performance Analytics System")
st.write(
    "Customizable student grading system with exact grade boundaries and dynamic subject rows."
)

# Sidebar Navigation
mode = st.sidebar.selectbox(
    "Select Mode",
    ["Individual Grading (Dynamic Subjects)", "Class Analytics (CSV Upload)"],
)


# Updated Custom Grading Scale Function
def calculate_grade_gpa(percentage):
    if percentage >= 80:
        return "A", 4.0
    elif percentage >= 75:
        return "B+", 3.5
    elif percentage >= 70:
        return "B", 3.0
    elif percentage >= 65:
        return "C+", 2.5
    elif percentage >= 60:
        return "C", 2.0
    elif percentage >= 55:
        return "D+", 1.5
    elif percentage >= 50:
        return "D", 1.0
    else:
        return "F", 0.0


# --- MODE 1: INDIVIDUAL GRADING ---
if mode == "Individual Grading (Dynamic Subjects)":
    st.subheader("📝 Individual Student Report Card")

    student_name = st.text_input("Student Name", "Abrish")

    st.write("### 📚 Enter Marks for Subjects")
    st.caption(
        "💡 **Note:** Subject 1 to 5 pehle se set hain. Agar Subject 6, 7 wagera add karna chahte hain toh table ke neeche **`+` (Add row)** button par click karein."
    )

    # Default 5 Subjects with 100 Total Marks
    default_data = pd.DataFrame([
        {"Subject": "Subject 1", "Obtained Marks": 75, "Total Marks": 100},
        {"Subject": "Subject 2", "Obtained Marks": 80, "Total Marks": 100},
        {"Subject": "Subject 3", "Obtained Marks": 68, "Total Marks": 100},
        {"Subject": "Subject 4", "Obtained Marks": 72, "Total Marks": 100},
        {"Subject": "Subject 5", "Obtained Marks": 85, "Total Marks": 100},
    ])

    # Dynamic Table allowing addition/deletion of rows
    edited_df = st.data_editor(
        default_data, num_rows="dynamic", use_container_width=True
    )

    if st.button("Generate Report Card", type="primary"):
        if not edited_df.empty and edited_df["Total Marks"].sum() > 0:
            total_obtained = edited_df["Obtained Marks"].sum()
            total_max = edited_df["Total Marks"].sum()
            percentage = (total_obtained / total_max) * 100
            grade, gpa = calculate_grade_gpa(percentage)

            st.success(f"### 🎯 Official Result Card for {student_name}")

            # Key Summary Metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Obtained", f"{total_obtained} / {total_max}")
            col2.metric("Overall Percentage", f"{percentage:.2f}%")
            col3.metric("Final Grade", grade)
            col4.metric("GPA", f"{gpa:.2f}")

            # Individual Subject Breakdown with New Grading Scale
            edited_df["Percentage"] = (
                edited_df["Obtained Marks"] / edited_df["Total Marks"]
            ) * 100
            results = edited_df["Percentage"].apply(calculate_grade_gpa)
            edited_df["Subject Grade"] = [r[0] for r in results]
            edited_df["Subject GPA"] = [r[1] for r in results]

            st.write("#### 📊 Subject-wise Detailed Breakdown")
            st.dataframe(edited_df, use_container_width=True)
        else:
            st.error(
                "Please enter valid subject data before generating the report!"
            )

# --- MODE 2: CLASS ANALYTICS ---
elif mode == "Class Analytics (CSV Upload)":
    st.subheader("📊 Class Performance Analytics")
    st.write("Upload a CSV file containing columns: `Name`, `Percentage`")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        results = df["Percentage"].apply(calculate_grade_gpa)
        df["Grade"] = [r[0] for r in results]
        df["GPA"] = [r[1] for r in results]

        st.write("### 📋 Processed Class Data", df)

        st.write("### 📈 Class Statistical Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Class Average Percentage", f"{df['Percentage'].mean():.2f}%"
        )
        col2.metric("Highest Percentage", f"{df['Percentage'].max():.2f}%")
        col3.metric(
            "Total Students Passed",
            f"{df[df['Grade'] != 'F'].shape[0]} / {df.shape[0]}",
        )

        st.write("### 📊 Grade Distribution Chart")
        grade_order = ["A", "B+", "B", "C+", "C", "D+", "D", "F"]
        grade_counts = df["Grade"].value_counts().reindex(grade_order, fill_value=0)

        fig, ax = plt.subplots()
        grade_counts.plot(
            kind="bar",
            color=[
                "#4CAF50",
                "#8BC34A",
                "#2196F3",
                "#03A9F4",
                "#FFC107",
                "#FF9800",
                "#FF5722",
                "#F44336",
            ],
            ax=ax,
        )
        ax.set_xlabel("Grades")
        ax.set_ylabel("Number of Students")
        ax.set_title("Overall Class Grade Distribution")
        st.pyplot(fig)
