from typing import Dict, Optional, List

from pydantic import BaseModel


class RAssignment(BaseModel):
    bundle_name: Optional[str]
    tests_collection: Optional[List[Dict]]
    assignment_name: Optional[str]
    package_names: Optional[str]
    datasets: Optional[List[str]]
    setup_code: Optional[str]
    assignment_id: Optional[int]


class RAssignmentId(BaseModel):
    assignment_id: int
