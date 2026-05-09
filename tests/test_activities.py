def test_get_all_activities(client, reset_activities):
    """Test that GET /activities returns all activities"""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(activities_data) >= 3
    for activity_name in expected_activities:
        assert activity_name in activities_data
        activity = activities_data[activity_name]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)


def test_activities_have_correct_structure(client, reset_activities):
    """Test that activities have the correct data structure"""
    # Arrange
    activity_name = "Chess Club"
    
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    activity = activities_data[activity_name]
    
    # Assert
    assert activity["max_participants"] > 0
    assert len(activity["participants"]) <= activity["max_participants"]
    assert all(isinstance(email, str) for email in activity["participants"])


def test_activities_participants_list(client, reset_activities):
    """Test that activity participants are displayed correctly"""
    # Arrange
    expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    chess_club = response.json()["Chess Club"]
    
    # Assert
    assert set(chess_club["participants"]) == set(expected_participants)
