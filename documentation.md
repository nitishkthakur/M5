
When downloading the M5 Walmart forecasting competition data, you'll typically find five CSV files. Each plays a distinct role in building and evaluating your forecasting models. 
Here's a breakdown of the files and their purpose:
sales_train_validation.csv: This file contains the historical daily unit sales data for each product and store for the initial training period. It covers sales from day 1 to day 1913. You'll primarily use this to train your models.
sales_train_evaluation.csv: This file extends the historical daily unit sales data, including sales up to day 1941. This was the dataset used for the Public leaderboard evaluation during the competition. It can be seen as an additional training set or as a validation set, depending on how you structure your model training and evaluation.
calendar.csv: This file contains information about the dates, including events and holidays, which can be useful as explanatory variables for your forecasting models. It includes details about special events like Super Bowl or Orthodox Easter.
sell_prices.csv: This file provides information about the selling prices of the products per store and date. This data is crucial as price significantly influences sales.
sample_submission.csv: This file serves as a template for submitting your forecasts. It defines the required format for your predictions, specifying the number of days to forecast (28 days) and how to identify each forecast (using id, which is a concatenation of item_id and store_id). 
Which is the test file?
There isn't a single "test file" in the traditional sense. Instead, the competition defines two forecasting periods for evaluation:
Validation: This corresponds to days d_1914 to d_1941. During the competition, this period's results were used for the Public leaderboard. The actual sales for this period were eventually released.
Evaluation (Test): This refers to forecasting the next 28 days following the end of the sales_train_evaluation.csv data, i.e., from d_1942 to d_1969. This is the true test set for which you need to generate your predictions for submission. 
The sample_submission.csv file provides the structure for both the validation and evaluation (test) rows you need to predict. The validation rows are for forecasting d_1914 to d_1941, and the evaluation rows are for forecasting d_1942 to d_1969.