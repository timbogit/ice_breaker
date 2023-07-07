from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent


def main(inf):
    print("Hello LangChain!")

    linkedin_profile_url = linkedin_lookup_agent(name=inf)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url, fake=True
    )

    twitter_username = twitter_lookup_agent(name=inf)
    tweets = scrape_user_tweets(username=twitter_username, num_tweets=5)

    summary_template = """
         given the Linkedin information {linkedin_information} and twitter {twitter_information} about a person from I want you to create:
         1. a short summary
         2. two interesting facts about them
         3. A topic that may interest them
         4. 2 creative Ice breakers to open a conversation with them 
     """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    print(chain.run(linkedin_information=linkedin_data, twitter_information=tweets))


if __name__ == "__main__":
    main("Tim Schmelmer Salesforce")
