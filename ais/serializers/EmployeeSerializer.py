from rest_framework import serializers


class EmployeeSerializer(serializers.Serializer):
    id_employee = serializers.CharField(read_only=True)
    empl_surname = serializers.CharField(max_length=50)
    empl_name = serializers.CharField(max_length=50)
    empl_patronymic = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    empl_role = serializers.ChoiceField(choices=["Касир", "Менеджер"])
    salary = serializers.DecimalField(max_digits=13, decimal_places=4)
    date_of_birth = serializers.DateField()
    date_of_start = serializers.DateField()
    phone_number = serializers.CharField(max_length=13)
    city = serializers.CharField(max_length=50)
    street = serializers.CharField(max_length=50)
    zip_code = serializers.CharField(max_length=9)
    password = serializers.CharField(write_only=True, required=False)
