from dotenv import load_dotenv
import json
import lambdas.user as user
import pytest

load_dotenv()

def test_user_create():
    event_add = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "USER-123",
        "email": "test@test.com",
        "username": "tester",
    }
    response = user.handler(event_add, {})

    event_destroy = {
        "action": "force_destroy",
        "orgId": "ORG-123",
        "userId": "USER-123",
    }
    user.handler(event_destroy, {})

    new_user = json.loads(response['body'].replace("'", '"'))
    assert new_user["orgId"] == event_add["orgId"]
    assert new_user["userId"] == event_add["userId"]
    assert new_user["email"] == event_add["email"]
    assert new_user["username"] == event_add["username"]

def test_user_create_no_id():
    event_add = {
        "action": "add",
        "orgId": "ORG-123",
        "email": "no-id@test.com",
        "username": "no id tester",
    }
    response = user.handler(event_add, {})
    new_user = json.loads(response['body'].replace("'", '"'))

    event_destroy = {
        "action": "force_destroy",
        "orgId": "ORG-123",
        "userId": new_user["userId"],
    }
    user.handler(event_destroy, {})

    assert new_user["orgId"] == event_add["orgId"]
    assert new_user["userId"] != "USER-123"
    assert new_user["email"] == event_add["email"]
    assert new_user["username"] == event_add["username"]

def test_user_create_bad_org():
    event_add = {
        "action": "add",
        "orgId": "BORG-123",
        "email": "no-id@test.com",
        "username": "no id tester",
    }
    with pytest.raises(Exception) as e:
        user.handler(event_add, {})

def test_user_create_bad_user_id():
    event_add = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "BUSER-123",
        "email": "no-id@test.com",
        "username": "no id tester",
    }
    with pytest.raises(Exception) as e:
        user.handler(event_add, {})

def test_user_update():
    event_add = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "USER-123UPDATE",
        "email": "update@test.com",
        "username": "update tester",
    }
    user.handler(event_add, {})

    event_update = {
        "action": "update",
        "orgId": "ORG-123",
        "userId": "USER-123UPDATE",
        "email": "update2@test.com",
        "username": "update2 tester",
    }
    response = user.handler(event_update, {})

    event_destroy = {
        "action": "force_destroy",
        "orgId": "ORG-123",
        "userId": "USER-123UPDATE",
    }
    user.handler(event_destroy, {})

    updated_user = json.loads(response['body'].replace("'", '"'))
    assert updated_user["email"] == event_update["email"]
    assert updated_user["username"] == event_update["username"]

def test_user_delete():
    event_add = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "USER-123DELETE",
        "email": "delete@test.com",
        "username": "delete tester",
    }
    user.handler(event_add, {})

    event_delete = {
        "action": "delete",
        "orgId": "ORG-123",
        "userId": "USER-123DELETE",
        "email": "delete@test.com",
        "username": "delete tester",
    }
    response = user.handler(event_delete, {})

    event_destroy = {
        "action": "force_destroy",
        "orgId": "ORG-123",
        "userId": "USER-123DELETE",
    }
    user.handler(event_destroy, {})

    deleted_user = json.loads(response['body'].replace("'", '"'))
    assert deleted_user["email"] == event_delete["email"]
    assert deleted_user["username"] == event_delete["username"]

def test_user_restore():
    event_add = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "USER-123RESTORE",
        "email": "restore@test.com",
        "username": "restore tester",
    }
    user.handler(event_add, {})

    event_delete = {
        "action": "delete",
        "orgId": "ORG-123",
        "userId": "USER-123RESTORE",
    }
    response = user.handler(event_delete, {})
    deleted_user = json.loads(response['body'].replace("'", '"'))
    assert 'deletedAt' in deleted_user

    event_restore = {
        "action": "restore",
        "orgId": "ORG-123",
        "userId": "USER-123RESTORE",
    }
    response = user.handler(event_restore, {})

    restored_user = json.loads(response['body'].replace("'", '"'))
    assert 'deletedAt' not in restored_user

    event_destroy = {
        "action": "force_destroy",
        "orgId": "ORG-123",
        "userId": "USER-123RESTORE",
    }
    user.handler(event_destroy, {})

def test_user_destroy():
    event_add = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "USER-123DESTROY",
        "email": "detroy@test.com",
        "username": "detroy tester",
    }
    user.handler(event_add, {})

    event_delete = {
        "action": "delete",
        "orgId": "ORG-123",
        "userId": "USER-123DESTROY",
    }
    response = user.handler(event_delete, {})

    event_destroy = {
        "action": "destroy",
        "orgId": "ORG-123",
        "userId": "USER-123DESTROY",
    }
    user.handler(event_destroy, {})

    destroyed_user = json.loads(response['body'].replace("'", '"'))
    assert destroyed_user["userId"] == event_delete["userId"]
    assert 'email' in destroyed_user
    assert "username" in destroyed_user

def test_user_destroy_nondeleted():
    event_add = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "USER-123NOTDELETED",
        "email": "detroy@test.com",
        "username": "detroy tester",
    }
    user.handler(event_add, {})

    event_destroy = {
        "action": "destroy",
        "orgId": "ORG-123",
        "userId": "USER-123NOTDELETED",
    }

    response = user.handler(event_destroy, {})
    assert response['statusCode'] == 400

    event_destroy = {
        "action": "force_destroy",
        "orgId": "ORG-123",
        "userId": "USER-123NOTDELETED",
    }
    user.handler(event_destroy, {})

def test_user_find():
    event_add = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "USER-123FIND",
        "email": "find@test.com",
        "username": "find tester",
    }
    user.handler(event_add, {})

    event_find = {
        "action": "find",
        "orgId": "ORG-123",
        "userId": "USER-123FIND",
    }
    response = user.handler(event_find, {})

    event_destroy = {
        "action": "force_destroy",
        "orgId": "ORG-123",
        "userId": "USER-123FIND",
    }
    user.handler(event_destroy, {})

    found_user = json.loads(response['body'].replace("'", '"'))
    assert found_user["userId"] == event_add["userId"]
    assert found_user["email"] == event_add["email"]

def test_user_find_all():
    event_add1 = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "USER-123FIND1",
        "email": "find1@test.com",
        "username": "find1 tester",
    }

    event_add2 = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "USER-123FIND2",
        "email": "find2@test.com",
        "username": "find2 tester",
    }

    user.handler(event_add1, {})
    user.handler(event_add2, {})

    event_find_all = {
        "action": "find_all",
        "orgId": "ORG-123",
    }
    response = user.handler(event_find_all, {})

    for find_userId in ["USER-123FIND1", "USER-123FIND2"]:
        event_destroy = {
            "action": "force_destroy",
            "orgId": "ORG-123",
            "userId": find_userId,
        }
        user.handler(event_destroy, {})

    found_users = json.loads(response['body'].replace("'", '"'))
    assert found_users[0]["userId"] == event_add1["userId"]
    assert found_users[1]["email"] == event_add2["email"]

def test_user_find_by_email():
    event_add = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "USER-123FINDEMAIL",
        "email": "findemail@test.com",
        "username": "find email tester",
    }
    user.handler(event_add, {})

    event_find_by_email = {
        "action": "find_by_email",
        "email": "findemail@test.com",
    }
    response = user.handler(event_find_by_email, {})

    event_destroy = {
        "action": "force_destroy",
        "orgId": "ORG-123",
        "userId": "USER-123FINDEMAIL",
    }
    user.handler(event_destroy, {})

    found_user = json.loads(response['body'].replace("'", '"'))
    assert found_user["userId"] == event_add["userId"]
    assert found_user["email"] == event_add["email"]