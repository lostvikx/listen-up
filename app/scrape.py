import requests
import os
from bs4 import BeautifulSoup

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
  tags = post.find_all(["p","h1","h2","h3","h4"])
  content = ""
  for tag in tags:
    text = tag.get_text()
    if text:
      # print(tag.name,text)
      content += text + "\n"
  return content.strip()

def fetch_articles(site_url):
  res = requests.get(site_url,headers={"user-agent": "Linux Machine (Listen Up)"})
  try:
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"html.parser")
    posts = parse_finshots(soup)
    post = display_posts(posts)  # Selected post to hear
    content = fetch_post_content(post["url"])
    print(content,len(content))
    # GoogleTTS(content)
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
