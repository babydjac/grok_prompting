from .nsfw_grok_describer import NSFWGrokDescriber
from .nsfw_grok_to_ponyxl import NSFWGrokToPonyXL
NODE_CLASS_MAPPINGS = {
    "NSFWGrokDescriber": NSFWGrokDescriber,
    "NSFWGrokToPonyXL": NSFWGrokToPonyXL,
}
print("[34mGrok Prompting Pack: [92mLoaded[0m")
