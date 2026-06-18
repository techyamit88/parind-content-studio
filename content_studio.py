import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from supabase import create_client, Client

# Load secure environment keys
load_dotenv()

# ==========================================
# NODE 1: The Roadmap Synthesis Engine
# ==========================================
def generate_learning_roadmap(topic, audience_level):
    print(f"\n-> [Node 1] Engaging Curriculum Designer... Structuring roadmap for: '{topic}'")
    
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    sys_instruction = """You are an elite Technical Curriculum Designer.
    Take the technical topic and break it down into a 3-step learning roadmap.
    Module 1: Mental model. Module 2: Mechanism. Module 3: Application.

    You MUST output a raw JSON object with EXACTLY this structure:
    {
        "roadmap_title": "A catchy title",
        "audience_alignment": "One sentence explanation of strategy.",
        "modules": [
            {"step": 1, "module_title": "Title 1", "core_objective": "Objective 1"},
            {"step": 2, "module_title": "Title 2", "core_objective": "Objective 2"},
            {"step": 3, "module_title": "Title 3", "core_objective": "Objective 3"}
        ]
    }
    Return raw JSON text only.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Topic: {topic}\nTarget Audience: {audience_level}",
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.4,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text.strip())
    except Exception as e:
        print(f"-> [ERROR] Node 1 failed: {e}")
        return None

# ==========================================
# NODE 2: The Script Sequence Splitter
# ==========================================
def generate_video_script(roadmap_data, video_format, tone):
    print(f"-> [Node 2] Engaging Video Producer... Translating roadmap into a {video_format} script")
    
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    sys_instruction = """You are an elite YouTube Video Producer and Scriptwriter.
    I will provide you with a 3-step pedagogical roadmap. 
    Your job is to translate this roadmap into a multi-scene production script tailored to the requested video format and tone.

    You MUST output a raw JSON array of scene objects with EXACTLY this structure:
    [
        {
            "scene_number": 1,
            "estimated_time": "0:00 - 0:15",
            "visual_cues": "Describe what the viewer sees (e.g., 'Camera on host, text graphic appears')",
            "audio_script": "The exact spoken words for the voiceover/host."
        },
        {
            "scene_number": 2,
            "estimated_time": "0:15 - 0:30",
            "visual_cues": "...",
            "audio_script": "..."
        }
    ]
    Make sure the number of scenes realistically fits the requested video format.
    Return raw JSON array text only.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Video Format: {video_format}\nTone: {tone}\nRoadmap Data:\n{json.dumps(roadmap_data, indent=2)}",
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.7, 
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text.strip())
    except Exception as e:
        print(f"-> [ERROR] Node 2 failed: {e}")
        return None

# ==========================================
# DATABASE: Supabase Integration Vault
# ==========================================
def save_to_database(topic, format_type, json_content):
    print(f"-> [Database] Archiving '{topic}' to Supabase cloud vault...")
    
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("-> [DB ERROR] Missing Supabase credentials in .env file.")
        return False
        
    try:
        supabase: Client = create_client(url, key)
        
        # Package the payload for insertion
        data_payload = {
            "topic": topic,
            "format": format_type,
            "content_data": json_content 
        }
        
        # Execute the database insert command
        response = supabase.table("generated_content").insert(data_payload).execute()
        return True
        
    except Exception as e:
        print(f"-> [DB ERROR] Failed to save to cloud: {e}")
        return False