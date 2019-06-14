def flattenTasks(item, userData):
    userData.tasks = []
    for task in item.tasks:
        task.project_name = item.name
        userData.tasks.append(task)
    return userData
