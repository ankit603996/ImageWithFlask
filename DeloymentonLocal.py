#!/usr/bin/env python
# coding: utf-8

# In[439]:
#####

#####

from flask import Flask, render_template, url_for, request, redirect,jsonify
import os
import numpy as np
import uuid
app = Flask(__name__)


# In[440]:


#os.chdir(r'F:\LocalDriveD\Analytics\Learning\Udemy Deploying machine learning models with flask for beginners\flaskdata\Practice')


# In[441]:


import pickle
filename = 'finalized_model.sav'
 
# load the model from disk
model = pickle.load(open(filename, 'rb'))


# In[442]:


Expected = {
"variable_0":{"min":-0.291358489,"max":95823.65222},
"variable_1":{"min":-2.363636364,"max":2.590909091},
"variable_2":{"min":0,"max":98},
"variable_3":{"min":-0.528734055,"max":318121.7754},
"variable_4":{"min":-0.744871795,"max":305.9320513},
"variable_5":{"min":-1.333333333,"max":8.333333332999999},
"variable_6":{"min":0,"max":98},
"variable_7":{"min":-0.5,"max":26.5},
"variable_8":{"min":0,"max":98},
"variable_9":{"min":0,"max":20}
}


# In[443]:


@app.route('/')
def index():
    return render_template('model.html')


@app.route('/api/image', methods=['POST'])
def class_predict():
    print ("ggg")
    content = {"variable_0":request.form['variable_0'],
    "variable_1":request.form['variable_1'],
    "variable_2":request.form['variable_2'],
    "variable_3":request.form['variable_3'],
    "variable_4":request.form['variable_4'],
    "variable_5":request.form['variable_5'],
    "variable_6":request.form['variable_6'],
    "variable_7":request.form['variable_7'],
    "variable_8":request.form['variable_8'],
    "variable_9":request.form['variable_9']}
    errors = []
    print('dictionary prepared')
    if(len(content['variable_0'])*len(content['variable_1'])*len(content['variable_2'])*len(content['variable_3'])*len(content['variable_4'])*len(content['variable_5'])*len(content['variable_6'])*len(content['variable_7'])*len(content['variable_8'])*len(content['variable_9'])==0):
        return "please enter all values in integer/float type"                
    else:
        try:
                for name in content:
                    print('names mapping with names from expected')
                    print(name)
                    if name in Expected:
                        expected_min = Expected[name]['min']
                        expected_max = Expected[name]['max']
                        print('min max set')
                        value = content[name]
                        print('value from dictionary taken')
                        if float(value) < expected_min or float(value) > expected_max:
                            print('comparison from min max')
                            errors.append(f"Out of bounds: {name}, has value of: {value}, but it should be between {expected_min} and {expected_max}.")
                    else:
                        errors.append(f"Unexpected field: {name}.")
                print('names mapped from expected')

                for name in Expected:
                    if name not in content:
                        errors.append(f"Missing_value:{name}")
                x= np.zeros((1,10))
                x[0,0] = content['variable_0']
                x[0,1] = content['variable_1']
                x[0,2] = content['variable_2']
                x[0,3] = content['variable_3']
                x[0,4] = content['variable_4']
                x[0,5] = content['variable_5']
                x[0,6] = content['variable_6']
                x[0,7] = content['variable_7']
                x[0,8] = content['variable_8']
                x[0,9] = content['variable_9']

                prediction = model.predict(x)
                class_col = float(prediction[0])
                class_col = np.where(class_col==0.0,'No Churn','Churn')
                print('prediction done')
                response = {"Deplyment_id": str(uuid.uuid4()), "class_prediction": str(class_col),"Total_errors_if_Any":errors}
                return render_template('model.html', prediction = 'Results are {}'.format(response))
        except:
                return render_template('model.html', prediction = 'No Results ')


# In[444]:


if __name__ =='__main__':
    app.run(debug=True, use_reloader=False)


# Below code worked well 

# #@app.route('/index')
# #def index():
# #    return render_template('model.html')
# 
# @app.route('/', methods=['POST', 'GET'])
# def class_predict():
#     if request.method == 'POST':
#         print ("ggg")
#         content = {"variable_0":request.form['variable_0'],
#         "variable_1":request.form['variable_1'],
#         "variable_2":request.form['variable_2'],
#         "variable_3":request.form['variable_3'],
#         "variable_4":request.form['variable_4'],
#         "variable_5":request.form['variable_5'],
#         "variable_6":request.form['variable_6'],
#         "variable_7":request.form['variable_7'],
#         "variable_8":request.form['variable_8'],
#         "variable_9":request.form['variable_9']}
#         errors = []
#         print('dictionary prepared')
#         if(len(content['variable_0'])*len(content['variable_1'])*len(content['variable_2'])*len(content['variable_3'])*len(content['variable_4'])*len(content['variable_5'])*len(content['variable_6'])*len(content['variable_7'])*len(content['variable_8'])*len(content['variable_9'])==0):
#             return "please enter all values in integer/float type"                
#         else:
#             try:
#                     for name in content:
#                         print('names mapping with names from expected')
#                         print(name)
#                         if name in Expected:
#                             expected_min = Expected[name]['min']
#                             expected_max = Expected[name]['max']
#                             print('min max set')
#                             value = content[name]
#                             print('value from dictionary taken')
#                             if float(value) < expected_min or float(value) > expected_max:
#                                 print('comparison from min max')
#                                 errors.append(f"Out of bounds: {name}, has value of: {value}, but it should be between {expected_min} and {expected_max}.")
#                         else:
#                             errors.append(f"Unexpected field: {name}.")
#                     print('names mapped from expected')
# 
#                     for name in Expected:
#                         if name not in content:
#                             errors.append(f"Missing_value:{name}")
#                     x= np.zeros((1,10))
#                     x[0,0] = content['variable_0']
#                     x[0,1] = content['variable_1']
#                     x[0,2] = content['variable_2']
#                     x[0,3] = content['variable_3']
#                     x[0,4] = content['variable_4']
#                     x[0,5] = content['variable_5']
#                     x[0,6] = content['variable_6']
#                     x[0,7] = content['variable_7']
#                     x[0,8] = content['variable_8']
#                     x[0,9] = content['variable_9']
# 
#                     prediction = model.predict(x)
#                     class_col = float(prediction[0])
#                     print('prediction done')
#                     response = {"id": str(uuid.uuid4()), "class_col": class_col,"errors":errors}
#                     return jsonify(response)
#             except:
#                     return render_template('model.html')
#     else:
#             return render_template('model.html')
# 

# In[ ]:





# In[ ]:




