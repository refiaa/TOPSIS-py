# TOPSIS Multi-Criteria Decision Making

This project implements the Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) for multi-criteria decision making. The project is structured into three main Python scripts: `data_loader.py`, `model_ranker.py`, and `topsis.py`. These scripts work together to load data, process it using the TOPSIS method, and rank models based on multiple criteria.

## Introduction to TOPSIS

TOPSIS is a multi-criteria decision analysis method that ranks alternatives based on their distance from an ideal solution. The method involves the following steps:

1. **Normalize the Decision Matrix**:
   Each criterion value is normalized to ensure comparability.


   $R_{ij} = \frac{X_{ij}}{\sqrt{\sum_{i=1}^{n} X_{ij}^2}}$


2. **Calculate the Weighted Normalized Decision Matrix**:
   Apply the weights to the normalized criteria.


   $V_{ij} = w_j \cdot R_{ij}$


3. **Determine the Positive and Negative Ideal Solutions**:
   Identify the best and worst values for each criterion.

    $A^+ = \{ \max(V_{ij}) \, | \, j \in J \}, \, \min(V_{ij}) \, | \, j \in J' \$

    $A^- = \{ \min(V_{ij}) \, | \, j \in J \}, \, \max(V_{ij}) \, | \, j \in J' \$

4. **Calculate the Separation Measures**:
   Compute the distance of each alternative from the positive and negative ideal solutions.


   $S_i^+ = \sqrt{\sum_{j=1}^{m} (V_{ij} - A_j^+)^2}$


   $S_i^- = \sqrt{\sum_{j=1}^{m} (V_{ij} - A_j^-)^2}$


5. **Calculate the Relative Closeness to the Ideal Solution**:
   Determine the relative closeness of each alternative to the ideal solution.


   $C_i^* = \frac{S_i^-}{S_i^+ + S_i^-}$


6. **Rank the Alternatives**:
   Rank the alternatives based on the relative closeness to the ideal solution.

## Scripts Explanation

### data_loader.py

This script is responsible for loading and preprocessing the data. The criteria, weights, and benefit criteria are dynamically loaded from environment variables.

- **load_data**: Reads the CSV file and extracts the decision matrix and model names.
- **preprocess_data**: Retrieves weights and benefit criteria from the environment variables.

### model_ranker.py

This script orchestrates the data loading, model ranking, and saving the results.

- **load_and_prepare_data**: Loads the data and prepares the decision matrix, weights, and benefit criteria.
- **rank_models**: Uses the TOPSIS class to rank the models.
- **gather_rankings**: Collects the rankings and prepares them for saving.
- **save_rankings**: Saves the rankings to a CSV file.

### topsis.py

This script implements the TOPSIS method.

- **normalize**: Normalizes the decision matrix.
- **apply_weights**: Applies the weights to the normalized matrix.
- **determine_ideal_solutions**: Determines the positive and negative ideal solutions.
- **calculate_separation_measures**: Calculates the separation measures.
- **calculate_scores**: Computes the relative closeness to the ideal solution.
- **rank**: Ranks the alternatives based on the calculated scores.

## Example Usage

Here is an example of how to run the script with the given environment variables and CSV data.

1. Create a `.env` file with the following content:

    ```plaintext
    CRITERIA=index1,index2,index3,index4
    WEIGHTS=0.25,0.25,0.25,0.25
    BENEFIT_CRITERIA=False,False,True,True
    INPUT_FILE=./data/sample.csv
    OUTPUT_FILE=./data/sample_ranked.csv
    ```

2. Create a CSV file `sample.csv` with the following content:

    ```csv
    Model,index1,index2,index3,index4
    Model_1,5.0,0.1,0.9,0.8
    Model_2,6.0,0.15,0.85,0.75
    Model_3,4.5,0.2,0.8,0.7
    Model_4,5.5,0.12,0.88,0.78
    Model_5,6.1,0.11,0.87,0.79
    ```

3. Run the script:

    ```python
    if __name__ == "__main__":
        input_file = os.getenv("INPUT_FILE")
        output_file_path = os.getenv("OUTPUT_FILE")
        ranker = ModelRanker(input_file, output_file_path)
        ranker.run()
    ```

This will read the input file, process the data using the TOPSIS method, and save the ranked models to the specified output file.
