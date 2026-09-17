# Chess Outcome Prediction

Predicting the outcome of chess games using player strength, historical performance, recent form, head-to-head statistics, opening statistics, and other features derived from a large collection of historical chess games.

The main goal of this project was to work with a **large real-world dataset and build a predictive modeling pipeline around it**, while dealing with challenges such as chronological data, evolving player statistics, class imbalance, and preventing data leakage.

The final dataset contains **3,255,656 chess games** and **91 predictive features**.

----------

## Results

The task is a 3-class classification problem from **White's perspective**:

| Class | Outcome | Result |
| :-: | :-- | :-: |
| **0** | Black Win | `0–1` |
| **1** | Draw | `½–½` |
| **2** | White Win | `1–0` |

Three tree-based models were evaluated on games from **2026**, which were completely held out from model training and validation.

| Model | Accuracy | Macro F1 | Weighted F1 |
| :--- | :-: | :-: | :-: |
| **Decision Tree** | **0.62** | 0.58 | 0.61 |
| **Random Forest** | **0.62** | 0.59 | 0.62 |
| **XGBoost** | **0.62** | 0.59 | 0.62 |

The models perform substantially differently across the three classes. Draws are considerably harder to predict than decisive games.

## Dataset

The chess games were obtained from **The Week in Chess (TWIC)**.

The raw data consists of PGN files containing games from **2012 through June 2026**. The PGN files were downloaded and combined using the [`twic.sh`](https://github.com/tegenterter/twic-builder/blob/master/twic.sh) script.

The PGN data was then converted into CSV format using the project's `src/png_to_csv.py` script.

The resulting dataset contains:

-   **3,255,656 games**
    
-   **91 predictive features**
    
-   **3 outcome classes**
    

### Outcome distribution


| Result | Games |
| :--- | --: |
| **White Win** | 1,365,355 |
| **Black Win** | 1,139,502 |
| **Draw** | 750,836 |

This creates a noticeable class imbalance, with draws being the smallest class.

----------

## Prediction Target

The objective is to predict the outcome of a chess game **from White's perspective**.

The target is encoded as:

```text
0 → Black Win
1 → Draw
2 → White Win
```

The prediction is made using information about the players, their previous games, their recent form, their head-to-head history, the opening, and other statistics available before the game.

----------

## Data Pipeline

The project follows this general pipeline:

```text
TWIC PGN files
      │
      ▼
Download and combine PGNs
      │
      ▼
PGN → CSV
      │
      ▼
Data cleaning
      │
      ▼
Chronological feature engineering
      │
      ▼
Final dataset
      │
      ├── Training:   2016–2023
      ├── Validation: 2024–2025
      └── Test:       2026
      │
      ▼
Hyperparameter tuning
      │
      ▼
Decision Tree / Random Forest / XGBoost
      │
      ▼
Final evaluation
```

----------

# Feature Engineering

A major part of the project was creating features from the historical game data.

Rather than relying only on the Elo ratings included in the original games, the dataset was expanded with statistics describing the players' previous performance.

The final dataset contains **91 predictive features** after removing identifying and target-related columns such as:

```text
Site
Date
White
Black
Result
ECO
```

### Elo Features

Basic player-strength features include:

-   `WhiteElo`
    
-   `BlackElo`
    
-   `EloDiff`
    
-   `absEloDiff`
    
-   `AvgElo`
    
-   `HigherRatedPlayer`
    

These provide information about the relative strength of the two players.

----------

### Overall Player Statistics

Historical statistics were calculated for both players, including:

-   Number of previous games
    
-   Wins
    
-   Losses
    
-   Draws
    
-   Win rate
    
-   Loss rate
    
-   Draw rate
    

For example:

```text
WhiteGames
WhiteWin
WhiteLoss
WhiteDraw

BlackGames
BlackWin
BlackLoss
BlackDraw
```

# Preventing Data Leakage

Because this is a time-dependent prediction problem, preventing temporal leakage was one of the most important parts of the project.

The games are processed chronologically.

For every game, player history, recent form, streaks, head-to-head statistics, and other historical features are calculated using **only games that occurred before that game**.

For example, when generating features for a game played in 2020, information from games played after that game is not used to construct its features.

This means that although the source data spans **2012–June 2026**, the historical features for each individual game only contain information that would have been available at the time that game was played.

This is particularly important for features such as:

-   Player win rates
    
-   Recent form
    
-   H2H statistics
    
-   Streaks
    
-   Days since last game
    
-   Opening statistics
    

Using future games to calculate these statistics would artificially improve the model's performance.

----------

# Train / Validation / Test Split

The dataset was split chronologically rather than randomly.

```text
2012 ───────────── 2015 ─────── 2023 ─────── 2025 ─────── June 2026
 │                    │             │             │              │
 │ Historical data    │             │             │              │
 └────────────────────┴─────────────┤             │              │
                                    │             │              │
                               Training        Validation       Test
                               2016–2023       2024–2025        2026

```

### Training

**2016–2023**

The model was trained on these games.

Training does not begin in 2012 because the earlier games are useful for establishing historical player statistics. Starting the training period later also avoids having the earliest observations dominated by players with little or no available history.

### Validation

**2024–2025**

Used for model selection and evaluation during development.

### Test

**2026**

The 2026 games were kept as a final unseen test period.

----------

# Models

Three tree-based classification models were evaluated.

## Decision Tree

The final Decision Tree was:

```python
DecisionTreeClassifier(
    ccp_alpha=1e-06,
    criterion="gini",
    class_weight={0: 1, 1: 1.5, 2: 1},
    max_depth=75,
    max_leaf_nodes=1000,
    min_samples_leaf=173,
    min_samples_split=626,
    random_state=67
)

```

----------

## Random Forest

The final Random Forest was:

```python
RandomForestClassifier(
    ccp_alpha=0,
    class_weight={0: 1, 1: 1.5, 2: 1},
    max_depth=40,
    max_features=0.5,
    min_samples_leaf=73,
    min_samples_split=51,
    n_estimators=195,
    bootstrap=True,
    random_state=67,
    n_jobs=-1
)

```


----------

## XGBoost

The final XGBoost classifier used:

```python
XGBClassifier(
    objective="multi:softprob",
    num_class=3,
    eval_metric="mlogloss",

    colsample_bytree=0.5158019945643415,
    gamma=0.18576353181073108,
    learning_rate=0.0238211139654102,
    max_depth=6,
    min_child_weight=7,
    n_estimators=733,
    reg_alpha=0.2155168238099609,
    reg_lambda=1.285808534044257,
    subsample=0.6576010179563144,

    random_state=67,
    tree_method="hist",
    n_jobs=-1
)

```

----------

# Hyperparameter Tuning

Hyperparameter tuning was performed on **Kaggle** because of the size of the dataset.

A **3-fold time-series cross-validation** approach was used during tuning rather than randomly shuffling the games.

The objective was to find hyperparameters that generalize to later games while preserving the chronological nature of the problem.

The models were then trained using the selected hyperparameters and evaluated on the completely held-out **2026 test set**.

----------

# Probability Thresholding for Draws

Because draws were consistently the most difficult class to predict, I also investigated whether changing the classification threshold could improve draw detection.

For a standard multi-class classifier, the predicted class is normally the class with the highest predicted probability. However, this does not necessarily provide the desired balance between precision and recall for the draw class.

The model's predicted probability for a draw was therefore examined separately.
The draw classifier achieved a **ROC-AUC of approximately 0.755**.

The Best Threshold Probability for:
 - Random Forest - 0.37
 - XGBoost - 0.29


# Final Results

## Decision Tree

Confusion matrix:

```text
[[33613  5622 13307]
 [ 7047  9926  8505]
 [12884  6280 42304]]
```


| Class | Precision | Recall | F1 |
| :--- | :-: | :-: | :-: |
| **Black Win** | 0.63 | 0.64 | 0.63 |
| **Draw** | 0.45 | 0.39 | 0.42 |
| **White Win** | 0.66 | 0.69 | 0.67 |
| **Accuracy** | — | — | **0.62** |

----------

## Random Forest

Confusion matrix:

```text
[[32999  6726 12817]
 [ 6240 11816  7422]
 [12348  7779 41341]]

```


| Class | Precision | Recall | F1 |
| :--- | :-: | :-: | :-: |
| **Black Win** | 0.64 | 0.63 | 0.63 |
| **Draw** | 0.45 | 0.46 | 0.46 |
| **White Win** | 0.67 | 0.67 | 0.67 |
| **Accuracy** | — | — | **0.62** |

----------

## XGBoost

Confusion matrix:

```text
[[33178  6410 12954]
 [ 6259 11597  7622]
 [12121  7477 41870]]
```


| Class | Precision | Recall | F1 |
| :--- | :-: | :-: | :-: |
| **Black Win** | 0.64 | 0.63 | 0.64 |
| **Draw** | 0.46 | 0.46 | 0.46 |
| **White Win** | 0.67 | 0.68 | 0.68 |
| **Accuracy** | — | — | **0.62** |

The three models have very similar overall accuracy.

The most noticeable difference is in the treatment of draws. All three models perform better on decisive games than on draws.

----------

# Why Are Draws Difficult to Predict?

The draw class is particularly challenging.

A draw can occur between:

-   Two similarly rated players
    
-   Two very different rated players
    
-   Players in different stages of a tournament
    
-   Players using different openings
    
-   Games that develop into unexpectedly balanced positions

----------

# Two-Stage Experiment

A two-stage prediction approach was also explored.

The idea was to first predict:

```text
Decisive game
      vs
Draw
```

and then, if the game was predicted to be decisive, predict:

```text
Black Win
      vs
White Win
```

This experiment was performed using the Decision Tree notebook.

Although the approach was explored as a way to handle the difficulty of predicting draws separately from decisive games, it did not become the final modeling approach.

The final reported results therefore use the direct **3-class classification problem**.

----------

# Repository Structure

```text
.
├── data/
│   ├── raw_data/
│   ├── cleaned_chess.csv
│   └── final_chess.csv
│
├── notebooks/
│   ├── 01_exploring_the_games.ipynb
│   ├── 02_preprocess.ipynb
│   ├── 03_feature_engg.ipynb
│   ├── 04.1_dtc.ipynb
│   ├── 04.2_rfc.ipynb
│   └── 04.3_xgb.ipynb
│
├── src/
│   └── png_to_csv.py
│
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

### Notebook Pipeline

The notebooks are organized roughly as follows:

#### `01_exploring_the_games.ipynb`

Initial exploration of the downloaded chess games and their structure.

#### `02_preprocess.ipynb`

Cleaning and preprocessing of the raw game data.

#### `03_feature_engg.ipynb`

Construction of the historical, player, H2H, opening, form, streak, and difference features.

#### `04.1_dtc.ipynb`

Decision Tree experiments, tuning, evaluation, and the two-stage experiment.

#### `04.2_rfc.ipynb`

Random Forest training, tuning, and evaluation.

#### `04.3_xgb.ipynb`

XGBoost training, tuning, and evaluation.

----------

# Reproducing the Dataset

The raw TWIC data is not included in this repository because of its size.

The original PGN files can be downloaded using the [`twic.sh`](https://github.com/tegenterter/twic-builder/blob/master/twic.sh) script.

The downloaded PGN data can then be converted into CSV using:

```text
src/png_to_csv.py

```

The resulting dataset contains the individual games along with their move information.

The notebooks can then be followed sequentially:

```text
01 → 02 → 03 → 04

```

to reproduce the exploration, preprocessing, feature engineering, and modeling stages.

The generated datasets and trained models are excluded from Git using `.gitignore` because of their size.
    

----------

# Technologies

-   Python
    
-   NumPy
    
-   Pandas
    
-   Scikit-learn
    
-   XGBoost
    
-   Jupyter Notebook
    
-   Kaggle
    
-   uv
    

----------

## Project Motivation

The main motivation behind this project was not simply to build a chess predictor.

I wanted to work with a **large real-world dataset** and go through the complete process of building a predictive model: collecting the data, understanding it, cleaning it, creating meaningful features, dealing with temporal structure, preventing data leakage, tuning models, and evaluating their performance on future unseen data.

Chess provides a useful setting for this because the outcome depends on many interacting factors, while the historical games provide enough data to construct detailed statistics about players and their previous performance.

The resulting project contains more than **3.2 million games**, making it a practical exercise in building and evaluating predictive models at a relatively large scale.