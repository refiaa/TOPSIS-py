import os
import pandas as pd
import numpy as np

from typing import Tuple, List
from dotenv import load_dotenv


load_dotenv()

class ModelDataLoader:
    @staticmethod
    def load_criteria_from_env() -> Tuple[List[str], List[float], List[bool]]:
        criteria = os.getenv("CRITERIA").split(",")
        weights = list(map(float, os.getenv("WEIGHTS").split(",")))
        benefit_criteria = list(map(lambda x: x.lower() == 'true', os.getenv("BENEFIT_CRITERIA").split(",")))
        return criteria, weights, benefit_criteria

    @staticmethod
    def load_data(file_path: str, axis: str = None) -> Tuple[List[str], np.ndarray]:
        try:
            df = pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            raise ValueError(f"File {file_path} is empty or cannot be read.")
        except FileNotFoundError:
            raise ValueError(f"File {file_path} not found.")

        df.columns = df.columns.str.strip()
        if axis:
            if "Axis" not in df.columns:
                raise ValueError(f"Column 'Axis' not found in {file_path}.")
            df = df[df["Axis"] == axis]

        criteria, _, _ = ModelDataLoader.load_criteria_from_env()
        decision_matrix = df[criteria].values
        models = df["Model"].values
        return models, decision_matrix
