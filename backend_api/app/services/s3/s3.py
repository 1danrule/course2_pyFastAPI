import aioboto3
from fastapi import APIRouter, Body, UploadFile

ACCESS_KEY = 'cbafcb0c07b925295c3a3521e9c5610a'
SECRET_KEY = '33e36591294650e5c601c3d2df5b689ff5a7ec002bb0f03643059582e4bdc83d'
BUCKET_NAME = 'course2pyworking170625'
ENDPOINT = 'https://a4b3d54821066174c5a25c39af37ef84.r2.cloudflarestorage.com/course2pyworking170625'
PUBLIC_URL = 'https://pub-d093ac9c609b4f3492ebbaf87535cd32.r2.dev'


class  S3Storage:
    def __init__(self):
        self.bucket_name = BUCKET_NAME

    async def get_s3_session(self):
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=ENDPOINT,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name='EEUR'
        ) as s3:
            yield s3

    async def upload_product_image(self, file: UploadFile, product_uuid: str) -> str:
        async for s3_client in self.get_s3_session():
            path = f'products/{product_uuid}/{file.filename}'
            await s3_client.upload_fileobj(file, self.bucket_name, path)
            url = f"{PUBLIC_URL}/{path}"
        return url


s3_storage = S3Storage()