"""
Faker data generator utility for AWS Audit Agent System.

This module provides deterministic generation of realistic dummy data including
company names, user names, emails, and file content for demonstration purposes.
"""

from faker import Faker
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class UserProfile:
    """Represents a generated user profile."""
    name: str
    email: str
    username: str
    role: str
    department: Optional[str] = None


@dataclass
class CompanyData:
    """Represents generated company data."""
    company_name: str
    business_type: str
    industry: str
    tagline: str
    address: str
    phone: str
    website: str


class FakerGenerator:
    """
    Generates realistic but fake data for audit demonstration.
    
    Uses Faker library with a deterministic seed to ensure reproducible
    data generation across multiple runs.
    """
    
    def __init__(self, seed: int = 42):
        """
        Initialize the Faker generator with a seed for deterministic output.
        
        Args:
            seed: Random seed for reproducible data generation. Defaults to 42.
        """
        self.seed = seed
        Faker.seed(seed)
        self.faker = Faker()
        self.faker.seed_instance(seed)
    
    def generate_company_name(self) -> str:
        """
        Generate a realistic company name.
        
        Returns:
            A fake company name.
        """
        return self.faker.company()
    
    def generate_company_data(self) -> CompanyData:
        """
        Generate comprehensive company data.
        
        Returns:
            CompanyData object with all company information.
        """
        return CompanyData(
            company_name=self.faker.company(),
            business_type=self.faker.bs(),
            industry=self.faker.random_element(elements=(
                'Technology', 'Retail', 'Finance', 'Healthcare', 
                'Manufacturing', 'E-commerce', 'Consulting'
            )),
            tagline=self.faker.catch_phrase(),
            address=self.faker.address().replace('\n', ', '),
            phone=self.faker.phone_number(),
            website=self.faker.url()
        )
    
    def generate_user_name(self) -> str:
        """
        Generate a realistic user name.
        
        Returns:
            A fake full name.
        """
        return self.faker.name()
    
    def generate_username(self, name: Optional[str] = None) -> str:
        """
        Generate a username, optionally based on a full name.
        
        Args:
            name: Optional full name to base username on.
        
        Returns:
            A username string.
        """
        if name:
            # Create username from name (e.g., "John Doe" -> "jdoe")
            parts = name.lower().split()
            if len(parts) >= 2:
                return f"{parts[0][0]}{parts[-1]}"
            else:
                return parts[0]
        else:
            return self.faker.user_name()
    
    def generate_email(self, name: Optional[str] = None, domain: Optional[str] = None) -> str:
        """
        Generate a realistic email address.
        
        Args:
            name: Optional full name to base email on.
            domain: Optional domain for the email address.
        
        Returns:
            A fake email address.
        """
        if name and domain:
            username = self.generate_username(name)
            return f"{username}@{domain}"
        elif domain:
            return f"{self.faker.user_name()}@{domain}"
        else:
            return self.faker.email()
    
    def generate_user_profile(
        self, 
        role: str, 
        department: Optional[str] = None,
        company_domain: Optional[str] = None
    ) -> UserProfile:
        """
        Generate a complete user profile with consistent data.
        
        Args:
            role: The user's role (e.g., "Administrator", "Developer").
            department: Optional department name.
            company_domain: Optional company domain for email generation.
        
        Returns:
            UserProfile object with all user information.
        """
        name = self.generate_user_name()
        username = self.generate_username(name)
        email = self.generate_email(name, company_domain)
        
        return UserProfile(
            name=name,
            email=email,
            username=username,
            role=role,
            department=department
        )
    
    def generate_user_profiles(
        self, 
        count: int, 
        roles: Optional[List[str]] = None,
        company_domain: Optional[str] = None
    ) -> List[UserProfile]:
        """
        Generate multiple user profiles.
        
        Args:
            count: Number of user profiles to generate.
            roles: Optional list of roles to assign. If provided, cycles through them.
            company_domain: Optional company domain for email generation.
        
        Returns:
            List of UserProfile objects.
        """
        if roles is None:
            roles = ["Administrator", "Developer", "Business User", "Analyst", "Manager"]
        
        profiles = []
        for i in range(count):
            role = roles[i % len(roles)]
            profile = self.generate_user_profile(role, company_domain=company_domain)
            profiles.append(profile)
        
        return profiles
    
    def generate_file_content(
        self, 
        content_type: str = "text", 
        size_kb: Optional[int] = None
    ) -> str:
        """
        Generate dummy file content.
        
        Args:
            content_type: Type of content to generate ("text", "csv", "json", "log").
            size_kb: Optional target size in KB. If None, generates small sample.
        
        Returns:
            Generated file content as a string.
        """
        if content_type == "text":
            return self._generate_text_content(size_kb)
        elif content_type == "csv":
            return self._generate_csv_content(size_kb)
        elif content_type == "json":
            return self._generate_json_content(size_kb)
        elif content_type == "log":
            return self._generate_log_content(size_kb)
        else:
            return self._generate_text_content(size_kb)
    
    def _generate_text_content(self, size_kb: Optional[int] = None) -> str:
        """Generate plain text content."""
        if size_kb is None:
            # Generate a few paragraphs
            return "\n\n".join([self.faker.paragraph(nb_sentences=5) for _ in range(3)])
        else:
            # Generate text to approximate size
            target_chars = size_kb * 1024
            content = []
            current_size = 0
            
            while current_size < target_chars:
                paragraph = self.faker.paragraph(nb_sentences=5)
                content.append(paragraph)
                current_size += len(paragraph) + 2  # +2 for newlines
            
            return "\n\n".join(content)
    
    def _generate_csv_content(self, size_kb: Optional[int] = None) -> str:
        """Generate CSV content with sample data."""
        rows = 10 if size_kb is None else max(10, (size_kb * 1024) // 100)
        
        lines = ["Name,Email,Department,Role"]
        for _ in range(rows):
            name = self.faker.name()
            email = self.faker.email()
            department = self.faker.random_element(elements=(
                'Engineering', 'Sales', 'Marketing', 'Finance', 'HR'
            ))
            role = self.faker.job()
            lines.append(f"{name},{email},{department},{role}")
        
        return "\n".join(lines)
    
    def _generate_json_content(self, size_kb: Optional[int] = None) -> str:
        """Generate JSON content with sample data."""
        import json
        
        records = 5 if size_kb is None else max(5, (size_kb * 1024) // 200)
        
        data = {
            "records": [
                {
                    "id": i + 1,
                    "name": self.faker.name(),
                    "email": self.faker.email(),
                    "address": self.faker.address().replace('\n', ', '),
                    "phone": self.faker.phone_number(),
                    "company": self.faker.company(),
                    "job_title": self.faker.job()
                }
                for i in range(records)
            ]
        }
        
        return json.dumps(data, indent=2)
    
    def _generate_log_content(self, size_kb: Optional[int] = None) -> str:
        """Generate log file content."""
        lines = 20 if size_kb is None else max(20, (size_kb * 1024) // 100)
        
        log_lines = []
        for _ in range(lines):
            timestamp = self.faker.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S")
            level = self.faker.random_element(elements=('INFO', 'WARN', 'ERROR', 'DEBUG'))
            message = self.faker.sentence()
            log_lines.append(f"[{timestamp}] {level}: {message}")
        
        return "\n".join(log_lines)
    
    def generate_aws_resource_name(self, resource_type: str, prefix: str = "") -> str:
        """
        Generate a realistic AWS resource name.
        
        Args:
            resource_type: Type of AWS resource (e.g., "bucket", "instance", "user").
            prefix: Optional prefix for the resource name.
        
        Returns:
            A generated resource name following AWS naming conventions.
        """
        # Generate a random word for uniqueness
        random_word = self.faker.word().lower()
        random_number = self.faker.random_int(min=100, max=999)
        
        if prefix:
            return f"{prefix}-{resource_type}-{random_word}-{random_number}"
        else:
            return f"{resource_type}-{random_word}-{random_number}"
    
    def reset_seed(self, seed: Optional[int] = None) -> None:
        """
        Reset the Faker seed for reproducibility.
        
        Args:
            seed: New seed value. If None, uses the original seed.
        """
        if seed is not None:
            self.seed = seed
        
        Faker.seed(self.seed)
        self.faker.seed_instance(self.seed)
