import pytest
from fastapi.testclient import TestClient
from src.app import app, activities, logged_in_teachers


@pytest.fixture
def client():
    """Create a test client for the FastAPI application"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Join the school soccer team and compete in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice and play basketball with the school team",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore your creativity through painting and drawing",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
        },
        "Drama Club": {
            "description": "Act, direct, and produce plays and performances",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
        },
        "Math Club": {
            "description": "Solve challenging problems and participate in math competitions",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 10,
            "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
        }
    }

    # Replace activities with original state
    activities.clear()
    activities.update(original_activities)

    yield

    # Cleanup after test
    activities.clear()
    activities.update(original_activities)


# ============================================================================
# Root Endpoint Tests
# ============================================================================

class TestRootEndpoint:
    """Test the root endpoint"""

    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


# ============================================================================
# Get Activities Tests
# ============================================================================

class TestGetActivities:
    """Test the GET /activities endpoint"""

    def test_get_all_activities(self, client, reset_activities):
        """Test retrieving all activities"""
        response = client.get("/activities")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9

    def test_get_activities_contains_all_expected(self, client, reset_activities):
        """Test that all expected activities are present"""
        response = client.get("/activities")
        data = response.json()

        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class",
            "Soccer Team", "Basketball Team", "Art Club",
            "Drama Club", "Math Club", "Debate Team"
        ]

        for activity in expected_activities:
            assert activity in data

    def test_activity_structure(self, client, reset_activities):
        """Test that each activity has correct structure"""
        response = client.get("/activities")
        data = response.json()

        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


# ============================================================================
# Signup Tests
# ============================================================================

class TestSignup:
    """Test the POST /activities/{activity_name}/signup endpoint"""

    def test_successful_signup(self, client, reset_activities):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]

        # Verify student was actually added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "newstudent@mergington.edu" in activities_data["Chess Club"]["participants"]

    def test_signup_nonexistent_activity(self, client):
        """Test signup for a non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_student(self, client, reset_activities):
        """Test that duplicate signup is rejected"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_different_students(self, client, reset_activities):
        """Test that different students can signup"""
        student1_response = client.post(
            "/activities/Programming Class/signup",
            params={"email": "student1@mergington.edu"}
        )
        assert student1_response.status_code == 200

        student2_response = client.post(
            "/activities/Programming Class/signup",
            params={"email": "student2@mergington.edu"}
        )
        assert student2_response.status_code == 200

        # Verify both were added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        participants = activities_data["Programming Class"]["participants"]
        assert "student1@mergington.edu" in participants
        assert "student2@mergington.edu" in participants


# ============================================================================
# Unregister Tests
# ============================================================================

class TestUnregister:
    """Test the DELETE /activities/{activity_name}/unregister endpoint"""

    def test_successful_unregister(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        # First signup
        client.post(
            "/activities/Gym Class/signup",
            params={"email": "testuser@mergington.edu"}
        )

        # Then unregister
        response = client.delete(
            "/activities/Gym Class/unregister",
            params={"email": "testuser@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]

        # Verify student was actually removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "testuser@mergington.edu" not in activities_data["Gym Class"]["participants"]

    def test_unregister_existing_student(self, client, reset_activities):
        """Test unregistering an existing student from an activity"""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 200

        # Verify student was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "michael@mergington.edu" not in activities_data["Chess Club"]["participants"]

    def test_unregister_nonexistent_activity(self, client):
        """Test unregister from a non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent Club/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_not_signed_up_student(self, client, reset_activities):
        """Test unregistering a student who is not signed up"""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "notstudent@mergington.edu"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Test multiple operations together"""

    def test_signup_and_unregister_flow(self, client, reset_activities):
        """Test complete signup and unregister flow"""
        email = "integration@mergington.edu"
        activity = "Soccer Team"

        # Verify student not in activity
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]

        # Signup
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200

        # Verify student in activity
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]

        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200

        # Verify student not in activity
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]

    def test_multiple_signups_same_student(self, client, reset_activities):
        """Test that a student can signup for multiple activities"""
        email = "multistudent@mergington.edu"
        activities_to_join = ["Chess Club", "Art Club", "Math Club"]

        for activity in activities_to_join:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Verify student is in all activities
        response = client.get("/activities")
        data = response.json()
        for activity in activities_to_join:
            assert email in data[activity]["participants"]


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and unusual inputs"""

    def test_signup_with_special_characters_email(self, client, reset_activities):
        """Test signup with special characters in email"""
        email = "test+tag@mergington.edu"
        response = client.post(
            "/activities/Drama Club/signup",
            params={"email": email}
        )
        assert response.status_code == 200

        # Verify it was added
        activities_response = client.get("/activities")
        assert email in activities_response.json()[
            "Drama Club"]["participants"]

    def test_activity_name_case_sensitive(self, client):
        """Test that activity names are case-sensitive"""
        response = client.post(
            "/activities/chess club/signup",  # lowercase
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404


# ============================================================================
# Authentication Tests
# ============================================================================

class TestAuthentication:
    """Test teacher authentication and authorization"""

    @pytest.fixture(autouse=True)
    def cleanup_logged_in(self):
        """Clear logged in teachers before and after each test"""
        logged_in_teachers.clear()
        yield
        logged_in_teachers.clear()

    def test_successful_login(self, client):
        """Test successful teacher login"""
        response = client.post(
            "/login",
            params={"username": "teacher1", "password": "password123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Login successful"
        assert data["username"] == "teacher1"

    def test_invalid_password(self, client):
        """Test login with invalid password"""
        response = client.post(
            "/login",
            params={"username": "teacher1", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_nonexistent_teacher(self, client):
        """Test login with non-existent teacher"""
        response = client.post(
            "/login",
            params={"username": "nonexistent", "password": "password123"}
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_successful_logout(self, client):
        """Test successful teacher logout"""
        # First login
        client.post(
            "/login",
            params={"username": "teacher1", "password": "password123"}
        )

        # Then logout
        response = client.post(
            "/logout",
            params={"username": "teacher1"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Logout successful"

    def test_logout_not_logged_in_user(self, client):
        """Test logout of user who wasn't logged in"""
        response = client.post(
            "/logout",
            params={"username": "teacher1"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "User was not logged in"

    def test_multiple_teachers_login(self, client):
        """Test multiple teachers can login"""
        # Teacher 1 login
        response1 = client.post(
            "/login",
            params={"username": "teacher1", "password": "password123"}
        )
        assert response1.status_code == 200

        # Teacher 2 login
        response2 = client.post(
            "/login",
            params={"username": "teacher2", "password": "password456"}
        )
        assert response2.status_code == 200

        # Both should be able to logout
        logout1 = client.post(
            "/logout",
            params={"username": "teacher1"}
        )
        logout2 = client.post(
            "/logout",
            params={"username": "teacher2"}
        )
        assert logout1.status_code == 200
        assert logout2.status_code == 200


# ============================================================================
# Authorization Tests
# ============================================================================

class TestAuthorization:
    """Test teacher authorization for activity management"""

    @pytest.fixture(autouse=True)
    def cleanup_logged_in(self):
        """Clear logged in teachers before and after each test"""
        logged_in_teachers.clear()
        yield
        logged_in_teachers.clear()

    def test_teacher_can_unregister_students(self, client, reset_activities):
        """Test that logged-in teacher can unregister students"""
        # First login
        client.post(
            "/login",
            params={"username": "teacher1", "password": "password123"}
        )

        # Teacher unregisters a student
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={
                "email": "michael@mergington.edu",
                "teacher_username": "teacher1"
            }
        )
        assert response.status_code == 200

        # Verify student was removed
        activities_response = client.get("/activities")
        assert "michael@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]

    def test_teacher_can_signup_students(self, client, reset_activities):
        """Test that teacher can signup students for activities"""
        # First login
        client.post(
            "/login",
            params={"username": "teacher1", "password": "password123"}
        )

        # Teacher signs up a student
        response = client.post(
            "/activities/Drama Club/signup",
            params={
                "email": "newstudent@mergington.edu",
                "teacher_username": "teacher1"
            }
        )
        assert response.status_code == 200

        # Verify student was added
        activities_response = client.get("/activities")
        assert "newstudent@mergington.edu" in activities_response.json()["Drama Club"]["participants"]
