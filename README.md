# Mumbai Real Estate Price Predictor App
An AI project that uses Random Forest Regression to predict real-estate prices in Mumbai, India. The model was trained on data from 2023 with almost 30000 samples. It achieved an average accuracy of 94% using Random Forest Regression and 88% using Linear Regression respectively.

## Observations
From the test scores, it is evident that the model is able to predict values well. The Random Forest model gave us
an almost 6% increase in accuracy over Linear Regression. However, there is room for improvement by improving
quality of data as well as tuning hyperparameters. For example, some of the locations in the dataset can be
grouped into larger clusters if we knew which locality they belonged to. The model performs well with 1-3BHK
apartments as they constituted a large percentage of the dataset. Hence when predicting values for 5BHK
apartments it tends to predict a comparatively reduced price. To conclude, this was an interesting project which
helped learn about the various stages in using AI from data extraction to deployment to predict house prices.

## Project Summary
<details>
  <summary> View Image </summary>

  ![CIA 2 AI](https://github.com/Valeron-T/mumbai-real-estate-prices-predictor/assets/32789691/e115f722-8c33-48cd-944b-0b69331ef22e)
</details>




## References
Florian Dedov [NeuralNine]. (2022). House price prediction in python. YouTube.
https://www.youtube.com/watch?v=Wqmtf9SA_kk
