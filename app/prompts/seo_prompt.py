from typing import List, Optional


def build_seo_prompt(
    template: str,
    primary_input: str,
    secondary_input: str,
    optional_input: Optional[str],
    recent_contents: List[str],
) -> str:
    prompt_lines = [template.strip()]
    
    prompt_lines.append(f"\nPrimary keyword: {primary_input}")
    prompt_lines.append(f"Secondary keyword: {secondary_input}")
    
    if optional_input:
        prompt_lines.append(f"Optional keyword: {optional_input}")

    if recent_contents:
        prompt_lines.append(
            "\nDo not generate content similar to any provided content."
            " Use a completely different structure, wording, opening, body flow, and CTA."
        )
        prompt_lines.append("Previous content examples:")
        for idx, content in enumerate(recent_contents, start=1):
            prompt_lines.append(f"{idx}. {content}")

    prompt_lines.append(
        "\nEnsure the output is unique, persuasive, engaging, and optimized for SEO."
    )
    prompt_lines.append("Return only the generated content without metadata.")

    return "\n".join(prompt_lines)
