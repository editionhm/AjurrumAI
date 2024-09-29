"""
    This script implements the Iteration of Thought (IoT) and Generative Iteration of Thought (GIoT) models.
"""
import interact
import time
import signal

from typing import Optional

class IterationOfThought:
    """
    Class for performing Iteration of Thought (IoT)
    """
    def __init__(self, max_iterations: int = 5, timeout: int = 30, temperature: float = 0.5):
        self.max_iterations = max_iterations
        self.timeout = timeout
        self.temperature = temperature 

    def inner_dialogue_agent(self, query: str, previous_response: str) -> str:
        prompt = (
            f"Given the original query: '{query}' and the previous response: '{previous_response}', "
            "generate an instructive and context-specific prompt to refine and improve the answer. "
            "Ensure that the new prompt encourages deeper reasoning or addresses any gaps in the previous response."
        )
        return interact.generate_llm(prompt)

    def llm_agent(self, query: str, prompt: str) -> str:
        full_prompt = f"Query: {query}\nPrompt: {prompt}\nResponse:"
        return interact.generate_llm(full_prompt)

    def stopping_criterion(self, response: str) -> bool:
        lower_response = response.lower()
        return any(
            keyword in lower_response
            for keyword in [
                "answer:",
                "final answer:",
                "conclusion:",
                "summary:",
                "the answer is:",
            ]
        )

    def aiot(self, query: str) -> str:
        current_response = self.llm_agent(query, "Initial Prompt")  
        for iteration in range(1, self.max_iterations + 1):
            if self.stopping_criterion(current_response):
                break
            new_prompt = self.inner_dialogue_agent(query, current_response)
            current_response = self.llm_agent(query, new_prompt)
            #time.sleep(self.timeout)
        return current_response
      
def timeout_handler(signum, frame):
    raise TimeoutError("Process took too long")

def run_iot(iot: IterationOfThought, query: str) -> str:
    result = iot.aiot(query)
    return result
