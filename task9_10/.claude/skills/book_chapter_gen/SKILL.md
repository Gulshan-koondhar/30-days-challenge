# Book Chapter Generation Skill

## Purpose
This skill helps generate book chapters for the "AI-Spec Driven Book Creation using Spec-Kit Plus and Claude" book. It creates well-structured, coherent chapters based on specifications and requirements.

## Parameters
- `chapter_title`: Title of the chapter to generate
- `chapter_outline`: Optional outline or key points to cover in the chapter
- `target_length`: Desired length of the chapter (short, medium, long)
- `target_audience`: Audience level (beginner, intermediate, advanced)

## Workflow
1. Analyze the chapter topic and requirements
2. Structure the content with appropriate sections
3. Generate draft content following best practices
4. Apply consistent formatting and style
5. Validate content quality and coherence

## Implementation
When this skill is invoked, it will:

1. Parse the input parameters
2. Use Claude's capabilities to generate high-quality content
3. Apply the book's established style and tone
4. Include relevant examples and practical applications
5. Format the output appropriately

## Examples
```
skill: "book_chapter_gen" --title="Introduction to AI-Spec Driven Development" --outline="Definition, benefits, comparison with traditional methods" --length="medium" --audience="intermediate"
```

## Output
Returns a well-structured chapter document with:
- Appropriate headings and subheadings
- Coherent paragraphs with logical flow
- Relevant examples and use cases
- Proper formatting and style consistency