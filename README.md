# AI-Agents-for-Medical-Diagnostics

<img width="900" alt="image" src="https://github.com/user-attachments/assets/b7c87bf6-dfff-42fe-b8d1-9be9e6c7ce86">

A Python project designed to create specialized LLM-based AI agents that analyze complex medical cases. The system integrates insights from various medical professionals to provide comprehensive assessments and personalized treatment recommendations, demonstrating the potential of AI in multidisciplinary medicine.

## Current Version Overview

In the current version, we have implemented three AI agents using GPT-4o, each specializing in a different aspect of medical analysis. A medical report is passed to each of these agents, who then analyze the report simultaneously using threading, based on their specific area of expertise. Each agent provides recommendations and diagnoses from their perspective. After all AI agents complete their analyses, the results are combined and passed to a large language model, which summarizes the findings and identifies three potential health issues for the patient.

## How to Run on Your Local Machine

### Prerequisites
- Python 3.9 or higher
- Conda (recommended for environment management)
- An OpenAI API key with access to GPT-4o

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AI-Agents-for-Medical-Diagnostics.git
   cd AI-Agents-for-Medical-Diagnostics
   ```

2. **Create and activate a conda environment**
   ```bash
   conda create -n health-agents python=3.9
   conda activate health-agents
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your OpenAI API key**
   - Create an `apikey.env` file in the root directory
   - Add your API key in the following format:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

5. **Run the application**
   ```bash
   python Main.py
   ```

6. **Select a medical report to analyze**
   - The application will display a list of available medical reports
   - Enter the number corresponding to the report you want to analyze
   - The results will be saved in the `Results/final_diagnosis.txt` file

### Example Output
After running the application, the system will process the selected medical report through all three specialist agents and generate a diagnosis listing three possible health issues with supporting evidence.

## AI Agents

**1. Cardiologist Agent**

- **Focus**: Identify any potential cardiac issues that could explain the patient's symptoms, including ruling out conditions such as arrhythmias or structural abnormalities that might not be apparent in initial evaluations.
  
- **Recommendation**: Suggest additional cardiovascular testing or continuous monitoring if necessary to uncover hidden heart-related problems. Provide management strategies if a cardiovascular issue is identified.

**2. Psychologist Agent**

- **Focus**: Determine if the symptoms align with a psychological condition, such as panic disorder or another anxiety-related issue. Assess the impact of stress, anxiety, and lifestyle factors on the patient's overall condition.
  
- **Recommendation**: Recommend appropriate psychological interventions (e.g., therapy, stress management techniques) or medications to address the psychological aspects of the symptoms. Evaluate whether adjustments to the current psychological management are needed.

**3. Pulmonologist Agent**

- **Focus**: Assess whether symptoms like shortness of breath and dizziness are due to a respiratory condition, such as asthma or a breathing disorder, that could mimic cardiac symptoms.
  
- **Recommendation**: Suggest additional respiratory evaluations, such as lung function tests or exercise-induced bronchoconstriction tests, to rule out any underlying lung conditions. Recommend breathing exercises or other treatments if a respiratory issue is suspected.

## Repository Structure

- **Medical Reports Folder**: Contains various synthetic medical reports covering different conditions
- **Utils Folder**: Contains the AI agent implementations and helper functions
- **Results Folder**: Stores the outputs of the agentic system

## Troubleshooting

- If you encounter API errors, verify that your OpenAI API key is correct and has sufficient quota
- If the application cannot find a medical report, check the file paths and ensure the Medical Reports directory contains the expected files
- For Python package conflicts, try creating a fresh conda environment and reinstalling the dependencies

## Future Enhancements

In future versions, the system could expand to include a broader range of AI agents, each specializing in different medical fields, such as neurology, endocrinology, and immunology, to provide even more comprehensive analyses. These AI agents could be implemented using the [Assistant API from OpenAI](https://platform.openai.com/docs/assistants/overview) and use `function calling` and `code interpreter` capabilities to enhance their intelligence and effectiveness. Additionally, advanced parsing methodologies could be introduced to handle medical reports with more complex structures, allowing the system to accurately interpret and analyze a wider variety of medical data.
