import os
import requests
import json
from fastapi import APIRouter, Depends, HTTPException


IS_DEPLOYED = os.getenv("IS_DEPLOYED", "false").lower() == "true"

LINK = os.getenv("API_PREFIX", "empty")

router = APIRouter(prefix="/mockups/users", tags=["Mockup"])

@router.get("/")
def getAll(usertypes=None):
    return get_outside_users([])

@router.get('/{user_type}')
def get_spec_type(user_type: str):
    return get_outside_users([user_type])


def get_outside_users(usertypes: list[str]):
    results=[]
    if IS_DEPLOYED:
        if len(usertypes)!=0:
            for usertype in usertypes:
                response = requests.get(f"{LINK}api/v1/users", params=usertype)
                print(response.url)  # Shows the full URL with query parameters
                print(response.json())
                results.append(response.json())
        else:
            response = requests.get(f"{LINK}api/v1/users")
            print(response.url)  # Shows the full URL with query parameters
            print(response.json())
            results.append(response.json())
    else:
        #mockup from here, VERY low tech (Conner, don't judge me!)
        if len(usertypes)!=0:
            for usertype in usertypes:
                if usertype == "student":
                    for student in student_json:
                      results.append(student)
                elif usertype== "lecturer":
                    for lecturer in lecturer_json:
                      results.append(lecturer)
                elif usertype== "employee":
                    for employee in employee_json:
                      results.append(employee)
        else:
          for student in student_json:
            results.append(student)
          for lecturer in lecturer_json:
            results.append(lecturer)
          for employee in employee_json:
            results.append(employee)
    return results


student_string = """[
  {
    "id": "7720f0c4-9612-42ff-ad06-744e571f6fde",
    "dateOfBirth": "2003-01-01",
    "address": "Some other Address",
    "phoneNumber": "+4915100000048",
    "username": "student_g2_8@test.com",
    "firstName": "FirstNameG2",
    "lastName": "LastName8",
    "email": "student_g2_8@test.com",
    "matriculationNumber": "m_g2_8",
    "degreeProgram": "Business Informatics",
    "semester": 4,
    "studyStatus": "ENROLLED",
    "cohort": "BIN-T23-F1"
  },
  {
    "id": "8a172f8e-cdd1-4dd7-bf9a-914c4dad3da3",
    "dateOfBirth": "2003-01-01",
    "address": "Some other Address",
    "phoneNumber": "+4915100000043",
    "username": "student_g2_3@test.com",
    "firstName": "FirstNameG2",
    "lastName": "LastName3",
    "email": "student_g2_3@test.com",
    "matriculationNumber": "m_g2_3",
    "degreeProgram": "Business Informatics",
    "semester": 4,
    "studyStatus": "ENROLLED",
    "cohort": "BIN-T23-F1"
  },
  {
    "id": "0d0be51d-24ef-4b21-8062-82044aedb482",
    "dateOfBirth": "2002-01-01",
    "address": "Some Address",
    "phoneNumber": "+4915100000015",
    "username": "student_g1_5@test.com",
    "firstName": "FirstNameG1",
    "lastName": "LastName5",
    "email": "student_g1_5@test.com",
    "matriculationNumber": "m_g1_5",
    "degreeProgram": "Computer Science",
    "semester": 2,
    "studyStatus": "ENROLLED",
    "cohort": "BIN-T23-F4"
  }
  ]"""

lecturer_string ="""[
  {
    "id": "7428f350-231c-40d5-b62b-07c4d50108e3",
    "dateOfBirth": "1975-01-01",
    "address": "Lecturer Address",
    "phoneNumber": "+4915100000072",
    "username": "lecturer_2@test.com",
    "firstName": "LecturerFirstName",
    "lastName": "LastName2",
    "email": "lecturer_2@test.com",
    "employeeNumber": "L-002",
    "department": "IT",
    "officeNumber": "C2",
    "workingTimeModel": "FULL_TIME",
    "fieldChair": "Field 2",
    "title": "Prof. Dr.",
    "employmentStatus": "FULL_TIME_PERMANENT"
  },
  {
    "id": "f5534e30-bbe0-429d-810a-92ba7b667521",
    "dateOfBirth": "1975-01-01",
    "address": "Lecturer Address",
    "phoneNumber": "+4915100000071",
    "username": "lecturer_1@test.com",
    "firstName": "LecturerFirstName",
    "lastName": "LastName1",
    "email": "lecturer_1@test.com",
    "employeeNumber": "L-001",
    "department": "IT",
    "officeNumber": "C1",
    "workingTimeModel": "FULL_TIME",
    "fieldChair": "Field 1",
    "title": "Prof. Dr.",
    "employmentStatus": "FULL_TIME_PERMANENT"
  },
  {
    "id": "af98937b-14e1-4350-83d5-9c95256174f4",
    "dateOfBirth": "1975-01-01",
    "address": "Lecturer Address",
    "phoneNumber": "+4915100000074",
    "username": "lecturer_4@test.com",
    "firstName": "LecturerFirstName",
    "lastName": "LastName4",
    "email": "lecturer_4@test.com",
    "employeeNumber": "L-004",
    "department": "IT",
    "officeNumber": "C4",
    "workingTimeModel": "FULL_TIME",
    "fieldChair": "Field 4",
    "title": "Prof. Dr.",
    "employmentStatus": "FULL_TIME_PERMANENT"
  }
  ]"""

employee_string = """[
  {
    "id": "4f6bf355-6a63-45c5-8839-2f4b571cb478",
    "dateOfBirth": "1990-01-01",
    "address": "Test Address 3",
    "phoneNumber": "1122334455",
    "username": "test-sau-admin@sau-portal.de",
    "firstName": "Test",
    "lastName": "SAU-Admin",
    "email": "test-sau-admin@sau-portal.de",
    "employeeNumber": "E123",
    "department": "SAU",
    "officeNumber": "A101",
    "workingTimeModel": "FULL_TIME"
  },
  {
    "id": "471fb05c-e3c5-4bd1-9c41-dc355885811c",
    "dateOfBirth": "1985-01-01",
    "address": "Test Address 4",
    "phoneNumber": "5566778899",
    "username": "test-hochschulverwaltung@sau-portal.de",
    "firstName": "Test",
    "lastName": "Hochschulverwaltung",
    "email": "test-hochschulverwaltung@sau-portal.de",
    "employeeNumber": "E124",
    "department": "Administration",
    "officeNumber": "B202",
    "workingTimeModel": "PART_TIME"
  },
  {
    "id": "7428f350-231c-40d5-b62b-07c4d50108e3",
    "dateOfBirth": "1975-01-01",
    "address": "Lecturer Address",
    "phoneNumber": "+4915100000072",
    "username": "lecturer_2@test.com",
    "firstName": "LecturerFirstName",
    "lastName": "LastName2",
    "email": "lecturer_2@test.com",
    "employeeNumber": "L-002",
    "department": "IT",
    "officeNumber": "C2",
    "workingTimeModel": "FULL_TIME",
    "fieldChair": "Field 2",
    "title": "Prof. Dr.",
    "employmentStatus": "FULL_TIME_PERMANENT"
  }
  ]"""
employee_json=json.loads(employee_string)
lecturer_json=json.loads(lecturer_string)
student_json=json.loads(student_string)

