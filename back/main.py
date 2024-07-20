# app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.agents import load_tools
from crewai import Agent, Task, Crew
from crewai.project import crew, agent, task, CrewBase
from tasks import MedicalTasks
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from langchain_groq import ChatGroq

load_dotenv()

@CrewBase
class MedicalCrew:
    """Medical Crew"""

    agents_config = "config/medical/medical_agents_config.yaml"

    def __init__(self, nom, age, poids, symptoms, patient_history) -> None:
        self.groc_llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
        self.nom = nom
        self.age = age
        self.poids = poids
        self.symptoms = symptoms
        self.patient_history = patient_history
        self.human_tools = load_tools(["human"])
        self.search_tool = SerperDevTool()

    @agent
    def doctor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["agents"]["doctor_agent"],
            tools=[self.search_tool],
            llm=self.groc_llm,
        )

    @agent
    def reporter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["agents"]["reporter_agent"],
            llm=self.groc_llm,
        )

    @crew
    def medical_crew(self) -> Crew:
        task = MedicalTasks()
        analyse = task.analyse(
            nom=self.nom,
            age=self.age,
            poids=self.poids,
            symptoms=self.symptoms,
            patient_history=self.patient_history,
            agent=self.doctor_agent(),
        )
        reporter = task.repport(
            nom=self.nom,
            age=self.age,
            poids=self.poids,
            symptoms=self.symptoms,
            patient_history=self.patient_history,
            agent=self.reporter_agent(),
        )
        return Crew(agents=self.agents, tasks=[analyse, reporter], verbose=True)

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Define endpoint to run the medical crew
@app.route('/run_medical_crew', methods=['POST'])
def run_medical_crew():
    try:
        data = request.json
        # Extract data from the POST request
        nom = data.get('nom', "")
        age = data.get('age', 0)
        poids = data.get('poids', 0)
        symptoms = data.get('symptoms', "")
        patient_history = data.get('patient_history', "")
        
        # Initialize and run the medical crew
        medical_crew = MedicalCrew(nom, age, poids, symptoms, patient_history)
        crew = medical_crew.medical_crew()
        result = crew.kickoff()

        # Extract the text from CrewOutput if it's not already serializable
        result_text = ""
        if hasattr(result, 'text'):
            result_text = result.text
        elif isinstance(result, str):
            result_text = result
        else:
            result_text = str(result)

        return jsonify({"status": "success", "result": result_text})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Define a health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "API is running"})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
