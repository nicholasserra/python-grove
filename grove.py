import urllib
import urllib2
import base64

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        from django.utils import simplejson as json

class GroveUnauthorized(Exception):
    pass

class Grove404(Exception):
    pass

class GroveConnection(object):
    def __init__(self, username, password):
        '''
        Grove.io API class
        '''
        self.api_url = 'https://grove.io/api/'
        self.b64auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    def check_auth(self):
        """ check authentication """
        url = '%sauth' % self.api_url
        return self.call_and_parse(url)

    def get_organization(self, id):
        """ get organization info by id """
        url = '%sorganizations/%s' % (self.api_url, id)
        return self.call_and_parse(url)

    def get_channel_info(self, id):
        """ get channel info by id """
        url = '%schannels/%s' % (self.api_url, id)
        return self.call_and_parse(url)

    def get_messages(self, id):
        """ get messages from channel by channel id """
        url = '%schannels/%s/messages' % (self.api_url, id)
        return self.call_and_parse(url)

    def get_users(self, id):
        """ get users from channel by channel id """
        url = '%schannels/%s/users' % (self.api_url, id)
        return self.call_and_parse(url)

    def get_topic(self, id):
        """ get channel topic from channel by channel id """
        url = '%schannels/%s/topic' % (self.api_url, id)
        return self.call_and_parse(url)

    def get_join_list(self, id):
        """ get list of channels to join by organization id """
        url = '%sorganizations/%s/join' % (self.api_url, id)
        return self.call_and_parse(url)

    def join_channel(self, id):
        """ join a channel by channel id """
        url = '%schannels/%s/join' % (self.api_url, id)
        return self.call_and_parse(url, post={'j':1})

    def part_channel(self, id):
        """ part from a channel by channel id """
        url = '%schannels/%s/part' % (self.api_url, id)
        return self.call_and_parse(url, post={'p':1})

    def part_private_channel(self, id):
        """ part from a private channel by channel id """
        url = '%sprivate/%s/part' % (self.api_url, id)
        return self.call_and_parse(url, post={'p':1})

    def private_channel_info(self, org_name, username):
        """ get info about private channel """
        url = '%sprivate/%s/%s' % (self.api_url, org_name, username)
        return self.call_and_parse(url)

    def get_private_channel_messages(self, id, until_id=None):
        """ get private channel messages by channel id """
        if not until_id:
            url = '%sprivate/%s/messages' % (self.api_url, id)
        else:
            url = '%sprivate/%s/messages?until_id=%s' % (self.api_url, id, until_id)
        return self.call_and_parse(url)

    def update_topic(self, id, topic):
        """ update topic of a channel by channel id """
        url = '%schannels/%s/topic' % (self.api_url, id)
        return self.call_and_parse(url, post={'topic': topic})

    def post_message(self, id, message, cid=None):
        """ post a message to a channel by channel id """
        url = '%schannels/%s/messages' % (self.api_url, id)

        post = {'message': message}

        if cid:
            post['cid'] = cid

        return self.call_and_parse(url, post=post)
        
    def post_private_message(self, id, message, cid=None):
        """ post a message to a private channel by channel id """
        url = '%sprivate/%s/messages' % (self.api_url, id)

        post = {'message': message}

        if cid:
            post['cid'] = cid

        return self.call_and_parse(url, post=post)

    def call_and_parse(self, url, post=None):

        data = urllib.urlencode(post) if post else None

        try:
            r = urllib2.Request(url, data)
            r.add_header("Authorization", "Basic %s" % self.b64auth)
            response = urllib2.urlopen(r)
        except urllib2.URLError, e:
            if e.code == 401:
                raise GroveUnauthorized('Invalid login details')
            elif e.code == 404:
                raise Grove404('404')
            raise e

        content = response.read()
        response.close()
        parsed = json.loads(content)
        return parsed
