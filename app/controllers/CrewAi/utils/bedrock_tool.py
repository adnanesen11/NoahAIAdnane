from langchain_aws.chat_models import ChatBedrock

# Instantiate ChatBedrock
bedrock_llm = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",  # Your model ID
    region_name="us-east-1",  # Region for Bedrock
)
