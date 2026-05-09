def test_unregister_success(client, reset_activities):
    """Test successful unregister from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities").json()
    assert email not in activities_response[activity_name]["participants"]


def test_unregister_student_not_signed_up(client, reset_activities):
    """Test that unregister for non-participant returns 400 error"""
    # Arrange
    activity_name = "Chess Club"
    email = "notstudent@mergington.edu"  # Not signed up
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_activity_not_found(client, reset_activities):
    """Test that unregister from non-existent activity returns 404 error"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_then_signup_again(client, reset_activities):
    """Test that a student can unregister and then sign up again"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act - First unregister
    response_unregister = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert - Unregister succeeded
    assert response_unregister.status_code == 200
    
    # Act - Then sign up again
    response_signup = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Sign up succeeded
    assert response_signup.status_code == 200
    activities_response = client.get("/activities").json()
    assert email in activities_response[activity_name]["participants"]
