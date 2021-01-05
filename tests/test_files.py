import pytest
from ninja import NinjaAPI, File, UploadedFile
from client import NinjaClient
from django.core.files.uploadedfile import SimpleUploadedFile


api = NinjaAPI()


@api.post("/file")
def file_upload(request, file: UploadedFile = File(...)):
    return {"name": file.name, "data": file.read().decode()}


client = NinjaClient(api)


def test_files():
    response = client.post("/file")  # no file
    assert response.status_code == 422

    file = SimpleUploadedFile("test.txt", b"data123")
    response = client.post("/file", FILES={"file": file})
    assert response.status_code == 200
    assert response.json() == {"name": "test.txt", "data": "data123"}


def test_invalid_file():
    with pytest.raises(ValueError):
        UploadedFile.validate("not_a_file")
