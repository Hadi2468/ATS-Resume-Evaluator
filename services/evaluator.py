from services.openai_service import ask_llm

def evaluate_resume(
        prompt_template,
        resume_text,
        jd_text,
        system_prompt
):

    user_prompt = f"""
    Job Description:

    {jd_text}

    Resume:

    {resume_text}

    {prompt_template}
    """

    return ask_llm(
        system_prompt,
        user_prompt
    )