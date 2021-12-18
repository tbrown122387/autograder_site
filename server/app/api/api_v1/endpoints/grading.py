import ast
import io
import zipfile
from typing import List, Dict

from app.snippets import (make_grade_one_submission, make_run_autograder,
                          make_run_tests, make_setup_sh)
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post("/uploadfile")
async def create_upload_file(
    assignment_name: str = Form(...),
    package_names: str = Form(None),  # None indicates optional form field
    labels: str = Form(...),
    visibilities: str = Form(...),
    codes: str = Form(...),
    datasets: List[UploadFile] = File(None)
):
    # issue with List[str] interpreted as one element list, so need to convert str to List - https://github.com/tiangolo/fastapi/issues/842#issuecomment-857621157
    # TODO: ast.literal_eval() research speed/security - use json or custom solution?
    if package_names:
        package_names_list: List[str] = ast.literal_eval(package_names)
    labels_list: List[str] = ast.literal_eval(labels)
    visibilities_list: List[str] = ast.literal_eval(visibilities)
    codes_list: List[str] = ast.literal_eval(codes)

    if datasets:
        datasets_str = [
            {
                'data': await dataset.read(),
                'filename': dataset.filename
            }
            for dataset in datasets
        ]

    def iterfile():
        with io.BytesIO() as bytes:
            with zipfile.ZipFile(bytes, mode='w') as zip_file:
                if datasets:
                    for dataset in datasets_str:
                        zip_file.writestr(dataset['filename'], data=dataset['data'])
                zip_file.writestr("setup.sh", data=make_setup_sh(package_names_list))
                zip_file.writestr("run_autograder", data=make_run_autograder(assignment_name))
                zip_file.writestr("grade_one_submission.R", data=make_grade_one_submission(assignment_name))
                zip_file.writestr("run_tests.R", data=make_run_tests(labels_list, visibilities_list, codes_list))
            bytes.seek(0)
            yield from bytes

    headers = {"Content-Disposition": "attachment; filename=data.zip"}
    return StreamingResponse(iterfile(), media_type="application/zip", headers=headers)


@router.get("/sample")
def sample():
    return {"hello": "world"}
