# Data Model: Calculator

## Entities

- **Expression**: Represents the user's input mathematical string.
  - **Attributes**: 
    - `value`: string (e.g., "2+2", "3*5+2")

- **Result**: Represents the numerical outcome of a valid expression.
  - **Attributes**:
    - `value`: number (e.g., 4, 17)

- **ErrorMessage**: Represents an error encountered during processing.
  - **Attributes**:
    - `message`: string (e.g., "Division by Zero", "Invalid Input")
