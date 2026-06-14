from typing import List, Optional


def build_seo_prompt(
    primary_input: str,
    secondary_input: str,
    optional_input: Optional[str],
    recent_contents: List[str],
) -> str:
    prompt_lines = [
        "Write a single SEO-optimized marketing paragraph between 150 and 250 words.",
        "Use persuasive, human-written language with a strong call-to-action.",
        "Place the primary and secondary keywords naturally and avoid robotic phrasing.",
        "Keep readability high, vary sentence structure, and provide a unique introduction and closing.",
    ]

    if optional_input:
        prompt_lines.append(
            f"If appropriate, include the optional keyword phrase '{optional_input}' in a natural way."
        )

    prompt_lines.append(f"Primary keyword: {primary_input}")
    prompt_lines.append(f"Secondary keyword: {secondary_input}")

    if recent_contents:
        prompt_lines.append(
            "Do not generate content similar to any provided content."
            " Use a completely different structure, wording, opening, body flow, and CTA."
        )
        prompt_lines.append("Previous content examples:"
                            )
        for idx, content in enumerate(recent_contents, start=1):
            prompt_lines.append(f"{idx}. {content}")

    prompt_lines.append(
        "Ensure the output is unique, persuasive, engaging, and optimized for SEO."
    )
    prompt_lines.append("Return only the generated content without metadata.")

    return "\n".join(prompt_lines)
