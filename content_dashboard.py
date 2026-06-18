import streamlit as st
import pandas as pd
import time
from content_studio import generate_learning_roadmap, generate_video_script, save_to_database

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(page_title="ParindAI Content Studio", page_icon="🎬", layout="wide")

st.title("🎬 ParindAI Content Automation Studio")
st.write("Generate structured technical roadmaps and timed video scripts instantly.")

# ==========================================
# 2. Production Parameters (The Inputs)
# ==========================================
st.markdown("### ⚙️ Content Configuration")
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input("Technical Topic:", value="Introduction to Prompt Engineering")
    audience = st.selectbox("Target Audience Level:", [
        "Absolute Beginners with zero coding experience",
        "Intermediate Users with basic tech knowledge",
        "Advanced Developers"
    ])

with col2:
    format_type = st.selectbox("Video Format & Length:", [
        "60-Second YouTube Short",
        "3-Minute Concept Explainer",
        "10-Minute Deep Dive Tutorial"
    ])
    tone = st.selectbox("Content Tone:", [
        "Energetic & Engaging",
        "Calm & Highly Technical",
        "Humorous & Relatable"
    ])

st.divider()

# ==========================================
# 3. Pipeline Execution
# ==========================================
if st.button("Generate Content Assets", type="primary"):
    
    # --- PHASE 1: NODE 1 ---
    with st.spinner("Phase 1: Synthesizing Pedagogical Roadmap..."):
        roadmap = generate_learning_roadmap(topic, audience)
        
    if not roadmap:
        st.error("⚠️ Failed to generate roadmap. Check your API limits.")
    else:
        st.success("✅ Roadmap successfully structured!")
        
        # Display the Roadmap cleanly
        st.subheader(f"🗺️ {roadmap['roadmap_title']}")
        st.info(f"**Educational Strategy:** {roadmap['audience_alignment']}")
        
        # Put the 3 steps into columns side-by-side
        step_cols = st.columns(3)
        for i, mod in enumerate(roadmap['modules']):
            with step_cols[i]:
                st.markdown(f"**Step {mod['step']}: {mod['module_title']}**")
                st.caption(f"*Objective:* {mod['core_objective']}")
                
        st.divider()
        
        # --- PHASE 2: NODE 2 ---
        with st.spinner(f"Phase 2: Drafting {format_type} Production Script... Taking a quick 3-second breath for API limits..."):
            time.sleep(3) # API Rate-Limit Protection
            script = generate_video_script(roadmap, format_type, tone)
            
        if not script:
            st.error("⚠️ Failed to generate production script.")
        else:
            
            # --- PHASE 3: DATABASE ARCHIVE ---
            with st.spinner("Archiving production assets to the Supabase cloud vault..."):
                db_success = save_to_database(topic, format_type, script)
            
            if db_success:
                st.success("✅ Production Script Ready and Saved to Cloud Library!")
            else:
                st.warning("⚠️ Production Script Ready, but Cloud Save failed (Check terminal for errors).")
            
            # Render the final output table
            st.subheader("🎥 Scene-by-Scene Breakdown")
            
            df = pd.DataFrame(script)
            df = df[['scene_number', 'estimated_time', 'visual_cues', 'audio_script']]
            df.columns = ['Scene', 'Timestamp', 'Visual & B-Roll Cues', 'Audio / Voiceover']
            
            # Use width='stretch' to fix the Streamlit deprecation warning
            st.dataframe(df, hide_index=True, width="stretch")