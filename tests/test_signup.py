def test_signup_success(client, reset_activities):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities").json()
    assert email in activities_response[activity_name]["participants"]


def test_signup_duplicate_student(client, reset_activities):
    """Test that duplicate signup returns 400 error"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found(client, reset_activities):
    """Test that signup for non-existent activity returns 404 error"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_new_student_different_activities(client, reset_activities):
    """Test that a student can sign up for multiple different activities"""
    # Arrange
    email = "versatile@mergington.edu"
    activities_to_join = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act & Assert
    for activity_name in activities_to_join:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify student was added to this activity
        activities_response = client.get("/activities").json()
        assert email in activities_response[activity_name]["participants"]
