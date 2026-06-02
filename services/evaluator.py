from services.openai_service import ask_llm

def evaluate_resume(
        prompt_template,
        resume_text,
        jd_text,
        system_prompt,
        model_name,
        temperature
):
    user_prompt = f"""
Job Description:

{jd_text}

Resume:

{resume_text}

{prompt_template}
"""

    return ask_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model_name=model_name,
        temperature=temperature
    )
