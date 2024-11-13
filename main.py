import asyncio
from playwright.async_api import async_playwright, Playwright
import requests
import json
import time

# Code automatizing Facebook Messenger messages sending with the use of a local LLaMA model.


class LLamaClient:
    def __init__(self, url):
        self.base_url = url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    async def get_models(self):
        response = requests.get(f"{self.base_url}/v1/models", headers=self.headers)
        return json.loads(response.text)

    async def complete_chat(self, messages, max_tokens=1000, temperature=0.5, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
        data = {
            'messages': messages,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'frequency_penalty': frequency_penalty,
            'presence_penalty': presence_penalty
        }
        response = requests.post(f"{self.base_url}/v1/chat/completions", headers=self.headers, json=data)
        return json.loads(response.text)

    async def complete_text(self, prompt, max_tokens=1000):
        data = {
            'prompt': prompt,
            'max_tokens': max_tokens
        }
        response = requests.post(f"{self.base_url}/v1/completions", headers=self.headers, json=data)
        return json.loads(response.text)

    async def get_embeddings(self, text):
        data = {
            'text': text
        }
        response = requests.post(f"{self.base_url}/v1/embeddings", headers=self.headers, json=data)
        return json.loads(response.text)


async def read_config():
    try:
        with open('config.txt', 'r') as f:
            url = f.read().strip()
            return url
    except FileNotFoundError:
        print("Config file not found")
        raise


async def run_messenger(playwright_webkit, llama_client):
    browser = await playwright_webkit.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://www.facebook.com/messages/t/me")
    print('Launching Google Chrome browser, please log in to Facebook with it.')

    # wait for message
    while True:
        try:
            messenger_search_input = await page.wait_for_selector(".xdvlbce.xc9qbxq", timeout=900000)
            break
        except Exception as e:
            print('Facebook not loaded')

    return context, page


async def look_for_new_msg_conversation(playwright_context, llama_client, page):
    while True:
        try:
            new_message_element = await page.wait_for_selector("span.x1sibtaa.xzsf02u, span.xeuugli.xveuv9e", timeout=60000)

            print(f'Found a new message ...')
            await new_message_element.click()
            break
        except Exception as e:
            print('No message received, still looking ...')


async def receive_message(llama_client, page):
    text_spans = await page.query_selector_all('div.x1yc453h.x18lvrbx')
    if text_spans:
        last_text_span = text_spans[-1]
    else:
        print("No text messages found.")
        return None

    non_text_spans = await page.query_selector_all('.xz74otr.xmz0i5r')
    if non_text_spans:
        for span in reversed(non_text_spans):
            last_top = await last_text_span.evaluate("el => el.offsetTop")
            top = await span.evaluate("el => el.offsetTop")
            if last_top <= top:
                print("The message wasn't text. The app won't respond.")
                await page.goto("https://www.facebook.com/messages/t/me")
                return None

    message = await last_text_span.text_content()
    print('The message is: ' + message)
    return message


async def get_response(llama_client, style_of, message):
    try:
        print('Generating response ...')
        while True:
            try:
                response = await llama_client.complete_chat(
                    messages=[
                        {'role': 'system', 'content': f"You're {style_of}. you answer your private messages on "
                                                      f"Facebook Messenger."},
                        {'role': 'user', 'content': message},
                    ]
                )
                break
            except Exception as e:
                print(f'An error occurred while generating response: {e}')
                time.sleep(10)
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f'An unexpected error occurred: {e}')


async def write_fb_message(playwright_context, page, message):
    try:
        text_field = await page.query_selector('p.xdj266r')
        print(f'Writing response to messenger ...')
        await text_field.click()
        time.sleep(2.5)
        await page.keyboard.type(message, delay=0.1)
        await page.keyboard.press('Enter')

        await page.goto("https://www.facebook.com/messages/t/me")
        print('Message sent!')
    except Exception as e:
        print(f'An unexpected error occurred while sending message: {e}')


async def main():
    url = await read_config()
    llama_client = LLamaClient(url)
    async with async_playwright() as playwright:
        style_of = input('Who are we today?\n')
        print(f'Okie dokie!')
        playwright_driver = await run_messenger(playwright.chromium, llama_client)
        while True:
            try:
                await look_for_new_msg_conversation(playwright.chromium, llama_client, playwright_driver[1])
                fb_message = await receive_message(llama_client, playwright_driver[1])
                if fb_message is None:
                    continue
                message_response = await get_response(llama_client, style_of, fb_message)
                await write_fb_message(playwright.chromium, playwright_driver[1], message_response)
            except Exception as e:
                await playwright_driver[1].goto("https://www.facebook.com/messages/t/me")
                print(e)


if __name__ == "__main__":
    import sys

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print(
            "Please install the 'playwright' library. You can do this by running 'pip install playwright' in your terminal.")
        sys.exit()

    asyncio.run(main())
