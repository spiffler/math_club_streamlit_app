import streamlit as st
import json
from openai import OpenAI

# Placeholder function for generating lesson script & Canva prompts using OpenAI
# Replace with actual OpenAI API integration

def generate_lesson_script(lesson_concept, difficulty):
    response = {
        "stages": [
            {
                "story": f"Welcome to the adventure of learning {lesson_concept}! Let's start our journey.",
                "canva_prompt": f"Create an engaging Canva image related to {lesson_concept} with colorful elements suitable for kids.",
                "discussion_prompts": [
                    "What do you think about this topic?",
                    "Can you find an example in real life?"
                ],
                "hands_on_activity": "Use manipulatives or drawings to explore this concept.",
                "hints": "Think about how numbers relate to real objects."
            },
            {
                "story": f"Now, let's dive deeper into {lesson_concept}! What happens next?",
                "canva_prompt": f"Create an advanced visual on Canva showcasing the next step of {lesson_concept}.",
                "discussion_prompts": [
                    "How does this connect to what we just learned?",
                    "Can you explain this in your own words?"
                ],
                "hands_on_activity": "Work in pairs to demonstrate the concept.",
                "hints": "Break the problem into smaller steps."
            }
        ]
    }
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
