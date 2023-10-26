from ....lambdas.user import user

# example tests. To run these tests, uncomment this file along with the example
# resource in refactor/refactor_stack.py
def test_user_create():
    event_add = {
        "action": "add",
        "orgId": "ORG-123",
        "userId": "USER-123",
        "email": "test@test.com"
    }
    response = user.handler(event_add, {})
    assert response['userId'] == "USER-123"
    assert response['email'] == "test@test.com"
    assert response['orgId'] == "ORG-123"

    event_destroy = {
        "action": "force_destroy",
        "orgId": "ORG-123",
        "userId": "USER-123",
    }
    user.handler(event_destroy, {})