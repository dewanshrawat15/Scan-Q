from django.db import models

class extended_user(models.Model):
	user_code = models.CharField(max_length=6, null=True)
	teacher = models.NullBooleanField()

	def __str__(self):
		return self.user_code

class teacher_user(models.Model):
	class_name = models.CharField(max_length=64, null=True)
	subject_name = models.CharField(max_length=64, null=True)
	teacher_code = models.PositiveIntegerField(null=True)
	count = models.PositiveIntegerField(null=True)
	lectures = models.PositiveIntegerField(default=1, null=True)
	sha_digest = models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.subject_name

class student_list(models.Model):
	student_code = models.PositiveIntegerField(null=True)
	subject = models.CharField(max_length=64, null=True)
	attendance = models.PositiveIntegerField(null=True)
	digest = models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.student_code