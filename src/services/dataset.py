import json
from typing import TypedDict, Literal, Iterator


Message = tuple[str, str]


class Conversation(TypedDict):
    dataset_split: Literal["base"]
    ls_model_type: Literal["chat"]
    # Array of Role / Message
    inputs: list[Message]
    # Array of Role / Message
    outputs: list[Message]


def load_dataset_base(file_name: str) -> Iterator[dict]:
    with open(file_name, 'r') as json_file:
        for line in json_file:
            yield json.loads(line)


def load_dataset(file_name: str) -> Iterator[Conversation]:
    for record in load_dataset_base(file_name):
        metadata = record.get('metadata', {})
        inputs = [(msg['role'], msg['content']) for msg in record.get('inputs', {}).get('messages', [])]
        outputs = [(msg['role'], msg['content']) for msg in [record.get('outputs', {}).get('message', [])]]

        yield dict(
            dataset_split=metadata.get('dataset_split', 'base'),
            ls_model_type=metadata.get('ls_model_type', 'chat'),
            inputs=inputs,
            outputs=outputs,
        )
