import requests
import logging

logging.basicConfig(level=logging.DEBUG)

TOKEN = "<token>"
AUTH_HEADER = {'Authorization': 'Bearer ' + TOKEN}

API_URL = f"https://gitlab.catedras.linti.unlp.edu.ar/api/v4"

GROUP_ID = 123123 # Group of ps 2020
TEMPLATE_PROJECT_ID = 12312312 # Project template id

PROJECT_IDS = [1 ,2 ,3, 4, 5] # List to groups ids to populate

def milestones(project_id):
    path = f"/projects/{project_id}/milestones"
    response = requests.get(API_URL + path, headers=AUTH_HEADER)

    return response.json()


def issues(project_id, milestone_id):
    path = f"/projects/{project_id}/milestones/{milestone_id}/issues"
    response = requests.get(API_URL + path, headers=AUTH_HEADER)

    return response.json()


def build_milestone(data):
    return {
        "title": data["title"],
        "description": data["description"],
        "due_date": data["due_date"],
        "start_date": data["start_date"]
    }


def create_milestone(project_id, milestone_data):
    path = f"/projects/{project_id}/milestones"
    new_milestone = build_milestone(milestone_data)
    print(new_milestone)
    response = requests.post(API_URL + path, json=new_milestone, headers=AUTH_HEADER)
    response.raise_for_status()

    return response.json()["id"]


def build_issue(data):
    return {
        "title": data["title"],
        "description": data["description"],
        "due_date": data["due_date"],
        "labels": data["labels"]
    }

def create_issues(project_id, milestone_id, issues):
    path = f"/projects/{project_id}/issues"
    for issue in sorted(issues, key=lambda elem: elem["iid"]):
        new_issue = build_issue(issue)
        new_issue["milestone_id"] = milestone_id
        response = requests.post(API_URL + path, json=new_issue, headers=AUTH_HEADER)
        response.raise_for_status()


def create_board(project_id, template_board):
    for item in template_board:
        milestone_id = create_milestone(project_id, item['milestone'])
        create_issues(project_id, milestone_id, item['issues'])


template_milestones = milestones(TEMPLATE_PROJECT_ID)

template_board = []
for milestone in sorted(template_milestones, key=lambda elem: elem["iid"]):
    template_issues = issues(TEMPLATE_PROJECT_ID, milestone['id'])
    template_board.append({"milestone": milestone, 'issues': template_issues})
try:
    for project_id in PROJECT_IDS:
        create_board(project_id, template_board)
except Exception as e:
    print(e)
    print("El proceso terminó con error!")
