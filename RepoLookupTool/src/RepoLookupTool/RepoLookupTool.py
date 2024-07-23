from azure.devops.connection import Connection 
from msrest.authentication import BasicAuthentication
import json
import pprint

# Fill in with your Azure DevOps personal access token and organization URL
personal_access_token = 'YOUR_PERSONAL_ACCESS_TOKEN'
organization_url = 'https://dev.azure.com/YOUR_ORGANIZATION'

# Create a connection to the Azure DevOps organization
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client for the Git API
git_client = connection.clients.get_git_client()

# Specify the project name
project = 'YOUR_PROJECT_NAME'

# List repositories in the project
repositories = git_client.get_repositories(project)

print("List of repositories in project '{}':".format(project))
repo_list = []
for repo in repositories:
    print(" - {} (id: {})".format(repo.name, repo.id))
    repo_list.append({
        'name': repo.name,
        'id': repo.id
    })

# Query details of a specific repository by name
repo_name = 'YOUR_REPOSITORY_NAME'
repo = next((r for r in repositories if r.name == repo_name), None)

repo_details = {}
if repo:
    print("\nDetails of repository '{}':".format(repo_name))
    repo_details = repo.__dict__
    pprint.pprint(repo.__dict__)
else:
    print("\nRepository '{}' not found.".format(repo_name))
    repo_details = {"error": "Repository not found"}

# Output the results to a JSON file
output_data = {
    "project": project,
    "repositories": repo_list,
    "specific_repo_details": repo_details
}

output_file = 'azure_repo_output.json'
with open(output_file, 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

print(f"\nOutput written to {output_file}")
