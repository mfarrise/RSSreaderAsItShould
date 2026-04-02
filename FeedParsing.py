import feedparser
import certifi
import requests



def parse_feeds_to_list():
    rss_url_list=[]#ill put them in list to make it scalable for multiple feeds from future json
    rss_url_list.append("https://feeds.bbci.co.uk/news/rss.xml")
    rss_url_list.append("https://journals.lww.com/CJASN/_layouts/15/OAKS.Journals/feed.aspx?FeedType=CurrentIssue")
    rss_url_list.append("https://www.nejm.org/action/showFeed?jc=nejm&type=etoc&feed=rss")
    rss_url_list.append("https://www.techradar.com/feeds.xml")
    rss_url_list.append("https://feeds.feedburner.com/ign/all")
    rss_url_list.append("https://academic.oup.com/rss/site_5333/3199.xml")

    final_parse_list = []




    for url in rss_url_list:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(
                url,
                headers=headers,
                verify=certifi.where(),
                timeout=10
            )
            feed = feedparser.parse(response.content)
        except Exception as e:
            print("RSS fetch failed:", e)
            return []
        for entry in feed.entries:
            string = ""  # start temp internal string
            string += getattr(feed.feed,"title","") + ": "  # start it with news source name
            string += getattr(entry, "title","") + "," #add to its the news name
            string += getattr(entry, "summary","") + "," # add the description
            final_parse_list.append([string,getattr(entry, "link","")]) # make list of dictionaries {string,link}
            #rinse and repeat
    print(final_parse_list)

    return final_parse_list # this is a list of two item lists ,each has first item string,other link of the string







