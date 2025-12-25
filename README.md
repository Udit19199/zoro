# Zoro Project

This repository contains a collection of Python tools and a sample application, primarily focused on an AI Code Assistant interface and a Calculator utility.

## Project Overview

The project is divided into two main components:

1.  **AI Code Assistant**: A CLI tool located at the root that interacts with the Google Gemini API to generate content based on user prompts. It includes a set of utility functions for file system operations.
2.  **Calculator**: A standalone command-line calculator application located in the `calculator/` directory.

## Prerequisites

-   Python 3.12 or higher
-   A Google Gemini API Key (stored in `GEMINI_API_KEY` environment variable)

## Installation

This project uses `uv` for dependency management, but can also be installed via standard pip tools.

### Using `uv` (Recommended)

```bash
uv sync
```

### Using `pip`

```bash
pip install .
```

## Configuration

Create a `.env` file in the root directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

### AI Code Assistant

Run the main script to interact with the Gemini model:

```bash
python main.py "Your prompt here"
```

**Options:**
-   `--verbose`: Enable verbose output to see token usage.

### Calculator App

The calculator is located in the `calculator/` directory. You can run it directly:

```bash
python calculator/main.py "3 + 5 * 2"
```

It supports basic arithmetic operations (`+`, `-`, `*`, `/`) and respects operator precedence.

## Project Structure

-   `main.py`: Entry point for the AI Assistant CLI.
-   `functions/`: Utility modules for file operations (`get_file_content`, `write_file`, etc.).
-   `calculator/`: The calculator application source code.
    -   `pkg/`: Core logic for the calculator.
-   `tests/`: Unit tests for the root utility functions.

## Testing

To run the tests for the utility functions:

```bash
python -m unittest discover . -p "test_*.py"
```
