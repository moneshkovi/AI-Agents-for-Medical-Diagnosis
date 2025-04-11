# Importing the needed modules 
from dotenv import load_dotenv
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
import os
import sys
import datetime

# Add templates directory to path for importing pdf_utils
sys.path.append(os.path.abspath('templates'))
from pdf_utils import PDFReport

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
    # Save as text file (original functionality)
    final_diagnosis_text = "### Final Diagnosis:\n\n" + final_diagnosis
    txt_output_path = "Results/final_diagnosis.txt"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(txt_output_path), exist_ok=True)

    # Write the final diagnosis to the text file
    with open(txt_output_path, "w") as txt_file:
        txt_file.write(final_diagnosis_text)

    print(f"Final diagnosis has been saved to {txt_output_path}")
    
    # Generate PDF report (new functionality)
    try:
        pdf_generator = PDFReport(output_dir="Results")
        
        # Get report name from file path
        report_name = os.path.basename(report_path).replace("_Patient.txt", "").replace("_", " ")
        
        # Generate PDF filename based on medical condition
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"{report_name}_Report_{timestamp}.pdf"
        
        pdf_path = pdf_generator.generate_pdf(
            medical_report=medical_report,
            cardiologist_report=responses["Cardiologist"],
            psychologist_report=responses["Psychologist"],
            pulmonologist_report=responses["Pulmonologist"],
            final_diagnosis=final_diagnosis,
            output_filename=pdf_filename
        )
        
        print(f"\nPDF report has been generated: {pdf_path}")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
    
    print("\nDiagnosis Summary:")
    print(final_diagnosis)
else:
    print("Error: Could not generate final diagnosis")
