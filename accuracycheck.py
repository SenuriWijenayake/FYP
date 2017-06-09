from postanalysis import mapValues
from pymongo import MongoClient
from sklearn.metrics import mean_absolute_error,mean_squared_error
import math

client = MongoClient("localhost", 27017)
db = client.script

preferences = list(db.preferences.find())

preferenceData = []
locationData = []
userData = []

actualRatings = {}
predictedRatings = {}

sentimentResults = mapValues()
postAnalysisResults = []

def checkAccuracy():
        total_count = 0
        predicted_count = 0
        postAnalysisResults = sentimentResults
        for post in postAnalysisResults:

            postId = post['post id']
            userId = post['user id']
            location = post['location']
            postRating = post['rating']

            #sentimentData.append({"post_id": postId, "user_id": userId, "location": location, "rating": postRating})
            predictedRatings[postId] = {"post_id": postId, "user_id": userId, "location": location, "rating": postRating}

        for user in preferences:
            user_id = user['user_id']
            prefs = user['prefs']

            for pref in prefs:
                location = pref['name']
                postId = pref['post_id']
                rating = pref['rating']

                actualRatings[postId] = {"user_id": user_id, "location": location, "post_id": postId, "rating": rating}

        print(predictedRatings)
        print(actualRatings)

        print ("Number of predicted posts : " + str(len(predictedRatings)))
        predicted_ratings_array = []
        actual_ratings_array = []
        for post in predictedRatings:
            if (post in actualRatings):
                predicted_ratings_array.append(predictedRatings[post]['rating'])
                actual_ratings_array.append(actualRatings[post]['rating'])

        mae = mean_absolute_error(actual_ratings_array,predicted_ratings_array)
        rmse = math.sqrt(mean_squared_error(actual_ratings_array, predicted_ratings_array))

        print (mae)
        print (rmse)

        return()

checkAccuracy()
