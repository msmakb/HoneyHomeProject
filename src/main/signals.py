from django.contrib.auth.models import Group, User
from human_resources.models import Employee
from .models import Person

def createGroups(**kwargs):
    """
    This function creates all groups after migrating all database models
    """
    if not Group.objects.all().exists():
        GROUPS = (
        'Accounting Manager',
        'Admin',
        'CEO',
        'Designer',
        'Distributor',
        'Human Resources',
        'Social Media Manager',
        'Warehouse Admin',
        )

        Person.objects.create(name="CEO")
        person = Person.objects.all()[0]
        User.objects.create_superuser(
            username=person.name,
            password=person.name,
            ).save()
        super_user = User.objects.all()[0]
        Employee.objects.create(person=person, account=super_user, position="CEO")
        print(f"  Super User '{super_user.username}' was created.")

        for name in GROUPS:
            group = Group.objects.create(name=name)
            print(f"  {group} group was created.")

            if name == 'CEO':
                group.user_set.add(super_user)
                print(f"  The super user added to {name} group.")
