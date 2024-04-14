from fastapi.testclient import TestClient
import pytest


@pytest.mark.parametrize("tag_ids,feature_id,content,is_active,token,status_code", [
    ([7], 7, {"title": "some title"}, True, "admin_token", 201),
    ([7], 7, {"title": "some title"}, True, "admin_token", 400),
    ([], 1, {}, False, "admin_token", 400),
    ([1], None, {}, False, "admin_token", 400),
    (None, 1, {}, True, "admin_token", 400),
    ([100], 100, {"title": "some title"}, True, "user_token", 403),
    ([100], 100, {"title": "some title"}, True, "", 401),
])
def test_post_banner(tag_ids, feature_id, content, is_active, status_code, token, c: TestClient):
    response = c.post(
        "/banner",
        headers={"token": token},
        json={
        "tag_ids": tag_ids,
        "feature_id": feature_id,
        "content": content,
        "is_active": is_active
        })
    assert response.status_code == status_code
    if status_code == 201:
        assert isinstance(response.json()["banner_id"], int)
