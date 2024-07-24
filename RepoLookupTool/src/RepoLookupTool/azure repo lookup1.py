from azure.devops.connection import Connection 
from msrest.authentication import BasicAuthentication 
import json
import pprint


# Define a subroutine (function)
def query_repo(access_token,org_url, project_name, repo_name):
    """
    This subroutine populates the repo details for the given repository.
    """
    # Create a connection to the Azure DevOps organization
    credentials = BasicAuthentication('', access_token)
    connection = Connection(base_url=org_url, creds=credentials)

    # Get a client for the Git API
    git_client = connection.clients.get_git_client()


    # List repositories in the project
    repositories = git_client.get_repositories(project_name)
    """
    print("List of repositories in project '{}':".format(project_name))
        repo_list = []
        for repo in repositories:
            print(" - {} (id: {})".format(repo.name, repo.id))
            repo_list.append({
                'name': repo.name,
                'id': repo.id
            })

    """
    
    # Query details of a specific repository by name
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
        "project": project_name,
        "repo_name" : repo_name,
        "specific_repo_details": repo_details
    }

    output_file = 'azure_repo_output.json'
    with open(output_file, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)

    print(f"\nOutput written to {output_file}")



# Define the main method
def main(personal_access_token,organization_url,project_name,repo_name):
    """
    Main method to run the program.
    """
   
    # Call the query_repo subroutine
    query_repo(personal_access_token,organization_url,project_name, repo_name)
    

# Run the main method when thescript is executed
if __name__ == "__main__":
    main()
