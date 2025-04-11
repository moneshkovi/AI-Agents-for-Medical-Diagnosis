# Importing the needed modules 
from dotenv import load_dotenv
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
import os

# Loading API key from the dotenv file
load_dotenv(dotenv_path='apikey.env')

# Set the report path directly for testing
report_path = "Medical Reports/Rheumatoid_Arthritis.txt"
print(f"\nAnalyzing: {report_path}")

# Read the medical report
with open(report_path, "r") as file:
    medical_report = file.read()

# Initialize the agents
agents = {
    "Cardiologist": Cardiologist(medical_report),
    "Psychologist": Psychologist(medical_report),
    "Pulmonologist": Pulmonologist(medical_report)
}

# Run each agent sequentially for testing purposes
responses = {}
for name, agent in agents.items():
    print(f"Running {name}...")
    response = agent.run()
    print(f"{name} completed")
    responses[name] = response

# Run the MultidisciplinaryTeam agent
print("Running MultidisciplinaryTeam...")
team_agent = MultidisciplinaryTeam(
    cardiologist_report=responses.get("Cardiologist"),
    psychologist_report=responses.get("Psychologist"),
    pulmonologist_report=responses.get("Pulmonologist")
)

# Generate the final diagnosis
final_diagnosis = team_agent.run()
if final_diagnosis:
    final_diagnosis_text = "### Final Diagnosis:\n\n" + final_diagnosis
    txt_output_path = "Results/final_diagnosis.txt"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(txt_output_path), exist_ok=True)

    # Write the final diagnosis to the text file
    with open(txt_output_path, "w") as txt_file:
        txt_file.write(final_diagnosis_text)

    print(f"Final diagnosis has been saved to {txt_output_path}")
    print("\nDiagnosis Summary:")
    print(final_diagnosis)
else:
    print("Error: Could not generate final diagnosis")
