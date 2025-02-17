import streamlit as st
import json
import openai
import os

# Load OpenAI API Key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

# Function to generate a structured lesson plan for place value

def generate_place_value_lesson(difficulty):
    stages = []
    learning_progression = [
        ("Understanding Ones, Tens, Hundreds", "Numbers live in homes: ones, tens, and hundreds."),
        ("Identifying Place Value", "Recognizing which digit represents ones, tens, or hundreds."),
        ("Grouping into Tens", "Understanding that 10 ones make a ten."),
        ("Skip Counting by Tens", "Counting by 10s to understand number patterns."),
        ("Breaking Numbers into Expanded Form", "Representing 345 as 300 + 40 + 5."),
        ("Comparing Numbers", "Understanding which numbers are greater using place value."),
        ("Building 4-digit Numbers", "Introducing thousands and how they relate to hundreds."),
        ("Adding with Place Value", "Adding numbers by breaking them into place values."),
        ("Subtracting with Place Value", "Using place value knowledge to subtract numbers."),
        ("Real-World Applications", "Using place value in money and measurements."),
    ]
    for i, (concept, story) in enumerate(learning_progression, start=1):
        stages.append({
            "story": f"Stage {i}: {story}",
            "concept": concept,
            "discussion_prompts": [
                f"How does this concept help us with numbers?",
                "Can you think of a real-world example?"
            ],
            "hands_on_activity": "Use manipulatives or drawings to explore the concept.",
            "canva_prompt": (
                f"🎨 **Canva Image Prompt - Stage {i}: {concept}**\n"
                "------------------------------------------------------------\n"
                f"1️⃣ **Scene:** The adventurers must solve a puzzle related to {concept}.\n"
                "2️⃣ **What to Include:**\n"
                "   - Characters engaging with the math concept in a fun way.\n"
                "   - Clear, labeled objects to help visualize {concept}.\n"
                "3️⃣ **Technical Details:**\n"
                "   - **Size:** 1024x1024 pixels\n"
                "   - **Format:** PNG\n"
                "   - **No Watermarks**\n"
            )
        })
    return {"stages": stages}

# Streamlit App
st.set_page_config(page_title="Math Club Lesson Generator", layout="wide")

# Sidebar for Teacher Inputs
st.sidebar.header("Generate Place Value Lesson")
lesson_difficulty = st.sidebar.selectbox("Select Difficulty Level", ["Basic", "Intermediate", "Advanced"])
if st.sidebar.button("Generate Full Lesson"):
    generated_data = generate_place_value_lesson(lesson_difficulty)
    st.session_state["lesson_data"] = generated_data
    st.session_state["uploaded_images"] = {}

# Teacher Section
st.title("Teacher Section - Lesson Planning")

if "lesson_data" in st.session_state:
    lesson_data = st.session_state["lesson_data"]
    total_stages = len(lesson_data["stages"])
    
    for i, stage_data in enumerate(lesson_data["stages"]):
        st.subheader(f"Stage {i + 1} of {total_stages}")
        
        # Display Lesson Content
        story = st.text_area(f"Story Progression (Stage {i + 1}):", stage_data["story"])
        concept = st.text_area(f"Concept Being Taught (Stage {i + 1}):", stage_data["concept"])
        discussion_prompts = st.text_area(f"Discussion Prompts (Stage {i + 1}):", "\n".join(stage_data["discussion_prompts"]))
        hands_on_activity = st.text_area(f"Hands-On Activity (Stage {i + 1}):", stage_data["hands_on_activity"])
        canva_prompt = st.text_area(f"Canva Image Prompt (Stage {i + 1}):", stage_data["canva_prompt"])
        
        # Image Upload for Each Stage
        uploaded_file = st.file_uploader(f"Upload Canva Image for Stage {i + 1}", type=["png", "jpg"], key=f"image_{i}")
        if uploaded_file is not None:
            st.session_state["uploaded_images"][i] = uploaded_file
            st.image(uploaded_file, caption=f"Uploaded Image for Stage {i + 1}", use_column_width=True)
            st.success(f"Image for Stage {i + 1} uploaded successfully!")
        
    if st.button("Save Full Lesson & Move to Kids Section"):
        final_lesson = {
            "stages": lesson_data["stages"],
            "uploaded_images": st.session_state["uploaded_images"]
        }
        with open("saved_lesson.json", "w") as f:
            json.dump(final_lesson, f)
        st.session_state["lesson_ready"] = True
        st.success("Lesson Saved! Switch to the Kids Section.")

# Kids Section
if "lesson_ready" in st.session_state and st.session_state["lesson_ready"]:
    st.title("Kids Section - Live Lesson")
    lesson_data = st.session_state["lesson_data"]
    total_stages = len(lesson_data["stages"])
    current_stage = st.session_state.get("current_stage", 0)
    stage_data = lesson_data["stages"][current_stage]
    
    st.subheader(f"Stage {current_stage + 1}")
    st.write(stage_data["story"])
    st.write("### Concept Being Taught")
    st.write(stage_data["concept"])
    
    if current_stage in st.session_state["uploaded_images"]:
        st.image(st.session_state["uploaded_images"][current_stage], caption="Lesson Image", use_column_width=True)
    
    st.write("### Discussion Prompts")
    for prompt in stage_data["discussion_prompts"]:
        st.write(f"- {prompt}")
    
    st.write("### Hands-On Activity")
    st.write(stage_data["hands_on_activity"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous Stage") and current_stage > 0:
            st.session_state["current_stage"] -= 1
    with col2:
        if st.button("Next Stage") and current_stage < total_stages - 1:
            st.session_state["current_stage"] += 1
