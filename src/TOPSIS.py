import numpy as np

from typing import List, Tuple

class TOPSIS:
    def __init__(self, decision_matrix: np.ndarray, weights: List[float], benefit_criteria: List[bool]):
        self.decision_matrix = np.array(decision_matrix)
        self.weights = np.array(weights)
        self.benefit_criteria = benefit_criteria
        self.normalized_matrix: np.ndarray = np.array([])
        self.weighted_normalized_matrix: np.ndarray = np.array([])
        self.positive_ideal_solution: np.ndarray = np.array([])
        self.negative_ideal_solution: np.ndarray = np.array([])
        self.scores: np.ndarray = np.array([])
        self.positive_distances: np.ndarray = np.array([])
        self.negative_distances: np.ndarray = np.array([])

    def normalize(self):
        norms = np.sqrt(np.sum(self.decision_matrix ** 2, axis=0))
        self.normalized_matrix = self.decision_matrix / norms

    def apply_weights(self):
        self.weighted_normalized_matrix = self.normalized_matrix * self.weights

    def determine_ideal_solutions(self):
        self.positive_ideal_solution = np.max(self.weighted_normalized_matrix, axis=0)
        self.negative_ideal_solution = np.min(self.weighted_normalized_matrix, axis=0)
        for i, is_benefit in enumerate(self.benefit_criteria):
            if not is_benefit:
                self.positive_ideal_solution[i], self.negative_ideal_solution[i] = (
                    self.negative_ideal_solution[i],
                    self.positive_ideal_solution[i],
                )

    def calculate_separation_measures(self):
        self.positive_distances = np.linalg.norm(
            self.weighted_normalized_matrix - self.positive_ideal_solution, axis=1
        )
        self.negative_distances = np.linalg.norm(
            self.weighted_normalized_matrix - self.negative_ideal_solution, axis=1
        )

    def calculate_scores(self):
        self.calculate_separation_measures()
        self.scores = self.negative_distances / (self.positive_distances + self.negative_distances)

    def get_detailed_separations(self) -> Tuple[np.ndarray, np.ndarray]:
        positive_separations = np.abs(self.weighted_normalized_matrix - self.positive_ideal_solution)
        negative_separations = np.abs(self.weighted_normalized_matrix - self.negative_ideal_solution)
        return positive_separations, negative_separations

    def rank(self) -> Tuple[np.ndarray, np.ndarray]:
        self.normalize()
        self.apply_weights()
        self.determine_ideal_solutions()
        self.calculate_scores()
        return np.argsort(-self.scores), self.scores

    def get_proximity_scores(self) -> np.ndarray:
        positive_separations, negative_separations = self.get_detailed_separations()
        proximities = negative_separations / (positive_separations + negative_separations)
        return proximities
