import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Setup
st.set_page_config(page_title="Student Grading System", page_icon="🎓", layout="wide")

st.title("🎓 Smart Student Grading & Performance Analytics System")
st.write("Customizable grading system for any course, degree, or class batch.")

# Sidebar Navigation
mode = st.sidebar.selectbox("Select Mode", ["Individual Grading (Dynamic Subjects)", "Class Analytics (CSV Upload)"])

# Function to calculate Grade and GPA based on percentage
def calculate_grade_gpa(percentage):
    if percentage >= 85: return "A", 4.0
    elif percentage >= 75: return "B", 3.0
    elif percentage >= 65: return "C", 2.0
    elif percentage >= 50: return "D", 1.0
    else: return "F", 0.0

# --- MODE 1: DYNAMIC INDIVIDUAL GRADING ---
if mode == "Individual Grading (Dynamic Subjects)":
    st.subheader("📝 Individual Student Report Card")
    
    student_name = st.text_input("Student Name", "Abrish")
    
    st.write("### 📚 Enter Your Subjects & Marks")
    st.caption("💡 **Tip:** Table mein kisi bhi cell par double-click karke Subject Name aur Marks change karein. Niche `+` button se naya subject add karein!")
    
    # Interactive Dynamic Table Template
    default_data = pd.DataFrame([
        {"Subject": "Subject 1", "Obtained Marks": 75, "Total Marks": 100},
        {"Subject": "Subject 2", "Obtained Marks": 82, "Total Marks": 100},
        {"Subject": "Subject 3", "Obtained Marks": 68, "Total Marks": 100},
    ])
    
    # Allows adding/deleting rows dynamically
    edited_df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)
    
    if st.button("Generate Report Card", type="primary"):
        if not edited_df.empty and edited_df["Total Marks"].sum() > 0:
            total_obtained = edited_df["Obtained Marks"].sum()
            total_max = edited_df["Total Marks"].sum()
            percentage = (total_obtained / total_max) * 100
            grade, gpa = calculate_grade_gpa(percentage)
            
            st.success(f"### 🎯 Official Result for {student_name}")
            
            # Key Metrics Display
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Obtained", f"{total_obtained} / {total_max}")
            col2.metric("Overall Percentage", f"{percentage:.2f}%")
            col3.metric("Final Grade", grade)
            col4.metric("GPA", f"{gpa:.2f}")
            
            # Individual Subject Breakdown
            edited_df["Percentage"] = (edited_df["Obtained Marks"] / edited_df["Total Marks"]) * 100
            results = edited_df["Percentage"].apply(calculate_grade_gpa)
            edited_df["Subject Grade"] = [r[0] for r in results]
            edited_df["Subject GPA"] = [r[1] for r in results]
            
            st.write("#### 📊 Detailed Subject Breakdown")
            st.dataframe(edited_df, use_container_width=True)
        else:
            st.error("Please enter valid subject data before generating the report!")

# --- MODE 2: CLASS ANALYTICS ---
elif mode == "Class Analytics (CSV Upload)":
    st.subheader("📊 Class Performance Analytics")
    st.write("Upload a CSV file with columns: `Name`, `Percentage`")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        results = df['Percentage'].apply(calculate_grade_gpa)
        df['Grade'] = [r[0] for r in results]
        df['GPA'] = [r[1] for r in results]
        
        st.write("### 📋 Processed Class Data", df)
        
        st.write("### 📈 Class Statistical Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Class Average Percentage", f"{df['Percentage'].mean():.2f}%")
        col2.metric("Highest Percentage", f"{df['Percentage'].max():.2f}%")
        col3.metric("Total Students Passed", f"{df[df['Grade'] != 'F'].shape[0]} / {df.shape[0]}")
        
        st.write("### 📊 Grade Distribution Chart")
        grade_counts = df['Grade'].value_counts().reindex(["A", "B", "C", "D", "F"], fill_value=0)
        
        fig, ax = plt.subplots()
        grade_counts.plot(kind='bar', color=['#4CAF50', '#2196F3', '#FFC107', '#FF9800', '#F44336'], ax=ax)
        ax.set_xlabel("Grades")
        ax.set_ylabel("Number of Students")
        ax.set_title("Overall Class Grade Distribution")
        st.pyplot(fig)
