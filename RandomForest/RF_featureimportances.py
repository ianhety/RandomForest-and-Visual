import pandas as pd
import numpy as np
import patsy
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn import ensemble as ske
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import cross_val_predict
from numpy import float32
le = preprocessing.LabelEncoder()

# Import the data and output the null summary
path = 'C:\\Users\\310249682\Documents\\data.xlsx'
data = pd.read_excel(path)
pd.set_option('display.max_columns',80)
pd.set_option('display.max_rows',66)
NaN_count = [len(data[i])-data[i].count() for i in data.columns]
variable = [str([j.encode("utf-8") if type(j) is unicode else j for j in list(data[i].unique())]) for i in data.columns]
vtype = ['ID','ID','Numeric_int','categorical','categorical','Numeric_int','Categorical','Numeric_int','Categorical','Categorical',
         'Categorical','Categorical','Categorical','Categorical','Categorical','Categorical','Categorical','Categorical','Categorical','Numeric_int',
         'Categorical','Numeric_float','Numeric_float','Numeric_float','Numeric_float','Categorical','Categorical','Categorical','Numeric_int','Numeric_int',
         'Categorical','Categorical','Categorical','Categorical','Categorical','Categorical','Categorical','Categorical','Categorical','Categorical',
         'Numeric_int','Categorical','Categorical','Categorical','Categorical','Categorical','Categorical','Numeric_int','Numeric_int','Numeric_int',
         'Numeric_int','Numeric_int','Numeric_float','Numeric_int','Numeric_int','Numeric_int','Numeric_int','Numeric_int','Categorical','Categorical',
         'Categorical','Numeric_int','Categorical','Numeric_int','Categorical']
dtype = pd.DataFrame(data = data.dtypes, columns = ['Type'])
dvtype = pd.DataFrame(data = vtype, columns = ['variable type'],index = dtype.index)
dNaN = pd.DataFrame(data = NaN_count, columns = ['Number of null'],index = dtype.index)
dvar = pd.DataFrame(data = variable, columns = ['Items'],index = dtype.index)
frame=[dvtype,dNaN,dvar]
Nullsummary = pd.concat(frame,axis=1)

#Function:Check the data type
def dattype( data ):
    ddtype = 'Error'
    data=data[pd.notnull(data)]
    for i in data:
        ddtype = type(i)
        break
    return ddtype

#convert the data
def typetransform ( data ):
    if dattype( data ) is unicode:
        le.fit( data )
        data = le.transform( data )
    else:
            imp = Imputer(missing_values='NaN', strategy='mean',axis = 1)
            imp.fit(data)
            data = imp.transform( data )
    return data


#delete the data
data = pd.read_excel('C:\\Users\\310249682\\Documents\\data1.xlsx')
del data['HISTORY_HYPERTENSION']
del data['TOTAL_CHOLESTEROL']
del data['CATH EVENTS']
del data['EJECTION_FRACTION']
del data['WEIGHT']
del data['HEIGHT']
del data['HEART_RATE']
del data['Euroscore']
del data['CLINICAL_SYNDROME']
del data['Indication for intervention']
del data['Presenting ECG']
del data['Thrombolysis']
del data['COMPLICATION']
del data['Replacement Device?']
del data['Replacement Reason']
del data['Device type']
del data['Device type.1']
del data['Indication for stent']
del data['LMS Protected']
del data['LENGTH_STAY_PROC_TO_DISCH']
del data['Patient_DB_ID']
del data['Procedure_Unique_Identifier']

#transform the data
for i in data.columns:
    if dattype( data[i] ) is unicode:
        data[i] = typetransform(data[i])
    else:
        data[i] = typetransform(data[i])[0]

#balance the data with oversampling and undersampling
out_alive = data[data['OUTCOME'] == 1]
out_dead = data[data['OUTCOME'] == 2]
out_dead_new = pd.concat([out_dead]*5)
out_alive_new = out_alive[0:1265]
data_new = pd.concat([out_alive_new,out_dead_new])

#Random Forest Tree
outcome = 'OUTCOME'
predictors = data.columns
predictors = list(predictors)
del predictors[39]
data_training = data

data_training = data_training[data_training[outcome] != 3]
pre = data_training[predictors] #predictors dataframe
out = typetransform(data_training[outcome]) #outcome dataframe
out_array = np.asarray(out).ravel()
rfc = ske.RandomForestClassifier(n_estimators=1000) #random tree
scores = cross_val_score(rfc, pre, out_array)
pred = cross_val_predict(rfc,pre, out_array)

rfc2 = ske.RandomForestClassifier(n_estimators=1000).fit(pre,out_array)
feature_importance = rfc2.feature_importances_

#Feature Importance
indices = np.argsort(feature_importance)[::-1]
print "Feature Importances:"
for f in range(42):
    print("%d. %s (%f)" % (f + 1, list(data.columns)[f],feature_importance[indices[f]]))

#CV score
var = [list(data.columns)[i] for i in list(indices[0:25])]
def nrtc_cv( outcome , predictors , data_training ):
    #transform training data
    pre = data_training[predictors] #predictors dataframe
    out = typetransform(data_training[outcome]) #outcome dataframe
    out_array = np.asarray(out).ravel()
    rfc = ske.RandomForestClassifier(n_estimators=1000) #random tree
    scores = cross_val_score(rfc, pre, out_array)
    pred = cross_val_predict(rfc,pre, out_array)
    return scores.mean(),pred
nrtc_cv( 'OUTCOME' , var , data )
