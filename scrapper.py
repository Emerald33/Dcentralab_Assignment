import os
import json
from openai import OpenAI
import asyncio
from crawl4ai import *
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = openai_api_key)

def generate_response(messages, temperature=0):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

def get_completion(user_message: str, system_message: str):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    return generate_response(messages)

    
async def scrape(url: str):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
        )
        return result.markdown


if __name__ == "__main__":
    
    file_paths = ("./full_scrape.txt", "./data_dir/description.txt")
    if os.path.exists(file_paths[0]):
        os.remove(file_paths[0])
    if os.path.exists(file_paths[1]):
        os.remove(file_paths[1])

    base_url = "https://cryptorank.io/all-coins-list"

    initial_scrape = asyncio.run(scrape(base_url))

    system_message_one = """
    You are a Python program that processes the scraped HTML content of a webpage to extract cryptocurrency names and their respective URLs. 

    The content contains various cryptocurrencies and links to pages with descriptions and other relevant information. Your task is to extract the name of each coin and its corresponding URL into a valid JSON dictionary object, for the first 10 coins only.

    Additionally:
    1. The URLs in the HTML may contain invalid “<>” tags that render them unusable. You must remove these tags to ensure the URLs are valid.
    2. Each key in the JSON object should be the name of a cryptocurrency, and each value should be its properly formatted URL.

    The output must:
    1. Be a valid JSON object that can be directly loaded into a Python dictionary.
    2. Contain only the first 10 cryptocurrencies as keys and their corrected URLs as values.

    For example, if the scraped HTML contains:
    - Coin name: Bitcoin
    - URL: https://cryptorank.io/</price/bitcoin>

    You should correct the URL to:
    - https://cryptorank.io/price/bitcoin

    Output only the valid JSON object without any additional text or explanations.
    """

    system_message_two = """
        You will be provided with the scraped content of a webpage in HTML format. This content contains detailed information about a cryptocurrency. Your task is to extract specific key information and output a valid JSON dictionary. The dictionary should have the following structure:

        {
            "Name": "<coin name>",
            "Website": "<valid website URL>",
            "Socials": {
                "<social name 1>": "<valid URL>",
                "<social name 2>": "<valid URL>",
                ...
            },
            "Details": {
                "symbol": "<coin symbol>",
                "price": "<coin price>",
                "market-cap": "<coin market cap>",
                "24h-volume": "<coin 24h volume>",
                "circulation-supply": "<coin circulation supply>",
                ...
            },
            "Description": "<a detailed description of the coin utilizing all available quantitative and qualitative information>"
        }

        **Key requirements:**
        1. Ensure all URLs are valid by removing any invalid characters such as `<` and `>`. Fix malformed URLs where necessary.
        2. Include all provided numerical and descriptive information under the appropriate keys. 
        3. Construct the "Description" field to include a comprehensive summary of the coin, combining both quantitative (e.g., price, market cap) and qualitative (e.g., unique features or purposes) details.
        4. Only include keys where data is available; if any information is missing, exclude that key from the JSON object.

        Your output must be a well-formatted and valid JSON object that can be parsed directly into a Python dictionary.
        """
    
    json_urls = get_completion(str(initial_scrape), system_message_one)
    url_dict = json.loads(str(json_urls))

    for url in url_dict.values():
        scrape_content = asyncio.run(scrape(url))
        json_info = get_completion(str(scrape_content), system_message_two)
        coin_desc = json.loads(str(json_info)).get("Description")

        with open("./full_scrape.txt", "a") as f:
            f.write(str(json_info) + "\n\n")
        with open("./data_dir/description.txt", "a") as f:
            f.write(str(coin_desc) + "\n\n")






