import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os
import shutil
shutil.rmtree('img')
os.mkdir('img')


def f(x):
    # return np.sin(x) + np.cos(np.sqrt(3) * x)
    return np.sin(2 * np.pi * x / 10) + 0.2 * np.sin(2 * np.pi * x / 2.5) + 0.3 * np.cos(2 * np.pi * x / 20)
    # return np.sin(10 * np.pi * x) / (2 * x) + (x - 1)**4


def k(a, b):
    param = 1.0
    return np.exp(-0.5 * ((a - b) / param)**2)


def kroneker(i, j):
    if(i == j):
        return 1
    else:
        return 0


x = np.linspace(-17.5, 17.5, 1000)
y = f(x)

noiseSD = 0.1
noiseVar = noiseSD**2

limits = [int(0.20 * len(x)), int(0.80 * len(x))]

x_interval = x[limits[0]:limits[1]]

numSamples = 0
varianceThreshold = 0.00001
averageVarianceHistory = []
maxVarianceHistory = []
maxVariance = 1000000
x_samples = []
y_samples = []
sampleCoverage = []
y_variance = []
dpi = 200
convertCommand = "convert -delay 40 -loop 0 img/GP.gif"

iterations = 0
maxIterations = 100

while maxVariance > varianceThreshold and iterations <= maxIterations:

    if(iterations > 0):
        if(np.random.uniform() > 0.2):
            occurances = y_variance[limits[0]:limits[1]].count(maxVariance)
            if(occurances == 1):
                index = y_variance[limits[0]:limits[1]].index(
                    maxVariance) + limits[0]
            else:
                instances = [i for i, n in enumerate(
                    y_variance[limits[0]:limits[1]]) if n == maxVariance]
                index = instances[np.random.randint(
                    0, len(instances))] + limits[0]
        else:
            index = np.random.randint(limits[0], limits[1])

        x_samples.append(x[index])
        y_samples.append(y[index] + np.random.normal(scale=noiseSD))

    covariance_matrix = np.identity(len(x_samples)) * noiseVar
    for i in range(len(x_samples)):
        for j in range(len(x_samples)):
            covariance_matrix[i][j] += k(x_samples[i], x_samples[j])

    try:
        inv_covariance_matrix = np.linalg.inv(covariance_matrix)
    except:
        x_samples.pop()
        y_samples.pop()
        continue
    else:
        numSamples += 1
        numTries = 0
        y_predictions = []
        y_variance = []
        lowerBound = []
        upperBound = []
        for i in range(len(x)):
            kStar = np.zeros(len(x_samples))
            for j in range(len(x_samples)):
                kStar[j] = k(x[i], x_samples[j])

            prediction = np.matmul(kStar, np.matmul(
                inv_covariance_matrix, y_samples))
            variance = k(x[i], x[i]) - np.matmul(kStar,
                                                 np.matmul(inv_covariance_matrix, np.transpose(kStar)))

            y_predictions.append(prediction)
            y_variance.append(variance)

            lowerBound.append(prediction - 2 * np.sqrt(variance))
            upperBound.append(prediction + 2 * np.sqrt(variance))

        maxVariance = np.max(y_variance[limits[0]:limits[1]])
        averageVariance = np.mean(y_variance[limits[0]:limits[1]])

        averageVarianceHistory.append(averageVariance * 100)
        maxVarianceHistory.append(maxVariance)

        coverage = 100 * len(x_samples) / float(len(x))
        sampleCoverage.append(coverage)

        plt.clf()
        plt.style.use('seaborn-white')
        # plt.figure(figsize=(8, 5.333))
        plt.ylim(-2.5, 2.5)
        plt.axvline(x=x_interval[0], linestyle='--', color='silver')
        plt.axvline(x=x_interval[-1], linestyle='--', color='silver')
        plt.xlabel(r'$x$')
        plt.ylabel(r'$y$')
        plt.fill_between(x, lowerBound, upperBound,
                         color='gray', alpha=0.2, label='Uncertainty')
        plt.plot(x, y, 'r', label='Truth')
        plt.plot(x, y_predictions, label='Predicted')
        plt.plot(x_samples, y_samples, 'kx',
                 label="Training set", markersize=3)
        plt.legend(loc='upper center', bbox_to_anchor=(
            0.5, 1.12), ncol=4, fancybox=True)
        plt.savefig('img/' + str(iterations) + '.png',
                    bbox_inches='tight', dpi=dpi)
        plt.close()
        convertCommand += " img/" + str(iterations) + ".png"

    iterations += 1

plt.clf()
plt.style.use('seaborn-white')
# plt.figure(figsize=(6, 4))
plt.grid(True, which="both")
plt.ylabel("Average Uncertainty (%)")
plt.xlabel("Training Set Size")
plt.plot(averageVarianceHistory, label='average uncertainty')
# plt.plot(maxVarianceHistory,label='max uncertainty')
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=2, fancybox=True)
plt.savefig('img/uncertainty.png', bbox_inches='tight', dpi=dpi)

# subprocess.call(convertCommand, shell=True)
