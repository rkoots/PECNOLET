from django.contrib.auth.models import User

# Define user attributes
username = 'a'
email = 'your_email@example.com'
password = 'a'
first_name = 'Raj'
last_name = 'Kumar'

# Create the superuser
user = User.objects.create_superuser(
    username=username,
    email=email,
    password=password
)

# Set additional attributes
user.first_name = first_name
user.last_name = last_name
user.save()

print(f'Superuser {username} created successfully.')
