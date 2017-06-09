from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
import emoji
from collections import Counter
import re
from pymongo import MongoClient
# create the database connection
client = MongoClient("localhost", 27017)
db = client.script

original = db.locationPosts
data = list(original.find())
locationData=[]
locationDetails=[]
postDetails = []

commentDetails =[]
locationData.append(data)
# extract the post details
def extractDbData(postDetails,commentDetails):
        for d in locationData[0]:
                locationDetails = d['locations']
                for location in locationDetails:
                        # append the status data
                        if('message' in location):
                                postDetails.append({"user_id": d['user_id'], "locationName": location['place']['name'],
                                              "message": location['message'], "post_id":location['post_id']})
                        if('comments' in location):
                                # append the comment data
                                commnts = location['comments']

                                for cmnt in commnts:
                                        a = cmnt['from']
                                        commentDetails.append({"userid": a['id'],"locationName": location['place']['name'],"user_id": d['user_id'],
                                              "comments": cmnt['message'], "post_id":location['post_id']})

                                # print(commentDetails)
        return(postDetails,commentDetails)

result = []
emoji = []
emoji_list = []
emoji_listfinal = []
comments = []
comment_results = []
comment_emoji = []
comment_emojilist = []
comment_emojilist_final = []
compoundstatus = []
userid = []
postid = []
sid = SentimentIntensityAnalyzer()
emoji_total = 0
positive = 0
neutral = 0
negative = 0
sum = 0
postData=[]
finalStatusCompound=0
compoundstatus=[]

def extractPostStatusandEmoji():
        # preprocess the extracted status and split the status into words
        extractDbData(postDetails, commentDetails)
        for item in postDetails:
                emoji_count = 0
                userid = item['user_id']
                postid = item['post_id']
                location = item['locationName']
                messages = item['message']
                result = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",messages).split()
                print("User id : " + str(userid))
                print("Post id : " + str(postid))
                print(result)
        # result = tokenize.word_tokenize(messages,'english')
        # extract emoji
                emoji = re.findall(r'[^\w\s,]', messages)
                for emo in emoji:
                        emoji_totalstatus=0
                        # emoji_list = bytes(emo, 'utf-8')
                        emoji_list = emo.encode('unicode_escape')
                        emoji_listfinal = emoji_list.decode('utf-8').strip("\\\:\#\.")
                        # print(emoji_listfinal)
                        # check the available emoji and get the probabilities
                        if emoji_listfinal == 'u2764':
                                emoji_count += 1
                                positive = 0.922
                                neutral = 0.049
                                negative = 0.03
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))

                        elif emoji_listfinal == 'u1f602':
                                emoji_count += 1
                                positive = 0.608
                                neutral = 0.206
                                negative = 0.186
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))
                        elif emoji_listfinal == 'u2665':
                                emoji_count += 1
                                positive = 0.336
                                neutral = 0.347
                                negative = 0.316
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))
                        elif emoji_listfinal == 'u1f60d':
                                emoji_count += 1
                                positive = 0.902
                                neutral = 0.088
                                negative = 0.01
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))
                        elif emoji_listfinal == 'u1f62d':
                                emoji_count += 1
                                positive = 0.373
                                neutral = 0.118
                                negative = 0.510
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))
                        elif emoji_listfinal == 'u1f618':
                                emoji_count += 1
                                positive = 0.892
                                neutral = 0.089
                                negative = 0.02
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))
                        elif emoji_listfinal == 'u1f60a':
                                emoji_count += 1
                                positive = 0.762
                                neutral = 0.198
                                negative = 0.03
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))
                        elif emoji_listfinal == 'u1f44c':
                                emoji_count += 1
                                positive = 0.650
                                neutral = 0.270
                                negative = 0.08
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))
                        elif emoji_listfinal == 'u1f44f':
                                emoji_count += 1
                                positive = 0.574
                                neutral = 0.317
                                negative = 0.109
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))
                        elif emoji_listfinal == 'u1f629':
                                emoji_count += 1
                                positive = 0.161
                                neutral = 0.293
                                negative = 0.546
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))
                        elif emoji_listfinal == 'u1f604':
                                emoji_count += 1
                                positive = 0.832
                                neutral = 0.129
                                negative = 0.04
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))
                        elif emoji_listfinal == 'u1f603':
                                emoji_count += 1
                                positive = 0.784
                                neutral = 0.167
                                negative = 0.049
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))
                        elif emoji_listfinal == 'u1f61c':
                                emoji_count += 1
                                positive = 0.696
                                neutral = 0.255
                                negative = 0.049
                                emoji_totalstatus = positive - negative
                                print("emoji_total : " + str(emoji_totalstatus))


                print("emoji count : " + str(emoji_count))
                countStatusWords = len(result)
                sumStatus=0
                # perform the Vader sentiment analysis for the texts
                for wordresult in result:
                        print(wordresult)
                        ss = sid.polarity_scores(wordresult)
                        for k in sorted(ss):
                                print('{0}: {1}, '.format(k, ss[k]), end='')
                        compoundstatus = ss['compound']

                        if (compoundstatus == 0.0):
                                countStatusWords -= 1
                        sumStatus += compoundstatus

                        if (countStatusWords == 0):
                                finalStatusCompound = 0
                        else:
                                finalStatusCompound = (sumStatus / countStatusWords)
                # Combine the text sentiment polarities of status with the emoji sentiment polarities of status
                emojiStatusProbability = emoji_count*emoji_totalstatus
                if (emojiStatusProbability == 0):
                        finalStatusProbability = finalStatusCompound
                else:
                        finalStatusProbability = finalStatusCompound * emojiStatusProbability
                print("count words = " + str(countStatusWords))
                print("sum status = " + str(sumStatus))
                print("final status probability = " + str(finalStatusProbability))
                postData.append({"user id":userid, "post id":postid, "status result":result, "location":location, "final status probability":finalStatusProbability})
        return (postData)

statusdata = extractPostStatusandEmoji()

commentData = []
def extractPostCommentsandEmoji():
        # preprocess the extracted comments and split the status into words
        extractDbData(postDetails,commentDetails)
        emoji_count = 0
        for comment in commentDetails:
                # extract the comments of the user tagged in the status
                if (comment['user_id'] == comment['userid']):
                        comments = comment['comments']
                        comment_results = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",comments).split()
                       # comment_results = tokenize.word_tokenize(comments,'english')
                        comment_emoji = re.findall(r'[^\w\s,]', comments)
                        userid = comment['user_id']
                        postid = comment['post_id']
                        print("usr id : "+comment['user_id'])
                        print("post_id : "+comment['post_id'])
                        print("comment results = " + str(comment_results))
                        # extract emoji
                        for commentemo in comment_results:
                                emoji_total=0
                                positive = 0
                                neutral = 0
                                negative = 0
                                comment_emojilist = commentemo.encode('unicode_escape')
                                comment_emojilist_final = comment_emojilist.decode('utf-8').strip("\\\:\#\.")
                                # print(comment_emojilist_final)
                                # check the available emoji and get the probabilities
                                if comment_emojilist_final == 'u2764':
                                        positive = 0.922
                                        neutral = 0.049
                                        negative = 0.03
                                        emoji_total = positive-negative
                                        print("emoji_total : "+ str(emoji_total))
                                elif comment_emojilist_final == 'u1f602':
                                        emoji_count += 1
                                        positive = 0.608
                                        neutral = 0.206
                                        negative = 0.186
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                                elif comment_emojilist_final == 'u2665':
                                        emoji_count += 1
                                        positive = 0.336
                                        neutral = 0.347
                                        negative = 0.316
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                                elif comment_emojilist_final == 'u1f60d':
                                        emoji_count += 1
                                        positive = 0.902
                                        neutral = 0.088
                                        negative = 0.01
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                                elif comment_emojilist_final == 'u1f62d':
                                        emoji_count += 1
                                        positive = 0.373
                                        neutral = 0.118
                                        negative = 0.510
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                                elif comment_emojilist_final == 'u1f618':
                                        emoji_count += 1
                                        positive = 0.892
                                        neutral = 0.089
                                        negative = 0.02
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                                elif comment_emojilist_final == 'u1f60a':
                                        emoji_count += 1
                                        positive = 0.762
                                        neutral = 0.198
                                        negative = 0.03
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                                elif comment_emojilist_final == 'u1f44c':
                                        emoji_count += 1
                                        positive = 0.650
                                        neutral = 0.270
                                        negative = 0.08
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                                elif comment_emojilist_final == 'u1f44f':
                                        emoji_count += 1
                                        positive = 0.574
                                        neutral = 0.317
                                        negative = 0.109
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                                elif comment_emojilist_final == 'u1f629':
                                        emoji_count += 1
                                        positive = 0.161
                                        neutral = 0.293
                                        negative = 0.546
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                                elif comment_emojilist_final == 'u1f604':
                                        emoji_count += 1
                                        positive = 0.832
                                        neutral = 0.129
                                        negative = 0.04
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                                elif comment_emojilist_final == 'u1f603':
                                        emoji_count += 1
                                        positive = 0.784
                                        neutral = 0.167
                                        negative = 0.049
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                                elif comment_emojilist_final == 'u1f61c':
                                        emoji_count += 1
                                        positive = 0.696
                                        neutral = 0.255
                                        negative = 0.049
                                        emoji_total = positive - negative
                                        print("emoji_total : " + str(emoji_total))
                        print("emoji count : " + str(emoji_count))
                        sumComment = 0
                        finalCommentCompound=0
                        countCompound=0
                        countWords = len(comment_results)
                        compoundValue=[]
                        # perform the Vader sentiment analysis for the texts in comments
                        for word in comment_results:
                                print(word)
                                ss = sid.polarity_scores(word)
                                for k in sorted(ss):
                                        format = print('{0}: {1}, '.format(k, ss[k]), end='')
                                compoundValue = ss['compound']
                                if(compoundValue == 0.0):
                                        countWords -= 1

                                sumComment += compoundValue

                                if(countWords == 0):
                                        finalCommentCompound = 0
                                else:
                                        finalCommentCompound =(sumComment/countWords)
                        # Combine the text sentiment polarities of status with the emoji sentiment polarities of comments
                        emojiCommentProbability = emoji_count*emoji_total
                        if(emojiCommentProbability==0):
                                finalCommentProbability = finalCommentCompound
                        else:
                                finalCommentProbability = finalCommentCompound*emojiCommentProbability
                        print("count words = " + str(countWords))
                        print("sum comment = " + str(sumComment))
                        print("final comment probability = " + str(finalCommentProbability))
                commentData.append({"comment results":comment, "userid":userid, "postid":postid, "final comment probability":finalCommentProbability})
                # print("comment data=" + str(commentData))
        return commentData
data=extractPostCommentsandEmoji()


finalValuSet = []
def aggregateProbabilities():
        Comment_data = data
        Status_data = statusdata
        # combine and get the final probabilities in user status with the relevant user comments
        for status in Status_data:
                post_id = status['post id']
                user_id = status['user id']
                location = status['location']
                status_probability = status['final status probability']
                for comnt in Comment_data:
                        comment_uid = comnt['userid']
                        comment_id = comnt['postid']
                        comment_probability = comnt['final comment probability']

                if((post_id==comment_id)&(user_id==comment_uid)&(comment_probability==0)):
                        final_probability = status_probability
                elif((post_id==comment_id)&(user_id==comment_uid)&(comment_probability!=0)):
                        final_probability = status_probability*comment_probability
                else:
                        final_probability = status_probability
                print("post id= "+ str(post_id))
                print("user id =" + str(user_id))
                print("location: " + str(location))
                print("final= " + str(final_probability))
                finalValuSet.append({"post_id":post_id, "user_id":user_id, "location":location, "final_probability":final_probability})
        return finalValuSet
# aggregateProbabilities()

results = aggregateProbabilities()
finalresults = []
def mapValues():
        #location_rating = 0
        final_results = results
        for value in final_results:
                combined_probability = value['final_probability']

                if (combined_probability == 0):
                        continue;
                # print("cp = " + str(combined_probability))
                if(combined_probability <= 0.10000000 ):
                        location_rating = 1.0

                elif(0.10000000 < combined_probability <= 0.20000000 ):
                        location_rating = 2.0

                elif(0.20000000 < combined_probability <= 0.30000000):
                        location_rating = 3.0

                elif(0.30000000 < combined_probability <= 0.40000000):
                        location_rating = 4.0

                elif(0.40000000 < combined_probability):
                        location_rating = 5.0


                postId = value['post_id']
                userId = value['user_id']
                location = value['location']


                print("post id= " + str(value['post_id']))
                print("user id =" + str(value['user_id']))
                print("location: " + str(value['location']))
                print("rating : " + str(location_rating))

                finalresults.append({"post id": postId, "user id": userId, "location":location, "rating": location_rating })

        # print("sssss = " + str(finalresults))

        return finalresults

mapValues()
