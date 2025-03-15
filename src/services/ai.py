import json
import logging
from collections import defaultdict
from typing import Iterator

from src import config
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.schema import Prompt, ConversationPrompt, ExtractThemesPrompt, ExtractTopicsPrompt
from src.services.dataset import Message, Conversation

logger = logging.getLogger(__name__)


class ConversationResult:
    feedback_score: float  # 0.0 to 1.0
    success_score: float  # 0.0 to 1.0
    topic: str
    themes: list[str]
    length: int


class PromptService:
    openai_key = config.OPENAI_API_KEY
    openai_model = config.OPENAI_API_MODEL

    @classmethod
    def prompt_template(cls, prompt: Prompt) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(
            prompt.base_prompt,
            partial_variables=dict(
                inputs=prompt.inputs,
                outputs=prompt.outputs,
            )
        )

    @classmethod
    def llm(cls) -> ChatOpenAI:
        return ChatOpenAI(openai_api_key=cls.openai_key, model_name=cls.openai_model, temperature=0.0)

    @classmethod
    def content_to_str(cls, content: list['Message']):
        return '\n'.join([
            f'{x}: {y}' for x, y in content
        ])


class ConversationService(PromptService):
    def extract_common_topics(self, conversations: Iterator[Conversation]) -> dict[str, int]:
        common_data: dict[str, int] = defaultdict(int)
        prompt = ExtractTopicsPrompt

        for conv in conversations:
            content = [*conv['inputs'], *conv['outputs']]
            chain = self.prompt_template(prompt) | self.llm()

            response = chain.invoke({
                'input_data': {
                    'conversation': self.content_to_str(content),
                    'previous': list(common_data.keys()),
                }
            })

            try:
                value = json.loads(response.content)
                for datum in value.get('values', []):
                    common_data[datum] += 1
            except Exception as e:
                logger.error(e)

        return common_data

    def extract_common_themes(self, conversations: Iterator[Conversation]) -> dict[str, int]:
        common_data: dict[str, int] = defaultdict(int)
        prompt = ExtractThemesPrompt

        for conv in conversations:
            content = [*conv['inputs'], *conv['outputs']]
            chain = self.prompt_template(prompt) | self.llm()

            response = chain.invoke({
                'input_data': {
                    'conversation': self.content_to_str(content),
                    'previous': list(common_data.keys()),
                }
            })

            try:
                value = json.loads(response.content)
                for datum in value.get('values', []):
                    common_data[datum] += 1
            except Exception as e:
                logger.error(e)

        return common_data

    def label(self, conv: Conversation, topics: list[str], themes: list[str]) -> ConversationResult:
        content = [*conv['inputs'], *conv['outputs']]
        chain = self.prompt_template(ConversationPrompt) | self.llm()
        response = chain.invoke({
            'input_data': {
                'common_topics': topics,
                'common_themes': themes,
                'conversation': self.content_to_str(content)
            }
        })

        try:
            value = json.loads(response.content)
        except Exception as e:
            value = {'response_content': response.content}
            logger.error(e)

        return {
            'length': len(conv['inputs']),
            **value,
        }
