def test_root_redirect(client):
    """Test that root endpoint redirects to static/index.html"""
    # Arrange
    expected_url = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert expected_url in response.headers["location"]
