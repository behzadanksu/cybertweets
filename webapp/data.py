from pymongo import MongoClient
from bson import CodecOptions, SON, ObjectId


class DataEngine(object):
    """
    This class is a wrapping module around the database. All database interactions MUST use this class.
    """

    def __init__(self):
        """
        The default constructor of DataEngine. Initializes and prepares a database connection.
        """
        # establish the database connection
        self.connection = MongoClient('127.0.0.1', 27017, connect=False) #server.local_bind_port)
        self.db = self.connection.threat
        self.options = CodecOptions(document_class=SON)

    def fetch_tweet_types(self):
        """
        This method returns the list of all types of threats in the dataset
        :return: list(str)
        """
        # scan through the tweets to find all the possible types
        types = list(self.db.tweets.find())
        # calculate how many tweets per each type was found
        types_info = {'all': len(types)}

        for t in types:
            if 'type' in t:
                current_count = types_info.setdefault(t['type'][0], 0)
                types_info[t['type'][0]] = current_count + 1

        return sorted(types_info.items(), key=lambda m: m[0])

    def annotate_tweet(self, id, annotation, relevance):
        """
        This method updates the binary relevance key in the dataset and the annotation key to classify the tweet
        into "threat", "business" and "irrelevant"
        :param id: id of tweet document in db
        :param annotation: string whether is "threat", "business", and "irrelevant"
        :param relevance: boolean whether the tweet is relevant or not
        :return: None
        """
        self.db.tweets.update_one({'_id': ObjectId(id)}, {"$set": {"annotation": annotation, "relevant": relevance}}, upsert=False)

    def threat_annotate(self, id, threat):
        """
        This method updates the threat type of a tweet.
        :param id: id of tweet document in db
        :param threat: string of the type of tweet annotated
        :return: None
        """
        self.db.tweets.update_one({'_id': ObjectId(id)}, {"$set": {"type": [threat.lower()]}}, upsert=False)

    def fetch_tweets(self, filters=None, limit=None):
        """
        The method that returns all the papers. If a filters object is present, all the papers that satisfy the
        filtering conditions.
        :param filters: a dictionary with values for filtering, example: {paper_id: 123}
        :param limit: a 'page' number, say 3 if a user wants results from 30-40 out of 100. Range is a constant that
        is set to be ITEMS_PER_PAGE.
        :return: a cursor pointing to the first item in the found items list
        """
        if filters is not None:
            if limit is not None:
                tweets = list(self.db.tweets.with_options(codec_options=self.options).find(filters).sort('_id').limit(limit))
            else:
                tweets = list(self.db.tweets.with_options(codec_options=self.options).find(filters).sort('_id'))
        else:
            if limit is not None:
                tweets = list(self.db.tweets.with_options(codec_options=self.options).find().sort('_id').limit(limit))
            else:
                tweets = list(self.db.tweets.with_options(codec_options=self.options).find().sort('_id'))

        for tweet in tweets:

            if limit is not None:
                # delete extra information
                if 'date' in tweet:
                    del tweet['date']
                if 'id' in tweet:
                    del tweet['id']

                # prepare tweet
                tweet['author'] = tweet['tweet']['user']['screen_name']
                tweet['author_name'] = tweet['tweet']['user']['name']

                if "extended_tweet" in tweet['tweet'].keys():
                    tweet['text'] = tweet['tweet']['extended_tweet']['full_text']

                del tweet['tweet']
                tweet['type'] = tweet['type'][0]

                cats = []
                for cat in tweet['watson']['categories']:
                    cats.append(cat)
                tweet['categories'] = cats
                del tweet['watson']

        return tweets
