#!/usr/bin/env python3
import json
import random
import time
from os import makedirs
from string import Template
from sys import argv

from helpers import VKAPI, VKAPIError, delay, token_is_valid


def update_status_line():
    status_line = "Progress: {}/{} walls checked, {} liked posts found".format(
        checked_public_pages,
        total_public_pages,
        len(liked_posts_urls)
    )
    print(status_line, end="\r")


def update_html_output(liked_posts_urls, output_filename):
    with open("etc/template.html", "r") as f:
        html_template = Template(f.read())
    html_content = ""
    for link in liked_posts_urls:
        if link == "":
            html_content += '<div class="divider"></div>\n'
        else:
            name = link.replace("https://vk.com/wall-", "")
            html_content += '<a href="{}" target="_blank" class="link">{}</a>\n'.format(link, name)
    output_html = html_template.substitute({
        "title": user_first_name+" "+user_last_name,
        "content": html_content
    })
    with open(output_filename, "w") as f:
        f.write(output_html)

success_auth = False
while not success_auth:
    try:
        with open("access_token.txt", "r") as f:
            access_token = f.read()
            access_token = access_token.rstrip()
        if token_is_valid(access_token):
            success_auth = True
            vk = VKAPI(access_token)
            break
    except FileNotFoundError:
        pass
    import auth
    print("---")


try:
    user_link = argv[1]
except IndexError:
    try:
        user_link = input("> Enter target id (durov, 123456): ")
    except KeyboardInterrupt:
        exit()

global user_data, user_id, user_first_name, user_last_name
user_data = vk.method("users.get", user_ids=user_link)[0]
user_id = user_data["id"]
user_first_name = user_data["first_name"]
user_last_name = user_data["last_name"]
print("{} {} (vk.com/id{})".format(user_first_name, user_last_name, user_id))

try:
    amount_of_posts_to_check = int(argv[2])
except IndexError:
    try:
        amount_of_posts_to_check = input("> Amount of posts on every wall to check (200 recommended): ")
    except KeyboardInterrupt:
        exit()
    if amount_of_posts_to_check == "":
        amount_of_posts_to_check = 200
    else:
        amount_of_posts_to_check = int(amount_of_posts_to_check)

dir_prefix = "posts/"
makedirs(dir_prefix, exist_ok=True)
makedirs("cache/", exist_ok=True)
timestamp = str(int(time.time()))
global liked_urls_filename, html_output_filename, user_subscriptions_filename
liked_urls_filename = dir_prefix+"{}_{}_id{}-{}-liked.txt".format(user_first_name, user_last_name, user_id, timestamp)
html_output_filename = dir_prefix+"{}_{}_id{}-{}-liked.html".format(user_first_name, user_last_name, user_id, timestamp)
user_subscriptions_filename = "cache/{}_{}_id{}-subscriptions.json".format(user_first_name, user_last_name, user_id)

try:
    with open(user_subscriptions_filename, "r") as f:
        try:
            user_subscriptions = json.load(f)
            subscriptions_loaded_from_cache = True
            print("Subscriptions loaded from cache ({})".format(user_subscriptions_filename))
        except:
            subscriptions_loaded_from_cache = False
except FileNotFoundError:
    subscriptions_loaded_from_cache = False

if not subscriptions_loaded_from_cache:
    user_subscriptions = []
    print("Fetching user subscriptions... ", end="")
    with open("etc/fetch-subscriptions.js", "r") as f:
        code_template = Template(f.read())
    code_to_execute = code_template.substitute({"user_id": user_id})
    user_subscriptions = vk.method("execute", code=code_to_execute)
    if user_subscriptions:
        print("[OK]")
    else:
        print("[FAILED]")
        print("Server response:", str(user_subscriptions))
        exit()
    print("Dumping subscriptions to file {}... ".format(user_subscriptions_filename), end="")
    with open(user_subscriptions_filename, "w") as f:
        json.dump(user_subscriptions, f, indent=4)
        print("[OK]")
print("---")
print("Found posts: {}".format(liked_urls_filename))
print("HTML table: {}".format(html_output_filename))

print("Loading... ", end="\r")
# preload code templates to save time
with open("etc/find-liked-posts.js", "r") as f:
    code_template = Template(f.read())

# stats
global liked_posts_urls, checked_public_pages, total_public_pages
liked_posts_urls = []
checked_public_pages = 0
total_public_pages = len(user_subscriptions)

try:
    # check every public/group
    for public_page in user_subscriptions:
        # 24 is maximal amount of posts to check via 1 request
        times_to_execute = int(amount_of_posts_to_check/24)+1
        # marker
        found_something = False
        for i in range(1, times_to_execute+1):
            posts_offset = 24 * i
            # modify template
            code_to_execute = code_template.substitute({
                "wall_id": -public_page["id"],
                "user_id": user_id,
                "posts_offset": posts_offset
            })
            response = vk.method("execute", code=code_to_execute)
            for url in response:
                liked_posts_urls.append(url)
                with open(liked_urls_filename, "a") as f:
                    f.write(url+"\n")
            if len(response) > 0:
                found_something = True
                update_status_line()
            delay()
        # add visual delimeter
        if found_something:
            liked_posts_urls.append("")
            with open(liked_urls_filename, "a") as f:
                f.write("\n")
        # update stats
        checked_public_pages += 1
        update_html_output(liked_posts_urls, html_output_filename)
        update_status_line()
    print("\n---")
    print("Done!")
except KeyboardInterrupt:
    print(" "*50)
    exit(1)
