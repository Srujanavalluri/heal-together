"""
assessments.py - OOP Assessment Architecture for Heal-Together
Demonstrates Python OOP concepts (Days 17-22):
- Day 17: Classes, Objects, Instance variables, Constructors (__init__)
- Day 18: Member functions, Encapsulation, Single inheritance
- Day 19: super(), Constructors
- Day 20: Hierarchical inheritance (Multiple assessments inherit from Base Assessment)
- Day 21: Method overriding, Polymorphism
- Day 22: abc module, ABC, @abstractmethod (Abstract Base Classes)
"""

from abc import ABC, abstractmethod


# ====================================================================
# BASE ABSTRACT CLASS (Day 17-22: Abstraction, Encapsulation, Classes)
# ====================================================================
class Assessment(ABC):
    """
    Abstract Base Class representing a general self-reflection assessment.
    Encapsulates core assessment attributes and defines common abstract interface.
    """

    def __init__(self, assessment_type: str, max_score: int):
        # Protected instance variables demonstrating encapsulation (Day 17 & 18)
        self._assessment_type = assessment_type
        self._max_score = max_score

    @property
    def assessment_type(self) -> str:
        """Getter for assessment type."""
        return self._assessment_type

    @property
    def max_score(self) -> int:
        """Getter for maximum possible score."""
        return self._max_score

    @abstractmethod
    def calculate_score(self, responses: list[int]) -> int:
        """
        Abstract method (Day 22) to calculate assessment score from user responses.
        Must be implemented by all concrete subclasses.
        """
        pass

    @abstractmethod
    def get_interpretation(self, score: int) -> str:
        """
        Abstract method (Day 22) to interpret the calculated score.
        Must be implemented by all concrete subclasses.
        """
        pass

    # Concrete method (Day 22: Concrete methods in ABC)
    def get_disclaimer(self) -> str:
        """Returns the non-diagnostic disclaimer for all assessments."""
        return (
            "🌿 Note: This assessment is designed solely as a self-reflection and well-being tool "
            "to help you understand your thoughts and emotions. It is not a clinical or medical diagnosis."
        )


# ====================================================================
# 1. MENTAL HEALTH ASSESSMENT CLASS (Day 18, 19, 21: Single Inheritance & Overriding)
# ====================================================================
class MentalHealthAssessment(Assessment):
    """
    Mental Health Assessment class for emotional well-being check-ins.
    Inherits from Assessment (Day 18).
    """

    def __init__(self):
        # Calling parent constructor using super() (Day 19)
        super().__init__(assessment_type="Mental Health", max_score=20)

    # Method Overriding & Polymorphism (Day 21)
    def calculate_score(self, responses: list[int]) -> int:
        """
        Calculates Mental Health score.
        Responses 1-4 are scored normally, response 5 is reverse-scored for hopefulness.
        """
        if len(responses) < 5:
            return 0
        q1, q2, q3, q4, q5 = responses[:5]
        # Question 5 is reverse-scored (4 - q5)
        total = q1 + q2 + q3 + q4 + (4 - q5)
        return total

    # Method Overriding & Polymorphism (Day 21)
    def get_interpretation(self, score: int) -> str:
        """Returns empathetic interpretation based on emotional score."""
        if 0 <= score <= 4:
            return "Positive Well-being: You are maintaining a healthy emotional balance."
        elif 5 <= score <= 8:
            return "Mild Distress: Some days feel heavier; gentle self-care is recommended."
        elif 9 <= score <= 12:
            return "Moderate Distress: Your heart deserves kindness and extra breathing space."
        elif 13 <= score <= 16:
            return "Noticeable Strain: Struggles become lighter when shared with trusted people."
        else:
            return "Significant Emotional Load: Please reach out for support and gentle care."


# ====================================================================
# 2. LONELINESS ASSESSMENT CLASS (Day 18, 19, 21: Single Inheritance & Overriding)
# ====================================================================
class LonelinessAssessment(Assessment):
    """
    Loneliness Assessment class for social connection check-ins.
    Inherits from Assessment (Day 18).
    """

    def __init__(self):
        # Calling parent constructor using super() (Day 19)
        super().__init__(assessment_type="Loneliness", max_score=20)

    # Method Overriding & Polymorphism (Day 21)
    def calculate_score(self, responses: list[int]) -> int:
        """
        Calculates Loneliness score.
        Responses 1-3 scored directly; 4 & 5 reverse-scored for companionship/belonging.
        """
        if len(responses) < 5:
            return 0
        q1, q2, q3, q4, q5 = responses[:5]
        total = q1 + q2 + q3 + (4 - q4) + (4 - q5)
        return total

    # Method Overriding & Polymorphism (Day 21)
    def get_interpretation(self, score: int) -> str:
        """Returns supportive interpretation based on loneliness score."""
        if 0 <= score <= 4:
            return "Strongly Connected: You feel a healthy sense of belonging and community."
        elif 5 <= score <= 8:
            return "Mild Disconnection: Occasional feelings of distance; nurturing existing bonds can help."
        elif 9 <= score <= 12:
            return "Moderate Loneliness: Your heart deserves to be heard; consider sharing your thoughts."
        elif 13 <= score <= 16:
            return "Noticeable Isolation: Heavy feelings of detachment; small social outreach steps are encouraged."
        else:
            return "Deep Isolation: Please remember you don't have to face this alone. Reach out for care."


# ====================================================================
# 3. COMBINED ASSESSMENT CLASS (Day 20 & 21: Hierarchical Inheritance & Polymorphism)
# ====================================================================
class CombinedAssessment(Assessment):
    """
    Combined Assessment for assessing both Mental Health and Loneliness together.
    Inherits from Assessment (Day 20).
    """

    def __init__(self):
        super().__init__(assessment_type="Both", max_score=40)
        # Composition of specialized assessment models
        self.mh_calculator = MentalHealthAssessment()
        self.lon_calculator = LonelinessAssessment()

    # Method Overriding & Polymorphism (Day 21)
    def calculate_score(self, responses: list[int]) -> tuple[int, int, int]:
        """
        Calculates individual (Mental Health, Loneliness) scores and total score.
        Returns: (mental_score, loneliness_score, total_score)
        """
        if len(responses) < 10:
            return 0, 0, 0
        mh_responses = responses[:5]
        lon_responses = responses[5:10]

        # Calculate using individual polymorphic calculators
        mh_score = self.mh_calculator.calculate_score(mh_responses)
        lon_score = sum(lon_responses)
        total_score = mh_score + lon_score

        return mh_score, lon_score, total_score

    # Method Overriding & Polymorphism (Day 21)
    def get_interpretation(self, score: int) -> str:
        """Returns comprehensive reflection for total combined score."""
        if score <= 10:
            return "Balanced & Grounded: You have a healthy emotional state and strong feelings of connection."
        elif score <= 20:
            return "Mild Stress / Solitude: Minor emotional fluctuations; self-reflection and gentle connection are helpful."
        elif score <= 30:
            return "Moderate Burden: Feeling strained in mind and connection; consider opening up to someone you trust."
        else:
            return "Significant Emotional Load: Please seek supportive companionship and take gentle steps toward self-care."


# ====================================================================
# 4. GENERAL WELLBEING ASSESSMENT CLASS (Day 21: Polymorphic Subclass)
# ====================================================================
class GeneralWellbeingAssessment(Assessment):
    """
    General Wellbeing Check-In for users unsure about their specific state.
    Inherits from Assessment (Day 21).
    """

    def __init__(self):
        super().__init__(assessment_type="Not Sure", max_score=40)

    # Method Overriding & Polymorphism (Day 21)
    def calculate_score(self, responses: list[int]) -> int:
        """Calculates general wellbeing reflection score."""
        if len(responses) < 10:
            return 0
        q1, q2, q3, q4, q5, q6, q7, q8, q9, q10 = responses[:10]
        score = q1 + q2 + q3 + (4 - q4) + (4 - q5) + q6 + (4 - q7) + q8 + (4 - q9) + (4 - q10)
        return score

    # Method Overriding & Polymorphism (Day 21)
    def get_interpretation(self, score: int) -> str:
        """Returns reflective interpretation for general wellbeing."""
        if 0 <= score <= 8:
            return "Balanced & Centered: You are navigating your daily experiences with clarity."
        elif 9 <= score <= 16:
            return "Gentle Awareness: Subtle shifts in feelings; taking quiet reflective pauses is beneficial."
        elif 17 <= score <= 24:
            return "Moderate Uncertainty: You may be carrying mixed emotions; give yourself patience."
        elif 25 <= score <= 32:
            return "Elevated Stress: Sharing your thoughts with a trusted friend can lighten the load."
        else:
            return "Heavy Burden: Please consider reaching out for extra guidance and gentle care."
