from django.apps import apps
from django.test import TestCase
from django.urls import reverse
from funcy import compose, first, partial, where
from parameterized import parameterized

from containers.models import Container

Student = apps.get_model(app_label="main", model_name="Student")
Group = apps.get_model(app_label="schedule", model_name="Group")
Teacher = apps.get_model(app_label="schedule", model_name="Teacher")
Subject = apps.get_model(app_label="schedule", model_name="Schedule")


def get_student(student):
    return {
        "id": 1,
        "firstname": student.firstname,
        "middlename": student.middlename,
        "lastname": student.lastname,
        "group": student.group_id,
    }


def get_group(group):
    return {
        "id": 1,
        "name": group.name,
        "students": list(group.student_set.all().values_list("pk", flat=True)),
        "subjects": list(group.schedule_set.all().values_list("pk", flat=True)),
    }


def get_teacher(teacher):
    return {
        "id": 1,
        "firstname": teacher.firstname,
        "middlename": teacher.middlename,
        "lastname": teacher.lastname,
    }


def get_subject(subject):
    return {
        "id": 1,
        "name": subject.name,
        "teachers": list(subject.teachers.all().values_list("pk", flat=True)),
        "group": subject.group.pk,
    }


def get_container(container):
    return {
        "id": 1,
        "name": container.name,
        "group": container.group.id,
        "do_not_remove": False,
        "cores": container.cores,
        "memory_gb": container.memory_gb,
        "partition_size_gb": container.partition_size_gb,
    }


class TestVzhipaEndpoints(TestCase):
    fixtures = ["zhipa_api.json"]

    @parameterized.expand(
        [
            (
                reverse("api-v1:students"),
                Student,
                get_student,
                compose(first, partial(where, id=1)),
            ),
            (
                reverse("api-v1:groups"),
                Group,
                get_group,
                compose(first, partial(where, id=1)),
            ),
            (
                reverse("api-v1:teachers"),
                Teacher,
                get_teacher,
                compose(first, partial(where, id=1)),
            ),
            (
                reverse("api-v1:subjects"),
                Subject,
                get_subject,
                compose(first, partial(where, id=1)),
            ),
            (
                reverse("api-v1:containers"),
                Container,
                get_container,
                compose(first, partial(where, id=1)),
            ),
            (
                reverse("api-v1:students", kwargs={"pk": 1}),
                Student,
                get_student,
                lambda student: student,
            ),
            (
                reverse("api-v1:groups", kwargs={"pk": 1}),
                Group,
                get_group,
                lambda group: group,
            ),
            (
                reverse("api-v1:teachers", kwargs={"pk": 1}),
                Teacher,
                get_teacher,
                lambda teacher: teacher,
            ),
            (
                reverse("api-v1:subjects", kwargs={"pk": 1}),
                Subject,
                get_subject,
                lambda subject: subject,
            ),
            (
                reverse("api-v1:containers", kwargs={"pk": 1}),
                Container,
                get_container,
                lambda container: container,
            ),
        ]
    )
    def test_api_is_available(self, url, model, item_getter, retrieve):
        expected_item = item_getter(model.objects.get(id=1))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_item = retrieve(response.json())
        self.assertEqual(response_item, expected_item)
