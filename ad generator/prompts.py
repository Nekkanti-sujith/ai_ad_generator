def build_image_prompt(
    product: str,
    persona: str,
    scene: str,
    interaction: str,
    emotion: str,
    visual_style: str,
    tagline: str
) -> str:
    return f"""
High-quality lifestyle advertising photograph.

Product:
{product}

Person:
{persona}

Scene:
{scene}

Interaction:
Person is {interaction} the product using their right hand.

Emotion:
{emotion}

Visual style:
{visual_style}

Text on image:
A short, catchy tagline reading: "{tagline}"

The text is placed slightly below the top edge,
centered horizontally, with generous padding.

The text uses elegant, flowing, cursive or italic typography,
with smooth curves and a premium, stylish feel.
The lettering looks modern, clean, and visually pleasing.

High contrast so the text is clearly readable.
The text is fully visible and not touching the edges of the image.

Rules:
- Photorealistic
- Professional advertising photography
- Natural human posture
- No distorted hands
- No extra fingers
- No excessive text (only the tagline)
"""
