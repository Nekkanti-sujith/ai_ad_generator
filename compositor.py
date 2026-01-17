"""
compositor.py

Responsibilities:
- Insert real product image into the person's hand
- Add realistic shadow for blending
- Place brand logo cleanly
- Fully deterministic (NO AI logic)
"""

from PIL import Image, ImageEnhance, ImageFilter


# -------------------------------------------------
# HAND POSITION LOGIC (RIGHT HAND ONLY)
# -------------------------------------------------
def get_hand_position(
    image_width: int,
    image_height: int,
    interaction: str
):
    """
    Returns (x, y) coordinates for right-hand placement.

    Drinking  -> near mouth (upper-right)
    Holding   -> near waist (lower-right)
    """

    if interaction == "drinking":
        # Right hand near mouth
        return int(image_width * 0.58), int(image_height * 0.42)

    # Default: holding
    return int(image_width * 0.62), int(image_height * 0.58)


# -------------------------------------------------
# PLACE PRODUCT INTO HAND (ILLUSION-BASED)
# -------------------------------------------------
def place_product_in_hand(
    background: Image.Image,
    product_path: str,
    interaction: str,
    scale: float = 0.20,
    offset=(0, 0)
) -> Image.Image:
    """
    Places the product image at the correct hand location
    based on interaction type.

    Args:
        background: Generated scene image
        product_path: Transparent PNG of product
        interaction: "drinking" | "holding"
        scale: Relative size of product
        offset: Manual fine-tuning (x, y)

    Returns:
        PIL.Image
    """

    bg = background.convert("RGBA")
    product = Image.open(product_path).convert("RGBA")

    bw, bh = bg.size

    # Resize product (keep aspect ratio)
    new_width = int(bw * scale)
    aspect_ratio = product.height / product.width
    product = product.resize(
        (new_width, int(new_width * aspect_ratio)),
        Image.LANCZOS
    )

    # Get correct hand position
    x, y = get_hand_position(bw, bh, interaction)
    x += offset[0]
    y += offset[1]

    # Create soft shadow for realism
    shadow = product.copy()
    shadow = ImageEnhance.Brightness(shadow).enhance(0)
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))

    # Paste shadow then product
    bg.paste(shadow, (x + 6, y + 6), shadow)
    bg.paste(product, (x, y), product)

    return bg.convert("RGB")


# -------------------------------------------------
# PLACE LOGO (CLEAN, SAFE)
# -------------------------------------------------
def place_logo(
    image: Image.Image,
    logo_path: str,
    scale: float = 0.15,
    position: str = "top_left"
) -> Image.Image:
    """
    Places brand logo in a clean corner.
    """

    img = image.convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    bw, bh = img.size

    # Resize logo
    new_width = int(bw * scale)
    aspect_ratio = logo.height / logo.width
    logo = logo.resize(
        (new_width, int(new_width * aspect_ratio)),
        Image.LANCZOS
    )

    padding = 40

    positions = {
        "top_left": (padding, padding),
        "top_right": (bw - logo.width - padding, padding),
        "bottom_left": (padding, bh - logo.height - padding),
        "bottom_right": (bw - logo.width - padding, bh - logo.height - padding),
    }

    img.paste(logo, positions.get(position, positions["top_left"]), logo)
    return img.convert("RGB")
