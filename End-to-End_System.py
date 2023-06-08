import os
import sys
sys.path.append('../..')
import utils
import panel as pn #GUI
pn.extension()
import basic_api_usage as ai


def process_user_message(user_input, all_messages, debug=True):
    delimiter = "```"
    # Step 1: Check input to see if it flags the Moderation API or is a prompt injection
    moderation_output = ai.moderation(user_input)

    if moderation_output["flagged"]:
        print("Step 1: Input flagged by Modertaion API.")
        return "Sorry, we cannot process this request."

    if debug: print("Step 1: Input passed modertaion check")
    
    category_and_product_response = utils.find_category_and_product_only(user_input, utils.get_products_and_category())
    print(category_and_product_response)
    # Step 2: Extract the list of products
    category_and_product_list = utils.read_string_to_list(category_and_product_response)

    if debug: print("Step 2: Extracted list of products.")

    # Step 3: If products are found, look them up
    product_information = utils.generate_output_string(category_and_product_list)
    if debug: print("Step 3: Looked up Product information")

    # Step 4: Answer the user question
    system_messgae = f"""
    You are a customer service assistant for a large electronic store. \
    Respond in a friendly and helpful tone, with concise answer. \
    Make sure to ask the user relevant follow-up questions.
    """
    messages = [
        {'role':'system','content':system_messgae},
        {'role':'user','content':f"{delimiter}{user_input}{delimiter}"},
        {'role':'assistant', 'content':f"Relevant product information:\n{product_information}"}
    ]

    final_response = ai.get_completion_from_messages(all_messages + messages)
    if debug:print("Step 4: Generated response to user question.")

    all_messages = all_messages + messages[1:]
    
    # Step 5: Put the answer through the Moderation API
    modertaion_output = ai.moderation(input=final_response)
    
    if modertaion_output["flagged"]:
        if debug: print("Step 5:  Response flagged by Moderation API.")
        return "Sorry, we cannot provided this information"
    
    if debug: print("Step 5: response passed modertaion check")

    # Step 6: Ask the model if the response answers the inital user query
    user_message = f"""
    Customer messgae:{delimiter}{user_input}{delimiter}
    Agent respons:{delimiter}{final_response}{delimiter}

    Does the response sufficiently answer the question?
    """

    messages = [
        {'role':'system','content': system_messgae},
        {'role':'user','content':user_message}
    ]

    evaluation_response = ai.get_completion_from_message(messages)
    if debug: print("Step 6: Model evaluated the response.")

    # Step 7: If yes, use this ansewr; if not, say that you will connect to a human
    if "Y" in evaluation_response: 
        if debug: print("Step 7: Model approved the response")
        return final_response, all_messages
    else:
        if debug: print("Step 7: Model disapproved the response.")
        neg_str = "I'm unbale to provide the information you're looking for.I'll connect you with a human representative for further assistance."
        return neg_str, all_messages
    
user_input = "tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what tell me about your tvs"
    