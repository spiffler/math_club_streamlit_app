import streamlit as st
import json
from openai import OpenAI

# Placeholder function for generating lesson script & Canva prompts using OpenAI
# Replace with actual OpenAI API integration

def generate_lesson_script(lesson_concept, difficulty):
    response = {
        "story": f"Welcome to the adventure of learning {lesson_concept}! Today, we will explore it step by step.",
        "canva_prompt": f"Create an engaging Canva image related to {lesson_concept} with colorful elements suitable for kids.",
        "discussion_prompts": [
            "What do you think about this topic?",
            "Can you find an example in real life?"
        ],
        "hands_on_activity": "Use manipulatives or drawings to explore this concept.",
        "hints": "Think about how numbers relate to real objects."
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
    else:
        st.sidebar.error("Please enter both Lesson Concept and Difficulty Level.")

# Teacher Section
st.title("Teacher Section - Lesson Preparation")

if "lesson_data" in st.session_state:
    lesson_data = st.session_state["lesson_data"]
    
    # Editable Lesson Content
    story = st.text_area("Story Setup:", lesson_data["story"])
    canva_prompt = st.text_area("Canva Image Prompt:", lesson_data["canva_prompt"])
    discussion_prompts = st.text_area("Discussion Prompts:", "\n".join(lesson_data["discussion_prompts"]))
    hands_on_activity = st.text_area("Hands-On Activity:", lesson_data["hands_on_activity"])
    hints = st.text_area("Hints:", lesson_data["hints"])
    
    if st.button("Save Lesson"):
        final_lesson = {
            "story": story,
            "canva_prompt": canva_prompt,
            "discussion_prompts": discussion_prompts.split("\n"),
            "hands_on_activity": hands_on_activity,
            "hints": hints
        }
        with open("saved_lesson.json", "w") as f:
            json.dump(final_lesson, f)
        st.success("Lesson Saved Successfully!")

    if st.button("Start Lesson"):
        st.session_state["lesson_ready"] = True
        st.success("Lesson is ready! Switch to Kids Section to start.")

# Placeholder for Kids Section (To be built in the next phase)
st.title("Kids Section - Live Lesson")
if "lesson_ready" in st.session_state and st.session_state["lesson_ready"]:
    st.write("Lesson in Progress...")
    # This section will display the story, images, and discussion prompts in read-only mode.
else:
    st.write("Lesson not started yet. Go to Teacher Section to prepare the lesson.")
