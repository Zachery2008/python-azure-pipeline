from subprocess import Popen, PIPE
import constants
import json
import sys 

def list_build_pipelines():
  """
  List all build pipelines

  az command example: az pipelines list --organization https://dev.azure.com/<org name> --project <project name>
  """
  results = []
  count = 0
  cmd = 'az pipelines list --organization ' +  "https://dev.azure.com/" + constants.ORG_NAME + ' --project ' + '"{}"'.format(constants.PROJECT_NAME)

  try:
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if err:
      raise ValueError(err.decode('utf-8'))
    else:
      pipelines = json.loads(out.decode("utf-8"))

      # Filter info as needed
      for pipeline in pipelines:
        count += 1
        results.append({
          "id": pipeline["id"],
          "name": pipeline["name"],
          "type": pipeline["type"],
          "path": pipeline["path"],
          "url": pipeline["url"],
        })

      print("Build pipelines total: " + str(count))
      return results
  except ValueError as err:
    print("Error: {}".format(err))
    sys.exit()


def list_release_pipelines():
  """
  List all release pipelines

  az command example: az pipelines list --organization https://dev.azure.com/<org name> --project <project name>
  """
  results = []
  count = 0
  cmd = 'az pipelines release definition list --organization ' +  "https://dev.azure.com/" + constants.ORG_NAME + ' --project ' + '"{}"'.format(constants.PROJECT_NAME)

  try:
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if err:
      raise ValueError(err.decode('utf-8'))
    else:
      pipelines = json.loads(out.decode("utf-8"))

      # Filter info as needed
      for pipeline in pipelines:
        count += 1
        results.append({
          "id": pipeline["id"],
          "name": pipeline["name"],
          "path": pipeline["path"],
          "url": pipeline["url"],
        })

      print("Relase pipelines total: " + str(count))
      return results
  except ValueError as err:
    print("Error: {}".format(err))
    sys.exit()


def get_build_pipeline_metadata(id: str):
  """
  Get build pipeline metadata

  az command example: az pipelines show --organization https://dev.azure.com/<org name> --project <project name> --id <pipeline id>

  Args:
    id(str): pipeline id
  """
  cmd = 'az pipelines show --organization ' +  "https://dev.azure.com/" + constants.ORG_NAME + ' --project ' + '"{}"'.format(constants.PROJECT_NAME) + ' --id ' + '"{}"'.format(id)

  try:
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if err:
      raise ValueError(err.decode('utf-8'))
    else:
      pipeline = json.loads(out.decode("utf-8"))

      # Filter info as needed
      return {
        "id": pipeline["id"],
        "name": pipeline["name"],
        "path": pipeline["path"],
        "phases": pipeline["process"]["phases"] if ("phases" in pipeline["process"]) else [],  
        "variableGroups": pipeline["variableGroups"],
      }
  except ValueError as err:
    print("Error: {}".format(err))
    sys.exit()


def get_release_pipeline_metadata(id: str):
  """
  Get release pipeline metadata

  az command example: az pipelines release definition show --organization https://dev.azure.com/<org name> --project <project name> --id <pipeline id>

  Args:
    id(str): pipeline id
  """
  cmd = 'az pipelines release definition show --organization ' +  "https://dev.azure.com/" + constants.ORG_NAME + ' --project ' + '"{}"'.format(constants.PROJECT_NAME) + ' --id ' + '"{}"'.format(id)

  try:
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if err:
      raise ValueError(err.decode('utf-8'))
    else:
      pipeline = json.loads(out.decode("utf-8"))

      # Filter info as needed
      return {
        "environments": pipeline["environments"],
        "id": pipeline["id"],
        "name": pipeline["name"],
        "path": pipeline["path"],
      }
  except ValueError as err:
    print("Error: {}".format(err))
    sys.exit()
