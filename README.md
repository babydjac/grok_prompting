# grok_prompting

This package provides ComfyUI nodes that use X.AI's Grok models to
generate detailed prompts for NSFW content.

## NSFWGrokToPonyXL
The `generate_prompts` method returns four strings:
1. `ponyxl_prompt` - tag-based prompt for PonyXL.
2. `wan_prompt` - short Wan video description.
3. `negative_prompt` - tags to avoid.
4. `explanation` - summary of how the prompt was optimized.
