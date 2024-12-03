import google.generativeai as genai

def AIInsightModel(score,score_history):
    genai.configure(api_key="AIzaSyD_2QetHE4eB9v9haIih5kwV4-6jVfkimk")
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    )

    chat_session = model.start_chat(
    history=[
    ]
    )
    if score_history[:-1]:
        response1 = chat_session.send_message(f"The student just scored {score}, and the previous scores achieved by this student are: {score_history[:-1]}. These scores are all from the same subject. BASED SOLELY ON THESE SCORES, please provide feedback on whether the student is performing poorly or well, whether the student is progressing forward or backward, and additional observations if necessary. Based on the scores alone, do you think this student is likely to pass this subject (a score above 5 indicates a likely pass)? Please write a brief paragraph.")

        response2 = chat_session.send_message(f"""Based on the previous feedback, classify the evaluation into one of the following categories: Bad, Try Harder, Improvement, Worsening, or Good.
            - **Bad**: Scores are poor, with little variation between them, usually below average, though exceptions may exist.
            - **Improvement**: Scores were mostly poor but suddenly show a significant positive improvement.
            - **Worsening**: Scores were mostly good but suddenly drop significantly in a negative direction.
            - **Try Harder**: Scores show little variation, neither improving nor worsening, typically ranging from 5 to 8.
            - **Good**: Scores are strong, usually above 8, with little variation between them, though exceptions may exist.
            Note: Only respond with one of the following: Bad, Try Harder, Improvement, Worsening, Good.""")

        return response1.text, response2.text
    else:
        response1 = chat_session.send_message(f"The student just scored {score}. Based solely on this score, please provide feedback on whether the student is performing poorly or well, and any additional observations if necessary. Write a brief paragraph.")

        response2 = chat_session.send_message(f"""Based on the previous feedback, classify the evaluation into one of the following categories: Bad, Try Harder, or Good.
            - **Bad**: Scores are poor, below 5.
            - **Try Harder**: Scores range from 5 to 8.
            - **Good**: Scores are strong, usually above 8.
            Note: Only respond with one of the following: Bad, Try Harder, Good.""")

    return response1.text, response2.text