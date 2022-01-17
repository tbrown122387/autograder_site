from typing import Dict, List, Optional

from app.models import RAssignment, User
from fastapi.exceptions import HTTPException
from sqlmodel import Session


def save_assignment(
    session: Session,
    current_user: User,
    assignment_id: Optional[int],
    bundle_name: Optional[str],
    tests_collection: Optional[List[Dict]],
    assignment_name: Optional[str],
    package_names: Optional[str],
    datasets: Optional[List[str]],
    setup_code: Optional[str]
):
    assignment: Optional[RAssignment] = session.get(RAssignment, assignment_id)
    # if assignment exists, overwrite existing assignment with new data; else create new assignment
    if assignment:
        if assignment.user_id == current_user.id:  # making sure assignment belongs to user
            assignment.bundle_name = bundle_name
            assignment.tests_collection = tests_collection
            assignment.assignment_name = assignment_name
            assignment.package_names = package_names
            assignment.datasets = datasets
            assignment.setup_code = setup_code
        else:
            raise HTTPException(status_code=400, detail="Assignment does not belong to user")

    else:
        assignment = RAssignment(
            tests_collection=tests_collection,
            bundle_name=bundle_name,
            assignment_name=assignment_name,
            package_names=package_names,
            datasets=datasets,
            setup_code=setup_code,
            user_id=current_user.id
        )

    session.add(assignment)
    session.commit()
    session.refresh(assignment)

    return assignment


def get_assignments_from_user(current_user: User):
    return current_user.rAssignments


def delete_assignment_from_id(current_user: User, session: Session, assignment_id: int):
    assignment = session.get(RAssignment, assignment_id)
    if assignment:
        if assignment.user_id == current_user.id:  # making sure assignment belongs to user
            session.delete(assignment)
            session.commit()
            return assignment
        else:
            raise HTTPException(status_code=400, detail="Assignment does not belong to user")
    else:
        raise HTTPException(status_code=400, detail="Assignment does not exist")


def get_assignment_from_id(current_user: User, session: Session, assignment_id: int):
    assignment = session.get(RAssignment, assignment_id)
    if assignment:
        if assignment.user_id == current_user.id:  # making sure assignment belongs to user
            return assignment
        else:
            raise HTTPException(status_code=400, detail="Assignment does not belong to user")
    else:
        raise HTTPException(status_code=400, detail="Assignment does not exist")
