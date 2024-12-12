A link to the live site: https://ai-sale-rep.streamlit.app/

Sales Insights Assistant

The Sales Insights Assistant is a Streamlit-powered web application that helps sales representatives generate actionable insights about target companies and competitors. This tool leverages AI to analyze input data, retrieve relevant information from online sources, and produce professional, concise sales reports.


Features:
*Home Page: An introduction to the tool and its functionality.
*Generate Insights: 
 - Input details about the product, company, competitors, and more.
 - Upload optional product overview documents for additional context.
 - Automatically generate structured insights, including:
    `Company Strategy: Key activities and projects of the target company.
    `Competitor Mentions: Analysis of competitor engagement and collaborations.
    `Leadership Information: Key executives and their relevance to sales.
    `Product/Strategy Summary: Insights into the product's alignment with the company.
    `References: Hyperlinks to sources used in the analysis.
 - Export the generated summary as a text file.
*Settings: Customize your preferences, including API keys and search result limits.


Technology Stack:
Framework: Streamlit https://streamlit.io/
AI Model: LangChain https://www.langchain.com/ with the Groq LLM API
Search Engine: Tavily Search Results for retrieving online information


Installation:
1. Clone the repository: git clone https://github.com/your-username/sales-insights-assistant.git
2. Navigate to the project directory: cd sales-insights-assistant
3. Install the required dependencies: pip install -r requirements.txt
4. Add your Groq API key and other secrets to the .streamlit/secrets.toml file: GROQ_API_KEY = "your-api-key"


Usage:
1. Run the application: streamlit run app.py
2. Open the application in your web browser at http://localhost:8501.
3. Use the sidebar to navigate between pages and provide input to generate sales insights.


Future Enhancements:
 - Integration with additional AI models and data sources.
 - Advanced visualization of generated insights.
 - Email alerts for updates on target company activity.