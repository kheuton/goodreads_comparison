import json

from rauth.service import OAuth1Service, OAuth1Session


def authorize(path_to_keys):
    api_keys = json.load(open(path_to_keys,'rb'))
    KEY = api_keys['KEY']
    SECRET = api_keys['KEY']

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
