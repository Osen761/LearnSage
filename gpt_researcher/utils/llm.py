from __future__ import annotations

import json
import logging
from typing import Optional, Any, Dict

from colorama import Fore, Style
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

from gpt_researcher.master.prompts import generate_subtopics_prompt
from .validators import Subtopics

# Use GoogleProvider directly
from ..llm_provider import GoogleProvider


async def create_chat_completion(
        messages: list,  # type: ignore
        model: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        stream: Optional[bool] = False,
        websocket: Any | None = None,
        llm_kwargs: Dict[str, Any] | None = None,
) -> str:
    """Create a chat completion using the Google Gemini Pro API
    Args:
        messages (list[dict[str, str]]): The messages to send to the chat completion.
            Ensure these messages are in the format expected by GoogleProvider.
        model (str, optional): The Gemini Pro model to use. Defaults to None.
        temperature (float, optional): The temperature to use. Defaults to 1.0.
        max_tokens (int, optional): The max tokens to use. Defaults to None.
        stream (bool, optional): Whether to stream the response. Defaults to False.
        websocket (WebSocket): The websocket used in the current request.
    Returns:
        str: The response from the chat completion
    """

    if model is None:
        raise ValueError("Model cannot be None")

    provider = GoogleProvider(model=model, temperature=temperature)

    response = await provider.get_chat_response(messages, stream)
    return response


async def construct_subtopics(task: str, data: str, config, subtopics: list = []) -> list:
    try:
        parser = PydanticOutputParser(pydantic_object=Subtopics)

        prompt = PromptTemplate(
            template=generate_subtopics_prompt(),
            input_variables=["task", "data", "subtopics", "max_subtopics"],
            partial_variables={
                "format_instructions": parser.get_format_instructions()},
        )

        print(f"\n🤖 Calling {config.smart_llm_model}...\n")

        temperature = config.temperature
        provider = GoogleProvider(
            model=config.smart_llm_model,
            temperature=temperature
        )

        chain = prompt | provider.llm | parser

        output = chain.invoke({
            "task": task,
            "data": data,
            "subtopics": subtopics,
            "max_subtopics": config.max_subtopics
        })

        return output

    except Exception as e:
        print("Exception in parsing subtopics : ", e)
        return subtopics
