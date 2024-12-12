import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults

# Model and Agent tools
llm = ChatGroq(api_key=st.secrets.get("GROQ_API_KEY"))
search = TavilySearchResults(max_results=2)
parser = StrOutputParser()

# Page Header
st.title("Sales Insights Assistant")
st.markdown("Your AI-powered assistant to gain actionable sales insights.")

# Sidebar for Navigation
st.sidebar.header("Navigation")
page_selection = st.sidebar.radio("Go to:", ["Home", "Generate Insights", "Settings"])

if page_selection == "Home":
    st.header("Welcome to the Sales Insights Assistant")
    st.markdown("""
    Use this tool to generate strategic insights for your sales efforts. Navigate through the options in the sidebar:
    - **Generate Insights:** Provide inputs and get actionable reports.
    - **Settings:** Customize your experience.
    """)

elif page_selection == "Generate Insights":
    # Data collection/inputs
    with st.form("sales_info_form", clear_on_submit=True):
        product_name = st.text_input("Product Name:", help="What product are you selling?")
        company_url = st.text_input("Company URL:", help="Website of the target company.")
        product_category = st.text_input("Product Category:", help="Describe the domain of the product.")
        competitors = st.text_area("Competitors (URLs):", help="Provide URLs of competitor companies, separated by commas.")
        value_proposition = st.text_area("Value Proposition:", help="Short description of your product's value.")
        target_customer = st.text_input("Target Customer:", help="Who is your target individual or audience?")
        product_overview = st.file_uploader("Product Overview Sheet (optional):", type=["pdf", "docx", "txt"], help="Upload additional context about the product.")
        export_summary = st.checkbox("Export Summary", help="Generate a downloadable summary.")
        advanced_features = st.checkbox("Enable Advanced Features", help="Include alerts and additional insights.")

        # Placeholder for the insights result
        company_insights = ""
        references = []

        # Process data when form is submitted
        if st.form_submit_button("Generate Insights"):
            if product_name and company_url:
                with st.spinner("Processing..."):
                    try:
                        # Search internet for company data
                        company_data = search.invoke(company_url)
                        
                        # Summarize uploaded document if provided
                        uploaded_document_summary = "No additional context provided."
                        if product_overview:
                            uploaded_document_summary = f"Uploaded document: {product_overview.name}"
                        
                        # Constructing the AI prompt
                        prompt = """
                        You are a Sales Assistant AI prototype designed to assist sales representatives. Your role is to analyze provided inputs, gather insights from public sources, and generate a professional, concise, and actionable one-page summary for the sales representative.

                        Inputs to process:
                        1. Product Name: {product_name}
                        2. Company URL: {company_url}
                        3. Product Category: {product_category}
                        4. Competitors: {competitors}
                        5. Value Proposition: {value_proposition}
                        6. Target Customer: {target_customer}
                        7. Additional Context: {uploaded_document_summary}

                        Task Instructions:
                        1. Company Strategy:
                         - Analyze public statements, press releases, or articles associated with the target company.
                         - Identify key activities or projects that align with the product being sold.
                         - Summarize job postings to infer the company’s focus areas and technology trends.

                        2. Competitor Mentions:
                         - Identify any collaborations, partnerships, or rivalries involving the provided competitors.
                         - Highlight how these competitors are engaging with the target company, if applicable.

                        3. Leadership Information:
                         - List key executives, including titles and recent public statements or contributions.
                         - Focus on individuals relevant to the product's domain or decision-making process.

                        4. Product/Strategy Summary:
                         - Include insights from public reports or relevant online documents.
                         - Relate these findings to the product or value proposition provided.

                        5. References:
                         - Include links to all sources (e.g., articles, press releases) cited in the analysis.

                        Constraints:
                        - Respond only to the specific use case: assisting sales representatives in understanding prospective accounts.
                        - Ensure all insights are accurate, concise, and actionable.
                        """

                        # Prompt Template
                        prompt_template = ChatPromptTemplate([("system", prompt)])
                        
                        # Chain
                        chain = prompt_template | llm | parser

                        # Generate insights
                        company_insights = chain.invoke({
                            "company_url": company_url,
                            "company_data": company_data,
                            "product_name": product_name,
                            "competitors": competitors,
                            "product_category": product_category,
                            "value_proposition": value_proposition,
                            "target_customer": target_customer,
                            "uploaded_document_summary": uploaded_document_summary,
                        })

                        # Collect references from company_data
                        references = company_data.get("references", []) if isinstance(company_data, dict) else []
                    
                    except Exception as e:
                        st.error(f"Error generating insights: {e}")

            else:
                st.error("Please fill in at least the Product Name and Company URL fields.")

    # Display insights
    if company_insights:
        st.subheader("Generated Insights")
        st.markdown(company_insights)

        if references:
            st.subheader("References")
            for ref in references:
                st.markdown(f"- [Source]({ref})")

        if export_summary:
            st.download_button(
                label="Download Summary",
                data=company_insights,
                file_name="sales_insights_summary.txt",
                mime="text/plain"
            )

    # Optional Advanced Features
    if advanced_features:
        st.markdown("### Advanced Features")
        st.markdown("* Alerts: Enable email notifications for updates.")
        st.markdown("* Additional Insights: Include predictive trends or opportunities.")

elif page_selection == "Settings":
    st.header("Settings")
    st.markdown("Adjust your preferences for the Sales Insights Assistant.")
    st.text_input("API Key:", value=st.secrets.get("GROQ_API_KEY"), help="Enter your API key for the LLM.")
    st.slider("Max Results for Search:", 1, 10, value=2, help="Set the maximum number of results for searches.")

