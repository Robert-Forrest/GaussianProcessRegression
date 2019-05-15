import matplotlib.pyplot as plt
import numpy as np 
import subprocess
import os
import shutil
shutil.rmtree('img')
os.mkdir('img')

def f(x):
    return np.sin(x) + np.cos(np.sqrt(3)*x)

def k(a,b):
  params = [1.0,1.0]
  
  return (params[0]**2)*np.exp(-((a-b)**2) /(2*params[1]**2))

x = np.linspace(0,20,400,dtype=float)
y = f(x)

limits=[int(0.20*len(x)),int(0.80*len(x))]

x_interval = x[limits[0]:limits[1]]

numSamples = 0
varianceThreshold = 0.0001
averageVarianceHistory=[]
maxVarianceHistory=[]
maxVariance=1000000
x_samples = []
y_samples = []
convertCommand = "convert -delay 40 -loop 0 "
while maxVariance>varianceThreshold:
  
  if(len(x_samples)>1):
    index = y_variance.index(maxVariance)
  else:
    index = np.random.random_integers(limits[0],limits[1])

  x_samples.append(x[index])
  y_samples.append(y[index])

  covariance_matrix = np.zeros([len(x_samples),len(x_samples)])

  for i in range(len(x_samples)):
    for j in range(len(x_samples)):
      covariance_matrix[i][j] = k(x_samples[i],x_samples[j])

  try:
    inv_covariance_matrix = np.linalg.inv(covariance_matrix)
  except:
    x_samples.pop()
    y_samples.pop()
    continue
  else:
    numSamples+=1
    numTries=0
    y_predictions = []
    y_variance = []
    lowerBound = []
    upperBound = []
    for i in range(len(x)):
      kStar = np.zeros(len(x_samples))
      for j in range(len(x_samples)):
        kStar[j]=k(x[i],x_samples[j])
      
      prediction = np.matmul(kStar,np.matmul(inv_covariance_matrix,y_samples))
      variance = k(x[i],x[i]) - np.matmul(kStar,np.matmul(inv_covariance_matrix,np.transpose(kStar)))

      y_predictions.append(prediction)
      y_variance.append(variance)

      lowerBound.append(prediction-2*np.sqrt(variance))
      upperBound.append(prediction+2*np.sqrt(variance))

    maxVariance = np.max(y_variance[limits[0]:limits[1]])
    averageVarianceHistory.append(np.mean(y_variance[limits[0]:limits[1]]))
    maxVarianceHistory.append(maxVariance)

    plt.clf()
    plt.ylim(-2.5,2.5)
    plt.axvline(x=x_interval[0],linestyle='--',color='k')
    plt.axvline(x=x_interval[-1],linestyle='--',color='k')
    plt.plot(x, y,'r',label='true')
    plt.plot(x_samples,y_samples,'ko',label="training set",markersize=4)
    plt.plot(x, y_predictions,label='prediction')
    plt.fill_between(x, lowerBound, upperBound,color='gray',alpha=0.2,label='uncertainty')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),ncol=4, fancybox=True)
    plt.savefig('img/'+str(numSamples)+'.png')

    convertCommand+=" img/"+str(numSamples)+".png"

plt.clf()
plt.plot(averageVarianceHistory,label='average uncertainty')
plt.plot(maxVarianceHistory,label='max uncertainty')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),ncol=2, fancybox=True)
plt.savefig('img/variance.png')

convertCommand+=" img/regression.gif"
subprocess.call(convertCommand,shell=True)