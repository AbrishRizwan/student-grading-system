import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App Title
st.title("🎓 Student Grading & Performance Analytics System")
st.write("Upload class records or calculate individual student grades instantly.")

# Sidebar for Navigation
mode = st.sidebar.selectbox("Select Mode", ["Individual Grading", "Class Analytics (CSV Upload)"])

# Function to calculate Grade and GPA based on percentage
def calculate_grade_gpa(percentage):
    if percentage >= 85: return "A", 4.0
    elif percentage >= 75: return "B", 3.0
    elif percentage >= 65: return "C", 2.0
    elif percentage >= 50: return "D", 1.0
    else: return "F", 0.0

# --- MODE 1: INDIVIDUAL GRADING ---
if mode == "Individual Grading":
    st.subheader("📝 Individual Student Report Card")
    
    student_name = st.text_input("Student Name", "Ali")
    
    # Subject Marks Inputs
    col1, col2 = st.columns(2)
    with col1:
        stats_marks = st.number_input("Applied Statistics Marks (Out of 100)", 0, 100, 75)
        math_marks = st.number_input("Mathematics Marks (Out of 100)", 0, 100, 68)
    with col2:
        sampling_marks = st.number_input("Sampling Techniques Marks (Out of 100)", 0, 100, 82)
        law_marks = st.number_input("Introduction to Law Marks (Out of 100)", 0, 100, 55)
        
    if st.button("Generate Report Card"):
        total_marks = stats_marks + math_marks + sampling_marks + law_marks
        percentage = (total_marks / 400) * 100
        grade, gpa = calculate_grade_gpa(percentage)
        
        # Display Results
        st.success(f"### Report for {student_name}")
        st.write(f"**Total Obtained Marks:** {total_marks} / 400")
        st.write(f"**Percentage:** {percentage:.2f}%")
        st.write(f"**Final Grade:** {grade}")
        st.write(f"**GPA:** {gpa}")

# --- MODE 2: CLASS ANALYTICS ---
elif mode == "Class Analytics (CSV Upload)":
    st.subheader("📊 Class Performance Analytics")
    st.write("Upload a CSV file with columns: `Name`, `Percentage`")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Apply the grading function to the entire dataframe using Pandas
        results = df['Percentage'].apply(calculate_grade_gpa)
        df['Grade'] = [r[0] for r in results]
        df['GPA'] = [r[1] for r in results]
        
        st.write("### 📋 Processed Class Data", df)
        
        # Statistical Summary
        st.write("### 📈 Class Statistical Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Class Average Percentage", f"{df['Percentage'].mean():.2f}%")
        col2.metric("Highest Percentage", f"{df['Percentage'].max():.2f}%")
        col3.metric("Total Students Passed", f"{df[df['Grade'] != 'F'].shape[0]} / {df.shape[0]}")
        
        # Visualizing Grade Distribution (Bar Chart)
        st.write("### 📊 Grade Distribution Chart")
        grade_counts = df['Grade'].value_counts().reindex(["A", "B", "C", "D", "F"], fill_value=0)
        
        fig, ax = plt.subplots()
        grade_counts.plot(kind='bar', color=['#4CAF50', '#2196F3', '#FFC107', '#FF9800', '#F44336'], ax=ax)
        ax.set_xlabel("Grades")
        ax.set_ylabel("Number of Students")
        ax.set_title("Overall Class Grade Distribution")
        st.pyplot(fig)
        