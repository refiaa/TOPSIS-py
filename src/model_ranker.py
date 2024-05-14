import os
import numpy as np
import pandas as pd

from typing import Optional, List, Tuple
from TOPSIS import TOPSIS
from data_loader import ModelDataLoader
from dotenv import load_dotenv

load_dotenv()

class ModelRanker:
    def __init__(self, input_file: str, output_file: Optional[str] = None):
        self.input_file = input_file
        self.output_file = output_file
        self.all_rankings = []
        self.criteria, self.weights, self.benefit_criteria = ModelDataLoader.load_criteria_from_env()

    def load_and_prepare_data(self) -> Tuple[List[str], np.ndarray, List[float], List[bool]]:
        try:
            models, decision_matrix = ModelDataLoader.load_data(self.input_file)
            return models, decision_matrix, self.weights, self.benefit_criteria
        except (ValueError, FileNotFoundError) as e:
            print(f"Error loading data: {e}")
            raise

    def rank_models(self, models: List[str], decision_matrix: np.ndarray, weights: List[float], benefit_criteria: List[bool]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        topsis = TOPSIS(decision_matrix, weights, benefit_criteria)
        ranks, scores = topsis.rank()
        proximity_scores = topsis.get_proximity_scores()
        return ranks, scores, proximity_scores

    def gather_rankings(self) -> None:
        models, decision_matrix, weights, benefit_criteria = self.load_and_prepare_data()
        ranks, scores, proximity_scores = self.rank_models(models, decision_matrix, weights, benefit_criteria)

        for rank, index in enumerate(ranks, start=1):
            ranking_data = {
                "Rank": rank,
                "Model": models[index],
                "Score": scores[index]
            }
            for i, criterion in enumerate(self.criteria):
                ranking_data[criterion] = proximity_scores[index, i]
            self.all_rankings.append(ranking_data)
        self.all_rankings.append({key: "" for key in ["Rank", "Model", "Score"] + self.criteria})

    def save_rankings(self) -> None:
        if not self.output_file:
            print("Output file not specified; skipping save.")
            return

        df = pd.DataFrame(self.all_rankings)
        df.to_csv(self.output_file, index=False)
        print(f"Rankings saved to {self.output_file}")

    def run(self) -> None:
        self.gather_rankings()
        if self.output_file:
            self.save_rankings()

if __name__ == "__main__":
    input_file = os.getenv("INPUT_FILE")
    output_file_path = os.getenv("OUTPUT_FILE")
    ranker = ModelRanker(input_file, output_file_path)
    ranker.run()
