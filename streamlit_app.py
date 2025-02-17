import streamlit as st
import json
import openai
import os

# Load OpenAI API Key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

# Function to generate a detailed, story-specific Canva prompt

def generate_canva_prompt(lesson_concept, difficulty, stage, story):
    return (
        f"🎨 **Canva Image Prompt for {lesson_concept} - Stage {stage}**\n"
        "------------------------------------------------------------\n"
        "1️⃣ **Story Context:**\n"
        f"   - Scene: {story}\n"
        "2️⃣ **Visual Elements to Include:**\n"
        "   - Background: The scene should reflect the adventure setting.\n"
        "   - Key Objects: Represent the core math concept using objects, characters, or symbols.\n"
        "   - Labels: Clearly mark numbers, doors, or any key interactive parts.\n"
        "   - Extra Fun Elements: Include engaging elements like an explorer, a talking animal guide, or magical effects.\n"
        "3️⃣ **Technical Specifications:**\n"
        "   - **Size:** 1024x1024 pixels for optimal display.\n"
        "   - **File Format:** PNG for high resolution.\n"
        "   - **Color Palette:** Bright and engaging for ages 6-10.\n"
        "   - **Keep High Contrast:** For readability in classroom settings.\n"
        "   - **No Watermarks:** Ensure a clean, professional look.\n"
    )

# Placeholder function for generating lesson script

def generate_lesson_script(lesson_concept, difficulty):
    response = {
        "stages": []
    }
    for stage in range(1, 4):  # Example: 3 stages
        story_text = f"Welcome to {lesson_concept}! Stage {stage} presents a new challenge where we must solve a puzzle to move forward."
        response["stages"].append({
            "story": story_text,
            "canva_prompt": generate_canva_prompt(lesson_concept, difficulty, stage, story_text),
            "discussion_prompts": [
                f"How does {lesson_concept} apply here?",
                "Can you explain this in your own words?"
            ],
            "hands_on_activity": "Use manipulatives or drawings to explore this concept.",
            "hints": "Break the problem into smaller steps."
        })
    return response

# Streamlit App
st.set_page_config(page_title="Math Club Lesson Generator", layout="wide")

# Sidebar for Teacher Inputs
st.sidebar.header("Teacher Input")
lesson_concept = st.sidebar.text_input("Enter Lesson Concept:")
difficulty = st.sidebar.text_input("Enter Difficulty Level:")

generated_data = None

if st.sidebar.button("Generate Lesson"):
    if lesson_concept and difficulty:
        generated_data = generate_lesson_script(lesson_concept, difficulty)
        st.session_state["lesson_data"] = generated_data
        st.session_state["current_stage"] = 0
        st.session_state["uploaded_images"] = {}
    else:
        st.sidebar.error("Please enter both Lesson Concept and Difficulty Level.")

# Teacher Section
st.title("Teacher Section - Lesson Preparation")

if "lesson_data" in st.session_state and "current_stage" in st.session_state:
    lesson_data = st.session_state["lesson_data"]
    current_stage = st.session_state["current_stage"]
    total_stages = len(lesson_data["stages"])
    
    stage_data = lesson_data["stages"][current_stage]
    
    st.subheader(f"Stage {current_stage + 1} of {total_stages}")
    
    # Display Lesson Content
    story = st.text_area("Story Setup:", stage_data["story"])
    canva_prompt = st.text_area("Canva Image Prompt:", stage_data["canva_prompt"])
    discussion_prompts = st.text_area("Discussion Prompts:", "\n".join(stage_data["discussion_prompts"]))
    hands_on_activity = st.text_area("Hands-On Activity:", stage_data["hands_on_activity"])
    hints = st.text_area("Hints:", stage_data["hints"])
    
    # Image Upload for Current Stage
    uploaded_file = st.file_uploader("Upload Canva Image for this Stage", type=["png", "jpg"])
    if uploaded_file is not None:
        st.session_state["uploaded_images"][current_stage] = uploaded_file
        st.success("Image uploaded successfully!")
    
    # Navigation Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous") and current_stage > 0:
            st.session_state["current_stage"] -= 1
    with col2:
        if st.button("Next") and current_stage < total_stages - 1:
            st.session_state["current_stage"] += 1

    if st.button("Save Lesson"):
        final_lesson = {
            "stages": lesson_data["stages"],
            "uploaded_images": st.session_state["uploaded_images"]
        }
        with open("saved_lesson.json", "w") as f:
            json.dump(final_lesson, f)
        st.success("Lesson Saved Successfully!")

    if st.button("Start Lesson"):
        st.session_state["lesson_ready"] = True
        st.success("Lesson is ready! Switch to Kids Section to start.")

# Kids Section
st.title("Kids Section - Live Lesson")
if "lesson_ready" in st.session_state and st.session_state["lesson_ready"]:
    current_stage = st.session_state.get("current_stage", 0)
    lesson_data = st.session_state["lesson_data"]
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
        if st.button("Next Stage") and current_stage < len(lesson_data["stages"]) - 1:
            st.session_state["current_stage"] += 1
