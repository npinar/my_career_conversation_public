import gradio as gr
import os
from dotenv import load_dotenv

load_dotenv(override=True)
hf_token = os.getenv("HF_READ_TOKEN")

with gr.Blocks() as demo:
    
    # Load your Space dynamically inside the container
    gr.load(name="npinar/my_career_conversation", src="spaces", token=hf_token)

if __name__ == "__main__":
    demo.launch()