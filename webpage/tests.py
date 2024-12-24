from django.test import TestCase, Client
from django.urls import reverse
from .models import add_event, user_account
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.contrib.auth.models import User


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.teacher = self.User.objects.create_user(
            username="teacher", password="teacherpass", studentid='T001',
            first_name='teacher test', is_staff=True
        )
        self.student = self.User.objects.create_user(
            username="student", password="studentpass", studentid='01057064',
            first_name='student test', is_staff=False
        )
        self.event = add_event.objects.create(
            title="Test Event",
            description="This is a test event.",
            venue="Test Venue",
            event_date=make_aware(datetime(2024, 12, 25)),
            registration_deadline=make_aware(datetime(2024, 12, 24)),
            user=self.teacher,
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        )



class UserAuthTestCase(BaseTestCase):
    def test_login(self):
        """
        測試用戶是否能成功登入。
        """
        response = self.client.post(reverse("login"), {
            "username": "teacher",
            "password": "teacherpass",
        })
        self.assertEqual(response.status_code, 302)  # 重定向到首頁
        self.assertRedirects(response, reverse("get_main_page"))

    def test_register(self):
        """
        測試用戶註冊功能。
        """
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "newuserpass123",
            "password2": "newuserpass123",
            "identity": "student",
            "first_name": 'usertest',
            "studentid":"00000000",
        })
        self.assertEqual(response.status_code, 302)  # 重定向到登入頁面
        self.assertTrue(self.User.objects.filter(username="newuser").exists())


class EventManagementTestCase(BaseTestCase):
    def test_participate_event(self):
        """
        測試用戶參加活動功能。
        """
        self.client.login(username="student", password="studentpass")
        response = self.client.post(reverse("participate_event", args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("您已成功報名此活動！", response.json()["message"])
        self.assertTrue(self.event.participants.filter(id=self.student.id).exists())

    def test_cancel_registration(self):
        """
        測試取消報名功能。
        """
        self.event.participants.add(self.student)  # 預先模擬參加活動
        self.client.login(username="student", password="studentpass")
        response = self.client.post(reverse("cancel_registration", args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("取消報名成功", response.json()["message"])
        self.assertFalse(self.event.participants.filter(id=self.student.id).exists())

    def test_edit_event(self):
        """
        測試編輯活動功能。
        """
        self.client.login(username="teacher", password="teacherpass")
        response = self.client.post(reverse("edit_event", args=[self.event.id]), {
            "title": "Updated Event Title",
            "description": self.event.description,
            "venue": self.event.venue,
            "event_date": self.event.event_date,
            "registration_deadline": self.event.registration_deadline,
        })
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Updated Event Title")

    def test_delete_event(self):
        """
        測試刪除活動功能。
        """
        self.client.login(username="teacher", password="teacherpass")
        response = self.client.post(reverse("delete_event", args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("活動已成功刪除。", response.json()["message"])
        self.assertFalse(add_event.objects.filter(id=self.event.id).exists())


class ProfileManagementTestCase(BaseTestCase):
    def test_profile_edit(self):
        """
        測試編輯個人資料功能。
        """
        self.client.login(username="teacher", password="teacherpass")

        # Perform the POST request with the updated data
        response = self.client.post(reverse("profile_edit"), {
            "username":"teacher",
            "first_name": "Updated Teacher Name",
            "studentid": "T002",
        })

        # Ensure the response status is correct
        self.assertEqual(response.status_code, 302)

        # Fetch the user object directly from the database
        updated_user = user_account.objects.get(username="teacher")  # Adjust if your user model is named differently

        # Check if the fields were updated correctly
        self.assertEqual(updated_user.first_name, "Updated Teacher Name")
        self.assertEqual(updated_user.studentid, "T002")


    def test_password_edit(self):
        """
        測試修改密碼功能。
        """
        self.client.login(username="teacher", password="teacherpass")
        response = self.client.post(reverse("password_edit"), {
            "old_password": "teacherpass",
            "new_password1": "newteacherpass",
            "new_password2": "newteacherpass",
        })
        self.assertEqual(response.status_code, 302)
        self.teacher.refresh_from_db()
        self.assertTrue(self.teacher.check_password("newteacherpass"))


class SearchEventTestCase(BaseTestCase):
    def test_search_event(self):
        """
        測試活動搜索功能。
        """
        response = self.client.get(reverse("get_main_page"), {"search": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")
        response_no_match = self.client.get(reverse("get_main_page"), {"search": "NoMatch"})
        self.assertNotContains(response_no_match, "Test Event")
