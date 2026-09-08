from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

output = "data/student_services_policy.pdf"

doc = SimpleDocTemplate(
    output,
    pagesize=A4,
    rightMargin=50,
    leftMargin=50,
    topMargin=50,
    bottomMargin=50,
)

styles = getSampleStyleSheet()

title_style = styles["Title"]
title_style.alignment = TA_CENTER

story = []

story.append(
    Paragraph(
        "MediCore University Student Services Policy 2026",
        title_style
    )
)

story.append(Spacer(1, 20))

sections = [
    (
        "STU-15.1 — Student Support Services",
        """MediCore University provides academic and administrative
        support services intended to help students successfully participate
        in university life. Student services may include academic advising,
        career guidance, library assistance, accessibility support, financial
        guidance, and general administrative assistance."""
    ),
    (
        "STU-15.2 — Academic Advising",
        """Students may consult their academic advisor regarding course
        selection, academic progression, examination requirements, attendance
        concerns, graduation planning, and other academic matters. Students
        remain responsible for verifying their own registration and academic
        records."""
    ),
    (
        "STU-15.3 — Student Records",
        """Students may request access to academic records through the
        designated University procedure. Requests must contain sufficient
        information for the University to identify the relevant student
        record. Corrections to records may be requested when a student
        identifies a possible administrative error."""
    ),
    (
        "STU-15.4 — Identity Verification",
        """Certain student services may require identity verification before
        information is disclosed or an administrative request is processed.
        University personnel should use reasonable procedures to protect
        student information from unauthorized access."""
    ),
    (
        "STU-15.5 — Library Services",
        """Students with valid University enrollment may use library
        facilities subject to library rules. Borrowed materials must be
        returned within the applicable borrowing period. Students may be
        responsible for replacement costs or other charges arising from
        lost or seriously damaged materials."""
    ),
    (
        "STU-15.6 — Career Services",
        """The Career Services Office may provide assistance with career
        planning, resume preparation, interview preparation, employer
        events, internships, and placement-related activities. Participation
        in a career service does not guarantee employment or placement."""
    ),
    (
        "STU-15.7 — Student Complaints",
        """Students may submit complaints regarding academic administration,
        facilities, student services, or other University matters through
        the designated complaint procedure. Complaints should contain
        sufficient information to allow the University to understand and
        investigate the issue."""
    ),
    (
        "STU-15.8 — Complaint Review",
        """The receiving office may request additional information before
        reviewing a complaint. Where a complaint concerns another University
        office, the matter may be forwarded to an appropriate administrative
        authority."""
    ),
    (
        "STU-15.9 — Accessibility Support",
        """Students who require approved accessibility support may contact
        the designated University office. Support arrangements should be
        based on documented requirements and reasonable institutional
        procedures."""
    ),
    (
        "STU-15.10 — Emergency Student Assistance",
        """Students experiencing an urgent administrative or academic
        difficulty should contact the appropriate University office as soon
        as reasonably possible. Emergency assistance is subject to
        verification and availability of appropriate University resources."""
    ),
    (
        "STU-15.11 — Communication",
        """Official student-service communications may be delivered through
        University email, student portals, notices, or other authorized
        channels. Students are responsible for checking official
        communications relevant to their academic and administrative
        responsibilities."""
    ),
    (
        "STU-15.12 — Service Requests",
        """Student-service requests should be submitted using the procedure
        specified by the responsible office. Requests submitted through
        unofficial channels may not be processed until they are submitted
        through the appropriate system."""
    ),
    (
        "STU-15.13 — Processing Times",
        """Processing times vary depending on the type and complexity of a
        request. A standard processing period does not guarantee completion
        by a particular date when additional verification or information is
        required."""
    ),
    (
        "STU-15.14 — Privacy",
        """Student-service personnel should handle personal and academic
        information responsibly. Information should be accessed or
        disclosed only when required for legitimate University functions
        or when otherwise authorized."""
    ),
    (
        "STU-15.15 — Service Eligibility",
        """Eligibility for a particular student service may depend on
        enrollment status, academic status, documentation, deadlines, or
        other requirements established by the responsible University office."""
    ),
    (
        "STU-15.16 — Appeals",
        """Where a student-service decision includes an appeal mechanism,
        the student may submit an appeal according to the applicable
        procedure. Appeals should identify the decision being challenged
        and provide relevant supporting information."""
    ),
    (
        "STU-15.17 — Interpretation",
        """Questions regarding interpretation of this policy should be
        directed to the responsible student-services authority. More
        specific University regulations may take precedence where they
        directly govern a particular student-service matter."""
    ),
]

for heading, body in sections:
    story.append(
        Paragraph(
            f"<b>{heading}</b>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 6))

    story.append(
        Paragraph(
            body,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 12))

doc.build(story)

print(f"Created: {output}")