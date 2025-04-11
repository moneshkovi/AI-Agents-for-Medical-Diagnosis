# Importing the needed modules 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
import json, os, glob, sys
import datetime
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add templates directory to path for importing pdf_utils
sys.path.append(os.path.abspath('templates'))
from pdf_utils import PDFReport

# Loading API key from a dotenv file.
load_dotenv(dotenv_path='apikey.env')

# Get available medical reports
def get_medical_reports():
    return sorted([os.path.basename(f) for f in glob.glob("Medical Reports/*.txt")])

# Select medical report
def select_report():
    reports = get_medical_reports()
    print("\nAvailable Medical Reports:")
    for i, report in enumerate(reports, 1):
        print(f"{i}. {report}")
    
    while True:
        try:
            choice = int(input("\nSelect a report to analyze (enter number): "))
            if 1 <= choice <= len(reports):
                return f"Medical Reports/{reports[choice-1]}"
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

# Get selected report
report_path = select_report()
print(f"\nAnalyzing: {report_path}")

# Read the medical report
with open(report_path, "r") as file:
    medical_report = file.read()


agents = {
    "Cardiologist": Cardiologist(medical_report),
    "Psychologist": Psychologist(medical_report),
    "Pulmonologist": Pulmonologist(medical_report)
}

# Function to run each agent and get their response
def get_response(agent_name, agent):
    response = agent.run()
    return agent_name, response

# Run the agents concurrently and collect responses
responses = {}
with ThreadPoolExecutor() as executor:
    futures = {executor.submit(get_response, name, agent): name for name, agent in agents.items()}
    
    for future in as_completed(futures):
        agent_name, response = future.result()
        responses[agent_name] = response

team_agent = MultidisciplinaryTeam(
    cardiologist_report=responses["Cardiologist"],
    psychologist_report=responses["Psychologist"],
    pulmonologist_report=responses["Pulmonologist"]
)

# Run the MultidisciplinaryTeam agent to generate the final diagnosis
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
    
    # Generate PDF report
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
