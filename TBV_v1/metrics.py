#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve 
from sklearn.metrics import roc_auc_score, f1_score, recall_score
get_ipython().run_line_magic('pylab', 'inline')
pd.set_option('display.max_column',None)


'''Function that returns the confusion matrix and classification report
    Input
    ----------
    target : pd.Series with dependent or target data, where rows are observations

    predicted : array with predicted data, where rows are observations

    Returns
    -------     
    returns confusion matrix and classification report
'''

def plot_cm(target, predicted):
    
    # confusion matrix
    print('Confusion matrix:')
    print(confusion_matrix(target,predicted))
    
    # classification report
    print('Classification report:')
    print(classification_report(target,predicted))


'''Function that returns confusin matriz and classification report
    Input
    ----------
    target : pd.Series with dependent or target data, where rows are observations

    probs : array with probability of success of the data predicted, where rows are observations
    
    label : name of the classifier

    Returns
    -------     
    returns AUC score, false positive rate, true positive rate and plots ROC curve 
'''

def plot_roc_curve(target, probs, label=None):

    # No Skill probability
    ns_prob = [0 for _ in range(len(target))]
    
    #calculate scores
    ns_auc = roc_auc_score(target, ns_prob)
    clf_auc_roc = roc_auc_score(target, probs)

    # summarize scores and compare with previous classifiers
    print('No Skill: ROC AUC=%.3f' % (ns_auc))
    print(label+': ROC AUC=%.3f' % (clf_auc_roc))

    # calculate roc curves
    ns_fpr, ns_tpr, _ = roc_curve(target, ns_prob)
    _fpr, _tpr, _th = roc_curve(target, probs)

    # plot the roc curve for the model
    plt.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
    plt.plot(_fpr, _tpr, marker='.', label=label)

    # axis labels
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    # show the legend
    plt.legend()

    # show the plot
    plt.show()
    
    return(clf_auc_roc, _fpr, _tpr, _th)


'''Function that returns confusin matriz and classification report
    Input
    ----------
    target : pd.series with dependent or target data, where rows are observations

    predicted : array with predicted data, where rows are observations
    
    probs : array probability of success of the data predicted, where rows are observations
    
    label : name of the classifier

    Returns
    -------     
    returns f1, precision and recall scores and plots precision-recall curve 
'''

'''Function that takes y_test, y_prediction, y_probability and the name of the classifier and returns: 
f1, precision and recall scores and plots precision-recall curve'''


def plot_prec_rec(target, predicted, probs,label=None):

    # precision, recall and f1
    _precision, _recall, _th2 = precision_recall_curve(target, probs)
    _f1, _auc = f1_score(target, predicted), auc(_recall, _precision)

    # summarize scores
    print(label+': f1=%.3f auc=%.3f' % (_f1, _auc))

    # plot the precision-recall curves
    no_skill = len(target[target==1]) / len(target)
    plt.plot([0, 1], [no_skill, no_skill], linestyle='--', label='No Skill')
    plt.plot(_recall, _precision, marker='.', label=label)

    # axis labels
    plt.xlabel('Recall')
    plt.ylabel('Precision')

    # show the legend
    plt.legend()

    # show the plot
    plt.show()
    
    return (_f1, _precision, _recall)


''' Find the optimal probability cutoff point for a classification model 
    ----------
    target : Matrix with dependent or target data, where rows are observations

    predicted : Matrix with predicted data, where rows are observations

    Returns
    -------     
    list type, with optimal cutoff value

    '''
def Find_Optimal_Cutoff(target, predicted):
    fp, tp, thresholds = roc_curve(target, predicted)
    i = np.arange(len(tp)) 
    roc = pd.DataFrame({'tf' : pd.Series(tp-(1-fp), index=i),
                        'thresholds' : pd.Series(thresholds, index=i)})
    roc_t = roc.loc[(roc.tf-0).abs().argsort()[:1]]

    # return list(roc_t['thresholds'])
    print('The optimal cut-off is: %0.2f' %(float(roc_t['thresholds'])))
    return float(roc_t['thresholds'])
