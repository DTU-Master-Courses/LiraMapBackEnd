# Deployment to the vm
In this section we assume that the user has installed the following programs:
    Open VPN (for database access)
    GitHub (for obtaining the repositories)
    GitBash (for the scp commands and connection to the vm)

As a quick overview we first need to run OpenVPN. Then in WSL we First build the front-end and then run the back-end to have the full system running and accessible. For this we have to go through the following steps:
## setup 
- Ensure that both the front- and back-end repositories are cloned locally into the same parent folder.
- Ensure that you have sudo access on the vm. 
- Ensure that the host name of the vm is:
    "se2-b.compute.dtu.dk"
- Ensure that the following tools are installed on the vm:
    Docker
    Docker Compose
- Ensure that the vm has external access to 3rd party repositories
- Connect to the DTU VPN using OpenVPN.

**s123456** = your id from dtu 

**./YOURPATH** = the parent folder that you have cloned the two 

## Remote copy
repositories to.
- Run this command in the parent folder of the two repositories:

>scp -r **./YOURPATH/LiraMapBackEnd** **s123456**@se2-b.compute.dtu.dk:/home/**s123456**/code/backend


*We will be doing this in our wsl environment but if you cloned the repository to windows the repositories should be accessible from GitBash.*
- run the same command for the backend:


>scp -r **./YOURPATH/LiraMapFrontEnd** **s123456**@se2-b.compute.dtu.dk:/home/**s123456**/code/frontend

    

*this should give the following structure on the vm:

    |-code
    |   |-fontend
    |   |   |-...
    |   |-backend
    |   |   |-...

## docker build and start
now we are going to build and start  the code on the vm
- ssh into the vm using the following command in a new GitBash window


>ssh s123456@se2-b.compute.dtu.dk

- Then once you have logged in using you dtu password run the following command from the "frontend" folder:


>sudo docker-compose -f deploy/docker-compose.yml --project-directory . build


This will build the front-end on the vm. 
- Now we can build the backend and bring up both front- and back-end with the following command from the "backend" folder:

>sudo docker-compose -f deploy/docker-compose.prod.yml --env-file ./.env --project-directory . up --build

- following starts can be done without the additional --build tag:

>sudo docker-compose -f deploy/docker-compose.prod.yml --env-file ./.env --project-directory . up

## Using the running code

You should now be able to access our Lira-Map now in the url: 

>se2-b.compute.dtu.dk:8080

additionally you can access the swagger docs though the url:

>se2-b.compute.dtu.dk:8000/docs
