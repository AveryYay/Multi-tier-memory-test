from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import OpenAIBackendRole


def read_from_long_term_memory():
    with open("tartaglia_persona", "r", encoding="utf-8") as file:
        char_persona = file.read()
        long_term = BaseMessage.make_assistant_message(
            role_name="Assistant",
            content=char_persona,
        )
        tartaglia.update_memory(long_term, OpenAIBackendRole.SYSTEM)

def summarize():
    summary_prompt = (
        "Please summarize the conversation so far focusing on key "
        "events, decisions, and character traits. Keep it to "
        "three concise sentences."
    )
    summary = tartaglia.step(summary_prompt).msgs[0].content
    return summary

tartaglia = ChatAgent(
    system_message="You are role playing tartaglia. Stay in character "
                   "throughout the conversation."
)
read_from_long_term_memory()


turn_count = 0
summary_interval = 10
while True:
    user_input = input("Traveler: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = tartaglia.step(user_input).msgs[0].content
    print(f"Tartaglia: {response}")
    turn_count += 2

    if turn_count >= summary_interval:
        summary = summarize()
        print("\n--- Conversation Summary ---")
        print(summary)
        print("----------------------------\n")
        tartaglia.reset()

        tartaglia.update_memory(
            BaseMessage.make_assistant_message(
            role_name="Assistant",
            content=summary,
            ),
            OpenAIBackendRole.SYSTEM
        )

        turn_count = 0
