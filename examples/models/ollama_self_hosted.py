import asyncio

from browser_use import Agent, ChatOllama


async def main():
	# Connect to local Ollama instance running on default port (11434)
	# For self-hosted setups, llama3.1:8b, qwen2.5:7b, or llama3.2-vision:11b are recommended.
	llm = ChatOllama(
		model='llama3.1:8b',
		num_ctx=32768,  # Larger context window for DOM processing
	)

	agent = Agent(
		task='Go to https://news.ycombinator.com and find the top headline',
		llm=llm,
	)

	result = await agent.run()
	print('Final Result:', result.final_result())


if __name__ == '__main__':
	asyncio.run(main())
