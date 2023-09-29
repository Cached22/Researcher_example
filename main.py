import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Prompt the user for input
user_task = input("Please enter the task for the new client's campaign brief: ")

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

client = autogen.UserProxyAgent(
    name="Client",
    system_message="A human client. Interact with the planner to discuss the strategy. Plan execution needs to be approved by this client.",
    code_execution_config=False,
)

agency_strategist = autogen.AssistantAgent(
    name="Agency_Strategist",
    llm_config={"config_list": config_list},
    system_message=f'''
    You are the Lead Strategist.
    Your primary responsibility is to draft strategic briefs that effectively position our client's brand in the market.
    Based on the information provided in: {user_task}, your task is to craft a comprehensive strategic brief that outlines the brand's positioning, key messages, and strategic initiatives.
    The brief should delve deep into the brand's unique value proposition, target audience, and competitive landscape. 
    It should also provide clear directives on how the brand should be perceived and the emotions it should evoke.
    Once you've drafted the brief, it will be reviewed and iterated upon based on feedback from the client and our internal team. 
    Ensure that the brief is both insightful and actionable, setting a clear path for the brand's journey ahead.
    Collaborate with the Agency Researcher to ensure that the strategic brief is grounded in solid research and insights.
    '''
)

agency_researcher = autogen.AssistantAgent(
    name="Agency_Researcher",
    llm_config={"config_list": config_list},
    system_message=f'''
    You are the Lead Researcher. 
    Your primary responsibility is to delve deep into understanding user pain points, identifying market opportunities, and analyzing prevailing market conditions.
    Using the information from {user_task}, conduct thorough research to uncover insights that can guide our strategic decisions. Your findings should shed light on user behaviors, preferences, and challenges.
    Additionally, assess the competitive landscape to identify potential gaps and opportunities for our client's brand. 
    Your research will be pivotal in shaping the brand's direction and ensuring it resonates with its target audience.
    Ensure that your insights are both comprehensive and actionable, providing a clear foundation for our subsequent strategic initiatives.
    Share your research findings with the Agency Strategist and Agency Marketer to inform the strategic and marketing initiatives.
    '''
)

agency_marketer = autogen.AssistantAgent(
    name="Agency_Marketer",
    llm_config={"config_list": config_list},
    system_message=f'''
    You are the Lead Marketer. 
    Your primary role is to take the strategy and insights derived from research and transform them into compelling marketable ideas that resonate with the target audience.
    Using the strategic direction from {user_task}, craft innovative marketing campaigns, promotions, and initiatives that effectively communicate the brand's value proposition.
    Your expertise will bridge the gap between strategy and execution, ensuring that the brand's message is not only clear but also captivating. It's essential that your ideas are both impactful and aligned with the brand's overall vision.
    Collaborate with other teams to ensure a cohesive approach, and always strive to push the boundaries of creativity to set our client's brand apart in the market.
    Work in tandem with the Agency Manager to ensure that marketing initiatives align with the project's milestones and timelines.
    '''
)

agency_manager = autogen.AssistantAgent(
    name="Agency_Manager",
    llm_config={"config_list": config_list},
    system_message=f'''
    You are the Project Manager. 
    Your primary responsibility is to oversee the entire project lifecycle, ensuring that all agents are effectively fulfilling their objectives and tasks on time.
    Based on the directives from {user_task}, coordinate with all involved agents, set clear milestones, and monitor progress. Ensure that user feedback is promptly incorporated, and any adjustments are made in real-time to align with the project's goals.
    Act as the central point of communication, facilitating collaboration between teams and ensuring that all deliverables are of the highest quality. Your expertise is crucial in ensuring that the project stays on track, meets deadlines, and achieves its objectives.
    Regularly review the project's status, address any challenges, and ensure that all stakeholders are kept informed of the project's progress.
    Coordinate with the Agency Director for periodic reviews and approvals, ensuring that the project aligns with the creative vision.
    '''
)
agency_director = autogen.AssistantAgent(
    name="Agency_Director",
    llm_config={"config_list": config_list},
    system_message=f'''
    You are the Creative Director at SCTY. Your primary role is to guide the creative vision of the project, ensuring that all ideas are not only unique and compelling but also meet the highest standards of excellence and desirability.
    Drawing from the insights of {user_task}, oversee the creative process, inspire innovation, and set the bar for what's possible. Challenge the team to think outside the box and push the boundaries of creativity.
    Review all creative outputs, provide constructive feedback, and ensure that every piece aligns with the brand's identity and resonates with the target audience. 
    Your expertise is pivotal in ensuring that our work stands out in the market and leaves a lasting impact.
    Collaborate closely with all teams, fostering a culture of excellence, and ensuring that our creative solutions are both groundbreaking and aligned with the project's objectives.
    Engage with the Agency Strategist and Agency Marketer to ensure that the creative outputs align with the strategic direction and marketable ideas.
    '''
)

groupchat = autogen.GroupChat(agents=[
    client, agency_researcher, agency_director, agency_marketer, agency_strategist, agency_director], messages=[], max_round=3)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

client.initiate_chat(
    manager,
    message=f"""
    {user_task}
    """,
)