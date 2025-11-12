from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import StudentPlacement,Enquiry
from .serializers import StudentPlacementSerializer
from rest_framework import status, generics,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import EnquirySerializer
from .models import Enquiry, StudentEnquiry, EnquiryList, DemoList,Course, BatchTiming, AccessControl
from .serializers import EnquirySerializer, StudentEnquirySerializer,EnquiryListSerializer, DemoListSerializer,CourseSerializer, BatchTimingSerializer,MinimalEnquirySerializer
from users.permissions import RoleBasedPermission
from rest_framework.decorators import api_view

# -------------------- Auth & User Management --------------------

class SampleView(APIView):
    @swagger_auto_schema(operation_description="GET a sample message")
    def get(self, request):
        return Response({"message": "Success"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=user.username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        role = AccessControl.objects.get(user=user).role

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
            'email': user.email,
            'role': role
        })


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        role = AccessControl.objects.get(user=user).role

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
            'email': user.email,
            'role': role
        })

from .serializers import StudentPlacementSerializer,StudentPlacement

class StudentPlacementCreateView(generics.CreateAPIView):
    queryset = StudentPlacement.objects.all()
    serializer_class = StudentPlacementSerializer
class CreateUserView(APIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    required_roles = ['admin']

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'username', 'password', 'role'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'role': openapi.Schema(type=openapi.TYPE_STRING,
                                       enum=[r[0] for r in AccessControl.USER_ROLES])
            }
        )
    )
    def post(self, request):
        data = request.data
        if User.objects.filter(username=data['username']).exists():
            return Response({'error': 'Username already exists'}, status=400)
        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'Email already exists'}, status=400)

        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        AccessControl.objects.create(user=user, role=data['role'])

        return Response({'email': user.email, 'username': user.username, 'role': data['role']}, status=201)

# -------------------- Enquiry APIs --------------------

class EnquiryListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    required_roles = ['admin', 'counsellor', 'accounts', 'hr']
    serializer_class = EnquirySerializer  #  Always full data

    def get_queryset(self):
        user_role = AccessControl.objects.get(user=self.request.user).role
        if user_role == 'admin':
            return Enquiry.objects.all()
        if user_role == 'accounts':
            return Enquiry.objects.filter(move_to_acc=True)
        if user_role == 'hr':
            return Enquiry.objects.exclude(follow_up_note="")
        return Enquiry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        enquiry = serializer.save(user=self.request.user)
        EnquiryList.objects.create(
            student_enquiry=None,
            subject_module=enquiry.module or '',
            training_mode=enquiry.trainingTime or '',
            training_timing=enquiry.timing or '',
            start_time=enquiry.startTime or '',
        )
class EnquiryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]


# -------------------- StudentEnquiry APIs --------------------

class StudentEnquiryListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = StudentEnquiry.objects.all()
        return Response(StudentEnquirySerializer(data, many=True).data)

    def post(self, request):
        serializer = StudentEnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class StudentEnquiryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        obj = get_object_or_404(StudentEnquiry, pk=pk)
        return Response(StudentEnquirySerializer(obj).data)

    def put(self, request, pk):
        obj = get_object_or_404(StudentEnquiry, pk=pk)
        serializer = StudentEnquirySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        obj = get_object_or_404(StudentEnquiry, pk=pk)
        obj.delete()
        return Response(status=204)


# -------------------- DemoList APIs --------------------

class DemoListListCreate(APIView):
    permission_classes = [IsAuthenticated , RoleBasedPermission]

    def get(self, request):
        data = DemoList.objects.all()
        return Response(DemoListSerializer(data, many=True).data)

    def post(self, request):
        serializer = DemoListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DemoListDetailView(APIView):
    permission_classes = [IsAuthenticated , RoleBasedPermission]

    def get(self, request, pk):
        obj = get_object_or_404(DemoList, pk=pk)
        return Response(DemoListSerializer(obj).data)

    def put(self, request, pk):
        obj = get_object_or_404(DemoList, pk=pk)
        serializer = DemoListSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        obj = get_object_or_404(DemoList, pk=pk)
        obj.delete()
        return Response(status=204)

# -------------------- HRlistAPIview --------------------
class HRListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Enquiry.objects.filter(move_to_hr=True)
        serializer = EnquirySerializer(data, many=True)
        return Response(serializer.data)


# -------------------- Public Views --------------------

class CourseListView(APIView):
    permission_classes = [AllowAny, RoleBasedPermission]

    def get(self, request):
        return Response(CourseSerializer(Course.objects.all(), many=True).data)


class BatchTimingListView(APIView):
    permission_classes = [AllowAny, RoleBasedPermission]

    def get(self, request):
        course_id = request.query_params.get('course_id')
        timings = BatchTiming.objects.filter(course_id=course_id) if course_id else BatchTiming.objects.all()
        return Response(BatchTimingSerializer(timings, many=True).data)

# -------------------- Role Protected Sample Views --------------------
class AdminOnlyView(APIView):
    permission_classes = [RoleBasedPermission]
    required_roles = ['admin']
    def get(self, request): return Response({"message": "Admin access granted"})


class CounsellorOnlyView(APIView):
    permission_classes = [RoleBasedPermission]
    required_roles = ['counsellor']
    def get(self, request): return Response({"message": "Counsellor access granted"})


class AccountsOnlyView(APIView):
    permission_classes = [RoleBasedPermission]
    required_roles = ['accounts']
    def get(self, request): return Response({"message": "Accounts access granted"})


class HROnlyView(APIView):
    permission_classes = [RoleBasedPermission]
    required_roles = ['hr']
    def get(self, request): return Response({"message": "HR access granted"})

@api_view(["GET", "POST", "PUT"])
def student_placement_view(request):
    """
    Handles:
      - GET: Prefill from Enquiry or show saved StudentPlacement
      - POST: Save student submission (create new)
      - PUT: HR updates existing record
    """
    enquiry_id = request.query_params.get("enquiry_id") or request.data.get("enquiry_id")
    if not enquiry_id:
        return Response({"error": "Missing enquiry_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        enquiry = Enquiry.objects.get(id=enquiry_id)
    except Enquiry.DoesNotExist:
        return Response({"error": "Enquiry not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        placement = StudentPlacement.objects.filter(enquiry=enquiry).first()
        if placement:
            serializer = StudentPlacementSerializer(placement)
            return Response({"prefilled": True, "data": serializer.data}, status=200)
        else:
            data = {
                "enquiry": enquiry.id,
                "full_name": enquiry.name,
                "phone": enquiry.phone,
                "email": enquiry.email,
                "course": enquiry.module,
                "location_current": enquiry.current_location,
                "consent": enquiry.consent,
            }
            return Response({"prefilled": False, "data": data}, status=200)
    elif request.method == 'POST':
        serializer = StudentPlacementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == 'PUT':
        placement = StudentPlacement.objects.filter(enquiry=enquiry).first()
        if not placement:
            return Response({"error": "Placement not found"}, status=404)
        serializer = StudentPlacementSerializer(placement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
@api_view(["GET", "POST"])
def create_student_placement(request):
    """
    Handles:
      - GET: Fetch StudentPlacement data by enquiry_id
      - POST: Create new StudentPlacement record
    """
    if request.method == "GET":
        enquiry_id = request.query_params.get("enquiry_id")
        if not enquiry_id:
            return Response({"error": "Missing enquiry_id"}, status=status.HTTP_400_BAD_REQUEST)
        placement = (
            StudentPlacement.objects.filter(enquiry__id=enquiry_id).first()
            or StudentPlacement.objects.filter(id=enquiry_id).first()
        )
        if not placement:
            return Response({"error": "No student placement record found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentPlacementSerializer(placement)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    serializer = StudentPlacementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

