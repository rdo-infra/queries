from pathlib import Path
from typing import List, Optional, Union

from pydantic import BaseModel, Field, Extra, HttpUrl


class Query(BaseModel):
    id: str
    name: Optional[str]
    pattern: Union[List[str], str]

    category: Optional[str]
    url: Optional[Union[List[HttpUrl], HttpUrl]]

    # elastic-search specific fields
    tags: Optional[Union[List[str], str]]
    suppress_graph: Optional[bool] = Field(
        alias='suppress-graph',
        description="Used for elastic-recheck")

    # artcl/sove specific fields
    regex: Optional[bool] = False
    # https://opendev.org/openstack/ansible-role-collect-logs/src/branch/master/vars/sova-patterns.yml#L47
    multiline: Optional[bool] = False
    files: Optional[List[str]] = Field(
        description="List of glob patterns, narrows down searching")

    class Config:
        extra = Extra.forbid


class Queries(BaseModel):
    queries: List[Query]


# this is equivalent to json.dumps(MainModel.schema(), indent=2):
my_dir = Path(__file__).resolve().parents[1]
output_file = my_dir / "output" / "queries-schema.json"
with open(output_file, "w") as f:
    f.write(Queries.schema_json(indent=2))
    f.write("\n")
