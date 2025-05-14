# main.py
from typing import Optional
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from filter import apply_image_filter, FilterTypeLiteral  # Import hàm từ filter.py
import io
from PIL import Image

app = FastAPI(title="TrueGift RAG Indexer", debug=False)

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
        
        img_byte_arr = io.BytesIO()
        output_format = 'JPEG'
        
        if file.filename.lower().endswith('.png'):
            output_format = 'PNG'
        elif file.filename.lower().endswith('.gif'):
            output_format = 'GIF'
        
        filtered_image.save(img_byte_arr, format=output_format)
        img_byte_arr.seek(0)
        
        media_type = f"image/{output_format.lower()}"
        
        return StreamingResponse(
            img_byte_arr, 
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="filtered_{filter_name}_{file.filename}"'}
        )

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý ảnh: {str(e)}")


@app.get("/image/filters")
async def list_available_filters():
    filters = {
        "Cơ bản": {
            "grayscale": "Chuyển đổi sang ảnh đen trắng",
            "sepia": "Tạo hiệu ứng màu nâu vàng cổ điển",
            "blur": "Làm mờ hình ảnh",
            "contour": "Hiển thị đường viền của hình ảnh"
        },
        "Nâng cao": {
            "sharpen": "Tăng độ sắc nét",
            "edge_enhance": "Tăng cường đường viền",
            "emboss": "Tạo hiệu ứng nổi 3D",
            "find_edges": "Phát hiện và hiển thị các cạnh"
        },
        "Điều chỉnh màu": {
            "brightness": "Điều chỉnh độ sáng",
            "contrast": "Điều chỉnh độ tương phản",
            "saturation": "Điều chỉnh độ bão hòa màu sắc"
        },
        "Hiệu ứng đặc biệt": {
            "vintage": "Hiệu ứng ảnh cổ điển",
            "negative": "Đảo ngược màu sắc",
            "solarize": "Đảo ngược một phần màu sắc",
            "posterize": "Giảm số lượng màu sắc",
            "vignette": "Làm tối các cạnh của hình ảnh",
            "sketch": "Tạo hiệu ứng phác họa",
            "watercolor": "Mô phỏng tranh màu nước",
            "oil_painting": "Mô phỏng tranh sơn dầu"
        }
    }
    
    return {
        "available_filters": filters,
        "usage": {
            "endpoint": "/image/filter",
            "method": "POST",
            "parameters": {
                "file": "Tệp hình ảnh (form-data)",
                "filter_name": "Tên của filter (form-data)",
                "strength": "Cường độ hiệu ứng, từ 0.0 đến 2.0 (form-data, tùy chọn)"
            }
        }
    }


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
