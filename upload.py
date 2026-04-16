import cloudinary.uploader

def upload_image_to_cloudinary(file_bytes):
    result = cloudinary.uploader.upload(file_bytes)
    return result["secure_url"]