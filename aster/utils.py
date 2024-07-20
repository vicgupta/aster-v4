def create_prompt(role: str, content: str):
    args = {"role": role, "content": content}
    return {**args}
