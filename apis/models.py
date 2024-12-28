from django.db import models

class AndroidApp(models.Model):
    version = models.CharField(max_length=20, help_text="Version of the Android app (e.g., 1.0.0)")
    apk_file = models.FileField(upload_to="apk_files/", help_text="Upload the APK file", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.version}"