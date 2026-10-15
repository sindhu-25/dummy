from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Profile




# ---------------- SIGN UP ----------------
def sign_up(request):

    if request.method == "POST":

        username = request.POST["username"]

        # Check whether username already exists
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "sign-up.html",
                {
                    "error": "Username already exists. Please choose a different one."
                }
            )

        # Create user
        user = User.objects.create_user(
            username=username,
            password=request.POST["password"]
        )

        # Create profile
        Profile.objects.create(
            Name=request.POST["Name"],
            user=user,
            phone_no=request.POST["phone_no"],
            country=request.POST["Country"]
        )

        return redirect("login")

    return render(request, "signup.html")


def login(request):
    if request.method=="POST":
        user=authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            auth_login(request,user)
            return redirect("dashboard")
        else:
            return render(request,"login.html",{"error":"invalid username or password"})

    return render(request,"login.html")

@login_required
def dashboard(request):
    return render(request,"dashboard.html")

@login_required
def logout(request):
    auth_logout(request)
    return redirect("login")


from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Student
from .serializer import StudentSerializer
from rest_framework import status

from .pagination import StudentPagination

from rest_framework.decorators import (
    api_view,
    permission_classes
)


from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser



@api_view(['GET'])
@permission_classes([IsAdminUser])
def student_list(request):

    students = Student.objects.all()

    paginator = StudentPagination()

    paginated_students = paginator.paginate_queryset(
        students,
        request
    )

    serializer = StudentSerializer(
        paginated_students,
        many=True
    )

    return paginator.get_paginated_response(
        serializer.data
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def student_detail(request,id):
    student = Student.objects.get(id=id)
    serializer = StudentSerializer(student,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def student_add(request):
    serializer = StudentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['PUT'])
def student_update(request,id):
    student = Student.objects.get(id=id)
    serializer = StudentSerializer(
        instance=student,
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['PATCH'])
def student_partial_update(request,id):
    student = Student.objects.get( id=id)
    serializer = StudentSerializer(
        instance=student,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
def student_delete(request,id):
    student = Student.objects.get(id=id)
    student.delete()
    return Response(
        {'message': 'Student deleted successfully'},
        status=status.HTTP_204_NO_CONTENT
    )