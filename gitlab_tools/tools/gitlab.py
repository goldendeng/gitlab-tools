import gitlab
from flask import current_app
from flask_login import current_user


class VisibilityError(Exception):
    pass


def check_project_visibility_in_group(project_visibility: str, group_id: int) -> None:
    visibility_to_int = {
        'private': 1,
        'internal': 2,
        'public': 3
    }
    group = get_group(group_id)
    if visibility_to_int.get(project_visibility) > visibility_to_int.get(group.visibility):
        raise VisibilityError('Project visibility is less restrictive than its group {} > {}'.format(project_visibility, group.visibility))


def get_gitlab_instance() -> gitlab.Gitlab:
    gl = gitlab.Gitlab(
        current_app.config['GITLAB_URL'],
        oauth_token=current_user.access_token,
        api_version=current_app.config['GITLAB_API_VERSION']
    )

    gl.auth()

    return gl


def get_group(group_id: int):
    gl = get_gitlab_instance()
    return gl.groups.get(group_id)


def get_project(project_id: int):
    gl = get_gitlab_instance()

    return gl.projects.get(project_id)
