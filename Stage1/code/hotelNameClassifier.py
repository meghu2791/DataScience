from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import ShuffleSplit
import os

train_source = "./../DataSets/TrainDataSet"
test_source = "./../DataSets/TestDataSet"

train_files = os.listdir(train_source)
test_files = os.listdir(test_source)

feature_names = ['hotel', 'good', 'great', 'room', 'is', 'service', 'stay']
dict = {"Florence","TV", "Would","Berlin","In","Having", "Overall","Europe","For","Park","Clean","After","Overall", "Bar", "Station,", "Station.", "Station", "Room", "Rooms", "Location," ,"Location", "Located", "Stay", "Hotel.", "Hotel!" "Hotel", "Hotel:", "Hotel," ,"Stayed", "Best", "The", "An", "Awesome", "Fantastic", "Be", "Excellent", "Family", "Station", "Location", "Dam", "Euro", "And", "Amsterdam", "Amsterdam,", "Amsterdam.", "A", "But", "Hi", "We", "On", "It", "To", "Its", "It's", "This", "All", "If", "Those", "These", "At", "I", "Then", "There", "They", "Our", "Great", "My", "No", "Hotel", "He", "You", "May", "Wonderful", "Just", "Staff", "Loved", "City", "Very", "So", "As", "Breakfast", "Nice", "Good", "Not", "What"}
dict1 = {"the", "time", "a", "on", "got", "as", "were", "would", "was", "I", "be", "and", ",", "of", "with", "it", "but", "had", "we", "to", "they", "are", "like", "has", "from", "only", "not" }
X = []
X_test = []
y_test = []
y = []

def feature_extractor(X, l, j):
    temp = [0] * len(feature_names)
    for k in range(1, 5):
        for i in range(len(feature_names)):
            if ((j + k) < len(l)) and (feature_names[i] in l[j+k].lower()):
                temp[i] = temp[i] + 1
            elif ((j - k) > -1) and (feature_names[i] in l[j-k].lower()):
                temp[i] = temp[i] + 1
    X.append(temp)

def checkNeighborhood(word, j, l):
    for k in range(1, 15):
        for i in range(len(feature_names)):
            if ((j + k) < len(l)) and (feature_names[i] in l[j + k].lower()):
                return True
            elif ((j - k) > -1) and (feature_names[i] in l[j - k].lower()):
                return True
        return False

def vectorizer(X, y, file, isTest):
    for line in file:
        l = line.split()
        for j,word in enumerate(l):
            if word in dict1:
                l.remove(word)
                continue
            if (word[0] == "#"):
                feature_extractor(X, l, j)
                if not isTest:
                    y.append(1)
                else:
                    y_test.append(1)
            elif (word[0].isupper() and word not in dict):
                feature_extractor(X, l, j)
                if not isTest:
                    y.append(0)
                else:
                    y_test.append(0)

for f in train_files:
    vectorizer(X, y, open(os.path.join(train_source, f),"r", encoding="utf8"), 0)
for f in test_files:
    vectorizer(X_test, y_test, open(os.path.join(test_source, f),"r", encoding="utf8"), 1)

cv = ShuffleSplit(n_splits=3, test_size=0.2, random_state=0)

clf = GaussianNB().fit(X,y)
logistic_model = LogisticRegression().fit(X, y)
decisionTree = tree.DecisionTreeClassifier(max_features=len(feature_names)).fit(X,y)
randomForest = RandomForestClassifier(n_estimators = len(feature_names)).fit(X, y)
svmClassifier = svm.SVC(C=47.0, kernel='linear').fit(X, y)

category = ["Non-hotel", "hotel"]

predicted = clf.predict(X_test)
print("GaussianNB")
print(metrics.classification_report(y_test, predicted, target_names=category))

predictLogistic = logistic_model.predict(X_test)
print("Logistic Regression")
print(metrics.classification_report(y_test, predictLogistic, target_names=category))

predictTree = decisionTree.predict(X_test)
print("Decision Tree")
print(metrics.classification_report(y_test, predictTree, target_names=category))

predictForest = randomForest.predict(X_test)
print("Random Forest")
print(metrics.classification_report(y_test, predictForest, target_names=category))

predictSvm = svmClassifier.predict(X_test)
print("SVM")
print(metrics.classification_report(y_test, predictSvm, target_names=category))