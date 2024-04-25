from django.shortcuts import render, redirect
from docker import DockerClient
from .models import DockerContainer

def monitor_docker_containers(request):
    # Connect to the Docker daemon
    docker_client = DockerClient.from_env()

    # Get all Docker containers from the model
    docker_containers = DockerContainer.objects.all()


    # Iterate over each Docker container
    for container in docker_containers:
        try:
            # Get the Docker container by its ID
            docker_container = docker_client.containers.get(container.container_id)
            
            # Get the status of the container
            container.status = docker_container.status
            container.logs = docker_container.logs(tail=50, timestamps=True).decode('utf-8')
            container.save()
            
        except Exception as e:
            # Handle exceptions, for example if the container does not exist
            print(f"Error getting status for container {container.name}: {e}")

    if request.method == 'POST':
        # If the request is a POST request, handle the start/stop action
        action = request.POST.get('action')
        container_id = request.POST.get('container_id')
        
        try:
            # Get the Docker container by its ID
            docker_container = docker_client.containers.get(container_id)

            if action == 'start':
                # Start the container
                docker_container.start()
            elif action == 'stop':
                # Stop the container
                docker_container.stop()

            # Redirect back to the monitor page after performing the action
            return redirect('monitor_docker_containers')
            
        except Exception as e:
            # Handle exceptions, for example if the container does not exist
            print(f"Error performing action for container {container_id}: {e}")

    # Render the monitor template with the Docker containers
    return render(request, 'monitor.html', {'docker_containers': docker_containers})
