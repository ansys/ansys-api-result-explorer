
def test_imports():
    from ansys.api.result_explorer.v0.solution_pb2 import SolutionCreate, SolutionList
    from ansys.api.result_explorer.v0.workspace_pb2 import WorkspaceList, WorkspaceCreate

def test_init():
    from ansys.api.result_explorer.v0.solution_pb2 import SolutionCreate

    _ = SolutionCreate(
        name="Test Solution",
    )