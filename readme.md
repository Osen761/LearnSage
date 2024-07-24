


# LearnSage: An AI Learning Assistant

LearnSage is a personalized learning platform that provides interactive educational experiences tailored to your unique learning style. Whether you're a student, a professional, or a lifelong learner, LearnSage is here to support your journey.
And It is alive [here](learnsage.streamlit.app)
#### It may not be alive sometimes since i am using my own api and they are paid for and i cant manage all the costs. 

## Features

With LearnSage, you can:

- **Ask Questions:** Ask any question and get instant answers.
- **Generate Report:** Create a detailed report on a topic of your choice.
- **Interact with your files:** Upload documents to interact with and analyze.
- **Interact with images:** Upload images and ask questions.
- **Summarize Documents:** Get a summary of your documents.
- **Quick Internet Search:** Perform quick searches on the web.
- **Download Summary:** Download a summary of your learning session.
- **Generate Q&A:** Create questions and answers based on your learning material.

## How It Works

1. **Get API Keys:**
   First, obtain your API keys from the following services:
   - [Google AI Studio](https://aistudio.google.com/)
   - [Assembly AI](https://www.assemblyai.com/)
   - [Tavily](https://www.tavily.com/)

2. **Upload Your Keys:**
   Start by uploading your learning keys to personalize your experience.

3. **Choose Your Learning Style:**
   Select a learning style that best suits you—whether it's visual, auditory, or kinesthetic.

4. **Select a Feature:**
   Pick a feature from the sidebar, such as report generation, document interaction, or quick summaries, and start your learning journey.

5. **Begin Learning:**
   Dive into personalized content and interactive materials designed to enhance your learning process.

For more detailed imformation about it refer check out the blog At **OsenInsights** [here](oseninsights.tech)

## Running Locally

To run LearnSage locally, follow these steps:

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/Osen761/LearningSage.git
   cd learningsage
   ```

2. **Install Dependencies:**
   Ensure you have Python installed, then install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. **Create Configuration Folder:**
   Create a `.streamlit` folder in the root directory of the project:
   ```sh
   mkdir .streamlit
   ```

4. **Create `secrets.toml` File:**
   Inside the `.streamlit` folder, create a `secrets.toml` file and store your API keys:
   ```toml
   [api_keys]
   GOOGLE_API_KEY = "YOUR_GOOGLE_AI_STUDIO_KEY"
   ASSEMBLYAI_API_KEY= "YOUR_ASSEMBLY_AI_KEY"
   TAVILY_API_KEY= "YOUR_TAVILY_KEY"
   ```

5. **Run the App:**
   Start the Streamlit app:
   ```sh
   streamlit run User_interface.py
   ```


Make sure to replace `"YOUR_GOOGLE_AI_STUDIO_KEY"`, `"YOUR_ASSEMBLY_AI_KEY"`, and `"YOUR_TAVILY_KEY"` with your actual API keys. Adjust the repository URL and any other project-specific details as needed.

## Our Mission

At Learning Sage, we believe that everyone has a unique way of learning. Our mission is to provide personalized educational experiences that help you achieve your goals. Whether you're a student, a professional, or a lifelong learner, Learning Sage is here to support your journey.


## Support

For any issues or questions related to the application, feel free to contact:

- **Osen Muntu**
- **X :** [Osen Insights](https://x.com/osen_muntu)
- **Email :** osenmuntu761@gmail.com
- **Blog :** [oseninsights.tech](https://oseninsights.tech)

## Contributing

Contributions are welcome! If you have any suggestions, feature requests, or bug fixes, please submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

