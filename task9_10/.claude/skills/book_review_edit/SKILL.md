# Book Content Review and Editing Skill

## Purpose
This skill performs comprehensive review and editing of book content for the "AI-Spec Driven Book Creation using Spec-Kit Plus and Claude" book. It checks for quality, consistency, clarity, and adherence to the established style guide.

## Parameters
- `content`: The book content to review (chapter, section, or entire document)
- `review_type`: Type of review (structural, content, style, technical accuracy, comprehensive)
- `checklist`: Specific items to check (clarity, consistency, technical accuracy, readability)
- `style_guide`: Style guide to follow (book's established style, target audience, format requirements)

## Workflow
1. Analyze the content against specified criteria
2. Identify issues with structure, content, or style
3. Provide specific suggestions for improvements
4. Highlight areas that need revision
5. Generate a summary of review findings

## Implementation
When this skill is invoked, it will:

1. Parse the input content and parameters
2. Apply appropriate review criteria based on review type
3. Use Claude's analytical capabilities to identify issues
4. Provide specific, actionable feedback
5. Suggest improvements while maintaining the author's voice

## Examples
```
skill: "book_review_edit" --content="chapter_1_draft.md" --type="comprehensive" --checklist="clarity,consistency,technical-accuracy" --style="book-style-guide"
```

## Output
Returns a comprehensive review with:
- Summary of issues found
- Line-by-line suggestions for improvements
- Structural recommendations
- Style consistency feedback
- Quality metrics and confidence scores