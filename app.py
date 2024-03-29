from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle 
import numpy as np 
from model import NLPModel

app = Flask(__name__)
api = Api(app)

model = NLPModel()

clf_path = 'lib/models/SentimentClassifier.pkl'
with open(clf_path, 'rb') as f:
	model.clf = pickle.load(f)

vec_path = 'lib/models/TFIDFVectorizer.pkl'
with open(vec_path, 'rb') as f:
	model.vectorizer = pickle.load(f)

parser = reqparse.RequestParser()
parser.add_argument('query')

class PredictSentiment(Resource):
	def get(self):
		args = parser.parse_args()
		user_query = args['query']

		uq_vectorized = model.vectorizer_transform(np.array([user_query]))
		prediction = model.predict(uq_vectorized)
		pred_proba = model.predict_proba(uq_vectorized)

		if prediction == 0:
			pred_text = 'Negative'
		else:
			pred_text = 'Positive'

		confidence = round(pred_proba[0], 3)

		output = {'prediction': pred_text, 'confidence': confidence}

		return output

api.add_resource(PredictSentiment, '/')

if __name__ == '__main__':
	app.run(debug=True)