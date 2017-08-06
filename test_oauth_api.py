import json
import time

from bs4 import BeautifulSoup
from rauth.service import OAuth1Service, OAuth1Session

# If you've read these you must be really wise
OFFICIAL_BOOKS = ['Neuromancer', 'Infinite Jest']

def authorize(path_to_keys):
    api_keys = json.load(open(path_to_keys,'rb'))
    KEY = api_keys['KEY']
    SECRET = api_keys['SECRET']

    goodreads = OAuth1Service(
        consumer_key=KEY,
        consumer_secret=SECRET,
        name='goodreads',
        request_token_url='http://www.goodreads.com/oauth/request_token',
        authorize_url='http://www.goodreads.com/oauth/authorize',
        access_token_url='http://www.goodreads.com/oauth/access_token',
        base_url='http://www.goodreads.com/'
    )

    # head_auth=True is important here; this doesn't work with oauth2 for some reason
    request_token, request_token_secret = goodreads.get_request_token(header_auth=True)

    authorize_url = goodreads.get_authorize_url(request_token)
    print 'Visit this URL in your browser: ' + authorize_url
    accepted = 'n'
    while accepted.lower() == 'n':
        # you need to access the authorize_link via a browser,
        # and proceed to manually authorize the consumer
        accepted = raw_input('Have you authorized me? (y/n) ')

    session = goodreads.get_auth_session(request_token, request_token_secret)
    time.sleep(1)

    # Grab the user id
    user_xml = session.get('https://www.goodreads.com/api/auth_user')

    user_id = BeautifulSoup(user_xml.content, 'lxml').find('user').get('id')

    # Build reviewed book query

    response = session.get('https://www.goodreads.com/review/list/'
                           '{u:s}.xml?key=XOjn5TvF7yh0VUK0re8v4Q&v=2'.format(u=user_id))

    parsed_html = BeautifulSoup(response.content, 'lxml')

    title_tags = parsed_html.body.findAll('title')
    titles = [tag.text for tag in title_tags]

    score = 0
    for book in OFFICIAL_BOOKS:
        if book in titles:
            score += 1

    print("Your score is {s:.2f}%".format(s=float(score)/len(OFFICIAL_BOOKS)*100))


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--path_to_keys", type=str,
                        help="String path to key json", required=True)

    args = parser.parse_args()

    authorize(args.path_to_keys)
