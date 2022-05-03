from utils import azure_pipeline
import csv, json

def get_build_pipeline_summary():
  
  results = []
  build_pipeline_dict = {}
  
  # Get all build pipelines
  build_pipelines = azure_pipeline.list_build_pipelines()

  if not build_pipelines:
    print("No build pipelines found")
    return None
    
  # Loop through all build pipelines
  for pipeline in build_pipelines:
    pipeline_detail = azure_pipeline.get_build_pipeline_metadata(pipeline["id"])
    
    # Check that pipeline imports variables groups containing "artifactory-repo-host"
    if (not pipeline_detail) or (not pipeline_detail["variableGroups"]):
      continue
    
    for variable_group in pipeline_detail["variableGroups"]:
      if "artifactory-repo-host" in variable_group:
        # Loop through phases
        for phase in pipeline_detail["phases"]:
          for step in phase["steps'"]:
            if "task" in step and step["task"]["definitionType"] == "task" and json.dumps(step).find("artifactory") != -1:
              
              if not pipeline["id"] in build_pipeline_dict:
                results.append({
                  "name": pipeline["name"],
                  "id": pipeline["id"],
                  "url": pipeline["url"],
                  "path": pipeline["path"],
                  "stage": "build pipeline",
                })
                
                build_pipeline_dict[pipeline["id"]] = pipeline["name"]
  return results
    
    
def get_release_pipeline_summary():  

  results = []
  release_pipeline_dict = {}
  
  # Get all release pipelines
  release_pipelines = azure_pipeline.list_release_pipelines()
  
  if not release_pipelines:
    print("No release pipelines found")
    return None
  
  # Loop through all release pipelines
  for pipeline in release_pipelines:
    pipeline_detail = azure_pipeline.get_release_pipeline_metadata(pipeline["id"])
    
    for environment in pipeline_detail["environments"]:
      for phase in environment["deployPhases"]:
        if not "workflowTasks" in phase:
          continue
        
        for task in phase["workflowTasks"]:
          if task["definitionType"] == "task" and json.dumps(task).find("artifactory") != -1:
            if not pipeline["id"] in release_pipeline_dict:
              results.append({
                "name": pipeline["name"],
                "id": pipeline["id"],
                "url": pipeline["url"],
                "path": pipeline["path"],
                "stage": "release pipeline",
              })
              
              release_pipeline_dict[pipeline["id"]] = pipeline["name"]
  return results


def main():
  
  build_results = get_build_pipeline_summary()
  release_results = get_release_pipeline_summary()
  
  build_results.extend(release_results)
  
  keys = ["name", "id", "url", "path", "stage"]
  with open("results.csv", "w") as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(build_results)


main()
