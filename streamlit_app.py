import streamlit as st
import json
import openai
import os

# Load OpenAI API Key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

# Function to generate a detailed, structured lesson plan with a full story progression

def generate_full_lesson(lesson_concept, difficulty):
    stages = []
    for stage in range(1, 15):  # Generate 14-15 structured stages
        story_text = f"**Stage {stage}:** The explorers arrive at a new challenge in {lesson_concept}. They must solve a puzzle to move forward!"
        canva_prompt = (
            f"🎨 **Canva Image Prompt for {lesson_concept} - Stage {stage}**\n"
            "------------------------------------------------------------\n"
            f"1️⃣ **Scene:** {story_text}\n"
            "2️⃣ **What to Include:**\n"
            "   - A visually engaging challenge related to {lesson_concept}.\n"
            "   - Characters interacting with the puzzle to solve.\n"
            "   - Fun, age-appropriate designs to maintain engagement.\n"
            "3️⃣ **Technical Details:**\n"
            "   - **Size:** 1024x1024 pixels\n"
            "   - **Format:** PNG\n"
            "   - **No Watermarks**\n"
        )
        stages.append({
            "story": story_text,
            "canva_prompt": canva_prompt,
            "discussion_prompts": [
                f"How does this challenge relate to {lesson_concept}?",
                "Can you think of another way to solve this puzzle?"
            ],
            "hands_on_activity": "Use manipulatives or drawings to demonstrate understanding.",
            "hints": "Think step by step—what should come first?"
        })
    return {"stages": stages}

# Streamlit App
st.set_page_config(page_title="Math Club Lesson Generator", layout="wide")

# Sidebar for Teacher Inputs
st.sidebar.header("Teacher Input")
lesson_concept = st.sidebar.text_input("Enter Lesson Concept:")
difficulty = st.sidebar.text_input("Enter Difficulty Level:")

generated_data = None
if st.sidebar.button("Generate Full Lesson"):
    if lesson_concept and difficulty:
        generated_data = generate_full_lesson(lesson_concept, difficulty)
        st.session_state["lesson_data"] = generated_data
        st.session_state["uploaded_images"] = {}
    else:
        st.sidebar.error("Please enter both Lesson Concept and Difficulty Level.")

# Teacher Section
st.title("Teacher Section - Lesson Planning")

if "lesson_data" in st.session_state:
    lesson_data = st.session_state["lesson_data"]
    total_stages = len(lesson_data["stages"])
    
    for i, stage_data in enumerate(lesson_data["stages"]):
        st.subheader(f"Stage {i + 1} of {total_stages}")
        
        # Display Lesson Content
        story = st.text_area(f"Story Setup (Stage {i + 1}):", stage_data["story"])
        canva_prompt = st.text_area(f"Canva Image Prompt (Stage {i + 1}):", stage_data["canva_prompt"])
        discussion_prompts = st.text_area(f"Discussion Prompts (Stage {i + 1}):", "\n".join(stage_data["discussion_prompts"]))
        hands_on_activity = st.text_area(f"Hands-On Activity (Stage {i + 1}):", stage_data["hands_on_activity"])
        hints = st.text_area(f"Hints (Stage {i + 1}):", stage_data["hints"])
        
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
