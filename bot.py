import praw
import OAuth2Util
from time import time


USERAGENT = "Special reporter for /r/upgrademypcforme"
CHECK_TEXT_Parts= "Part(s) to upgrade"
COMMENT_TEXT_Parts = "You must add the parts you want to upgrade or we wont be able to help you! Please edit your post within 24 hours or the moderators will take it down. See [this](http://redd.it/41va9s) post for information on post formatting. If you have edited the post, please answer to this comment with 'Done!'"
CHECK_TEXT_Budget= "Budget"
COMMENT_TEXT_Budget= "You must add your budget (including your currency) or we wont be able to help you! Please edit your post within 24 hours or the moderators will take it down.See [this](http://redd.it/41va9s) post for information on post formatting. If you have edited the post, please answer to this comment with 'Done!'"
CHECK_TEXT_Current_Build= "Current Build"
COMMENT_TEXT_Current_Build= "You must add your current build or we wont be able to help you! Please edit your post within 24 hours or the moderators will take it down.See [this](http://redd.it/41va9s) post for information on post formatting. If you have edited the post, please answer to this comment with 'Done!'"
CHECK_TEXT_Timeframe= "Timeframe"
COMMENT_TEXT_Timeframe= "You must add a timeframe or we wont be able to help you! Please edit your post within 24 hours or the moderators will take it down.See [this](http://redd.it/41va9s) post for information on post formatting. If you have edited the post, please answer to this comment with 'Done!'"
CHECK_TEXT_Overclock= "Overclock"
COMMENT_TEXT_Overclock= "You must add if you are willing to overclock or n or we wont be able to help you! Please edit your post within 24 hours or the moderators will take it down.See [this](http://redd.it/41va9s) post for information on post formatting. If you have edited the post, please answer to this comment with 'Done!'"
CHECK_TEXT_Buying_from= "Buying from"
COMMENT_TEXT_Buying_from= "You must add your preferred seller or we wont be able to help you! Please edit your post within 24 hours or the moderators will take it down.See [this](http://redd.it/41va9s) post for information on post formatting. If you have edited the post, please answer to this comment with 'Done!'"
SUBREDDIT = "upgrademypcforme"
REPORT_INTERVAL = 86400 #IN SECONDS (=1 day)

CHECK_LATER = []
MEMORY_CLEANER = []
DONE = []

r = praw.Reddit(USERAGENT)
o = OAuth2Util.OAuth2Util(r)
o.refresh(force=True)
sr = r.get_subreddit(SUBREDDIT)

while True:
    for post in sr.get_new(limit=100):
        MEMORY_CLEANER.append(post.id)
        if post.id not in [x.link_id for x in CHECK_LATER] and post.id not in DONE:
            if CHECK_TEXT_Parts not in post.selftext:
                CHECK_LATER.append(post.add_comment(COMMENT_TEXT_Parts))
            elif CHECK_TEXT_Budget not in post.selftext:
                CHECK_LATER.append(post.add_comment(COMMENT_TEXT_Budget))
            elif CHECK_TEXT_Current_Build not in post.selftext:
                CHECK_LATER.append(post.add_comment(COMMENT_TEXT_Current_Build))
            elif CHECK_TEXT_Timeframe not in post.selftext:
                CHECK_LATER.append(post.add_comment(COMMENT_TEXT_Timeframe))
            elif CHECK_TEXT_Overclock not in post.selftext:
                CHECK_LATER.append(post.add_comment(COMMENT_TEXT_Overclock))
            elif CHECK_TEXT_Buying_from not in post.selftext:
                CHECK_LATER.append(post.add_comment(COMMENT_TEXT_Buying_from))
            else:
                DONE.append(post.link_id)
    for comment in CHECK_LATER[:]:
        if (time() > comment.created_utc + REPORT_INTERVAL):
            comment.refresh()
            parent = r.get_submission(comment.permalink.rsplit('/', 1)[0])
            OP_DID_IT = any((getattr(i.author, "name", None) == getattr(parent.author, "name", None) and i.body == "Done!") for i in comment.replies)
            if not OP_DID_IT:
                parent.report()
            CHECK_LATER.remove(comment)
            DONE.append(comment.link_id)
    DONE = [z for z in DONE if z in MEMORY_CLEANER]
    MEMORY_CLEANER = []
    sr.refresh()
