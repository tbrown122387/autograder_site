import ast
import io
import zipfile
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from sqlmodel import Session, SQLModel, select

from db import engine
from models import Comment, User
from schemas import DeleteID
from snippets import (make_grade_one_submission, make_run_autograder,
                      make_run_tests, make_setup_sh)

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.get("/api/sample")
def sample():
    return {"Hello": "World"}


@app.post("/comments/create")
def create_comment(comment: Comment):
    comment.id = None

    with Session(engine) as session:
        # make sure user_id exists
        user = session.get(User, comment.user_id)
        if not user:
            comment.user_id = None
        session.add(comment)
        session.commit()
        session.refresh(comment)
    return comment


@app.post("/comments/delete")
def delete_comment(delete_id: DeleteID):
    with Session(engine) as session:
        comment = session.get(Comment, delete_id.id)
        if not comment:
            raise HTTPException(status_code=400, detail="Comment not found")
        session.delete(comment)
        session.commit()
    return comment


@app.get("/comments")
def read_comment():
    with Session(engine) as session:
        heroes = session.exec(select(Comment)).all()
        return heroes


@app.post("/uploadfile1")
def create_upload_file(file: UploadFile = File(...)):
    contents: str = file.file.read()
    headers = {"Content-Disposition": "attachment; filename=data_pandas.csv"}
    return FileResponse('data_pandas.csv', headers=headers)


@app.post("/uploadfile")
async def create_upload_file(
        assignment_name: str = Form(...),
        package_names: str = Form(None),  # None indicates optional form field
        labels: str = Form(...),
        visibilities: str = Form(...),
        codes: str = Form(...),
        datasets: List[UploadFile] = File(None)):
    # issue with List[str] interpreted as one element list, so need to convert str to List - https://github.com/tiangolo/fastapi/issues/842#issuecomment-857621157
    # TODO: ast.literal_eval() research speed/security - use json or custom solution?
    if package_names:
        package_names = ast.literal_eval(package_names)
    labels = ast.literal_eval(labels)
    visibilities = ast.literal_eval(visibilities)
    codes = ast.literal_eval(codes)

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
                zip_file.writestr("setup.sh", data=make_setup_sh(package_names))
                zip_file.writestr("run_autograder", data=make_run_autograder(assignment_name))
                zip_file.writestr("grade_one_submission.R", data=make_grade_one_submission(assignment_name))
                zip_file.writestr("run_tests.R", data=make_run_tests(labels, visibilities, codes))
            bytes.seek(0)
            yield from bytes

    headers = {"Content-Disposition": "attachment; filename=data.zip"}
    return StreamingResponse(iterfile(), media_type="application/zip", headers=headers)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# def main():
#     uvicorn.run("main:app", host="0.0.0.0", reload=True, port=5000)


# if __name__ == "__main__":
#     main()
