from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageChops
import numpy as np
from enum import Enum, auto
from typing import Union, Literal

class FilterType(Enum):
    """Enumeration of available image filters."""
    GRAYSCALE = auto()
    SEPIA = auto()
    BLUR = auto()
    CONTOUR = auto()
    SHARPEN = auto()
    EDGE_ENHANCE = auto()
    EMBOSS = auto()
    FIND_EDGES = auto()
    BRIGHTNESS = auto()
    CONTRAST = auto()
    SATURATION = auto()
    VINTAGE = auto()
    NEGATIVE = auto()
    SOLARIZE = auto()
    POSTERIZE = auto()
    VIGNETTE = auto()
    SKETCH = auto()
    WATERCOLOR = auto()
    OIL_PAINTING = auto()

# For String literal approach (alternative)
FilterTypeLiteral = Literal[
    "grayscale", "sepia", "blur", "contour", "sharpen", 
    "edge_enhance", "emboss", "find_edges", "brightness", 
    "contrast", "saturation", "vintage", "negative", 
    "solarize", "posterize", "vignette", "sketch", 
    "watercolor", "oil_painting"
]

def apply_image_filter(image: Image.Image, filter_name: Union[FilterType, FilterTypeLiteral, str], strength: float = 1.0) -> Image.Image:
    """
    Apply various filters to an image.
    
    Args:
        image: PIL Image object
        filter_name: Name of the filter to apply (can be FilterType enum, string literal, or string)
        strength: Intensity of the filter effect (0.0 to 2.0, default 1.0)
    
    Returns:
        Filtered PIL Image object
    """
    # Ensure we're working with a copy to avoid modifying the original
    img = image.copy()
    
    # Convert enum to string if needed
    if isinstance(filter_name, FilterType):
        filter_name = filter_name.name.lower()
    
    # Basic filters
    if filter_name == "grayscale" or filter_name == FilterType.GRAYSCALE.name.lower():
        return ImageOps.grayscale(img)
    
    elif filter_name == "sepia" or filter_name == FilterType.SEPIA.name.lower():
        gray_img = ImageOps.grayscale(img)
        sepia = ImageOps.colorize(gray_img, "#704214", "#C0A080")
        return Image.blend(img, sepia, strength) if strength < 1.0 else sepia
    
    elif filter_name == "blur" or filter_name == FilterType.BLUR.name.lower():
        return img.filter(ImageFilter.GaussianBlur(radius=strength * 2))
    
    elif filter_name == "contour" or filter_name == FilterType.CONTOUR.name.lower():
        return img.filter(ImageFilter.CONTOUR)
    
    # Enhanced filters
    elif filter_name == "sharpen" or filter_name == FilterType.SHARPEN.name.lower():
        enhancer = ImageEnhance.Sharpness(img)
        return enhancer.enhance(1.0 + strength)
    
    elif filter_name == "edge_enhance" or filter_name == FilterType.EDGE_ENHANCE.name.lower():
        return img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    
    elif filter_name == "emboss" or filter_name == FilterType.EMBOSS.name.lower():
        return img.filter(ImageFilter.EMBOSS)
    
    elif filter_name == "find_edges" or filter_name == FilterType.FIND_EDGES.name.lower():
        return img.filter(ImageFilter.FIND_EDGES)
        
    elif filter_name == "brightness" or filter_name == FilterType.BRIGHTNESS.name.lower():
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(strength)
    
    elif filter_name == "contrast" or filter_name == FilterType.CONTRAST.name.lower():
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(strength)
    
    elif filter_name == "saturation" or filter_name == FilterType.SATURATION.name.lower():
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(strength)
    
    elif filter_name == "vintage" or filter_name == FilterType.VINTAGE.name.lower():
        # Combination of sepia and lowered contrast
        gray_img = ImageOps.grayscale(img)
        sepia = ImageOps.colorize(gray_img, "#704214", "#C0A080")
        contrast = ImageEnhance.Contrast(sepia).enhance(0.8)
        return contrast
    
    elif filter_name == "negative" or filter_name == FilterType.NEGATIVE.name.lower():
        return ImageOps.invert(img)
    
    elif filter_name == "solarize" or filter_name == FilterType.SOLARIZE.name.lower():
        return ImageOps.solarize(img, threshold=128)
    
    elif filter_name == "posterize" or filter_name == FilterType.POSTERIZE.name.lower():
        return ImageOps.posterize(img, bits=int(8 - (strength * 6)))
    
    elif filter_name == "vignette" or filter_name == FilterType.VIGNETTE.name.lower():
        # Create a radial gradient for a vignette effect
        width, height = img.size
        center_x, center_y = width // 2, height // 2
        max_dist = np.sqrt(center_x**2 + center_y**2)
        
        vignette = Image.new('RGB', (width, height), (0, 0, 0))
        pix = vignette.load()
        
        for y in range(height):
            for x in range(width):
                dist = np.sqrt((center_x - x)**2 + (center_y - y)**2)
                factor = 1 - (dist / max_dist * strength)
                factor = max(factor, 0)
                pix[x, y] = (int(factor * 255), int(factor * 255), int(factor * 255))
                
        return ImageChops.multiply(img, vignette)
    
    elif filter_name == "sketch" or filter_name == FilterType.SKETCH.name.lower():
        # Combination of contour and grayscale
        contour = img.filter(ImageFilter.CONTOUR)
        gray = ImageOps.grayscale(contour)
        return gray
    
    elif filter_name == "watercolor" or filter_name == FilterType.WATERCOLOR.name.lower():
        # Combination of slight blur and increased saturation
        blur = img.filter(ImageFilter.GaussianBlur(radius=1.0))
        enhancer = ImageEnhance.Color(blur)
        return enhancer.enhance(1.2)
    
    elif filter_name == "oil_painting" or filter_name == FilterType.OIL_PAINTING.name.lower():
        # Apply median filter for oil painting effect
        return img.filter(ImageFilter.ModeFilter(size=5))
    
    else:
        valid_filters = [f.name.lower() for f in FilterType]
        raise ValueError(f"Filter '{filter_name}' không được hỗ trợ. Valid filters are: {', '.join(valid_filters)}")

# Example usage:
# from PIL import Image
# img = Image.open("your_image.jpg")
# 
# # Using string name
# filtered_img1 = apply_image_filter(img, "vintage")
# 
# # Using enum
# filtered_img2 = apply_image_filter(img, FilterType.VINTAGE)
# 
# # With strength parameter
# filtered_img3 = apply_image_filter(img, FilterType.BLUR, strength=1.5)
# 
# filtered_img1.save("filtered_image.jpg")