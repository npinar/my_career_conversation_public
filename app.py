import gradio as gr
import os
import time
from dotenv import load_dotenv
from huggingface_hub import HfApi

# 1. Load environment and setup API
load_dotenv(override=True)
hf_token = os.getenv("HF_READ_TOKEN")
repo_id = "npinar/my_career_conversation"
api = HfApi(token=hf_token)

def wake_and_load(repo_id, token):
    """Checks space status and wakes it if necessary before loading."""
    print(f"Checking status of {repo_id}...")
    try:
        runtime = api.get_space_runtime(repo_id=repo_id)
        
        # If sleeping, paused, or stopped, wake it up
        if runtime.stage in ["SLEEPING", "PAUSED", "STOPPED"]:
            print(f"Space is {runtime.stage}. Sending wake-up call...")
            api.restart_space(repo_id=repo_id)
            
            # Wait for it to reach RUNNING state
            while True:
                status = api.get_space_runtime(repo_id=repo_id).stage
                if status == "RUNNING":
                    print("Space is now RUNNING!")
                    break
                print(f"Waiting for Space to start (current status: {status})...")
                time.sleep(10) # 10s wait between checks
        else:
            print(f"Space is already {runtime.stage}.")
            
    except Exception as e:
        print(f"Error checking space status: {e}")

    # 2. Load the Space (This creates the Blocks object)
    return gr.load(name=repo_id, src="spaces", token=token)

# --- Execution ---

# Ensure the target space is awake
wake_and_load(repo_id, hf_token)

# Load the private space as the main demo
demo = gr.load(name=repo_id, src="spaces", token=hf_token)

if __name__ == "__main__":
    demo.launch()