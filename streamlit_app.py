import streamlit as st
import json
import openai
import os

# Load OpenAI API Key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

# Function to generate a structured lesson plan for teaching place value

def generate_place_value_lesson():
    stages = [
        {
            "story": "The adventurers find an ancient scroll that speaks about numbers having 'homes.'",
            "concept": "Understanding Ones, Tens, Hundreds as 'Homes'.",
            "discussion_prompts": [
                "What do you think it means for a number to have a home?",
                "Why do we need different places for numbers?"
            ],
            "hands_on_activity": "Kids place number blocks in drawn columns (e.g., house = ones, next house = tens, etc.).",
            "canva_prompt": (
                "🎨 **Canva Image Prompt - Stage 1: Place Value Homes**\n"
                "------------------------------------------------------------\n"
                "1️⃣ **Scene:** The adventurers find a scroll showing how numbers live in different 'homes'.\n"
                "2️⃣ **What to Include:**\n"
                "   - A fun village with three houses labeled Ones, Tens, Hundreds.\n"
                "   - Number blocks floating, waiting to be placed in their homes.\n"
                "3️⃣ **Technical Details:**\n"
                "   - **Size:** 1024x1024 pixels\n"
                "   - **Format:** PNG\n"
                "   - **No Watermarks**\n"
            )
        },
        {
            "story": "They approach a magic gate that will only open if numbers are placed correctly.",
            "concept": "Identifying Place Value (Ones vs. Tens)",
            "discussion_prompts": [
                "What happens if we put a number in the wrong place?",
                "Can you think of a real-life example where place matters?"
            ],
            "hands_on_activity": "Drag or manually write numbers in correct columns.",
            "canva_prompt": (
                "🎨 **Canva Image Prompt - Stage 2: Magic Gate of Place Value**\n"
                "------------------------------------------------------------\n"
                "1️⃣ **Scene:** The adventurers face a magic gate that requires numbers in the correct place to open.\n"
                "2️⃣ **What to Include:**\n"
                "   - A mystical gate with slots labeled 'Tens' and 'Ones'.\n"
                "   - A glowing lock mechanism to indicate a puzzle to solve.\n"
                "3️⃣ **Technical Details:**\n"
                "   - **Size:** 1024x1024 pixels\n"
                "   - **Format:** PNG\n"
                "   - **No Watermarks**\n"
            )
        }
    ]
    return {"stages": stages}

# Streamlit App
st.set_page_config(page_title="Math Club Lesson Generator", layout="wide")

# Sidebar for Teacher Inputs
st.sidebar.header("Generate Place Value Lesson")
if st.sidebar.button("Generate Full Lesson"):
    generated_data = generate_place_value_lesson()
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
