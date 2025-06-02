import asyncio
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from mcp_use import MCPAgent, MCPClient

async def main():
    # Load environment variables
    load_dotenv()

    model = os.getenv('MODEL_NAME')

    # Initialize client
    client = MCPClient.from_config_file(
        os.path.join("./configs/seismic_tools.json")
    )

    # Create LLM
    llm = ChatOllama(model=model, temperature=0.8, num_predict=4096)

    # Create agent
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    print("=== SeismicProcAgent Interactive Command Line ===")
    print("Type your query and press Enter to execute; type 'exit' or 'quit' to exit.")

    # Get current event loop
    loop = asyncio.get_event_loop()

    while True:
        # Call synchronous input() in executor to avoid blocking the event loop
        user_input = await loop.run_in_executor(
            None,
            input,
            "Please enter your query: "
        )
        user_input = user_input.strip()
        if not user_input:
            # If only Enter is pressed, prompt and continue loop
            print("⚠️ Please enter valid content, or type 'exit' to quit.")
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Program exited.")
            break

        try:
            # Call agent.run() to get the result
            result = await agent.run(user_input)
            print(f"\n{result}\n")
        except Exception as e:
            print(f"❌ Error during call: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
