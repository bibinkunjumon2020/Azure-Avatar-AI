# Azure Text to Avatar Video Synthesis ![Avatar Image](avatar.png)

This Streamlit application allows you to synthesize text into avatar videos using Microsoft Azure's Text to Speech with Avatar service.
## Generated Video-Demo


## Getting Started

### Prerequisites

Before running the application, ensure you have the following:

- **Azure Subscription**: You need an active Azure subscription.
- **Azure Speech API Subscription Key**: Obtain this key from your Azure portal.
- **Service Region**: Select one of the supported regions: West US 2, West Europe, or Southeast Asia.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your/repository.git
   cd repository-directory
2. Install the required Python packages:
pip install -r requirements.txt

3. Running the Application
streamlit run main.py


## Usage
Fill in Subscription Key and Region: Enter your Speech API subscription key and select the service region from the dropdown.

Enter Text: Input the text that you want to synthesize into an avatar video.

Submit: Click on the "Submit" button to initiate the avatar synthesis job.

Monitor Job Status: Once submitted, the application will display the job status (running, succeeded, or failed) and provide a download link for the video upon successful completion.

List Jobs: You can also view a list of previously submitted batch synthesis jobs and their details.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


## Acknowledgments
Microsoft Azure for providing the Text to Speech with Avatar service.
Streamlit for the user-friendly web application framework.
## Author
BIBIN KUNJUMON
bibinkunjumon2020@gmail.com