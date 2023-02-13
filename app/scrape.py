import requests
import os
import re
from bs4 import BeautifulSoup
from GoogleTTS import tts
from string import ascii_lowercase

def parse_finshots(soup:BeautifulSoup):
  """
  Website: Finshots
  """
  base_url = "https://finshots.in"
  posts_html = soup.select("article.post-card") # list of html str
  posts = []
  for post in posts_html:
    # img_url = post.find("img", {"class": "post-card-image"}).get("src")
    content_url = base_url + post.find("a", {"class": "post-card-content-link"}).get("href")
    post_title = post.find("h2", {"class": "post-card-title"}).string.strip()
    meta = {"url":content_url, "title":post_title}
    posts.append(meta)
  return posts

def parse_finshots_post(soup:BeautifulSoup):
  post = soup.find("div", {"class": "post-content"})
  tags = post.find_all(["p","h1","h2","h3","h4","hr","li"])
  # Remove promotions
  line_breaks = len(post.find_all("hr"))
  hr_count = 0
  # content = ""
  all_texts = []
  for tag in tags:
    if (tag.name == "hr") and line_breaks > 1:
      hr_count += 1
      if (hr_count == line_breaks):
        break
    else:
      # Can improve this!
      text = tag.get_text()
      dash = r"\u200a—\u200a"
      text = re.sub(dash," - ",text)
      if text:
        # print(tag.name,text)
        all_texts.append(text.strip())
  return all_texts

def fetch_articles(site_url):
  res = requests.get(site_url,headers={"user-agent": "Linux Machine (Listen Up)"})
  try:
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"html.parser")
    posts = parse_finshots(soup)
    post = display_posts(posts)  # Selected post to hear
    content = [post["title"]] + fetch_post_content(post["url"])
    # print(content,[len(c) for c in content])
    audio_file_name = clean_filename(post["title"])
    # print(audio_file_name)
    tts.GoogleTTS(text_list=content,audio_file_name=audio_file_name)
  except Exception as err:
    print(f"Error while fetching posts: {err}")

# Print all posts for selection
def display_posts(posts):
  for i,post in enumerate(posts):
    print(f"{i}. {post['title']}")
  try:
    post_number = int(input("Enter Post Number: "))
    selected_post = posts[post_number]
  except:
    print("Please Enter an Integer!")
  os.system("clear")
  return selected_post

def fetch_post_content(post_url):
  res = requests.get(post_url,headers={"user-agent": "Linux Machine (Listen Up)"})
  try:
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"html.parser")
    content = parse_finshots_post(soup)
  except Exception as err:
    print(f"Error while fetchin post content: {err}")
  return content

def clean_filename(name):
  # name = name.lower()
  new_name = ""
  for char in name.lower():
    if (char in ascii_lowercase) or (char == " "):
      new_name += char
  file_name = ""
  for char in new_name:
    if char == " ":
      file_name += "-"
    else:
      file_name += char
  return file_name
