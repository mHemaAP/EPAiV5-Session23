from datetime import datetime
from weakref import WeakValueDictionary
import re

class ValidatedProperty:
    """
    A descriptor class that provides property validation functionality.
    
    This class implements the descriptor protocol to validate values before they are
    assigned to instance attributes. It uses a provided validator function to check
    if values meet the required criteria.
    
    Attributes:
        validator (callable): A function that takes a value and returns True if valid
        name (str): The name of the property, set automatically by __set_name__
    """
    
    def __init__(self, validator):
        """
        Initialize the ValidatedProperty with a validator function.
        
        Args:
            validator (callable): A function that takes a value and returns True if valid
        """
        self.validator = validator
        self.name = None
    
    def __set_name__(self, owner, name):
        """
        Set the name of the property automatically when the descriptor is assigned to a class.
        
        Args:
            owner (type): The class owning this descriptor
            name (str): The name of the property in the class
        """
        self.name = name
    
    def __get__(self, instance, owner):
        """
        Get the value of the property.
        
        Args:
            instance: The instance accessing the property
            owner: The class owning this descriptor
            
        Returns:
            The value of the property or self if accessed on the class
        """
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        """
        Set the value of the property after validation.
        
        Args:
            instance: The instance the property is being set on
            value: The value to set
            
        Raises:
            ValueError: If the value fails validation
        """
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        instance.__dict__[self.name] = value

class UserProfileManager:
    """
    Manages user profiles with validation and caching functionality.
    
    This class provides mechanisms for creating and managing user profiles with
    validated attributes (username, email, last_login) and implements a caching
    system using weak references to prevent memory leaks.
    
    Class Attributes:
        _instance_cache (WeakValueDictionary): Cache for storing profile instances
        default_last_login (datetime): Default value for last_login when None
    """
    
    _instance_cache = WeakValueDictionary()
    default_last_login = datetime(2000, 1, 1)
    
    @staticmethod
    def validate_username(username):
        """
        Validate that a username is a non-empty string.
        
        Args:
            username: The username to validate
            
        Returns:
            bool: True if username is valid, False otherwise
        """
        return isinstance(username, str) and bool(username.strip())
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format using regex pattern.
        
        Args:
            email: The email address to validate
            
        Returns:
            bool: True if email format is valid, False otherwise
        """
        if not isinstance(email, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_last_login(date):
        """
        Validate that last_login is either None or a datetime object.
        
        Args:
            date: The date to validate
            
        Returns:
            bool: True if date is None or a datetime object, False otherwise
        """
        return date is None or isinstance(date, datetime)

    username = ValidatedProperty(validate_username)
    email = ValidatedProperty(validate_email)
    last_login = ValidatedProperty(validate_last_login)
    
    def __init__(self):
        """
        Initialize an empty UserProfileManager with default values.
        
        All attributes are initially set to None and can be set later with validation.
        """
        self._username = None
        self._email = None
        self._last_login = None
    
    @classmethod
    def add_to_cache(cls, instance):
        """
        Add a profile instance to the cache using its id as key.
        
        Args:
            instance: The UserProfileManager instance to cache
        """
        cls._instance_cache[id(instance)] = instance
    
    @classmethod
    def get_from_cache(cls, uid):
        """
        Retrieve a profile from cache by its id.
        
        Args:
            uid: The id of the profile to retrieve
            
        Returns:
            UserProfileManager: The cached profile instance or None if not found
        """
        return cls._instance_cache.get(uid)
    
    @property
    def last_login_with_default(self):
        """
        Get last_login with default value if None.
        
        Returns:
            datetime: The last_login value or default_last_login if None
        """
        return self.last_login if self.last_login is not None else self.default_last_login
    
    def update_last_login(self, new_time=None):
        """
        Update last_login time with provided time or current time.
        
        Args:
            new_time (datetime, optional): The time to set. Defaults to current time if None.
        """
        self.last_login = new_time if new_time is not None else datetime.now()
    
    def __str__(self):
        """
        Create a string representation of the profile.
        
        Returns:
            str: A string containing the profile's username, email, and last_login
        """
        return f"UserProfile(username={self.username}, email={self.email}, last_login={self.last_login})"