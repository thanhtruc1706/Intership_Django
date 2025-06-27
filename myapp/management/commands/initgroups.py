from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from myapp.models import Post

class Command(BaseCommand):
    help = 'Tạo các nhóm quyền: admin, editor, user'

    def handle(self, *args, **kwargs):
        # Nhóm admin: toàn quyền
        admin_group, created = Group.objects.get_or_create(name='admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Tạo nhóm admin'))
        # Gán tất cả quyền cho admin
        for perm in Permission.objects.all():
            admin_group.permissions.add(perm)

        # Nhóm editor: chỉ thêm/sửa/xóa bài viết của mình
        editor_group, created = Group.objects.get_or_create(name='editor')
        if created:
            self.stdout.write(self.style.SUCCESS('Tạo nhóm editor'))
        post_ct = ContentType.objects.get_for_model(Post)
        perms = Permission.objects.filter(content_type=post_ct, codename__in=['add_post', 'change_post', 'delete_post'])
        for perm in perms:
            editor_group.permissions.add(perm)

        # Nhóm user: chỉ xem
        user_group, created = Group.objects.get_or_create(name='user')
        if created:
            self.stdout.write(self.style.SUCCESS('Tạo nhóm user'))
        # Không gán quyền gì cho user (chỉ xem)

        self.stdout.write(self.style.SUCCESS('Đã tạo/cập nhật các nhóm quyền!')) 