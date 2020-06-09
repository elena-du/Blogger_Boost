from flask import Flask, render_template, request, url_for
from itertools import chain
import pickle
import sklearn
from sklearn.metrics import pairwise_distances

app = Flask(__name__)

with open('/Users/elena/Desktop/Metis/Project_4_Ted/Project-4-Ted/nmf_model.pkl', 'rb') as picklefile:
    nmf_model = pickle.load(picklefile)

with open('/Users/elena/Desktop/Metis/Project_4_Ted/Project-4-Ted/doc_topic_nmf.pkl', 'rb') as picklefile:
    doc_topic_nmf = pickle.load(picklefile)

with open('/Users/elena/Desktop/Metis/Project_4_Ted/Project-4-Ted/doc_topic.pkl', 'rb') as picklefile:
    doc_topic = pickle.load(picklefile)

with open('/Users/elena/Desktop/Metis/Project_4_Ted/Project-4-Ted/df.pkl', 'rb') as picklefile:
    df = pickle.load(picklefile)

with open('/Users/elena/Desktop/Metis/Project_4_Ted/Project-4-Ted/vectorizer_TF_IDF.pkl', 'rb') as picklefile:
    vectorizer_TF_IDF = pickle.load(picklefile)

with open('/Users/elena/Desktop/Metis/Project_4_Ted/Project-4-Ted/dict_.pkl', 'rb') as picklefile:
    df_dict = pickle.load(picklefile)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', posts = df_dict)

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    t = request.form.get('topic', 'technology and robots')
    t = list(eval('["' + t + '"]'))
    vt = vectorizer_TF_IDF.transform(t)
    tt = nmf_model.transform(vt)
    dist_order = pairwise_distances(tt,doc_topic,metric='cosine').argsort()
    sorted_ind = list(chain(*dist_order.tolist()))

    with open('/Users/elena/Desktop/Metis/Project_4_Ted/Project-4-Ted/df.pkl', 'rb') as picklefile:
        df = pickle.load(picklefile)
    #df = df.dropna()
    df = df.reindex(columns=['video_id', 'title', 'publushed_date'])
    df = df.reindex(index=sorted_ind).head(5)
    #recommendation = df.loc[sorted_ind, :].sort_values('polarity_pos_comments',
                                  #ascending=False).head(10).sort_values('publushed_date',
                                                          #ascending=False)

    return render_template('predictor.html', recommendation=df.to_html())


#str(doc_topic_nmf.iloc[255, :])

#@app.route('/my_next_TED') #methods['POST', 'GET']
#def predict():

#    url = request.args
#    index = df[df.video_id == url].index.values.tolist()
#    dist_order = pairwise_distances(doc_topic[index].reshape(1, -1),doc_topic,metric='cosine').argsort()
#    sorted_ind = list(chain(*dist_order.tolist()))

#    recommendation = df.loc[sorted_ind, ['video_id',
#                    'title',
#                    'publushed_date',
#                    'polarity_pos_comments'
#                   ]].sort_values('polarity_pos_comments',
#                                  ascending=False).head(10).sort_values('publushed_date',
#                                                          ascending=False)

#@app.route('/get_data', methods = ['GET', 'POST']) #methods['POST', 'GET']
#def get_data_():
#    text__ = request.args.get('text', 'test')
#    processed_text = text__.upper()




#    return render_template('predictor.html', processed_text=processed_text)

#@app.route('/<name>')
#def user(name):
#    return f"Hello {name}! Nothing is here!"


if __name__ == '__main__':
    app.run(debug=True)
