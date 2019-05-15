# Gaussian Process Regression

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)   

![Regression Animation](https://github.com/Robert-Forrest/GaussianProcessRegression/blob/master/examples/regression.gif)  

This simple python project performs Gaussian process regression, without depending on any external libraries.  

Gaussian process regression involves sampling from a distribution over all functions:  
![FunctionPosterior](http://www.sciweavers.org/tex2img.php?eq=%20%20%20%20p%28%5Cboldsymbol%7Bf%7D_%2A%7C%5Cboldsymbol%7By%7D%2C%5Cboldsymbol%7BX%7D%2C%5Cboldsymbol%7BX%7D_%2A%29%20%26%3D%20%5Cmathcal%7BN%7D%28%5Cboldsymbol%7Bf%7D_%2A%7C%5Cboldsymbol%7B%5Cmu%7D_%2A%2C%5Cboldsymbol%7B%5CSigma%7D_%2A%29&bc=White&fc=Black&im=jpg&fs=24&ff=fourier&edit=0)

Allowing us to make predictions based on a training data set consisting of samples from the true process:  
![FunctionPrediction](http://www.sciweavers.org/tex2img.php?eq=%20%20%20%20%5Cbar%7Bf%7D_%2A%20%20%3D%20%5Cboldsymbol%7Bk%7D_%2A%5E%7B%5Ctext%7BT%7D%7D%5Cboldsymbol%7B%5CSigma%7D%5E%7B-1%7D%5Cboldsymbol%7By%7D&bc=White&fc=Black&im=jpg&fs=24&ff=fourier&edit=0)  

![Uncertainty](http://www.sciweavers.org/tex2img.php?eq=%20%20%20%20%5Csigma_%2A%5E2%20%3D%20k_%7B%2A%2A%7D%20-%20%5Cboldsymbol%7Bk%7D_%2A%5E%7B%5Ctext%7BT%7D%7D%5Cboldsymbol%7B%5CSigma%7D%5E%7B-1%7D%5Cboldsymbol%7Bk%7D_%2A&bc=White&fc=Black&im=jpg&fs=24&ff=fourier&edit=0)  

### License
This project is licensed under the terms of MIT license. See the LICENSE file for more info.