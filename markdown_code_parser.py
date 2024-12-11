import re
import os
import sys

def parse_markdown_code(input_file, output_dir):
    """
    Parse a markdown file and extract code blocks with their preceding filenames.
    
    Args:
    input_file (str): Path to the input markdown file
    output_dir (str): Directory to save the extracted code files
    
    Returns:
    list: List of generated file paths
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Store generated file paths
    generated_files = []
    
    # Read the entire markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regular expression to match code blocks with optional language specification
    code_block_pattern = r'```(?:\w+)?\n(.*?)```'
    
    # Find all code blocks
    code_blocks = re.findall(code_block_pattern, content, re.DOTALL)
    
    # Remove leading numbers and dots from filenames
    def sanitize_filename(filename):
        # Remove leading numbering like "1. " or "1._"
        filename = re.sub(r'^[\d]+\.\s*_?', '', filename)
        # Sanitize remaining filename
        filename = re.sub(r'[^\w\-\. ]', '', filename)
        filename = filename.strip().replace(' ', '_')
        return filename if filename else 'code'

    # Find preceding lines for potential filenames
    for match in re.finditer(code_block_pattern, content, re.DOTALL):
        # Get the full match and the start position
        full_match = match.group(0)
        start_pos = match.start()
        
        # Extract the code block
        code_block = match.group(1).strip()
        
        # Find the line preceding the code block
        preceding_text = content[:start_pos].split('\n')
        
        # Use the last non-empty line before the code block as the filename
        filename = 'code.txt'
        for line in reversed(preceding_text):
            if line.strip():
                filename = sanitize_filename(line.strip())
                break
        
        # Ensure unique filename
        base, ext = os.path.splitext(filename)
        ext = ext if ext else '.txt'
        counter = 1
        full_filename = os.path.join(output_dir, f"{base}{ext}")
        
        while os.path.exists(full_filename):
            full_filename = os.path.join(output_dir, f"{base}_{counter}{ext}")
            counter += 1
        
        # Write the code block to the file
        with open(full_filename, 'w', encoding='utf-8') as f:
            f.write(code_block)
        
        generated_files.append(full_filename)
    
    return generated_files

def main():
    # Check if input file is provided
    if len(sys.argv) < 2:
        print("Usage: python markdown_code_parser.py <input_markdown_file>")
        sys.exit(1)
    
    input_markdown = sys.argv[1]
    output_directory = 'extracted_code'
    
    try:
        generated_files = parse_markdown_code(input_markdown, output_directory)
        print("Generated files:")
        for file in generated_files:
            print(os.path.relpath(file, output_directory))
    except FileNotFoundError:
        print(f"Error: Input file {input_markdown} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

# ------ run ---------
# python markdown_code_parser.py ~/Desktop/ua_list_vscode.md
# Generated files:
# Ill_help_you_create_a_VSCode_extension_for_an_AI_chat_tool_that_can_maintain_conversation_history._Ill_break_this_down_into_several_files_and_use_TypeScript_with_the_VSCode_extension_API.
# package.json
# constants.ts
# chatProvider.ts
# chatView.ts
# extension.ts
# tsconfig.json
# 
