
import requests
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage
)
from newspaper import Article
import os
from dotenv import load_dotenv, find_dotenv
import json

_ = load_dotenv(find_dotenv())

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# load the model
chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

article_url = "https://timesofindia.indiatimes.com/india/some-have-to-be-launched-multiple-times-pm-modis-apparent-dig-at-rahul-gandhi-at-startup-mahakumbh/articleshow/108641468.cms"

session = requests.Session()


try:
    response = session.get(article_url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        article = Article(article_url)
        article.download()
        article.parse()
        
        print(f"Title: {article.title}")
        print(f"Text: {article.text}")
        
    else:
        print(f"Failed to fetch article at {article_url}")
except Exception as e:
    print(f"Error occurred while fetching article at {article_url}: {e}")


# we get the article data from the scraping part
article_title = article.title
article_text = article.text

# prepare template for prompt
template = """You are a very good assistant that summarizes online articles.

Here's the article you want to summarize.

==================
Title: {article_title}

{article_text}
==================

Write a summary of the previous article.
"""

prompt = template.format(article_title=article.title, article_text=article.text)

messages = [HumanMessage(content=prompt)]

# generate summary
summary = chat(messages)
print(summary.content)


#If we want a bulleted list, we can modify a prompt and get the result.

# # prepare template for prompt
# template = """You are an advanced AI assistant that summarizes online articles into bulleted lists.

# Here's the article you need to summarize.

# ==================
# Title: {article_title}

# {article_text}
# ==================

# Now, provide a summarized version of the article in a bulleted list format.
# """

# # format prompt
# prompt = template.format(article_title=article.title, article_text=article.text)

# # generate summary
# summary = chat([HumanMessage(content=prompt)])
# print(summary.content)


#If you want to get the summary in French, you can instruct the model to generate the summary in French language.


# prepare template for prompt
# template = """You are an advanced AI assistant that summarizes online articles into bulleted lists in French.

# Here's the article you need to summarize.

# ==================
# Title: {article_title}

# {article_text}
# ==================

# Now, provide a summarized version of the article in a bulleted list format, in French.
# """

# format prompt
prompt = template.format(article_title=article.title, article_text=article.text)

# generate summary
# summary = chat([HumanMessage(content=prompt)])
# print(summary.content)
