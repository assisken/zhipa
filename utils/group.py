from datetime import datetime


def course(group_name: str) -> int:
    year = int(group_name.split('-')[-1])  # Get year from name of group
    now = datetime.now()
    course = now.year % 100 - year
    if now.month >= 9:  # Study time starts from September. So course must be increased
        course += 1
    return course
