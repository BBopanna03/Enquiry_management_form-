from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

# -------------------- Validators --------------------
def validate_phone_number(value):
    if not re.fullmatch(r"^[9876]\d{9}$", value):
        raise ValidationError("Phone number must start with 9, 8, 7, or 6 and be exactly 10 digits.")

def validate_gmail_email(value):
    if not value.lower().endswith("@gmail.com"):
        raise ValidationError("Only @gmail.com emails are allowed.")

def validate_name(value):
    if not re.fullmatch(r"^[A-Za-z ]{2,100}$", value):
        raise ValidationError("Name must be 2-100 characters long and contain only alphabets and spaces.")

# -------------------- Access Control --------------------
class AccessControl(models.Model):
    USER_ROLES = (
        ('counsellor', 'Counsellor'),
        ('accounts', 'Accounts'),
        ('hr', 'HR'),
        ('admin', 'Admin'),
        ('consumer', 'Consumer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='counsellor')

    class Meta:
        db_table = "access_control"

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# -------------------- Student Enquiry --------------------
class StudentEnquiry(models.Model):
    name = models.CharField(max_length=100, validators=[validate_name])
    phone_number = models.CharField(max_length=10, validators=[validate_phone_number])
    email = models.EmailField(validators=[validate_gmail_email])
    current_location = models.CharField(max_length=255)
    current_address = models.CharField(max_length=255, blank=True, null=True)

    COURSE_CHOICES = [
        ("Professional Starter Testing", "Professional Starter Testing"),
        ("Professional Experts with Java Automation", "Professional Experts with Java Automation"),
        ("Professional Experts with Python Automation", "Professional Experts with Python Automation"),
        ("Professional Experts with Mobile Automation", "Professional Experts with Mobile Automation"),
        ("Professional Experts with API Automation", "Professional Experts with API Automation"),
        ("SDET Xpert", "SDET Xpert"),
        ("Individual Courses", "Individual Courses"),
        ("AI Testing", "AI Testing"),
        ("Playwright", "Playwright"),
        ("Cypress", "Cypress"),
        ("Python Development Full Stack", "Python Development Full Stack"),
        ("Java Full Stack Development", "Java Full Stack Development"),
        ("MERN Stack", "MERN Stack"),
        ("UI/UX Designing", "UI/UX Designing"),
        ("AI/ML Engineering", "AI/ML Engineering"),
        ("Data Analytics", "Data Analytics"),
        ("Diploma in Software Engineering at Testing", "Diploma in Software Engineering at Testing"),
        ("Diploma in Software Engineering at Development", "Diploma in Software Engineering at Development"),
        ("Other", "Other"),
    ]
    course_enquiry = models.CharField(max_length=255, choices=COURSE_CHOICES)

    TRAINING_MODE_CHOICES = [("Offline", "Offline"), ("Online", "Online"), ("Hybrid", "Hybrid")]
    training_mode = models.CharField(max_length=20, choices=TRAINING_MODE_CHOICES)

    TRAINING_TIMING_CHOICES = [
        ("Morning (7AM Batch)", "Morning (7AM Batch)"),
        ("Evening (8PM Batch)", "Evening (8PM Batch)"),
        ("Anytime in Weekdays", "Anytime in Weekdays"),
        ("Weekends", "Weekends"),
    ]
    training_timing = models.CharField(max_length=50, choices=TRAINING_TIMING_CHOICES)

    START_TIME_CHOICES = [
        ("Immediate", "Immediate"),
        ("After 10 days", "After 10 days"),
        ("After 15 days", "After 15 days"),
        ("After 1 Month", "After 1 Month"),
    ]
    start_time = models.CharField(max_length=50, choices=START_TIME_CHOICES, default="Immediate")

    PROFESSIONAL_SITUATION_CHOICES = [
        ("Fresher", "Fresher"),
        ("Currently Working", "Currently Working"),
        ("Willing to Switch from Another Domain", "Willing to Switch from Another Domain"),
        ("Other", "Other"),
    ]
    professional_situation = models.CharField(max_length=100, choices=PROFESSIONAL_SITUATION_CHOICES)

    QUALIFICATION_CHOICES = [
        ("Diploma", "Diploma"),
        ("Bachelor's Degree", "Bachelor's Degree"),
        ("Master's Degree", "Master's Degree"),
        ("Other", "Other"),
    ]
    qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES)

    EXPERIENCE_CHOICES = [
        ("Less than 1 Year or Fresher", "Less than 1 Year or Fresher"),
        ("1-3 Years", "1-3 Years"),
        ("3-5 Years", "3-5 Years"),
        ("5+ Years", "5+ Years"),
    ]
    experience = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES)

    REFERRAL_CHOICES = [
        ("Instagram", "Instagram"),
        ("WhatsApp Channel", "WhatsApp Channel"),
        ("Facebook", "Facebook"),
        ("LinkedIn", "LinkedIn"),
        ("YouTube", "YouTube"),
        ("Friend Reference", "Friend Reference"),
        ("College Reference", "College Reference"),
        ("Other Social Network", "Other Social Network"),
    ]
    referral_source = models.CharField(max_length=100, choices=REFERRAL_CHOICES)

    consent_to_contact = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Student Enquiries"

    def __str__(self):
        return f"{self.name} - {self.course_enquiry}"


# -------------------- EnquiryList --------------------
class EnquiryList(models.Model):
    student_enquiry = models.ForeignKey(StudentEnquiry, related_name='enquiry_list', on_delete=models.CASCADE, null=True, blank=True)
    subject_module = models.CharField(max_length=255)
    training_mode = models.CharField(max_length=20)
    training_timing = models.CharField(max_length=50)
    start_time = models.CharField(max_length=50)
    calling1 = models.CharField(max_length=255, blank=True, null=True)
    calling2 = models.CharField(max_length=255, blank=True, null=True)
    calling3 = models.CharField(max_length=255, blank=True, null=True)
    calling4 = models.CharField(max_length=255, blank=True, null=True)
    calling5 = models.CharField(max_length=255, blank=True, null=True)
    move_to_demo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Enquiry Lists"

    def __str__(self):
        return f"Enquiry List for {self.student_enquiry.name if self.student_enquiry else 'N/A'}"


# -------------------- DemoList --------------------
class DemoList(models.Model):
    student_enquiry = models.ForeignKey(StudentEnquiry, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100, validators=[validate_name])
    phone_number = models.CharField(max_length=10, validators=[validate_phone_number])
    email = models.EmailField(validators=[validate_gmail_email])

    package_code = models.CharField(max_length=20)
    package = models.CharField(max_length=100)

    DEMO_STATUS_CHOICES = [
        ('Not yet started', 'Not yet started'),
        ('In progress', 'In progress'),
        ('Completed', 'Completed'),
    ]
    demo_class_status = models.CharField(max_length=20, choices=DEMO_STATUS_CHOICES, default='Not yet started')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Demo Lists"

    def __str__(self):
        return self.full_name


# -------------------- Course and Batch Timing --------------------
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users_course"

    def __str__(self):
        return self.name


class BatchTiming(models.Model):
    name = models.CharField(max_length=50)
    time_range = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batch_timings')

    class Meta:
        db_table = "users_batch_timings"

    def __str__(self):
        return f"{self.name} ({self.time_range})"


# -------------------- Final Enquiry Model --------------------
class Enquiry(models.Model):
    # Basic Info
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    current_location = models.CharField(max_length=100, blank=True, null=True)
    module = models.CharField(max_length=100, blank=True, null=True)
    timing = models.CharField(max_length=50, blank=True, null=True)
    trainingTime = models.CharField(max_length=50, blank=True, null=True)
    startTime = models.CharField(max_length=50, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=100, blank=True, null=True)
    experience = models.CharField(max_length=50, blank=True, null=True)
    referral = models.CharField(max_length=100, blank=True, null=True)
    consent = models.BooleanField(default=False)

    # Enquiry Details
    calling1 = models.CharField(max_length=50, blank=True, null=True)
    calling2 = models.CharField(max_length=50, blank=True, null=True)
    calling3 = models.CharField(max_length=50, blank=True, null=True)
    calling4 = models.CharField(max_length=50, blank=True, null=True)
    calling5 = models.CharField(max_length=50, blank=True, null=True)
    previous_interaction = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default='new')

    # Demo/Batch/Accounts
    batch_code = models.CharField(max_length=50, blank=True, null=True)
    batch_subject = models.CharField(max_length=100, blank=True, null=True)
    demo_class_status = models.CharField(max_length=50, blank=True, null=True)
    move_to_demo = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True, null=True)
    move_to_acc = models.BooleanField(default=False)
    
    #demolist1
    move_to_class = models.BooleanField(default=False)
    packageCost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amountPaid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balanceAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    #classList
    pay_calling1 = models.TextField(blank=True, null=True)
    pay_calling2 = models.TextField(blank=True, null=True)
    pay_calling3 = models.TextField(blank=True, null=True)
    pay_calling4 = models.TextField(blank=True, null=True)
    pay_calling5 = models.TextField(blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    move_to_hr = models.BooleanField(default=False)


    # HR/Placement/Interview
    #class_list1
    follow_up_note = models.TextField(blank=True, null=True)
    placement = models.CharField(max_length=20, blank=True, null=True)
    data_link = models.URLField(max_length=500, blank=True, null=True)
    data_updated = models.DateField(blank=True, null=True)
    move_to_placements = models.BooleanField(default=False)
    
    #placements_list
    placement_status = models.CharField(max_length=50, blank=True, null=True)
    placement_notes = models.TextField(blank=True, null=True)
    interview_status = models.CharField(max_length=50, blank=True, null=True)
    interview_notes = models.TextField(blank=True, null=True)
    
    #interviewlist 

    # System
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

# -------------------- Student Placement Model --------------------
class StudentPlacement(models.Model):
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    course = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    fresher = models.BooleanField(default=False)
    total_experience = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    relevant_experience = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    highest_degree = models.CharField(max_length=255, blank=True, null=True)
    major = models.CharField(max_length=255, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    edu_start = models.DateField(blank=True, null=True)
    edu_end = models.DateField(blank=True, null=True)
    edu_grade = models.CharField(max_length=50, blank=True, null=True)
    edu_ongoing = models.BooleanField(default=False)

    # Pre-University
    pre_uni_school = models.CharField(max_length=255, blank=True, null=True)
    pre_uni_place = models.CharField(max_length=255, blank=True, null=True)
    pre_uni_start = models.DateField(blank=True, null=True)
    pre_uni_end = models.DateField(blank=True, null=True)
    pre_uni_grade = models.CharField(max_length=50, blank=True, null=True)

    # High School
    high_school = models.CharField(max_length=255, blank=True, null=True)
    high_school_place = models.CharField(max_length=255, blank=True, null=True)
    high_school_start = models.DateField(blank=True, null=True)
    high_school_end = models.DateField(blank=True, null=True)
    high_school_grade = models.CharField(max_length=50, blank=True, null=True)

    # Location and work details
    location_current = models.CharField(max_length=255, blank=True, null=True)
    location_preferred = models.CharField(max_length=255, blank=True, null=True)
    currently_working = models.CharField(max_length=10, blank=True, null=True)
    notice_period = models.CharField(max_length=20, blank=True, null=True)
    current_ctc = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    expected_ctc = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    skills = models.TextField(blank=True, null=True)
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Experience(models.Model):
    student = models.ForeignKey(StudentPlacement, related_name="experiences", on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    employer = models.CharField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    ongoing = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.job_title} ({self.student.full_name})"


