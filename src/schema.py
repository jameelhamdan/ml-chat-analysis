""" Store schema formats for prompts """
import json
from attr import dataclass


@dataclass
class Prompt:
    base_prompt: str
    inputs: dict
    outputs: dict


ConversationPrompt = Prompt(
    base_prompt = """
        SYSTEM MESSAGE: 
        You must respond strictly in JSON format. Do not include extra text. 
        Every response must be a valid JSON object and not a markdown text.

        Separate system message from user message
        
        user message:"
        Analyze this conversation about difficult workplace discussions.
        1. Identify the primary topic only from common primary topics provided in Inputs
        2. Identify up to 3 key themes only from common themes provided in Inputs
        3. Evaluate user feedback score as float from 0.0 to 1.0
        4. Evaluate estimated success score as an float from 0.0 to 1.0
        "

        Return JSON formatted string: {outputs},
        
        Inputs:
        {inputs}
        {input_data}
    """,
    inputs = {
        "conversation": "string",
        "common_topics": "string[]",
        "common_themes": "string[]",
    },
    outputs = {
        "feedback_score": "float",
        "success_score": "float",
        "topic": "string",
        "themes": "string[]",
    },
)

ExtractThemesPrompt = Prompt(
    base_prompt="""
        SYSTEM MESSAGE: 
        You must respond strictly in JSON format. Do not include extra text. 
        Every response must be a valid JSON object and not a markdown text.

        Separate system message from user message

        user message:"
        Analyze the chain of conversations given one by one, for each conversation extract the most common themes in current while keeping in mind previously parsed themes given in input,
        And return them as json with an array inside based on outputs format

        Return JSON formatted string: {outputs},

        Inputs:
        {inputs}
        {input_data}
    """,
    inputs={
        "conversation": "string",
        "previous": "string[]",
    },
    outputs={
        "values": "string[]",
    },
)

ExtractTopicsPrompt = Prompt(
    base_prompt="""
        SYSTEM MESSAGE: 
        You must respond strictly in JSON format. Do not include extra text. 
        Every response must be a valid JSON object and not a markdown text.

        Separate system message from user message

        user message:"
        Analyze the chain of conversations given one by one, for each conversation extract the most common topics in current while keeping in mind previously parsed topics given in input,
        And return them as json with an array inside based on outputs format

        Return JSON formatted string: {outputs},

        Inputs:
        {inputs}
        {input_data}
    """,
    inputs={
        "conversation": "string",
        "previous": "string[]",
    },
    outputs={
        "values": "string[]",
    },
)
