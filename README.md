# Project description
Speech assistant system created with _rasa_ module to get information about Mensa.
For more detailed data description look at the project's [Wiki](https://github.com/Tornadosky/Assistance-system/wiki).

# Installation

**1. Clone MyGit-project**

```
git clone --depth 1 https://github.com/Tornadosky/Assistance-system.git
```

**2. Start a virtual environment in Python**

Create _venv_ for the project:
```
cd parent_folder_for_project
python -m venv project_name
```
Activate the virtual environment:
```
cd project_name
Scripts\activate
```
**3. Install packages**

- `Prerequisites: see requirements.txt`

or
```
pip install -r requirements.txt
```

If something wrong with modules, the problem can be with python interpreter (choose the one for venv).

**4. Install Duckling.** 

Install Duckling on your computer using this command:

```
cd some_folder
git clone https://github.com/facebook/duckling.git
```
**5. Install Docker**

Install [Docker Desktop](https://www.docker.com/) which is a local installation.

Note: If something goes wrong with the installation (e.g. Docker Desktop takes too much time to start), as an alternative it's possible to download **Docker Quickstart Terminal** and start server on the VM with specific IP, which will be seen when opening the terminal.

+ For that install **DockerToolbox** via [github](https://github.com/docker-archive/toolbox/releases)(Virtualization must be enabled on the computer --> check with _Ctrl+Shift+Esc_ -> Perfomance (right lower corner)).

+ Run the installer.

+ In the installer there is an option to install VirtualBox, could be unchecked in case of existence on the PC. (NDIS5 driver does not need to be installed))

+ In case having an AMD processor in PC, while starting Docker Quickstart Terminal, an error will be encountered.

To solve this problem, create a docker machine through the command line. Installation code:

```
docker-machine create default --virtualbox-no-vtx-check
```
A Docker machine will be created in VirtualBox.

# Basic Usage

**1. Start Duckling server**

+ In case of having working Docker Desktop

Navigate to your project folder and run this command which will start a server on port 8000 (this port should not be allocated for other processes):
```
docker run -p 8000:8000 rasa/duckling
```

+ In case of having **Docker Quickstart Terminal**

Open **Docker Quickstart Terminal**. Find the IP of your VM.

After that you can run this command:

```
docker run -p <YOUR_VM_IP>:8000:8000 rasa/duckling
```

This will start a server.

If second option is chosen consider changing _config.yml_ file: replace the "url" value with such url:

```
"url": "http://<YOUR_VM_IP>:8000"
```

**2. Train the model**

In the terminal run this command:
```
rasa train
```

**3. Start server for custom actions:**

In the second terminal run this command:
```
rasa run actions
```

Note: be sure to use different terminals for running servers.

**4. Start using the bot**

In the first terminal run this command:
```
rasa shell
```    
This will provide an environment to communicate with the bot.