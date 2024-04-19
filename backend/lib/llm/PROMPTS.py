"""
A module containing the prompts used by the model to generate the conversation.
"""

PROMPTS = {
    "CONVERSATIONAL_SYSTEM_PROMPT": {
        "text" : """You are a conversation partner who helps users learn and practice their conversational skills in english. 
The user goal is to practice english conversational skills so engage users in conversations to help them improve their listening and speaking skills and gain confidence in using the language.
The user level is {user_level} and the conversation difficulty is set to {conversation_difficulty}.
{conversation_topic}
You have to respond in an engaging, informative, and appropriate manner for the user level according to the conversation difficulty specified.
Maintain a relevant conversation but allow for natural digressions. 
Avoid sensitive topics, including harmful, unethical or illegal discussions with the user. Steer clear of controversial or potentially offensive subjects and that could harm the person you are talking with, and, in these cases, immediately steer back the conversation to the main conversation topic by telling the user that you are not allowed to talk about certain topics.
Encourage the user to continue the conversation.
The user will explicitely tell you when they want to end the conversation. 

Begin recording conversation for user review.""",
        "args": ["user_level", "conversation_difficulty", 'conversation_topic']
    },
}

def get_prompt(prompt_name: str, **kwargs) -> str:
    """Given the name of a prompt and the required arguments, return the prompt text with 
    the arguments filled in.

    :param prompt_name: name of the prompt to retrieve
    :type prompt_name: str
    :raises ValueError: if the number of arguments provided does not match the number of arguments 
                        required by the prompt
    :raises ValueError: if an argument required by the prompt is not provided
    :raises ValueError: if an argument provided is not a string
    :return: the prompt text with the arguments filled in
    :rtype: str
    """
    if len(PROMPTS.get(prompt_name).get("args")) != len(kwargs):
        raise ValueError(f"Prompt {prompt_name} requires {len(PROMPTS.get(prompt_name).get('args'))} arguments, but {len(kwargs)} were provided.")
    
    for arg in PROMPTS.get(prompt_name).get("args"):
        if arg not in kwargs:
            raise ValueError(f"Prompt {prompt_name} requires argument {arg}, but it was not provided. Provided arguments: {kwargs}")
        
        if not isinstance(kwargs.get(arg), str):
            raise ValueError(f"Argument {arg} for prompt {prompt_name} must be a string.")

    return PROMPTS.get(prompt_name).get("text").format(**kwargs)
