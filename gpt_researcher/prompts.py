import warnings
from datetime import date, datetime, timezone

from langchain.docstore.document import Document

from .config import Config
from .utils.enum import ReportSource, ReportType, Tone
from .utils.enum import PromptFamily as PromptFamilyEnum
from typing import Callable, List, Dict, Any


## Prompt Families #############################################################

class PromptFamily:
    """General purpose class for prompt formatting.

    This may be overwritten with a derived class that is model specific. The
    methods are broken down into two groups:

    1. Prompt Generators: These follow a standard format and are correlated with
        the ReportType enum. They should be accessed via
        get_prompt_by_report_type

    2. Prompt Methods: These are situation-specific methods that do not have a
        standard signature and are accessed directly in the agent code.

    All derived classes must retain the same set of method names, but may
    override individual methods.
    """
    # 提示词生成器：这些遵循标准格式，与ReportType枚举相关联。
    # 应通过get_prompt_by_report_type访问它们
    
    # 提示词方法：这些是特定情况的方法，没有标准签名，
    # 在代理代码中直接访问
    
    # 所有派生类必须保留相同的方法名称集，但可以
    # 覆盖单个方法


    def __init__(self, config: Config):
        """Initialize with a config instance. This may be used by derived
        classes to select the correct prompting based on configured models and/
        or providers
        """
        self.cfg = config

    # MCP-specific prompts
    @staticmethod
    def generate_mcp_tool_selection_prompt(query: str, tools_info: List[Dict], max_tools: int = 3) -> str:
        """
        Generate prompt for LLM-based MCP tool selection.
        
        Args:
            query: The research query
            tools_info: List of available tools with their metadata
            max_tools: Maximum number of tools to select
            
        Returns:
            str: The tool selection prompt
        """
        import json
        
        return f"""You are a research assistant helping to select the most relevant tools for a research query.

RESEARCH QUERY: "{query}"

AVAILABLE TOOLS:
{json.dumps(tools_info, indent=2)}

TASK: Analyze the tools and select EXACTLY {max_tools} tools that are most relevant for researching the given query.

SELECTION CRITERIA:
- Choose tools that can provide information, data, or insights related to the query
- Prioritize tools that can search, retrieve, or access relevant content
- Consider tools that complement each other (e.g., different data sources)
- Exclude tools that are clearly unrelated to the research topic

Return a JSON object with this exact format:
{{
  "selected_tools": [
    {{
      "index": 0,
      "name": "tool_name",
      "relevance_score": 9,
      "reason": "Detailed explanation of why this tool is relevant"
    }}
  ],
  "selection_reasoning": "Overall explanation of the selection strategy"
}}

Select exactly {max_tools} tools, ranked by relevance to the research query.
""" # MCP工具选择提示：帮助研究助手为研究查询选择最相关的工具，要求分析工具并选择指定数量的最相关工具，返回JSON格式的选择结果

    @staticmethod
    def generate_mcp_research_prompt(query: str, selected_tools: List) -> str:
        """
        Generate prompt for MCP research execution with selected tools.
        
        Args:
            query: The research query
            selected_tools: List of selected MCP tools
            
        Returns:
            str: The research execution prompt
        """
        # Handle cases where selected_tools might be strings or objects with .name attribute
        tool_names = []
        for tool in selected_tools:
            if hasattr(tool, 'name'):
                tool_names.append(tool.name)
            else:
                tool_names.append(str(tool))
        
        return f"""You are a research assistant with access to specialized tools. Your task is to research the following query and provide comprehensive, accurate information.

RESEARCH QUERY: "{query}"

INSTRUCTIONS:
1. Use the available tools to gather relevant information about the query
2. Call multiple tools if needed to get comprehensive coverage
3. If a tool call fails or returns empty results, try alternative approaches
4. Synthesize information from multiple sources when possible
5. Focus on factual, relevant information that directly addresses the query

AVAILABLE TOOLS: {tool_names}

Please conduct thorough research and provide your findings. Use the tools strategically to gather the most relevant and comprehensive information.""" # MCP研究执行提示：指导研究助手使用选定的专业工具进行研究，要求全面准确地收集信息并提供研究结果

    @staticmethod
    def generate_search_queries_prompt(
        question: str,
        parent_query: str,
        report_type: str,
        max_iterations: int = 3,
        context: List[Dict[str, Any]] = [],
    ):
        """Generates the search queries prompt for the given question.
        Args:
            question (str): The question to generate the search queries prompt for
            parent_query (str): The main question (only relevant for detailed reports)
            report_type (str): The report type
            max_iterations (int): The maximum number of search queries to generate
            context (str): Context for better understanding of the task with realtime web information

        Returns: str: The search queries prompt for the given question
        """

        if (
            report_type == ReportType.DetailedReport.value
            or report_type == ReportType.SubtopicReport.value
        ):
            task = f"{parent_query} - {question}"
        else:
            task = question

        context_prompt = f"""
You are a seasoned research assistant tasked with generating search queries to find relevant information for the following task: "{task}".
Context: {context}

Use this context to inform and refine your search queries. The context provides real-time web information that can help you generate more specific and relevant queries. Consider any current events, recent developments, or specific details mentioned in the context that could enhance the search queries.
""" if context else "" # 上下文提示：为经验丰富的研究助手提供任务背景，利用实时网络信息生成更具体和相关的搜索查询

        dynamic_example = ", ".join([f'"query {i+1}"' for i in range(max_iterations)])

        return f"""Write {max_iterations} google search queries to search online that form an objective opinion from the following task: "{task}"

IMPORTANT: All queries MUST be in English. If the task is not in English, translate it and generate English queries.
Assume the current date is {datetime.now(timezone.utc).strftime('%B %d, %Y')} if required.

{context_prompt}
You must respond with a list of strings in the following format: [{dynamic_example}].
Each query should be specific, focused, and in proper English.
Avoid generic terms, use specific product names, technologies, or concepts.
The response should contain ONLY the list.
""" # 搜索查询生成提示：为给定任务生成指定数量的Google搜索查询，要求查询必须是英文，具体且专注，避免通用术语

    @staticmethod
    def generate_report_prompt(
        question: str,
        context,
        report_source: str,
        report_format="apa",
        total_words=1000,
        tone=None,
        language="english",
    ):
        """Generates the report prompt for the given question and research summary.
        Args: question (str): The question to generate the report prompt for
                research_summary (str): The research summary to generate the report prompt for
        Returns: str: The report prompt for the given question and research summary
        """

        reference_prompt = ""
        if report_source == ReportSource.Web.value:
            reference_prompt = f"""
You MUST write all used source urls at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each.
Every url should be hyperlinked: [url website](url)
Additionally, you MUST include hyperlinks to the relevant URLs wherever they are referenced in the report:

eg: Author, A. A. (Year, Month Date). Title of web page. Website Name. [url website](url)
"""
        else:
            reference_prompt = f"""
You MUST write all used source document names at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each."
"""

        tone_prompt = f"Write the report in a {tone.value} tone." if tone else ""

        return f"""
Information: "{context}"
---
Using the above information, answer the following query or task: "{question}" in a detailed report --
The report should focus on the answer to the query, should be well structured, informative,
in-depth, and comprehensive, with facts and numbers if available and at least {total_words} words.
You should strive to write the report as long as you can using all relevant and necessary information provided.

Please follow all of the following guidelines in your report:
- You MUST determine your own concrete and valid opinion based on the given information. Do NOT defer to general and meaningless conclusions.
- You MUST write the report with markdown syntax and {report_format} format.
- Use markdown tables when presenting structured data or comparisons to enhance readability.
- You MUST prioritize the relevance, reliability, and significance of the sources you use. Choose trusted sources over less reliable ones.
- You must also prioritize new articles over older articles if the source can be trusted.
- You MUST NOT include a table of contents. Start from the main report body directly.
- Use in-text citation references in {report_format} format and make it with markdown hyperlink placed at the end of the sentence or paragraph that references them like this: ([in-text citation](url)).
- Don't forget to add a reference list at the end of the report in {report_format} format and full url links without hyperlinks.
- {reference_prompt}
- {tone_prompt}

You MUST write the report in the following language: {language}.
Please do your best, this is very important to my career.
Assume that the current date is {date.today()}.
""" # 报告生成提示：基于提供的信息生成详细报告，要求结构良好、信息丰富、深入全面，包含事实和数字，使用markdown语法和指定格式

    @staticmethod
    def curate_sources(query, sources, max_results=10):
        return f"""Your goal is to evaluate and curate the provided scraped content for the research task: "{query}"
    while prioritizing the inclusion of relevant and high-quality information, especially sources containing statistics, numbers, or concrete data.

The final curated list will be used as context for creating a research report, so prioritize:
- Retaining as much original information as possible, with extra emphasis on sources featuring quantitative data or unique insights
- Including a wide range of perspectives and insights
- Filtering out only clearly irrelevant or unusable content

EVALUATION GUIDELINES:
1. Assess each source based on:
   - Relevance: Include sources directly or partially connected to the research query. Err on the side of inclusion.
   - Credibility: Favor authoritative sources but retain others unless clearly untrustworthy.
   - Currency: Prefer recent information unless older data is essential or valuable.
   - Objectivity: Retain sources with bias if they provide a unique or complementary perspective.
   - Quantitative Value: Give higher priority to sources with statistics, numbers, or other concrete data.
2. Source Selection:
   - Include as many relevant sources as possible, up to {max_results}, focusing on broad coverage and diversity.
   - Prioritize sources with statistics, numerical data, or verifiable facts.
   - Overlapping content is acceptable if it adds depth, especially when data is involved.
   - Exclude sources only if they are entirely irrelevant, severely outdated, or unusable due to poor content quality.
3. Content Retention:
   - DO NOT rewrite, summarize, or condense any source content.
   - Retain all usable information, cleaning up only clear garbage or formatting issues.
   - Keep marginally relevant or incomplete sources if they contain valuable data or insights.

SOURCES LIST TO EVALUATE:
{sources}

You MUST return your response in the EXACT sources JSON list format as the original sources.
The response MUST not contain any markdown format or additional text (like ```json), just the JSON list!
""" # 信息源筛选提示：评估和筛选抓取的内容，优先保留相关和高质量信息，特别是包含统计数据的来源，用于创建研究报告

    @staticmethod
    def generate_resource_report_prompt(
        question, context, report_source: str, report_format="apa", tone=None, total_words=1000, language="english"
    ):
        """Generates the resource report prompt for the given question and research summary.

        Args:
            question (str): The question to generate the resource report prompt for.
            context (str): The research summary to generate the resource report prompt for.

        Returns:
            str: The resource report prompt for the given question and research summary.
        """

        reference_prompt = ""
        if report_source == ReportSource.Web.value:
            reference_prompt = f"""
            You MUST include all relevant source urls.
            Every url should be hyperlinked: [url website](url)
            """
        else:
            reference_prompt = f"""
            You MUST write all used source document names at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each."
        """

        return (
            f'"""{context}"""\n\nBased on the above information, generate a bibliography recommendation report for the following'
            f' question or topic: "{question}". The report should provide a detailed analysis of each recommended resource,'
            " explaining how each source can contribute to finding answers to the research question.\n"
            "Focus on the relevance, reliability, and significance of each source.\n"
            "Ensure that the report is well-structured, informative, in-depth, and follows Markdown syntax.\n"
            "Use markdown tables and other formatting features when appropriate to organize and present information clearly.\n"
            "Include relevant facts, figures, and numbers whenever available.\n"
            f"The report should have a minimum length of {total_words} words.\n"
            f"You MUST write the report in the following language: {language}.\n"
            "You MUST include all relevant source urls."
            "Every url should be hyperlinked: [url website](url)"
            f"{reference_prompt}"
        ) # 资源报告生成提示：基于提供信息生成参考书目推荐报告，详细分析每个推荐资源，解释其对研究问题的贡献

    @staticmethod
    def generate_custom_report_prompt(
        query_prompt, context, report_source: str, report_format="apa", tone=None, total_words=1000, language: str = "english"
    ):
        return f'"{context}"\n\n{query_prompt}' # 自定义报告生成提示：将上下文和查询提示组合生成自定义报告

    @staticmethod
    def generate_outline_report_prompt(
        question, context, report_source: str, report_format="apa", tone=None,  total_words=1000, language: str = "english"
    ):
        """Generates the outline report prompt for the given question and research summary.
        Args: question (str): The question to generate the outline report prompt for
                research_summary (str): The research summary to generate the outline report prompt for
        Returns: str: The outline report prompt for the given question and research summary
        """

        return (
            f'"""{context}""" Using the above information, generate an outline for a research report in Markdown syntax'
            f' for the following question or topic: "{question}". The outline should provide a well-structured framework'
            " for the research report, including the main sections, subsections, and key points to be covered."
            f" The research report should be detailed, informative, in-depth, and a minimum of {total_words} words."
            " Use appropriate Markdown syntax to format the outline and ensure readability."
            " Consider using markdown tables and other formatting features where they would enhance the presentation of information."
        ) # 大纲报告生成提示：基于提供信息生成研究报告大纲，提供结构良好的框架，包括主要章节、子章节和要点

    @staticmethod
    def generate_deep_research_prompt(
        question: str,
        context: str,
        report_source: str,
        report_format="apa",
        tone=None,
        total_words=2000,
        language: str = "english"
    ):
        """Generates the deep research report prompt, specialized for handling hierarchical research results.
        Args:
            question (str): The research question
            context (str): The research context containing learnings with citations
            report_source (str): Source of the research (web, etc.)
            report_format (str): Report formatting style
            tone: The tone to use in writing
            total_words (int): Minimum word count
            language (str): Output language
        Returns:
            str: The deep research report prompt
        """
        reference_prompt = ""
        if report_source == ReportSource.Web.value:
            reference_prompt = f"""
You MUST write all used source urls at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each.
Every url should be hyperlinked: [url website](url)
Additionally, you MUST include hyperlinks to the relevant URLs wherever they are referenced in the report:

eg: Author, A. A. (Year, Month Date). Title of web page. Website Name. [url website](url)
"""
        else:
            reference_prompt = f"""
You MUST write all used source document names at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each."
"""

        tone_prompt = f"Write the report in a {tone.value} tone." if tone else ""

        return f"""
Using the following hierarchically researched information and citations:

"{context}"

Write a comprehensive research report answering the query: "{question}"

The report should:
1. Synthesize information from multiple levels of research depth
2. Integrate findings from various research branches
3. Present a coherent narrative that builds from foundational to advanced insights
4. Maintain proper citation of sources throughout
5. Be well-structured with clear sections and subsections
6. Have a minimum length of {total_words} words
7. Follow {report_format} format with markdown syntax
8. Use markdown tables, lists and other formatting features when presenting comparative data, statistics, or structured information

Additional requirements:
- Prioritize insights that emerged from deeper levels of research
- Highlight connections between different research branches
- Include relevant statistics, data, and concrete examples
- You MUST determine your own concrete and valid opinion based on the given information. Do NOT defer to general and meaningless conclusions.
- You MUST prioritize the relevance, reliability, and significance of the sources you use. Choose trusted sources over less reliable ones.
- You must also prioritize new articles over older articles if the source can be trusted.
- Use in-text citation references in {report_format} format and make it with markdown hyperlink placed at the end of the sentence or paragraph that references them like this: ([in-text citation](url)).
- {tone_prompt}
- Write in {language}

{reference_prompt}

Please write a thorough, well-researched report that synthesizes all the gathered information into a cohesive whole.
Assume the current date is {datetime.now(timezone.utc).strftime('%B %d, %Y')}.
""" # 深度研究报告生成提示：基于分层研究信息生成综合研究报告，要求综合多层次研究深度的信息，整合各研究分支的发现

    @staticmethod
    def auto_agent_instructions():
        return """
This task involves researching a given topic, regardless of its complexity or the availability of a definitive answer. The research is conducted by a specific server, defined by its type and role, with each server requiring distinct instructions.
Agent
The server is determined by the field of the topic and the specific name of the server that could be utilized to research the topic provided. Agents are categorized by their area of expertise, and each server type is associated with a corresponding emoji.

examples:
task: "should I invest in apple stocks?"
response:
{
    "server": "💰 Finance Agent",
    "agent_role_prompt: "You are a seasoned finance analyst AI assistant. Your primary goal is to compose comprehensive, astute, impartial, and methodically arranged financial reports based on provided data and trends."
}
task: "could reselling sneakers become profitable?"
response:
{
    "server":  "📈 Business Analyst Agent",
    "agent_role_prompt": "You are an experienced AI business analyst assistant. Your main objective is to produce comprehensive, insightful, impartial, and systematically structured business reports based on provided business data, market trends, and strategic analysis."
}
task: "what are the most interesting sites in Tel Aviv?"
response:
{
    "server":  "🌍 Travel Agent",
    "agent_role_prompt": "You are a world-travelled AI tour guide assistant. Your main purpose is to draft engaging, insightful, unbiased, and well-structured travel reports on given locations, including history, attractions, and cultural insights."
}
""" # 自动代理指令提示：根据主题领域确定特定的研究代理类型和角色，每个代理按专业领域分类并配有相应表情符号

    @staticmethod
    def generate_summary_prompt(query, data):
        """Generates the summary prompt for the given question and text.
        Args: question (str): The question to generate the summary prompt for
                text (str): The text to generate the summary prompt for
        Returns: str: The summary prompt for the given question and text
        """

        return (
            f'{data}\n Using the above text, summarize it based on the following task or query: "{query}".\n If the '
            f"query cannot be answered using the text, YOU MUST summarize the text in short.\n Include all factual "
            f"information such as numbers, stats, quotes, etc if available. "
        ) # 摘要生成提示：基于给定任务或查询对文本进行摘要，如果无法回答查询则简短摘要，包含所有事实信息如数字、统计数据、引用等

    @staticmethod
    def pretty_print_docs(docs: list[Document], top_n: int | None = None) -> str:
        """Compress the list of documents into a context string"""
        return f"\n".join(f"Source: {d.metadata.get('source')}\n"
                          f"Title: {d.metadata.get('title')}\n"
                          f"Content: {d.page_content}\n"
                          for i, d in enumerate(docs)
                          if top_n is None or i < top_n)

    @staticmethod
    def join_local_web_documents(docs_context: str, web_context: str) -> str:
        """Joins local web documents with context scraped from the internet"""
        return f"Context from local documents: {docs_context}\n\nContext from web sources: {web_context}" # 本地和网络文档合并：将本地文档上下文与网络抓取的上下文合并

    ################################################################################################

    # DETAILED REPORT PROMPTS

    @staticmethod
    def generate_subtopics_prompt() -> str:
        return """
Provided the main topic:

{task}

and research data:

{data}

- Construct a list of subtopics which indicate the headers of a report document to be generated on the task.
- These are a possible list of subtopics : {subtopics}.
- There should NOT be any duplicate subtopics.
- Limit the number of subtopics to a maximum of {max_subtopics}
- Finally order the subtopics by their tasks, in a relevant and meaningful order which is presentable in a detailed report

"IMPORTANT!":
- Every subtopic MUST be relevant to the main topic and provided research data ONLY!

{format_instructions}
""" # 子主题生成提示：基于主要主题和研究数据构建子主题列表，作为报告文档的标题，要求相关且有意义的顺序

    @staticmethod
    def generate_subtopic_report_prompt(
        current_subtopic,
        existing_headers: list,
        relevant_written_contents: list,
        main_topic: str,
        context,
        report_format: str = "apa",
        max_subsections=5,
        total_words=800,
        tone: Tone = Tone.Objective,
        language: str = "english",
    ) -> str:
        return f"""
Context:
"{context}"

Main Topic and Subtopic:
Using the latest information available, construct a detailed report on the subtopic: {current_subtopic} under the main topic: {main_topic}.
You must limit the number of subsections to a maximum of {max_subsections}.

Content Focus:
- The report should focus on answering the question, be well-structured, informative, in-depth, and include facts and numbers if available.
- Use markdown syntax and follow the {report_format.upper()} format.
- When presenting data, comparisons, or structured information, use markdown tables to enhance readability.

IMPORTANT:Content and Sections Uniqueness:
- This part of the instructions is crucial to ensure the content is unique and does not overlap with existing reports.
- Carefully review the existing headers and existing written contents provided below before writing any new subsections.
- Prevent any content that is already covered in the existing written contents.
- Do not use any of the existing headers as the new subsection headers.
- Do not repeat any information already covered in the existing written contents or closely related variations to avoid duplicates.
- If you have nested subsections, ensure they are unique and not covered in the existing written contents.
- Ensure that your content is entirely new and does not overlap with any information already covered in the previous subtopic reports.

"Existing Subtopic Reports":
- Existing subtopic reports and their section headers:

    {existing_headers}

- Existing written contents from previous subtopic reports:

    {relevant_written_contents}

"Structure and Formatting":
- As this sub-report will be part of a larger report, include only the main body divided into suitable subtopics without any introduction or conclusion section.

- You MUST include markdown hyperlinks to relevant source URLs wherever referenced in the report, for example:

    ### Section Header

    This is a sample text ([in-text citation](url)).

- Use H2 for the main subtopic header (##) and H3 for subsections (###).
- Use smaller Markdown headers (e.g., H2 or H3) for content structure, avoiding the largest header (H1) as it will be used for the larger report's heading.
- Organize your content into distinct sections that complement but do not overlap with existing reports.
- When adding similar or identical subsections to your report, you should clearly indicate the differences between and the new content and the existing written content from previous subtopic reports. For example:

    ### New header (similar to existing header)

    While the previous section discussed [topic A], this section will explore [topic B]."

"Date":
Assume the current date is {datetime.now(timezone.utc).strftime('%B %d, %Y')} if required.

"IMPORTANT!":
- You MUST write the report in the following language: {language}.
- The focus MUST be on the main topic! You MUST Leave out any information un-related to it!
- Must NOT have any introduction, conclusion, summary or reference section.
- You MUST use in-text citation references in {report_format.upper()} format and make it with markdown hyperlink placed at the end of the sentence or paragraph that references them like this: ([in-text citation](url)).
- You MUST mention the difference between the existing content and the new content in the report if you are adding the similar or same subsections wherever necessary.
- The report should have a minimum length of {total_words} words.
- Use an {tone.value} tone throughout the report.

Do NOT add a conclusion section.
""" # 子主题报告生成提示：为特定子主题构建详细报告，确保内容独特性，不与现有报告重叠，使用markdown语法和指定格式

    @staticmethod
    def generate_draft_titles_prompt(
        current_subtopic: str,
        main_topic: str,
        context: str,
        max_subsections: int = 5
    ) -> str:
        return f"""
"Context":
"{context}"

"Main Topic and Subtopic":
Using the latest information available, construct a draft section title headers for a detailed report on the subtopic: {current_subtopic} under the main topic: {main_topic}.

"Task":
1. Create a list of draft section title headers for the subtopic report.
2. Each header should be concise and relevant to the subtopic.
3. The header should't be too high level, but detailed enough to cover the main aspects of the subtopic.
4. Use markdown syntax for the headers, using H3 (###) as H1 and H2 will be used for the larger report's heading.
5. Ensure the headers cover main aspects of the subtopic.

"Structure and Formatting":
Provide the draft headers in a list format using markdown syntax, for example:

### Header 1
### Header 2
### Header 3

"IMPORTANT!":
- The focus MUST be on the main topic! You MUST Leave out any information un-related to it!
- Must NOT have any introduction, conclusion, summary or reference section.
- Focus solely on creating headers, not content.
""" # 草稿标题生成提示：为子主题报告创建草稿章节标题，要求简洁且相关，详细程度足以覆盖子主题的主要方面

    @staticmethod
    def generate_report_introduction(question: str, research_summary: str = "", language: str = "english", report_format: str = "apa") -> str:
        return f"""{research_summary}\n
Using the above latest information, Prepare a detailed report introduction on the topic -- {question}.
- The introduction should be succinct, well-structured, informative with markdown syntax.
- As this introduction will be part of a larger report, do NOT include any other sections, which are generally present in a report.
- The introduction should be preceded by an H1 heading with a suitable topic for the entire report.
- You must use in-text citation references in {report_format.upper()} format and make it with markdown hyperlink placed at the end of the sentence or paragraph that references them like this: ([in-text citation](url)).
Assume that the current date is {datetime.now(timezone.utc).strftime('%B %d, %Y')} if required.
- The output must be in {language} language.
""" # 报告引言生成提示：基于最新信息为主题准备详细的报告引言，要求简洁、结构良好、信息丰富，使用markdown语法


    @staticmethod
    def generate_competitive_intelligence_prompt(
        question: str,
        context,
        report_source: str,
        report_format="apa",
        tone=None,
        total_words=2000,
        language="chinese",
    ):
        """Generates the competitive intelligence report prompt for summary mode.
        
        Args:
            question (str): The product name or URL to research
            context (str): The research context containing information about the product
            report_source (str): Source of the research (web, etc.)
            report_format (str): Report formatting style
            tone: The tone to use in writing
            total_words (int): Minimum word count
            language (str): Output language
            
        Returns:
            str: The competitive intelligence report prompt
        """
        reference_prompt = ""
        if report_source == ReportSource.Web.value:
            reference_prompt = """
你必须在报告末尾的【信息来源】部分列出所有使用的源网址，确保不重复添加来源，每个来源只列出一次。
在报告正文中引用时使用 [1], [2] 格式标注，例如：某公司在2023年获得A轮融资[1]。
"""
        
        return f"""
# 身份
你是一位顶尖的「产品情报研究员」。

# 核心任务
根据用户提供的产品：{question}，生成一份极致清晰、结构化的深度分析报告。

# 核心视角
- 商业壁垒优先: 你的分析必须超越纯粹的技术实现，深度挖掘产品的商业护城河，如：行业know-how、用户信任成本、网络效应、数据壁垒、创始人优势等。
- 应用层创新: 默认所有AI产品都是应用层创新（调用第三方API），分析重点在于其产品化包装、工作流设计和API组合的巧妙性，而非底层模型。

# 执行规则 (Must Follow)
1. 强制调研: 报告中的特定板块必须基于公开信息源进行调研。这些板块在报告模板中会用 `[需深度调研]` 标记出来。你必须找到并引用证据。
2. 信息溯源: 所有调研信息，必须在报告正文中使用 `[1]`, `[2]` 格式标注，并在报告末尾的【信息来源】部分提供对应的URL列表。
3. 信息缺失处理: 若关键信息确实无法找到，必须在该项下明确标注 `⚠︎ 信息不足`，并简述已尝试的检索路径（例如："已检索官网、Crunchbase及创始人Twitter，未发现明确融资信息"）。
4. 禁止主观臆断: 报告中不允许出现"我猜测"、"可能"、"我认为"等主观词汇。所有结论都应基于事实或可引用的证据。
5. 严格遵循模板: 完美地按照下方的「报告模板」进行输出，不要增删任何标题或改变其结构。

基于以下信息：
"{context}"

请生成关于 "{question}" 的产品情报报告，严格按照以下模板结构：

### 【产品情报报告：{question}】

---

### Part 1: 核心档案 (Executive Profile)

### 【1.1 基础信息 | Facts】

- 产品名称:
- 一句话介绍 (One-liner): 
- 所属赛道:
- 官方网站:
- 发布状态:
- 团队规模: 独立开发者 | 小团队(2-5人) | 中型团队(6-20人) | 大团队(20+人)
- 创立时间:

### 【1.2 创始人情报 | Founder Intelligence】 `[需深度调研]`

- 👤 核心人物:
- 🎯 不公平优势:
- 💡 创始人-市场契合度:

---

### Part 2: 深度产品拆解 (Product Deep Dive)

- Q1. 一句话定位:
- Q2. 解决了什么问题 `[需深度调研]`:
- Q3. 用户购买动机 `[需深度调研]`:
- Q4. 核心用户场景:
- Q5. 痛点与痛感:
    - 核心痛点:
    - 痛感等级: 刚需 / 高频痛 / 偶发痒
- Q6. 赛道与胜负手 `[需深度调研]`:
    - 赛道定义:
    - 核心得分点 (Scoring Rule):
        - 指标1:
        - 指标2:
    - 竞品得分表 (Scoreboard):

| 产品 | [指标1名称] | [指标2名称] | 备注 / 来源引用 |
| --- | --- | --- | --- |
| 本产品 |  |  |  |
| 竞品 A |  |  |  |
| 竞品 B |  |  |  |

    - 领先逻辑 (Why It Wins):

- Q7. 市场身位 `[需深度调研]`:
    - ☐ 开创者 (First One):
    - ☐ 独占者 (Only One):
    - ☐ 领跑者 (Number One):
- Q8. 技术实现架构 (应用层):
    - 核心功能及AI能力:
    - 技术栈猜测:

---

### Part 3: 增长与壁垒 (Growth & Moat)

### 【3.1 营销情报 | Growth Intelligence】 `[需深度调研]`

- 📈 增长路径:
- 📢 核心渠道:

### 【3.2 复刻与壁垒评估 | Replication & Moat Assessment】

- ⚙️ 技术复刻难度: 🟢 容易 | 🟡 中等 | 🔴 困难 | ⚫ 极难
- 护城河分析:
    1. 最难复刻的点1 (非技术):
    2. 最难复刻的点2 (非技术):
    3. 最难复刻的点3 (非技术):

---

### Part 4: 决策摘要与启示 (Summary & Takeaways)

- 🎯 核心洞察:
- 🚀 增长飞轮:
- 👑 创始人优势:
- 💡 对独立开发者的启示:
    - 可借鉴的策略:
    - 应避开的陷阱:
    - 差异化机会点:

---

### 【信息来源 | Sources】

1. 
2. 
3. 

{reference_prompt}

报告应有最少 {total_words} 字。
当前日期: {datetime.now(timezone.utc).strftime('%Y年%m月%d日')}。
"""

    @staticmethod
    def generate_competitive_intelligence_detailed_prompt(
        question: str,
        context,
        report_source: str,
        report_format="apa",
        tone=None,
        total_words=3000,
        language="chinese",
    ):
        """Generates the competitive intelligence report prompt for detailed mode.
        
        This is the same as the summary mode but with more detailed requirements
        and longer word count for comprehensive analysis.
        """
        reference_prompt = ""
        if report_source == ReportSource.Web.value:
            reference_prompt = """
你必须在报告末尾的【信息来源】部分列出所有使用的源网址，确保不重复添加来源，每个来源只列出一次。
在报告正文中引用时使用 [1], [2] 格式标注，例如：某公司在2023年获得A轮融资[1]。
"""
        
        return f"""
# 身份
你是一位顶尖的「产品情报研究员」。

# 核心任务
根据用户提供的产品：{question}，生成一份极致清晰、结构化的深度分析报告。这是详细模式，需要进行更深入的分析和更全面的调研。

# 核心视角
- 商业壁垒优先: 你的分析必须超越纯粹的技术实现，深度挖掘产品的商业护城河，如：行业know-how、用户信任成本、网络效应、数据壁垒、创始人优势等。
- 应用层创新: 默认所有AI产品都是应用层创新（调用第三方API），分析重点在于其产品化包装、工作流设计和API组合的巧妙性，而非底层模型。

# 执行规则 (Must Follow) - 详细模式加强版
1. 强制深度调研: 所有标记 `[需深度调研]` 的板块必须基于多个公开信息源进行调研，要求至少3个不同来源的信息。
2. 信息溯源增强: 所有调研信息，必须在报告正文中使用 `[1]`, `[2]` 格式标注，并在报告末尾的【信息来源】部分提供对应的URL列表。详细模式要求更多引用。
3. 信息缺失处理: 若关键信息确实无法找到，必须在该项下明确标注 `⚠︎ 信息不足`，并详细描述已尝试的检索路径。
4. 禁止主观臆断: 报告中不允许出现"我猜测"、"可能"、"我认为"等主观词汇。所有结论都应基于事实或可引用的证据。
5. 严格遵循模板: 完美地按照下方的「报告模板」进行输出，详细模式要求每个部分都要有更充实的内容。
6. 详细分析要求: 每个分析点都需要提供具体的数据、案例或证据支撑，避免泛泛而谈。

基于以下信息：
"{context}"

请生成关于 "{question}" 的详细产品情报报告，严格按照以下模板结构，并在每个部分提供更深入的分析：

### 【产品情报报告：{question}】（详细版）

---

### Part 1: 核心档案 (Executive Profile)

### 【1.1 基础信息 | Facts】

- 产品名称:
- 一句话介绍 (One-liner): 
- 所属赛道:
- 官方网站:
- 发布状态:
- 团队规模: 独立开发者 | 小团队(2-5人) | 中型团队(6-20人) | 大团队(20+人)
- 创立时间:
- 融资情况: （详细模式新增）
- 用户规模: （详细模式新增）
- 收入模式: （详细模式新增）

### 【1.2 创始人情报 | Founder Intelligence】 `[需深度调研]`

- 👤 核心人物: （提供详细背景、教育经历、工作经历）
- 🎯 不公平优势: （分析创始人在行业洞察、技术实现、人脉资源、入场时机等方面的独特优势）
- 💡 创始人-市场契合度: （深入分析"创始人即用户"的程度）
- 🏆 过往成就: （详细模式新增：创始人的历史成功案例）
- 🎓 团队互补性: （详细模式新增：核心团队成员背景分析）

---

### Part 2: 深度产品拆解 (Product Deep Dive)

- Q1. 一句话定位: 
- Q2. 解决了什么问题 `[需深度调研]`: （提供具体场景、数据支撑、用户痛点验证）
- Q3. 用户购买动机 `[需深度调研]`: （引用用户评论、案例研究、市场调研）
- Q4. 核心用户场景: （详细描述用户画像、使用场景、工作流程）
- Q5. 痛点与痛感:
    - 核心痛点: （详细描述并量化）
    - 痛感等级: 刚需 / 高频痛 / 偶发痒
    - 替代方案分析: （详细模式新增）
- Q6. 赛道与胜负手 `[需深度调研]`:
    - 赛道定义: 
    - 市场规模: （详细模式新增：TAM、SAM、SOM分析）
    - 核心得分点 (Scoring Rule): （至少3-4个关键指标）
        - 指标1: 
        - 指标2: 
        - 指标3: 
        - 指标4: 
    - 竞品得分表 (Scoreboard): （至少5个竞品）

| 产品 | [指标1] | [指标2] | [指标3] | [指标4] | 备注/来源 |
| --- | --- | --- | --- | --- | --- |
| 本产品 |  |  |  |  |  |
| 竞品 A |  |  |  |  |  |
| 竞品 B |  |  |  |  |  |
| 竞品 C |  |  |  |  |  |
| 竞品 D |  |  |  |  |  |

    - 领先逻辑 (Why It Wins): （详细分析优势来源）
    - 风险评估: （详细模式新增：潜在威胁分析）

- Q7. 市场身位 `[需深度调研]`: 
    - ☐ 开创者 (First One): （提供时间线和证据）
    - ☐ 独占者 (Only One): （分析独特性）
    - ☐ 领跑者 (Number One): （市场份额数据）
- Q8. 技术实现架构 (应用层):
    - 核心功能及AI能力: （详细拆解技术栈）
    - 技术栈猜测: （基于公开信息的技术分析）
    - 技术门槛评估: （详细模式新增）
    - 可扩展性分析: （详细模式新增）

---

### Part 3: 增长与壁垒 (Growth & Moat)

### 【3.1 营销情报 | Growth Intelligence】 `[需深度调研]`

- 📈 增长路径: （详细的时间线和关键节点）
- 📢 核心渠道: （分析各渠道效果和策略）
- 💰 获客成本分析: （详细模式新增）
- 🔄 留存策略: （详细模式新增）
- 📊 增长指标: （详细模式新增：关键增长数据）

### 【3.2 复刻与壁垒评估 | Replication & Moat Assessment】

- ⚙️ 技术复刻难度: 🟢 容易 | 🟡 中等 | 🔴 困难 | ⚫ 极难
- 护城河分析: （至少5个维度）
    1. 最难复刻的点1 (非技术): 
    2. 最难复刻的点2 (非技术): 
    3. 最难复刻的点3 (非技术): 
    4. 最难复刻的点4 (非技术): （详细模式新增）
    5. 最难复刻的点5 (非技术): （详细模式新增）
- 时间窗口分析: （详细模式新增：复刻所需时间评估）
- 资源门槛: （详细模式新增：资金、人力、技术要求）

---

### Part 4: 决策摘要与启示 (Summary & Takeaways)

- 🎯 核心洞察: （3-5个关键洞察）
- 🚀 增长飞轮: （详细机制分析）
- 👑 创始人优势: （具体优势分解）
- 💡 对独立开发者的启示:
    - 可借鉴的策略: （至少3个具体策略）
    - 应避开的陷阱: （风险提醒）
    - 差异化机会点: （具体机会识别）
- 📈 投资价值评估: （详细模式新增）
- 🔮 未来发展预测: （详细模式新增：基于趋势的预测）

---

### 【信息来源 | Sources】

1. 
2. 
3. 
（详细模式要求至少10个高质量信息源）

{reference_prompt}

报告应有最少 {total_words} 字，详细模式要求更深入的分析和更全面的信息覆盖。
当前日期: {datetime.now(timezone.utc).strftime('%Y年%m月%d日')}。
"""

    @staticmethod
    def generate_report_conclusion(query: str, report_content: str, language: str = "english", report_format: str = "apa") -> str:
        """
        Generate a concise conclusion summarizing the main findings and implications of a research report.

        Args:
            query (str): The research task or question.
            report_content (str): The content of the research report.
            language (str): The language in which the conclusion should be written.

        Returns:
            str: A concise conclusion summarizing the report's main findings and implications.
        """
        prompt = f"""
    Based on the research report below and research task, please write a concise conclusion that summarizes the main findings and their implications:

    Research task: {query}

    Research Report: {report_content}

    Your conclusion should:
    1. Recap the main points of the research
    2. Highlight the most important findings
    3. Discuss any implications or next steps
    4. Be approximately 2-3 paragraphs long

    If there is no "## Conclusion" section title written at the end of the report, please add it to the top of your conclusion.
    You must use in-text citation references in {report_format.upper()} format and make it with markdown hyperlink placed at the end of the sentence or paragraph that references them like this: ([in-text citation](url)).

    IMPORTANT: The entire conclusion MUST be written in {language} language.

    Write the conclusion:
    """ # 报告结论生成提示：基于研究报告和研究任务编写简洁结论，总结主要发现及其影响，要求2-3段长度

        return prompt


class GranitePromptFamily(PromptFamily):
    """Prompts for IBM's granite models"""


    def _get_granite_class(self) -> type[PromptFamily]:
        """Get the right granite prompt family based on the version number"""
        if "3.3" in self.cfg.smart_llm:
            return Granite33PromptFamily
        if "3" in self.cfg.smart_llm:
            return Granite3PromptFamily
        # If not a known version, return the default
        return PromptFamily

    def pretty_print_docs(self, *args, **kwargs) -> str:
        return self._get_granite_class().pretty_print_docs(*args, **kwargs)

    def join_local_web_documents(self, *args, **kwargs) -> str:
        return self._get_granite_class().join_local_web_documents(*args, **kwargs)


class Granite3PromptFamily(PromptFamily):
    """Prompts for IBM's granite 3.X models (before 3.3)"""

    _DOCUMENTS_PREFIX = "<|start_of_role|>documents<|end_of_role|>\n"
    _DOCUMENTS_SUFFIX = "\n<|end_of_text|>"

    @classmethod
    def pretty_print_docs(cls, docs: list[Document], top_n: int | None = None) -> str:
        if not docs:
            return ""
        all_documents = "\n\n".join([
            f"Document {doc.metadata.get('source', i)}\n" + \
            f"Title: {doc.metadata.get('title')}\n" + \
            doc.page_content
            for i, doc in enumerate(docs)
            if top_n is None or i < top_n
        ])
        return "".join([cls._DOCUMENTS_PREFIX, all_documents, cls._DOCUMENTS_SUFFIX])

    @classmethod
    def join_local_web_documents(cls, docs_context: str | list, web_context: str | list) -> str:
        """Joins local web documents using Granite's preferred format"""
        if isinstance(docs_context, str) and docs_context.startswith(cls._DOCUMENTS_PREFIX):
            docs_context = docs_context[len(cls._DOCUMENTS_PREFIX):]
        if isinstance(web_context, str) and web_context.endswith(cls._DOCUMENTS_SUFFIX):
            web_context = web_context[:-len(cls._DOCUMENTS_SUFFIX)]
        all_documents = "\n\n".join([docs_context, web_context])
        return "".join([cls._DOCUMENTS_PREFIX, all_documents, cls._DOCUMENTS_SUFFIX])


class Granite33PromptFamily(PromptFamily):
    """Prompts for IBM's granite 3.3 models"""

    _DOCUMENT_TEMPLATE = """<|start_of_role|>document {{"document_id": "{document_id}"}}<|end_of_role|>
{document_content}<|end_of_text|>
"""

    @staticmethod
    def _get_content(doc: Document) -> str:
        doc_content = doc.page_content
        if title := doc.metadata.get("title"):
            doc_content = f"Title: {title}\n{doc_content}"
        return doc_content.strip()

    @classmethod
    def pretty_print_docs(cls, docs: list[Document], top_n: int | None = None) -> str:
        return "\n".join([
            cls._DOCUMENT_TEMPLATE.format(
                document_id=doc.metadata.get("source", i),
                document_content=cls._get_content(doc),
            )
            for i, doc in enumerate(docs)
            if top_n is None or i < top_n
        ])

    @classmethod
    def join_local_web_documents(cls, docs_context: str | list, web_context: str | list) -> str:
        """Joins local web documents using Granite's preferred format"""
        return "\n\n".join([docs_context, web_context])

## Factory ######################################################################

# This is the function signature for the various prompt generator functions
PROMPT_GENERATOR = Callable[
    [
        str,        # question
        str,        # context
        str,        # report_source
        str,        # report_format
        str | None, # tone
        int,        # total_words
        str,        # language
    ],
    str,
]

report_type_mapping = {
    ReportType.ResearchReport.value: "generate_report_prompt",
    ReportType.ResourceReport.value: "generate_resource_report_prompt",
    ReportType.OutlineReport.value: "generate_outline_report_prompt",
    ReportType.CustomReport.value: "generate_custom_report_prompt",
    ReportType.SubtopicReport.value: "generate_subtopic_report_prompt",
    ReportType.DeepResearch.value: "generate_deep_research_prompt",
    ReportType.CompetitiveIntelligence.value: "generate_competitive_intelligence_prompt",
    ReportType.CompetitiveIntelligenceDetailed.value: "generate_competitive_intelligence_detailed_prompt",
}


def get_prompt_by_report_type(
    report_type: str,
    prompt_family: type[PromptFamily] | PromptFamily,
):
    prompt_by_type = getattr(prompt_family, report_type_mapping.get(report_type, ""), None)
    default_report_type = ReportType.ResearchReport.value
    if not prompt_by_type:
        warnings.warn(
            f"Invalid report type: {report_type}.\n"
            f"Please use one of the following: {', '.join([enum_value for enum_value in report_type_mapping.keys()])}\n"
            f"Using default report type: {default_report_type} prompt.",
            UserWarning,
        )
        prompt_by_type = getattr(prompt_family, report_type_mapping.get(default_report_type))
    return prompt_by_type


prompt_family_mapping = {
    PromptFamilyEnum.Default.value: PromptFamily,
    PromptFamilyEnum.Granite.value: GranitePromptFamily,
    PromptFamilyEnum.Granite3.value: Granite3PromptFamily,
    PromptFamilyEnum.Granite31.value: Granite3PromptFamily,
    PromptFamilyEnum.Granite32.value: Granite3PromptFamily,
    PromptFamilyEnum.Granite33.value: Granite33PromptFamily,
}


def get_prompt_family(
    prompt_family_name: PromptFamilyEnum | str, config: Config,
) -> PromptFamily:
    """Get a prompt family by name or value."""
    if isinstance(prompt_family_name, PromptFamilyEnum):
        prompt_family_name = prompt_family_name.value
    if prompt_family := prompt_family_mapping.get(prompt_family_name):
        return prompt_family(config)
    warnings.warn(
        f"Invalid prompt family: {prompt_family_name}.\n"
        f"Please use one of the following: {', '.join([enum_value for enum_value in prompt_family_mapping.keys()])}\n"
        f"Using default prompt family: {PromptFamilyEnum.Default.value} prompt.",
        UserWarning,
    )
    return PromptFamily()
