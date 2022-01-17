import ast
import io
import zipfile
from typing import List, Optional

from app.api import deps
from app.crud import crud_rassignment
from app import models
from app.schemas import assignment_schema
from app.snippets import (make_grade_one_submission, make_run_autograder,
                          make_run_tests, make_setup_sh)
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.param_functions import Depends
from fastapi.responses import StreamingResponse
from sqlmodel import Session

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
    package_names_list: Optional[List[str]] = None
    if package_names:
        package_names_list = ast.literal_eval(package_names)

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


@router.post("/save_assignment", response_model=models.RAssignment)
async def save_assignment(RAssignment: assignment_schema.RAssignment, session: Session = Depends(deps.get_session), current_user: models.User = Depends(deps.get_current_user)):
    assignment = crud_rassignment.save_assignment(
        session=session,
        current_user=current_user,
        assignment_id=RAssignment.assignment_id,
        bundle_name=RAssignment.bundle_name,
        tests_collection=RAssignment.tests_collection,
        assignment_name=RAssignment.assignment_name,
        package_names=RAssignment.package_names,
        datasets=RAssignment.datasets,
        setup_code=RAssignment.setup_code
    )
    session.refresh(current_user)
    return assignment


@router.post("/delete_assignment", response_model=models.RAssignment)
async def delete_assignment(assignment_id: assignment_schema.RAssignmentId, session: Session = Depends(deps.get_session), current_user: models.User = Depends(deps.get_current_user)):
    assignment = crud_rassignment.delete_assignment_from_id(
        current_user=current_user, session=session, assignment_id=assignment_id.assignment_id)
    session.refresh(current_user)
    return assignment


@router.get("/assignments", response_model=List[models.RAssignment])
async def assignments(current_user: models.User = Depends(deps.get_current_user)):
    assignments = crud_rassignment.get_assignments_from_user(current_user)
    return assignments


@router.get("/assignment/{assignment_id}", response_model=models.RAssignment)
async def get_assignment(
        assignment_id: int,
        session=Depends(deps.get_session),
        current_user: models.User = Depends(deps.get_current_user)):
    assignment = crud_rassignment.get_assignment_from_id(
        current_user=current_user, session=session, assignment_id=assignment_id)
    session.refresh(assignment)
    return assignment
