
import pytest
from user_profile_manager import UserProfileManager

def test_username_validation():
    manager = UserProfileManager()
    with pytest.raises(ValueError):
        manager.username = ""  # Invalid: Empty string
    manager.username = "valid_user"  # Valid
    assert manager.username == "valid_user"

def test_email_validation():
    manager = UserProfileManager()
    with pytest.raises(ValueError):
        manager.email = "invalidemail.com"  # Invalid: Missing '@'
    manager.email = "user@example.com"  # Valid
    assert manager.email == "user@example.com"

def test_last_login_default():
    manager = UserProfileManager()
    assert manager.last_login is None  # Default value

def test_cache_management():
    manager = UserProfileManager()
    manager.username = "cache_test"
    manager.email = "test@example.com"
    uid = id(manager)
    
    # Add to cache and check existence
    UserProfileManager.add_to_cache(manager)
    assert UserProfileManager.get_from_cache(uid) is manager
    
    # Delete strong reference and confirm weak ref removal
    del manager
    assert UserProfileManager.get_from_cache(uid) is None

def test_property_resolution():
    manager = UserProfileManager()
    manager.last_login = None  # Should resolve to default if unset
    assert manager.last_login is None
