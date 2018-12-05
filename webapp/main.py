from flask import Flask, render_template, request, jsonify, session, redirect
from data import DataEngine
import helpers


app = Flask(__name__)
engine = DataEngine()
### CHANGE FOR LIMIT OF TWEETS PER PAGE
LIMIT = 75


@app.route('/')
def hello_world():
    types = sorted(map(lambda mat: (mat[0].replace('_', ' ').title(), mat[1]), engine.fetch_tweet_types()))
    return render_template("base.html", threat_type_list=types)


@app.route('/tweets/', defaults={'page': 1})
@app.route('/tweets/page/<int:page>', methods=['GET'])
def get_tweets(page):
    threat_type = request.args.get('threat_type').lower()
    relevance = helpers.process_relevance(request.args.get('relevance'))
    annotation = request.args.get('annotation')
    tweet_filter = helpers.make_filter(threat_type, relevance, annotation)
    all_tweets = engine.fetch_tweets(tweet_filter)
    pagination = helpers.Pagination(page, LIMIT, len(all_tweets))
    if len(all_tweets) > 0:
        last_id = all_tweets[pagination.offset]['_id']

        tweet_filter['_id'] = {"$gte": last_id}
        tweets = engine.fetch_tweets(tweet_filter, LIMIT)

        types = sorted(map(lambda mat: (mat[0].replace('_', ' ').title(), mat[1]), engine.fetch_tweet_types()))

        return render_template("base.html", tweets=tweets,
                               threat_type_list=types, threat_type=threat_type, relevance=relevance, annotation=annotation,
                               prev_url=pagination.prev_url, next_url=pagination.next_url, pages_url=pagination.pages_url,
                               key_pages=pagination.key_pages)
    else:
        types = sorted(map(lambda mat: (mat[0].replace('_', ' ').title(), mat[1]), engine.fetch_tweet_types()))
        return render_template("base.html", threat_type_list=types)


@app.route("/annotate", methods=['POST'])
def annotate_tweet():
    id = request.form.get('id')
    annotation = request.form['annotation']
    if annotation == 'business' or annotation == 'irrelevant' or annotation == 'unknown':
        relevance = False
    else:
        relevance = True
    engine.annotate_tweet(id, annotation, relevance)
    return jsonify({'annotation': annotation, 'relevance': relevance})


@app.route("/threat_annotate", methods=['POST'])
def threat_annotate():
    id = request.form.get('id')
    annotation = request.form['annotation']
    engine.threat_annotate(id, annotation)
    return jsonify({"success": True})


if __name__ == '__main__':
    app.run()
