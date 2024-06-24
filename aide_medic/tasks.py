from crewai import Task
from textwrap import dedent

"""
Creating Tasks Cheat Sheet:
- Begin with the end in mind. Identify the specific outcome your tasks are aiming to achieve.
- Break down the outcome into actionable tasks, assigning each task to the appropriate agent.
- Ensure tasks are descriptive, providing clear instructions and expected deliverables.

Goal:
- Diagnostiquer le patient et recommander des traitements appropriés basés sur les symptômes présentés.

Key Steps for Task Creation:
1. Identify the Desired Outcome: Define what success looks like for your project.
    - Un diagnostic précis basé sur les symptômes du patient.

2. Task Breakdown: Divide the goal into smaller, manageable tasks that agents can execute.
    - Analyse des Symptômes: Examiner et interpréter les symptômes pour identifier des diagnostics potentiels.
    - Diagnostic Médical: Évaluer les symptômes analysés pour établir un diagnostic final.
    - Recommandation de Traitements: Proposer des traitements et des actions basées sur le diagnostic.

3. Assign Tasks to Agents: Match tasks with agents based on their roles and expertise.

4. Task Description Template:
  - Use this template as a guide to define each task in your CrewAI application. 
  - This template helps ensure that each task is clearly defined, actionable, and aligned with the specific goals of your project.
"""

class MedicalTasks:
    def __tip_section(self):
        return "Accurate diagnosis can lead to better patient outcomes!"

    def analyse(self, agent, nom, age, poids, symptoms, patient_history):
        return Task(
            description=dedent(
                f"""
                **Task**: Analyser les Symptômes
                **Description**: par rapport aux symptoms et les information de patient sur tout sur les symptoms et sur son maladie cronique et par la recherche effectuer en ligne sur DuckDuckGo pour obtenir des informations sur les symptômes spécifiés. 
                    Utilisez les résultats de recherche pour trouver des articles, des sites médicaux et d'autres sources fiables qui décrivent les symptômes et les maladies associées. 
                    Compilez et analysez ces informations pour identifier les maladies probables. 
                    L'agent doit faire des connexions entre les symptômes et les maladies possibles, et fournir une synthèse claire des informations trouvées.

                **Parameters**: 
                - Nom: {nom}
                - Age: {age}
                - Poids: {poids}
                - Symptômes: {symptoms}
                - Historique Médical: {patient_history}
                

                **Note**: {self.__tip_section()}
        """
            ),
            expected_output="Liste des diagnostics potentiels",
            agent=agent,
        )

    def repport(self, agent, nom, age, poids, symptoms, patient_history):
        return Task(
            description=dedent(
                f"""
                **Task**: reporter task
                **Description**: Générer un rapport de diagnostic complet basé sur les analyses du médecin en francais. 
                    Le rapport doit inclure les diagnostics possibles, des explications sur chaque diagnostic, des recommandations pour des tests supplémentaires si nécessaire, et des conseils pour les soins du patient.

                **Parameters**: 
                - Nom: {nom}
                - Age: {age}
                - Poids: {poids}
                - Symptômes: {symptoms}
                - Historique Médical: {patient_history}
                **Note**: {self.__tip_section()}
        """
            ),
            expected_output="Rapport médical détaillé",
            agent=agent,
        )