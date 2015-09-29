'''
Created on Sep 27, 2015

@author: Ray
'''

import praw;
import time;
import re
import os

def handle_ratelimit(func, *args, **kwargs):
    while True:
        try:
            func(*args, **kwargs)
            break
        except praw.errors.RateLimitExceeded as error:
            print ('\tSleeping for %d seconds' % error.sleep_time)
            time.sleep(error.sleep_time)

r = praw.Reddit('Test of Zynect');
r.login('ZynBot', 'qwerty')

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = filter(None, posts_replied_to)
already_done = [];

while True:
    subreddit = r.get_subreddit('me_irl');
    for submission in subreddit.get_hot(limit=25):
                 
        if submission.id not in posts_replied_to:
            submission.replace_more_comments(limit=None, threshold=0)
            all_comments = submission.comments
            flat_comments = praw.helpers.flatten_tree(all_comments)
            
            for comment in flat_comments:
                if (re.search("ME TOO THANKS", comment.body, re.IGNORECASE)):
                    if comment.id not in already_done:
                        handle_ratelimit(comment.reply, 'doot')
                        #comment.reply('doot \n \n &nbsp; \n \n ^(I\'m a robot and have nothing to do with Buddhism/Zen)')
                        already_done.append(comment.id)
                    
            """if re.search("TEST", submission.title, re.IGNORECASE):
                handle_ratelimit(submission.add_comment, "tested")
                submission.add_comment("tested")
                posts_replied_to.append(submission.id)"""
                
        with open("posts_replied_to.txt", "w") as f:
            for post_id in posts_replied_to:
                f.write(post_id + "\n")
        time.sleep(60)