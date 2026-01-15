from core.models import PilotInquiry

def create_pilot_inquiry(name: str, email: str, company_name: str = None, message: str = None) -> PilotInquiry:
    """
    Business logic for creating a pilot inquiry.
    In the future, this could trigger emails, notifications, etc.
    """
    inquiry = PilotInquiry.objects.create(
        name=name,
        email=email,
        company_name=company_name,
        message=message
    )
    return inquiry
