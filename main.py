from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from io import BytesIO
import base64
from transparent_background import Remover

app = FastAPI()


@app.post("/remove_background")
async def remove_background(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image uploaded")

    remover = Remover()
    
    img = Image.open(BytesIO(await image.read())).convert('RGB')
    result = remover.process(img)

    output_image_io = BytesIO()
    result.save(output_image_io, format='PNG')
    output_image_io.seek(0)
    encoded_image = base64.b64encode(output_image_io.getvalue()).decode("utf-8")
    full_base64_string = f"data:image/png;base64,{encoded_image}"

    return {"img": full_base64_string};


@app.get("/")
async def hello():
    return {"Hello you success"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5000)