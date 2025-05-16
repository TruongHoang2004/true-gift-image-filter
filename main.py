# main.py
from typing import Optional
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from filter import apply_image_filter, FilterTypeLiteral  # Import hàm từ filter.py
import io
from PIL import Image

app = FastAPI(title="TrueGift RAG Indexer", debug=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc thay bằng danh sách domain cụ thể như ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/image/filter")
async def filter_image(
    file: UploadFile = File(...),
    filter_name: FilterTypeLiteral = Form(...),
    strength: Optional[float] = Form(1.0, ge=0.0, le=2.0)
):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        if image.mode != "RGB":
            image = image.convert("RGB")
        filtered_image = apply_image_filter(image, filter_name, strength=strength)

        output_format = 'JPEG'
        ext = file.filename.split('.')[-1].lower()
        if ext in ['png', 'gif']:
            output_format = ext.upper()

        img_byte_arr = io.BytesIO()
        filtered_image.save(img_byte_arr, format=output_format)
        img_byte_arr.seek(0)

        return StreamingResponse(
            img_byte_arr,
            media_type=f"image/{output_format.lower()}",
            headers={"Content-Disposition": f'inline; filename="filtered_{filter_name}.{ext}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing error: {str(e)}")


@app.get("/image/filters")
async def list_available_filters():
    filters = {
        "grayscale": "Convert image to grayscale",
        "sepia": "Apply classic sepia tone effect",
        "blur": "Blur the image",
        "contour": "Show image contours",
        "sharpen": "Sharpen the image",
        "edge_enhance": "Enhance edges",
        "emboss": "Apply 3D emboss effect",
        "find_edges": "Detect and show edges",
        "brightness": "Adjust image brightness",
        "contrast": "Adjust image contrast",
        "saturation": "Adjust color saturation",
        "vintage": "Vintage photo effect",
        "negative": "Invert image colors",
        "solarize": "Partially invert colors",
        "posterize": "Reduce number of colors",
        "vignette": "Darken image corners",
        "sketch": "Sketch drawing effect",
        "watercolor": "Watercolor painting effect",
        "oil_painting": "Oil painting effect"
    }
    return {"available_filters": filters}

@app.get("/image/filter/preview/{filter_name}")
async def preview_filter(
    filter_name: FilterTypeLiteral,
    strength: Optional[float] = Query(1.0, ge=0.0, le=2.0)
):
    try:
        sample_img = Image.new('RGB', (400, 300), color=(73, 109, 137))
        filtered_image = apply_image_filter(sample_img, filter_name, strength=strength)
        
        img_byte_arr = io.BytesIO()
        filtered_image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        return StreamingResponse(img_byte_arr, media_type="image/jpeg")
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý ảnh: {str(e)}")
