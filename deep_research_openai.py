import asyncio
import streamlit as st
from typing import Dict, Any, List
from agents import Agent, Runner, trace
from agents import set_default_openai_key
from firecrawl import FirecrawlApp
from agents.tool import function_tool

# Set page configuration
st.set_page_config(
    page_title="FactFlux",
    page_icon="📘",
    layout="wide"
)

# ✅ Load API keys from Streamlit Secrets if available (for deployed version)
openai_api_key = st.secrets.get("OPENAI_API_KEY", "")
firecrawl_api_key = st.secrets.get("FIRECRAWL_API_KEY", "")

# ✅ If running locally, allow manual API key entry in sidebar
with st.sidebar:
    st.title("🔑 API Configuration")

    if not openai_api_key:
        openai_api_key = st.text_input("OpenAI API Key", type="password")

    if not firecrawl_api_key:
        firecrawl_api_key = st.text_input("Firecrawl API Key", type="password")

    # Store in session state
    st.session_state.openai_api_key = openai_api_key
    st.session_state.firecrawl_api_key = firecrawl_api_key

    # Set OpenAI API key globally
    if openai_api_key:
        set_default_openai_key(openai_api_key)

# Main content
st.title("📘 FactFlux")
st.markdown("A smart research agent that explores, extracts, and elevates web knowledge using OpenAI's Agents SDK and Firecrawl integration.")

# Research topic input
research_topic = st.text_input("Enter your research topic:", placeholder="e.g., Latest developments in AI")

# ✅ Deep Research Function using Firecrawl API
@function_tool
async def deep_research(query: str, max_depth: int, time_limit: int, max_urls: int) -> Dict[str, Any]:
    """ Perform comprehensive web research using Firecrawl's deep research endpoint. """
    try:
        firecrawl_app = FirecrawlApp(api_key=st.session_state.firecrawl_api_key)

        params = {
            "maxDepth": max_depth,
            "timeLimit": time_limit,
            "maxUrls": max_urls
        }

        def on_activity(activity):
            st.write(f"[{activity['type']}] {activity['message']}")

        with st.spinner("Performing deep research..."):
            results = firecrawl_app.deep_research(query=query, params=params, on_activity=on_activity)

        return {
            "success": True,
            "final_analysis": results['data']['finalAnalysis'],
            "sources_count": len(results['data']['sources']),
            "sources": results['data']['sources']
        }
    except Exception as e:
        st.error(f"Deep research error: {str(e)}")
        return {"error": str(e), "success": False}

# ✅ Define AI Agents
research_agent = Agent(
    name="research_agent",
    instructions="""You are a research assistant that can perform deep web research on any topic.

    When given a research topic or question:
    1. Use the deep_research tool to gather comprehensive information.
       - Always use these parameters:
         * max_depth: 3 (for moderate depth)
         * time_limit: 180 (3 minutes)
         * max_urls: 10 (sufficient sources)
    2. The tool will search the web, analyze multiple sources, and provide a synthesis.
    3. Review the research results and organize them into a well-structured report.
    4. Include proper citations for all sources.
    5. Highlight key findings and insights.
    """,
    tools=[deep_research]
)

elaboration_agent = Agent(
    name="elaboration_agent",
    instructions="""You are an expert content enhancer specializing in research elaboration.

    When given a research report:
    1. Analyze the structure and content of the report.
    2. Enhance the report by:
       - Adding more detailed explanations of complex concepts.
       - Including relevant examples, case studies, and real-world applications.
       - Expanding on key points with additional context and nuance.
       - Adding visual elements descriptions (charts, diagrams, infographics).
       - Incorporating latest trends and future predictions.
       - Suggesting practical implications for different stakeholders.
    3. Maintain academic rigor and factual accuracy.
    4. Preserve the original structure while making it more comprehensive.
    5. Ensure all additions are relevant and valuable to the topic.
    """
)

# ✅ Run Research Process
async def run_research_process(topic: str):
    """Run the complete research process."""
    
    with st.spinner("Conducting initial research..."):
        research_result = await Runner.run(research_agent, topic)
        initial_report = research_result.final_output

    # Display initial report
    with st.expander("📄 View Initial Research Report"):
        st.markdown(initial_report)

    # Enhance the report
    with st.spinner("Enhancing the report with additional insights..."):
        elaboration_input = f"""
        RESEARCH TOPIC: {topic}
        
        INITIAL RESEARCH REPORT:
        {initial_report}
        
        Please enhance this research report with additional information, examples, case studies, 
        and deeper insights while maintaining its academic rigor and factual accuracy.
        """

        elaboration_result = await Runner.run(elaboration_agent, elaboration_input)
        enhanced_report = elaboration_result.final_output

    return enhanced_report

# ✅ Handle Button Click to Start Research
if st.button("🚀 Start Research", disabled=not (openai_api_key and firecrawl_api_key and research_topic)):
    if not openai_api_key or not firecrawl_api_key:
        st.warning("⚠️ Please enter both API keys in the sidebar or configure them in Streamlit Secrets.")
    elif not research_topic:
        st.warning("⚠️ Please enter a research topic.")
    else:
        try:
            report_placeholder = st.empty()
            enhanced_report = asyncio.run(run_research_process(research_topic))

            report_placeholder.markdown("## 📑 Enhanced Research Report")
            report_placeholder.markdown(enhanced_report)

            # Add download button
            st.download_button(
                "📥 Download Report",
                enhanced_report,
                file_name=f"{research_topic.replace(' ', '_')}_report.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("🚀 Powered by OpenAI Agents SDK and Firecrawl")
