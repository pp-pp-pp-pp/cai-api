
from characterai import aiocai
import asyncio
import nest_asyncio
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from pydantic import ValidationError

nest_asyncio.apply()

async def main():
    char = 'LCMaBNdFrilQh7TOq8R1Z9h-D1D0nMKbbMoJxG2R4TA' # gigachad character by default :3
    client = aiocai.Client('980e930fe896d0c965b8657d1eca275910ac8ff1') # get this from the tutorial
    
    me = await client.get_me()
    chat_history = []
    initial_message_received = False  # Flag to track the initial welcome message

    while True:
        try:
            async with await client.connect() as chat:
                if not initial_message_received:
                    new, answer = await chat.new_chat(char, me.id)
                    print(f'{answer.name}: {answer.text}')
                    chat_history.append((answer.name, answer.text))
                    initial_message_received = True
                
                if chat_history:
                    # Summarize the chat history
                    history_text = '\n'.join([f'{name}: {text}' for name, text in chat_history])
                    summary_prompt = f"Conversation so far:\n{history_text}\nRespond to the last massage in that context to continue."
                    
                    # # Debugging step: print the context about to be reloaded
                    # print("\n--- Context About to be Reloaded ---")
                    # print(summary_prompt)
                    # print("------------------------------------\n")

                    try:
                        message = await chat.send_message(char, new.chat_id, summary_prompt)
                        print(f'{message.name}: {message.text}')
                    except ValidationError as ve:
                        print(f"ValidationError: {ve}")
                        print(f"Problematic input: {summary_prompt}")
                        continue
                
                while True:
                    text = input('USER: ')
                    chat_history.append(('USER', text))
                    try:
                        message = await chat.send_message(char, new.chat_id, text)
                        print(f'{message.name}: {message.text}')
                        chat_history.append((message.name, message.text))
                    except ValidationError as ve:
                        print(f"ValidationError: {ve}")
                        print(f"Problematic input: {text}")
                        # Include the failed user message in the history
                        chat_history.append((text))
                        continue
        
        except (ConnectionClosedError, ConnectionClosedOK) as e:
            # print("Connection was closed. Attempting to reconnect...")
            # print(f"Error: {e}")
            await asyncio.sleep(1)  # Delay reconnection to prevent rate limiting

asyncio.run(main())
