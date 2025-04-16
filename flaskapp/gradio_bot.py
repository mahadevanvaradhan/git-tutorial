import gradio as gr
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv() 

# Environment variables
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
NEWS_MCP_SERVER_URL = f"http://localhost:9001/sse"
GRADIO_SERVER_PORT = os.getenv('GRADIO_SERVER_PORT', '7860')  

# Model lists
ANTHROPIC_MODELS = [
    "claude-3-7-sonnet-20250219",
    "claude-3-5-sonnet-20241022",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307"
]
OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5-turbo"
]

# Global agent cache
agent_cache = {}

def setup_agent(llm_provider: str, model: str):
    if f"{llm_provider}:{model}" not in agent_cache:
        server_1 = MCPServerHTTP(url=NEWS_MCP_SERVER_URL)
        agent_id = f"{llm_provider}:{model}"
        agent_cache[agent_id] = Agent(agent_id, mcp_servers=[server_1])
    return agent_cache[f"{llm_provider}:{model}"]

async def process_query(query: str, llm_provider: str, model: str):
    agent = setup_agent(llm_provider, model)
    try:
        async with agent.run_mcp_servers():
            result = await agent.run(query)
            response = str(result.data)
            reasoning = "Reasoning not available"
        return response, reasoning
    except Exception as e:
        return f"An error occurred: {str(e)}", "Error occurred during processing"

def chat_handler(message, history, llm_provider, model):
    timestamp = datetime.now().strftime("%H:%M:%S")
    # Add user message to history using dictionary format
    history.append({
        "role": "user",
        "content": f"**User** ({timestamp}): {message}"
    })
    
    # Process query
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        response, reasoning = loop.run_until_complete(process_query(message, llm_provider, model))
        assistant_timestamp = datetime.now().strftime("%H:%M:%S")
        response_text = f"**Assistant** ({assistant_timestamp}): {response}"
        if reasoning != "Reasoning not available":
            response_text += f"\n\n**Reasoning**: {reasoning}"
        
        # Add assistant response using dictionary format
        history.append({
            "role": "assistant",
            "content": response_text
        })
    except Exception as e:
        history.append({
            "role": "assistant",
            "content": f"**Error** ({timestamp}): {str(e)}"
        })
    finally:
        loop.close()
    
    return history

def clear_history():
    return []

with gr.Blocks(title="MCP Gradio Chatbot", css=".gradio-container {background-color: #E3E4FA !important;} .clear-btn {background-color: #FF6347 !important; color: white !important;}") as demo:
    gr.Markdown("# MCP Gradio Chatbot")  
    
    with gr.Row():
        with gr.Column(scale=1):
            llm_provider = gr.Dropdown(
                choices=["anthropic", "openai"],
                label="LLM Provider",
                value="anthropic"
            )
            model = gr.Dropdown(
                choices=ANTHROPIC_MODELS,
                label="Model",
                value=ANTHROPIC_MODELS[0]
            )
            def update_models(provider):
                return gr.update(choices=ANTHROPIC_MODELS if provider == "anthropic" else OPENAI_MODELS)
            llm_provider.change(update_models, inputs=llm_provider, outputs=model)
            
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Chat History", type="messages")  # Added type="messages"
            msg = gr.Textbox(label="Your message", placeholder="Ask something...")
            clear = gr.Button("Clear Chat History", elem_classes="clear-btn")
            
    
    # Handle message submission
    msg.submit(
        chat_handler,
        inputs=[msg, chatbot, llm_provider, model],
        outputs=[chatbot]
    )
    
    # Handle clear button
    clear.click(
        clear_history,
        inputs=None,
        outputs=chatbot
    )
# Launch with specific port
demo.launch(server_name="0.0.0.0", 
        server_port=int(GRADIO_SERVER_PORT),
        share=False)