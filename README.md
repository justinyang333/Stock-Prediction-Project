# Machine Learning: Group 6 - Project Proposal

### Team Members: Curran Myers, Tilman Gromme, Braden Dunaway, Bryce McNealey, Justin Yang

## Project Introduction and Background

It's very difficult for hedge funds and day traders to outperform the market (i.e. stable index funds) over a long time. Stock market public accessibility is increasing with technologies like Robinhood, TD Ameritrade, Bitwallet, etc becoming more relevant. Accurate predictions of the stock market can assist in education and help advise important financial planning and decisions for companies and individuals alike.

---

## Problem Definition

Our team seeks to outperform the market (index funds: S&P 500, NASDAQ, etc.). We will implement the most recent methods of decision tree day-by-day to determine which stocks to buy or sell, given a principal amount of money, that maximizes profit and minimizes risk.

---

## Dataset
For our dataset, we are making use of [Marketdata’s API](https://docs.marketdata.app/api) to collect daily historical data for thousands of stock symbols over the past two decades.  The stock symbols are gathered from the [NASDAQ’s Stock Sceener](https://www.nasdaq.com/market-activity/stocks/screener), which provides basic information on stocks listed on the NASDAQ, NYSE, and AMEX.  This data will provide a solid foundation for engineering other indicator features to help the model predict future results.  Additionally, building a custom dataset allows the team to preprocess out unnecessary or irrelevant data thus reducing the overhead for data cleaning.

---

## Potential Methods and Techniques

For our model we will consider:
- **Random Forest Regression**: We would utilize an ensemble of decision trees, each with their own subset of (financial) features and samples (of stocks), to predict which stocks we should purchase and sell. We anticipate this method will be effective in capturing feature relationships and reducing overfitting. 

- **XGBoost**: As an option to further the Random Forest Regression, we will also consider using Extreme Gradient Boosting.  Due to the fact our data will be a time series, the sequential training XGBoost provides will help to more accurately extrapolate and forecast the trends in our data.  XGBoost has a python package from the developers **xgboost** [1].

- **Naive Bayes**: Assumes the stock’s features are conditionally independent and using Bayes Theorem, predicts the direction of stock price movements to suggest which stocks we may purchase or sell. We can use a variety of libraries to accomplish this, including **sci-kit-learn**.

To provide whichever model we decide to use with quality data, we will employ several methods in preprocessing to aid in reducing training time while maintaining data integrity and information.  These methods include feature engineering and compression among others. Ideally this process will make the model perform equally well if not better while reducing overhead.

---

## Potential Results and Discussion

In order to quantify our project results, we plan to employ the following metrics in order to fully represent our findings. When employing a regression model of Random Forest, the following metrics such as mean squared error, root mean squared error and R^2 would prove useful in forming performance benchmarks of our implementation [3]. For a Naïve Bayes classification approach, “accuracy and f-measure are used” [2] for creating performance benchmarks on the status of this approach.

---

## References

- [1] Chen, T., & Guestrin, C. (2016, August). Xgboost: A scalable tree boosting system. In Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data mining (pp. 785-794).
- [2] Patel, J., Shah, S., Thakkar, P., & Kotecha, K. (2015). Predicting stock and stock price index movement using trend deterministic data preparation and machine learning techniques. Expert systems with applications, 42(1), 259-268.
- [3] Plevris, Vagelis & Solorzano, German & Bakas, Nikolaos & Ben Seghier, Mohamed. (2022). Investigation of performance metrics in regression analysis and machine learning-based prediction models. 10.23967/eccomas.2022.155. 

---

## Project Timeline

![Project Operations Timeline](assets/timeline.png)

---

## Work Contribution Table

|       Task          |  Time Window  | Responsible Member(s) |
|       :---:         |    :---:      |        :---:          |
| Research            | 06/06 - 06/13 | All Members           |
| Proposal            | 06/13 - 06/16 | All Members           |
| Data Collection     | 06/16 - 06/24 | Braden                |
| Exp. Data Analysis  | 06/19 - 06/26 | Braden                |
| Feature Engineering | 06/21 - 07/02 | Curran                |
| Comparing Models    | 06/23 - 07/05 | Bryce                 |
| Midterm Report      | 07/02 - 07/07 | All members           |
| Implementation      | 07/07 - 07/19 | Tilman                |
| Model Tuning        | 07/14 - 07/21 | Justin                |
| Evaluation          | 07/19 - 07/24 | Curran                |
| Final Report        | 07/22 - 07/25 | All Members           |

---

## Checkpoint

For team checkpoints, we meet weekly to review the progress of current phases and completed phases.  This aids in aligning our team on project goals and properly distributing work among team members.  These project meetings will occur until the project has reached completion at the end of the term.

